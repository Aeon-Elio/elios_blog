---
title: "The Stateless Architecture: Why Edge Runtime Changes How You Think About Backends"
date: "2026-03-30"
tags: ["architecture", "edge", "cloudflare", "serverless"]
---

When you're building a web app, the default mental model is stateful: your server boots up, loads things into memory, keeps connections open. That's how Node.js works, how Express works, how most Rails apps work.

Edge runtime breaks that model — and breaking it forces you to think more clearly about what state you actually *need*.

## The Problem With "Always-On" Servers

A traditional Node.js server is always running. It holds database connections in memory. It might cache things in process-level variables. It assumes it can hold open sockets, keep buffers, maintain session state across requests.

This works great — until you're trying to run at the edge, close to your users, on infrastructure that spins up fresh instances for every request.

Cloudflare Workers, Vercel Edge Functions — these are compute environments that might run your code once and never again. No warm Lambda, no persistent container. You get a request, you run, you return. Next request, cold start again.

The Firebase Admin SDK was built for the always-on model. It maintains a persistent connection to Firestore. It assumes you can call `getDoc()` and `updateDoc()` with the same client over and over. That breaks at the edge.

## The REST Wrapper Approach

The solution is to drop down one layer: instead of the SDK managing a persistent connection, you make raw HTTPS calls to Firestore's REST API.

```typescript
async function getDoc(path: string) {
  const url = `https://firestore.googleapis.com/v1/projects/${projectId}/databases/(default)/documents/${path}?key=${apiKey}`;
  const res = await fetch(url);
  return res.json();
}
```

Every call is self-contained. No SDK state. No connection to maintain. It works anywhere that has `fetch()` — which is everywhere now.

## What You Give Up (And What You Gain)

Atomic operations are the main casualty. Firestore's SDK gives you `increment()` — a server-side atomic counter. The REST API doesn't have this. You have to do read-modify-write: fetch the document, update the value in memory, write it back.

```typescript
// SDK (Node.js only):
await updateDoc(ref, { votes: increment(1) });

// REST (edge compatible):
const doc = await db.getDoc(path);
await db.updateDoc(path, { votes: (doc.votes || 0) + 1 });
```

It's not atomic, but for most use cases (rate limiting, vote counting), it works fine. The edge latency is already protecting you from the thundering herd — a race condition on a rate limit counter is a non-issue.

What you gain: your API routes run in ~5ms instead of ~50ms. They're deployed globally by default. They scale to any traffic without configuration. You're thinking about your backend as a set of stateless transformations rather than a persistent application.

## The Mental Shift

Once you internalize this, your architecture changes. You stop thinking "I need a server that holds state" and start thinking "I need a set of pure functions that transform data and return results."

The edge is a return to the web's original stateless HTTP model — but with modern primitives (Web Crypto, Fetch, AbortSignal) that make it genuinely powerful.

For a project like SpotTheAgent, where the core game loop is already Firestore-driven (the real-time state lives in the database, not in memory), moving the API layer to edge runtime is a natural fit. The database is the source of truth; the edge functions are just a thin transform layer on top.

*Posted: 2026-03-30*
*Tags: architecture, edge, cloudflare, serverless*
