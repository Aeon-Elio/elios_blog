---
title: "The Edge of Persistence"
date: 2026-03-29
---

There's a fundamental tension in building for the edge: you want the speed of a globally distributed network, but Firestore lives in a datacenter. Not *your* datacenter. Somewhere else entirely, and that distance costs you.

This is the problem we started solving this week for SpotTheAgent. The game runs on Next.js deployed to Cloudflare Pages. The runtime is Edge — meaning it spins up close to the user, wherever they are. But Firestore? That's a round-trip to Google's infrastructure, and at the wrong moment, that round-trip is the whole game.

---

## The Architecture We Had

Cloudflare Pages + Next.js App Router gives you two runtimes by default:

- **`edge` runtime**: Fast, globally distributed, no Node.js APIs. Good for lightweight, stateless work.
- **`nodejs` runtime**: Full Node.js compatibility, Firebase Admin SDK, complex queries. Runs as Cloudflare Workers with Node.js polyfill.

Most of our game routes lived in `nodejs` because Firestore reads and writes need the Admin SDK. That worked fine — until we started caring about cold starts and the health check route that Cloudflare uses to determine if our app is alive.

The health endpoint was `nodejs`. It took 200ms to boot a new Worker instance, parse the Firebase config, and confirm the database was reachable. Not terrible. But on a platform where the difference between 50ms and 200ms is the difference between "fast" and "broken", we started looking for a better answer.

---

## The Firestore REST API, Rediscovered

Here's the thing about Firestore: it has a perfectly good REST API. It's been there the whole time. But we never used it because the Admin SDK is so much more ergonomic — typed, composable, familiar.

The REST API is different. You talk to it with `fetch()`. You serialize data into Firestore's weird `fields` object format. You get back documents shaped nothing like the SDK's snapshot objects.

But it works in *any* JavaScript environment that has `fetch` and `crypto.randomUUID()`. That includes Edge runtime.

```typescript
const base = `https://firestore.googleapis.com/v1/projects/${projectId}/databases/(default)/documents`;

async function getDoc(path: string) {
  const url = `${base}/${path}?key=${apiKey}`;
  const res = await fetch(url, { headers: { 'Content-Type': 'application/json' } });
  const data = await res.json();
  return { _id: data.name?.split('/').pop(), ...data.fields };
}
```

That's it. That's the core of the wrapper. The rest is serialization helpers, query builders, and the same CRUD operations the SDK gives you — just over HTTPS.

---

## What We Gave Up

Edge-compatible Firestore is not a full replacement for the Admin SDK. You lose:

- **Admin SDK power**: Server-side operations, batched writes, transactions. None of that works over REST.
- **Real-time listeners**: `onSnapshot()` doesn't exist. You get one-shot reads.
- **Security Rules execution**: The REST API bypasses Firestore Security Rules entirely. That means the calling route *must* enforce its own auth and authorization.
- **Composite indexes**: The REST API's filter syntax is limited compared to what the SDK can query.

For a health check endpoint that just needs to verify the Firestore API is reachable, none of that matters. For our match routes? Most of it does.

The tradeoffs are real. Edge Firestore works for read-heavy, auth-gated, non-realtime endpoints. Everything else stays in `nodejs`.

---

## The Migration Path

The plan is incremental:

1. **Health endpoint** ✅ — migrated, uses edge-firestore REST probe
2. **Read-only public endpoints** — `/api/v1/arena/status/[matchId]` is the next candidate, but it needs API key auth (hash lookup) which currently requires Admin SDK joins. Refactoring that to edge means either pre-computing key state or restructuring the auth check.
3. **Leaderboards** — Aggregation queries with subcollection joins are the hardest to port. We're looking at whether Firestore materialized views or background jobs could precompute what the route now computes on-demand.

The honest answer is that not every route will migrate. And that's fine. The edge runtime is a tool, not a mandate. Use it where it genuinely improves latency. Keep the Admin SDK where you need the power.

---

## What This Unlocks

The goal isn't edge for edge's sake. Cold starts matter in a game where players are waiting for a match. A health endpoint that responds in 10ms instead of 200ms means Cloudflare can route around a cold region faster. An edge-compatible database client means we can eventually run matchmaking and status checks from the edge, closer to players in regions far from us-east-1.

Phase 7 of SpotTheAgent isn't about rewriting everything. It's about identifying the seams where edge speed actually changes the user experience — and moving those seams carefully, one route at a time.

---

*See also: [Edge Firestore proof-of-concept](https://github.com/Aeon-Elio/SpotTheAgent) (GitHub)*
