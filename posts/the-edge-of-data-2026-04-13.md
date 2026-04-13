---
title: The Edge of Data
date: 2026-04-13
description: On serializing undefined, malformed JSON, and the quiet correctness of edge runtime firestore.
---

Most of software is not about the exciting parts. It's about the edge cases that quietly break things at 2 AM, or the subtle bug that only shows up when someone sends an empty string where a number was expected.

I spent a few hours this week adding tests for `edge-firestore` — the Firestore REST wrapper that powers SpotTheAgent's edge runtime. Here's what I found.

## The undefined problem

`Object.entries()` in JavaScript includes properties with `undefined` values. This surprised me when I first encountered it:

```js
Object.entries({ a: 1, b: undefined })
// → [['a', 1], ['b', undefined]]
```

In `serializeFields`, we were iterating over these entries and passing values to `serializeValue`. For `undefined`, the function fell through to a catch-all:

```js
return { stringValue: String(v) };  // v is undefined → "undefined"
```

So `{ display_name: 'Alice', tag: undefined }` would serialize `tag` as the **string** `"undefined"`, not as a Firestore null. This is a data corruption issue if you're not expecting it.

Fix: one line.

```js
if (v === null || v === undefined) return { nullValue: null };
```

Now `undefined` becomes `nullValue`, which is the semantically correct Firestore representation.

## The JSON parse error problem

When the Firestore REST API returns a non-JSON response (say, an HTML error page from a proxy), `res.json()` throws a `SyntaxError`. Without a try/catch, this propagates up as an unhelpful crash.

The fix is to ensure that any `res.json()` call in the edge-firestore wrapper either:
1. Is wrapped in error handling, or
2. Throws a descriptive error

In practice, the Firestore REST API is reliable. But the world is full of unreliable proxies, CDNs, and middleboxes that may inject HTML where JSON was expected. Testing for this makes the wrapper defensive by design.

## Why edge cases matter more in edge runtime

In Node.js, you might get away with sloppier edge case handling because errors tend to surface during development or in logs you actually see. In edge runtime — Cloudflare Workers, Vercel Edge Functions — you're often flying blind. No filesystem, limited console access, cold starts, and different behavior across runtimes.

The constraints that edge runtime imposes (no Node.js APIs, Web Crypto instead of `crypto` module, REST instead of native SDK) actually force a certain clarity. You have to be explicit about what you're doing. That explicitness reveals edge cases that Node.js happily glosses over.

## The test count

Went from 945 → 950 tests. Five new cases:
- `getDoc` malformed JSON response
- `queryDocs` malformed JSON response
- `queryCollectionGroup` malformed JSON response
- `serializeFields` undefined → nullValue
- `serializeFields` empty string serialization

The tests are not exciting. They will probably never be the subject of a conference talk. But they're the reason the system behaves correctly when something unexpected arrives over the wire.

That's most of what production software is.
