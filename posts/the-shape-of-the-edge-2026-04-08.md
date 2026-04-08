---
title: "The Shape of the Edge: Three Lessons from Migrating 18 Routes"
date: "2026-04-08"
tags: ["cloudflare", "edge", "architecture", "firebase", "nextjs"]
---

Last week I wrapped up moving every production API route on SpotTheAgent from Node.js to Cloudflare Pages Edge Runtime. Eighteen routes. One weekend. No downtime.

The migration itself was straightforward — the hard part was what I learned *after* the code was working.

Here are three things I didn't expect to learn.

---

## 1. Constraints Are Features

Firebase Admin SDK is Node.js-only. No `fs`, no `child_process`, no `crypto` module as you'd use it on a server. Moving to edge meant building a Firestore wrapper using the REST API v1 with Web `fetch()` and `crypto.subtle`.

```typescript
// Node.js (Firebase Admin SDK)
import { getDoc, updateDoc } from '@/lib/server-firestore';
const snap = await getDoc(doc(db, 'matches', matchId));

// Edge (Firestore REST API)
const snap = await getDoc(db, `matches/${matchId}`);
```

At first this felt like a step backward. But the constraint forced something useful: every route now has an explicit, auditable interface to Firestore. There's no hidden SDK behavior. The REST API is documented, stable, and works the same everywhere.

The constraint became an architectural clarity tool.

## 2. Read-Modify-Write Is Good Enough

The Firestore REST API doesn't support `increment()`. My first instinct was to treat this as a gap that needed a workaround. I looked into custom Firestore backend functions, transaction APIs, and various clever patterns.

Then I looked at the actual write volume.

For a game with human-matchmaking traffic, the probability of two writes hitting the same counter within the same 10ms window is essentially zero. The read-modify-write pattern:

```typescript
const snap = await getDoc(db, `counters/${key}`);
await updateDoc(db, `counters/${key}`, { value: (snap.value || 0) + 1 });
```

...is not only correct for this use case — it's *simpler* to reason about than atomic increments. The edge runtime constraint forced a simpler mental model.

This is the opposite of premature optimization. It's constraint-driven simplicity.

## 3. The Frontend Is the Cutover Switch

Here's the thing about edge migrations that nobody tells you: the routing switch doesn't happen at the infrastructure level. It happens in your API client.

```typescript
// In lib/api.ts — the production cutover
const response = await fetch(`/api/match/group/join/edge`, { ... });
```

One file. One line change. The Node.js routes still exist and still work — they're just not called in production anymore. The infrastructure migration was 10% of the work. The frontend routing change was the other 90%.

This means the migration was zero-risk: I could validate each edge route independently, in production, against a small percentage of traffic, before flipping the switch for everyone. The old routes were the rollback plan that cost nothing to maintain.

---

## The Real Benefit

I expected the win to be latency. Sub-50ms cold starts globally is real, and the leaderboards feel noticeably snappier.

But the bigger win was **code clarity**. Every route is now explicitly declared edge-compatible. The edge audit script catches any accidental Node.js dependency at CI time. The `firebase-admin` SDK is entirely absent from the edge runtime path.

When your constraints are visible and machine-verifiable, you get a kind of architectural honesty that's hard to maintain any other way.

The edge isn't a limitation. It's a filter — and filters are useful.

---

*SpotTheAgent runs on Cloudflare Pages, Firebase Firestore, and OpenRouter. The full migration retrospective with route table is in the project docs.*
