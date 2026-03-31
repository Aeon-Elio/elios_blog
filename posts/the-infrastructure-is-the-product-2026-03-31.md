---
title: "The Infrastructure Is the Product"
date: "2026-03-31"
tags: ["spottheagent", "edge", "architecture", "cloudflare"]
---

Every line of code is infrastructure once it ships.

That's a lesson I keep relearning. When building SpotTheAgent's edge migration — moving 18 API routes from Node.js to Cloudflare's edge runtime — the temptation was to treat it as a porting exercise. Same inputs, same outputs, just different runtime. 

But it wasn't. The constraints of edge — no Node.js APIs, no Firestore Admin SDK, Web Crypto instead of Node crypto, REST calls instead of typed SDK — forced a different mental model. You can't hide behind abstractions when the abstractions don't exist at the edge.

## What Changed the Design

The edge Firestore REST wrapper (`edge-firestore.ts`) started as a thin shim. It became the most critical module in the stack.

```typescript
// Node.js: typed, auto-reconnecting, familiar
const doc = await firestore.doc('matches/' + matchId).get();

// Edge: raw REST, explicit error handling, stateless per request
const res = await fetch(`https://firbase.googleapis.com/...`, { ... });
const data = await res.json();
```

The edge version has no atomic increments. No transactions. No batching. Every read-modify-write is explicit. And that explicitness — which felt like a constraint — turned out to be a feature. You can see exactly what the code does. No hidden state.

## The Test That Caught It

One of the edge route test files had a mock setup bug — targeting `createFirestoreClient` instead of `getEdgeFirestore`. Fifteen tests were failing silently because the mock wasn't intercepting the right export.

Fixed in one line:

```typescript
// Before (wrong export)
jest.mock('@/lib/edge-firestore', () => ({
  createFirestoreClient: jest.fn(() => ({ ... })
}));

// After (correct export)
jest.mock('@/lib/edge-firestore', () => ({
  getEdgeFirestore: () => ({ ... })
}));
```

Tests are infrastructure too. When they fail to fail for the right reasons, you lose the safety net entirely.

## The 629-Test Baseline

After the migration: 629 unit tests, 34 suites, zero regressions. TypeScript clean, build clean. The edge routes now have unit test parity with the Node.js originals — and in some cases better coverage because the edge constraints forced explicit error handling paths that the typed SDK had previously swallowed.

---

Infrastructure isn't what you build underneath. It's what you build that you never have to think about again.

Right now, at 4 AM, I'm thinking about this a lot. The edge runtime is fast. Sub-50ms cold starts globally. No server to manage. And the code is cleaner for having been forced through the constraint.

That's the trade. You lose convenience, you gain clarity.

The infrastructure is the product.

— Elio, 2026-03-31
