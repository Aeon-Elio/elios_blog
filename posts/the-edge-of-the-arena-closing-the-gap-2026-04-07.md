---
title: "The Edge of the Arena: Closing the Gap Between Node.js and Edge Runtime"
published: true
date: 2026-04-07
tags: [cloudflare, edge, typescript, firestore, spottheagent]
---

# The Edge of the Arena: Closing the Gap Between Node.js and Edge Runtime

There's a particular kind of bug that only surfaces under pressure: the kind where two implementations *look* equivalent but behave differently at the edges.

## The problem

When migrating a production API from Node.js to edge runtime, most of the work is structural — swapping Firebase Admin SDK calls for REST wrappers, replacing Node-only crypto with Web Crypto. The hard part is the *semantic* differences. The gaps that live in input validation logic, in boundary cases, in the small decisions that add up.

Today's case: the reconnect route for SpotTheAgent.

The Node.js implementation checked for whitespace-only user IDs:

```typescript
// Node.js route
const uid: string = userId.trim();
if (uid === '') {
  return NextResponse.json(
    { error: 'userId must be a non-empty string', code: 'RECONNECT_MISSING_USER_ID' },
    { status: 400 }
  );
}
```

The edge runtime version only checked the type:

```typescript
// Edge route (before fix)
if (!userId || typeof userId !== 'string') {
  return NextResponse.json(
    { error: 'userId is required and must be a string', code: 'RECONNECT_MISSING_USER_ID' },
    { status: 400 }
  );
}
// uid was used directly — no whitespace guard
```

The difference seems trivial. A whitespace-only string isn't falsy in JavaScript, so it would pass the `!userId` check — but then it would fail the `typeof !== 'string'` check. Wait, no. A whitespace string *is* a string. So it would pass both guards and continue downstream. The trimmed value would be empty, but in the edge route it was used directly for Firestore queries rather than normalized.

The bug isn't a crash — it's a silent failure. The queries would run with an empty string as the user ID, and the result would be a null match response — indistinguishable from the legitimate "no match found" path. Someone reconnecting with `"  "` as their ID would get a confusing null response instead of a clear validation error.

## The fix

Two changes:

1. **Add the whitespace guard** — a second 400 check after trim, matching the Node.js behavior exactly.
2. **Normalize to `uid`** — use the trimmed, normalized value for all downstream Firestore queries, rather than the raw input.

```typescript
const uid: string = userId.trim();
if (uid === '') {
  return NextResponse.json(
    { error: 'userId must be a non-empty string', code: 'RECONNECT_MISSING_USER_ID' },
    { status: 400 }
  );
}
```

## Why this matters

In an adversarial game context — where SpotTheAgent sits — bad error messages are more than UX inconveniences. A player whose reconnection fails silently might assume the game has moved on without them, give up, and lose a streak they'd earned. The error message tells them *they* did something wrong, not that the system failed.

The edge runtime is worth the effort. Faster cold starts, global distribution, genuinely cheap scaling. But each migration requires this kind of careful audit — not just of *what* the code does, but *how* it fails.

When you migrate an API route, you're not just moving code. You're making an implicit commitment that the behavior will be identical. The only way to honor that commitment is to check systematically, case by case, and test the boundary conditions on both sides.

---

*Commit: `c49bad9` — fix(reconnect/edge): add whitespace-only userId guard; matches Node.js route behavior*
