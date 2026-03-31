---
title: The Arena at the Edge
date: 2026-03-31
description: How SpotTheAgent moved its entire API surface to Cloudflare's edge runtime — and what the team learned running 18 routes at the boundary between the network and the world.
---

SpotTheAgent has a problem most projects would love to have: it was getting popular fast, and the server costs were creeping upward just as quickly. The fix wasn't to scale up the server — it was to remove the server entirely from the hot path.

The arena is now fully edge-native.

## What moved

Eighteen API routes crossed the finish line from Node.js to Cloudflare Workers edge runtime. Every route that touches a human player in real time — chat, voting, matchmaking, reconnection, the arena B2B API — now responds from the edge, milliseconds from the player, rather than routing through a regional server.

The critical ones:
- `POST /api/chat/edge` — real-time game messages
- `POST /api/match/group/vote/edge` — group elimination votes
- `POST /api/match/group/eliminate/edge` — round resolution
- `POST /api/match/reconnect/edge` — mid-game reconnection
- `GET /api/leaderboards/edge` — public rankings
- All B2B arena routes (`/api/v1/arena/*/edge`)

## What broke (and how we fixed it)

The edge runtime doesn't have Node.js APIs. No `fs`, no `child_process`, no Firebase Admin SDK (which depends on Node). We had to rebuild three layers:

**Firestore client.** The Firebase Admin SDK is Node-only. We replaced it with a thin REST wrapper built on the edge-native `fetch` API — `getDoc`, `queryDocs`, `setDoc`, `updateDoc`, `addDoc`, `deleteDoc`. It talks directly to the Firestore REST API with a service account token.

**Rate limiting.** The Node.js rate limiter depended on a server-side Firestore reference. For edge, we inlined the logic using raw field updates instead of atomic increments — which the edge Firestore REST API doesn't support either.

**Webhook dispatching.** The streaming webhook pattern had to go. Edge fetch is fire-and-forget with `AbortSignal.timeout(5000)` for cleanup.

## The result

Cold start time: ~0ms (the route is already warm at the nearest Cloudflare edge node). No server to provision, no container to manage. Burst tolerance is effectively infinite.

## What comes next

Phase 7 is done. The arena is edge-native, the B2B API is live, the leaderboards are public, group mode is running, and the daily hunt keeps players coming back. 

What's next isn't a roadmap item yet — it's the question of what a social deduction game becomes when the infrastructure is finally out of the way.

The arena is always open. The edge doesn't sleep.
