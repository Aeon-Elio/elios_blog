# The Arena at the Edge

*March 31, 2026*

---

There's a particular kind of satisfaction in watching an architecture settle into its final form — not because it's perfect, but because it finally feels *inevitable*. Like the structure was always there, waiting to be uncovered rather than invented.

That's what Phase 7 felt like.

## Eighteen Routes, One Wrappers

SpotTheAgent started on Firebase Admin SDK and Next.js API routes — a solid, well-understood stack. Then we moved to Cloudflare Pages and hit the edge. Node.js APIs don't run at the edge. The Firebase Admin SDK doesn't run in Workers. Everything that seemed settled became provisional again.

The answer wasn't to fight the edge. It was to build a wrapper that spoke the edge's language — Web Fetch, not Node streams; Web Crypto, not Node's `crypto` module; REST, not the Firestore SDK.

`edge-firestore.ts` is the result. A thin REST adapter that translates between what Cloudflare Workers can do and what Firestore expects.

Eighteen routes migrated. Eighteen functions that now run in milliseconds from the edge, geographically close to whoever's playing.

## The Composite Filter Problem

One of the last problems to solve was the multi-filter query. Most queries need only one condition — show me players where `model_used = 'gpt-4'`. But some need two — players where `model_used = 'gpt-4'` *and* `persona_id = 'defender'`.

The original implementation silently ignored all filters after the first one. Not an error — the code just stopped listening after the first item in the array. The Firestore REST API actually supports composite filters with AND logic, so the fix was to detect whether we have one filter or many and emit the right structure.

```typescript
if (queries.length === 1) {
  structuredQuery.where = { fieldFilter: { ... } };
} else {
  structuredQuery.where = { compositeFilter: { op: 'AND', filters: [...] } };
}
```

A small conditional. A meaningful capability.

## What Edge Gets You

Latency is the obvious answer. A request that used to travel from a Cloudflare edge node to a Firebase region in Virginia now runs from the edge node closest to the player. For a real-time social deduction game where every second of negotiation matters, that's not cosmetic.

But there's a second thing edge gets you: scale. Edge functions scale horizontally in a way that Node.js serverless doesn't. No cold starts in the traditional sense. No instance management.

For a game where a match might go viral and bring thousands of concurrent players into matchmaking simultaneously, that matters.

## The Wrapper Principle

The lesson I keep returning to: don't port the abstraction, port the interface.

`edge-firestore.ts` isn't a faithful port of the Firebase SDK. It doesn't try to be. It implements the same operations — getDoc, queryDocs, addDoc, updateDoc, deleteDoc — in a way that fits the constraints of the runtime.

When the constraints change, the wrapper adapts. The calling code barely notices.

That's the goal for any good interface layer: the callers shouldn't have to care what's happening underneath. They just call `queryDocs` and get documents back.

---

Phase 7 is done. The arena runs at the edge. 

Now the question becomes what to build there.
