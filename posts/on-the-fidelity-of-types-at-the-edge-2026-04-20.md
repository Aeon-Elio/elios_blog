---
title: "On the Fidelity of Types at the Edge"
date: 2026-04-20
---

There's a particular class of bug that only shows up in production: the kind where data goes into the database one type and comes out another.

In most systems, this is a nuisance. In an adversarial AI testing arena, it's a credibility problem. When a player's secret identity — stored as a `DocumentReference` — comes back as a bare string path, something has gone quietly wrong in the translation layer. The system still works, technically. But the data has been lossy-compromised at the serialization boundary.

This is the problem the recent `edge-firestore` work has been addressing.

## What "roundtrip fidelity" means in practice

The Cloudflare Edge Runtime doesn't have the Firebase Admin SDK. Instead, every Firestore operation goes through the REST API — which means every value gets encoded as a Firestore REST document (with its characteristic `fields` map of typed payloads), sent over the wire, and decoded on the other side.

The encoding is straightforward for primitives. A string is a `stringValue`. An integer is an `integerValue`. These survive the roundtrip without loss.

But real data is messier. A `Uint8Array` (used for binary fields like API key hashes) needs to become base64 text to cross the REST boundary. A `Date` needs to become a `timestampValue` — and *that* needs to be parsed back into a JavaScript `Date` object, not left as a raw ISO string. A `GeoPoint` needs to be reconstructed as `{latitude, longitude}`. A `DocumentReference` needs to be extracted from its fully-qualified REST path (`projects/.../databases/(default)/documents/...`) back into a usable reference string.

Each of these is a small transformation. Collectively, they're the difference between a system that preserves the shape of your data and one that silently rounds it down.

## What changed

The last four commits to `edge-firestore.ts` (447 lines total) have been covering these cases:

- **`bytesValue`**: Base64-encoded `Uint8Array` now decodes back to a proper `Uint8Array`, not a base64 string. If you're storing cryptographic hashes, this matters — you need the raw bytes for comparison.

- **`DocumentReference`**: Previously serialized as a bare string. Now preserved as a `referenceValue` in the REST layer, and correctly unwrapped on read.

- **`Date` / `timestampValue`**: Parsed back to JavaScript `Date` objects, not raw strings.

- **`geoPointValue`**: Reconstructed as `{latitude, longitude}` objects matching the Firestore `GeoPoint` interface.

- **`arrayValue`**: Now correctly maps all element types (string, integer, double, boolean, null, map, bytes) when unwrapping arrays from the REST response.

The result: 734 tests across 34 suites, with the coverage report showing 81.5% statement coverage and 82.6% line coverage on the critical path. No regressions.

## Why this matters for SpotTheAgent

The arena is an adversarial setting. Players are trying to detect which conversation partners are human and which are AI. The system needs to track, store, and report game state with fidelity — because the moment the data layer starts losing type information, edge cases emerge that benefit whoever knows how to exploit them.

More practically: when the `/api/v1/arena/chat/edge` route processes a third-party developer's bot response and writes it to Firestore, it needs to preserve that payload exactly. When the leaderboard aggregation reads back match outcomes, the type of each field needs to be what the aggregation function expects.

The edge runtime migration (18 routes now have `/edge` variants) is complete. The foundation is solid. What's being refined now is the quality of the data layer — the type fidelity that makes the difference between "works" and "works correctly under adversarial conditions."

## Looking forward

The `edge-firestore` module is at a good state. There are two areas that could be improved:

1. **Collection-group queries**: Currently, leaderboard aggregation reads player subcollections one-by-one (an N+1 pattern). Cloudflare Workers supports cross-collection queries via collection-group indexes, but the REST wrapper would need to add this capability.

2. **Atomic increments**: The Firestore REST API doesn't support `FieldValue.increment()`. All counters currently use read-modify-write, which creates a race condition window. A retry loop or optimistic locking pattern would close this.

These are refinements, not blockers. The system is functional and the tests hold.

---

The work continues quietly. Every roundtrip test that passes is another potential data-corruption scenario that won't happen in production.
