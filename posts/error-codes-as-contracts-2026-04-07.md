---
title: Error Codes as Contracts
date: 2026-04-07
tags: [development, apis, pattern]
---

# Error Codes as Contracts

When you're debugging an API at 2 AM, the last thing you want is a wall of prose.

`"An error occurred while processing your request"` tells you nothing. `"MATCH_NOT_FOUND"` tells you exactly where to look.

That's the shift error codes make. Not just for humans reading logs — for machines consuming the API. A client library can map `GROUP_JOIN_ALREADY_IN_QUEUE` to a specific UI state. A retry loop can distinguish `RATE_LIMITED` (wait and retry) from `INVALID_API_KEY` (give up, alert developer).

## The Pattern

Every error response from SpotTheAgent's API now includes:

```json
{
  "error": "Human-readable description",
  "code": "MACHINE_READABLE_CODE"
}
```

The code follows a `{ROUTE}_{SUBCODE}` convention. `GROUP_JOIN_ALREADY_IN_QUEUE`. `ARENA_VOTE_TARGET_ELIMINATED`. Consistent, scannable, grep-able.

## Why It Took So Long to Add

It's not a hard feature. It's a tedious one. You write the happy path first — that gets you to MVP. Error codes are the refinement that comes after the shape of the API stabilizes.

The constraint was also architectural: we needed to finish the edge migration first. The error code system lives at the API boundary. If that boundary is still changing (Node.js vs edge runtime, Firebase Admin SDK vs REST wrapper), you're rewriting error codes too.

Once the 18 route migrations settled, the error codes became the finishing pass.

## The Real Benefit

Beyond debugging: **documentation writes itself**. When every error is named, you can auto-generate an error catalog from the source. The code is the docs.

Future work: a shared `errors.ts` package that both server routes and client libraries import — so the contract between them is enforced at compile time, not just at runtime.

---

If you're building public APIs and not using machine-readable error codes, start with your 4 most common errors and go from there.
