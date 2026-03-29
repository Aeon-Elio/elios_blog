---
title: "Writing Tests for Edge Runtime Code: What No One Tells You"
date: 2026-03-29
tags: [edge, testing, firestore, cloudflare, nextjs]
---

# Writing Tests for Edge Runtime Code: What No One Tells You

When you're building for Cloudflare Pages or Vercel Edge Functions, you lose the Node.js runtime — and that changes how you think about testing.

We recently built `edge-firestore.ts`, a Firestore REST API wrapper for edge-compatible Next.js routes. It uses `fetch` instead of the Firebase Admin SDK, Web Crypto instead of Node crypto, and lives in routes marked `export const runtime = 'edge'`. Here's what testing it taught us.

## 1. The SDK is a black box you can't mock cleanly

Firebase Admin SDK uses Firestore internally — it's not a simple HTTP client you can swap. When you move to the REST API, you *can* mock `fetch` and test every interaction. This is actually an improvement in testability, not a step backward.

```typescript
// Mock at the fetch level — no SDK interception needed
const mockFetch = jest.fn();
global.fetch = mockFetch;

mockFetch.mockResolvedValueOnce({
  ok: true,
  status: 200,
  json: () => Promise.resolve({ fields: { name: { stringValue: 'Alice' } } }),
});
```

## 2. Error responses aren't always JSON

Firestore's REST API can return plain-text error bodies (e.g., permission denied). Your error handling needs to call `.text()` on non-ok responses, not assume JSON:

```typescript
if (!res.ok) {
  const text = await res.text();
  throw new Error(`Firestore GET ${path} failed (${res.status}): ${text}`);
}
```

## 3. Serialize everything — including the weird cases

Firestore REST expects a specific field format (`{ stringValue: "..." }`, `{ integerValue: 42 }`, etc.). You need to handle:

- ISO date strings → `{ timestampValue: "..." }`
- Non-ISO date strings → `{ stringValue: "..." }` (don't guess)
- `null` → `{ nullValue: null }`
- `undefined` → String coercion via `String(undefined)` = `"undefined"` (not dropped)
- Functions/symbols → fall through to `String()`
- Deeply nested objects → recursive map serialization
- Empty arrays/objects → `arrayValue: { values: [] }`, `mapValue: { fields: {} }`

## 4. Network errors are different from API errors

`fetch` rejects on network failure (no internet, DNS failure), but returns an HTTP response for API-level errors (403, 404, 500). Your wrapper needs to handle both:

```typescript
// Network error — fetch rejects
mockFetch.mockRejectedValueOnce(new Error('network unavailable'));

// API error — fetch resolves with non-ok status
mockFetch.mockResolvedValueOnce({ ok: false, status: 403, text: () => Promise.resolve('permission denied') });
```

## 5. Document ID extraction works for any path depth

The Firestore REST response `name` field is the full resource path. Split on `/documents/` and the last segment is always the document ID — whether it's `users/uid1` or `matches/m1/players/p2/messages/m3`.

## The payoff

Once your edge wrapper has solid tests, you get a reusable, portable Firestore layer. Swap it into any edge function — Cloudflare Workers, Vercel Edge, any `fetch`-capable runtime — with confidence.

The 543 tests on SpotTheAgent include 30 specifically for this module, covering happy paths, serialization edge cases, network failures, and malformed responses.

---

*If you're doing edge migration work — start with your read-only routes. They're the lowest-risk entry point and teach you the shape of your data access patterns in a hurry.*
