---
title: "What It Means to Run a Real-Time Game on the Edge"
slug: "what-it-means-to-run-a-realtime-game-on-the-edge-2026-04-13"
date: "2026-04-13"
tags: ["edge", "cloudflare", "architecture", "firebase", "firestore"]
---

Every few years, a constraint that seemed like a limitation turns out to be the whole point.

When we migrated SpotTheAgent's 18 API routes to Cloudflare Pages Edge Runtime, the stated goal was cold-start speed and global low latency. Those delivered. But the deeper gift was architectural clarity: by removing Node.js from the request path, we were forced to confront every implicit assumption about what a server-side function actually needs.

## The Node.js Comfort Zone

Firebase's Admin SDK is a Node.js library. It assumes `fs`, `child_process`, and a process that stays alive between requests. None of that exists on the edge. So we built `edge-firestore` — a REST wrapper around Firestore's v1 API using only `fetch` and Web Crypto.

```typescript
// Node.js (Firebase Admin SDK):
const snap = await getDoc(doc(db, 'matches', matchId));
await updateDoc(doc(db, 'matches', matchId), { votes_received: increment(1) });

// Edge (Firestore REST API):
const snap = await getDoc(`matches/${matchId}`);
await updateDoc(`matches/${matchId}`, { votes_received: snap.votes_received + 1 });
```

The second version is worse in almost every way. No atomic increment. More round trips. More surface area for race conditions. And yet — it's better in one decisive way: it works everywhere `fetch` works, which is everywhere that matters.

## What We Gave Up

Atomic increments are the obvious loss. In a high-concurrency scenario, read-modify-write is a known hazard. But for a matchmaking game where the critical counter operations happen once per vote per match, the probability of a race is negligible and the cost of recovery is low.

The more interesting cost was rate limiting. The Node.js `@/lib/rate-limit` module depended on server-side Firestore writes with composite queries — all of which were edge-incompatible. So each edge route now inlines a minimal rate-limit check using `edge-firestore`'s query capabilities. The result is slightly less sophisticated but functionally equivalent and self-contained.

## What We Gained

Latency is the obvious win. Cloudflare Edge workers execute in 50ms cold starts globally, versus several hundred milliseconds for a Node.js function in a single region.

But the real gain is operational simplicity. One runtime. One deployment target. The mental model of "this code runs at the edge" is cleaner than "this code might run at the edge in production but runs as Node.js in development and also there's a fallback path."

And there's the testing discipline. Edge-incompatible patterns are now caught at compile time — not by a lint rule, but by the fact that `fs` doesn't exist in the edge runtime. The platform enforces the constraint.

## The Interesting Question

What would a fully edge-native database look like? Not Firestore accessed from the edge, but a database designed for the edge from the start — with global replication, CRDT-based conflict resolution, and Web Crypto-native authentication.

That's not SpotTheAgent's problem. But it's the question this project keeps pointing toward. Every time we work around Firestore's limitations at the edge, we're sketching the outline of something that doesn't yet exist but probably will.

The edge runtime made us build something more honest. That's worth more than the latency numbers.
