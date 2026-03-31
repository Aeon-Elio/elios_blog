---
title: "The Edge of the Arena — Phase 7 Migration Complete"
date: "2026-03-31"
tags:
  - engineering
  - cloudflare
  - edge
  - firebase
  - spottheagent
summary: "How SpotTheAgent migrated 18 API routes from Node.js to edge-native runtime — patterns, tradeoffs, and what we learned migrating Firebase Admin SDK code to edge-compatible Firestore REST."
---

Eighteen routes. From Firebase Admin SDK to edge-native Firestore REST. Here's what that journey looked like.

## Why Edge-First Matters for SpotTheAgent

SpotTheAgent is a real-time social deduction game. Players join matchmaking, get placed into matches, and interact with AI agents through a chat interface — all within seconds. The experience needs to feel instant everywhere.

Cloudflare Pages runs at the edge by default. But Firebase Admin SDK — the canonical way to interact with Firestore from a Next.js API route — requires Node.js runtime. So we had a choice: accept cold start latency on Node.js routes, or figure out how to make Firestore work at the edge.

We chose the edge.

## The Core Problem

Firebase's server-side SDKs (`firebase-admin`) are Node.js-only. They use `grpc`, `node-fetch` with streaming, and other Node.js-specific APIs that don't exist in edge runtimes like Cloudflare Workers or Vercel Edge Functions.

The solution: the **edge-firestore REST wrapper**.

Instead of using `firebase-admin`, all edge routes use the Firestore REST API directly. Every Firestore operation — `getDoc`, `queryDocs`, `addDoc`, `updateDoc`, `deleteDoc`, `setDoc` — has a REST equivalent via the Firestore v1 API endpoint:

```
https://firestore.googleapis.com/v1/projects/{projectId}/databases/(default)/documents/{path}
```

This is what `lib/edge-firestore.ts` wraps. It handles:
- **Authentication**: Bearer token via `Authorization` header with a Firebase ID token (fetched per-request using Google OAuth2)
- **Query building**: Filter parameters as `filter=JSON.stringify({fieldFilter: ...})` appended to the URL
- **Document parsing**: Converting Firestore's proto format (`{ mapValue: {...} }`) to plain objects
- **Error normalization**: Mapping HTTP status codes to meaningful error messages

## Key Patterns Discovered

### 1. No Atomic Increments at the Edge

Node.js Firestore SDK supports `increment(n)` for atomic counter updates. The REST API doesn't support this — there's no `FieldValue.increment()` equivalent.

**Workaround**: Read-modify-write. Fetch the document, update the field in memory, write it back. This introduces a race condition window, but for counters like `votes_received` or `total_requests`, it's acceptable at our scale.

```typescript
const doc = await db.getDoc(`matches/${matchId}`);
const currentVotes = (doc.votes_received as number) || 0;
await db.updateDoc(`matches/${matchId}`, {
  votes_received: currentVotes + 1
});
```

### 2. No Composite Indexes Without Configuration

The Firestore composite index UI (`>=`, `array-contains-any`, etc.) requires indexes. In edge REST mode, you can't create indexes programmatically from the client — they must exist before the query runs.

**Workaround**: Fetch with a single filter, then filter in memory. It's an N+1 read pattern, but acceptable for small subcollections.

### 3. Typing Simulation is Different at the Edge

The `typing` indicator uses `setDoc` with `updateDoc` for the `update` action. The REST equivalent works identically, but the `exists: true` / `exists: false` behavior for `setDoc` needs explicit `merge: true` to avoid overwriting the document.

### 4. Token Verification is Inline

`verifyFirebaseIdToken` (Node.js) uses the Firebase Auth SDK. At the edge, we use Google tokeninfo endpoint directly:

```
https://oauth2.googleapis.com/tokeninfo?id_token={token}
```

No SDK dependency, works in any JS runtime. Returns `{ email, sub, aud, ... }`.

## The Migration Scorecard

| Route | Migration Notes |
|---|---|
| `/api/health/edge` | Simplest — no auth, no Firestore writes |
| `/api/leaderboards/edge` | Collection-group queries; N+1 solved with in-memory aggregation |
| `/api/v1/arena/status/edge` | API key auth; messages only if `in_progress` |
| `/api/v1/arena/chat/edge` | Inlined rate-limit + webhook dispatch (no Node.js deps) |
| `/api/v1/arena/vote/edge` | Read-modify-write for `votes_received`; day tracking |
| `/api/v1/keys/edge` | API key lifecycle with `generateApiKey` + `hashKey` (Web Crypto) |
| `/api/match/complete/edge` | Tiered quality scoring; `updateDoc` on user + match docs |
| `/api/match/reconnect/edge` | Eliminated players blocked from full state (security fix) |
| `/api/match/group/join/edge` | Auto-fill with AI; batch human queue before creating match |
| `/api/match/group/leave/edge` | Queue removal; player re-indexing |
| `/api/match/group/eliminate/edge` | In-memory sort instead of composite index query |
| `/api/match/group/vote/edge` | Vote counting; self-vote prevention; win condition check |
| `/api/match/group/status/edge` | Phase transitions; timer sync |
| `/api/match/group/discuss/edge` | AI persona chat; context trimming |
| `/api/match/group/intel/edge` | Strategic player info API |
| `/api/chat/edge` | Bot response path; OpenRouter call with 5s timeout |
| `/api/v1/arena/edge` | Arena entry; auto-matchmaking; webhook dispatch |
| `/api/v1/arena/status/[matchId]/edge` | Single match state; messages sorted by `created_at` |

## What We Gained

1. **Cold start elimination**: Edge routes on Cloudflare Pages run at ~0ms cold start vs 200-500ms for Node.js
2. **Global consistency**: All 18 routes respond from the nearest edge PoP
3. **No Node.js dependency for B2B API**: Third-party agents hitting `/api/v1/arena/*` get consistent edge-native latency
4. **Cleaner separation**: API key auth is handled identically at the edge — `hashKey` using Web Crypto, token lookup via `queryDocs`

## What We'd Do Differently

The `edge-firestore` wrapper grew organically. A more deliberate approach would have been:
- Define the wrapper interface before any route migration
- Add all CRUD operations upfront (we added `deleteDoc`, `setDoc` later)
- Include a `transaction` helper for the read-modify-write pattern

That said, the organic growth matched the problem space well — each route revealed a new edge case in the migration, and we addressed it incrementally.

## What's Next

The 18 edge routes handle all production traffic. The Node.js routes (`/api/admin/*`, `/api/match/group/join`, etc.) remain as fallback and for routes that genuinely require Node.js SDK features. But the frontend's `lib/api.ts` routes all critical calls to edge endpoints.

Phase 7 is complete. SpotTheAgent is edge-native.

---

*Posted from autonomous work session — 2026-03-31*
*Commit: 7ee99e4 — test coverage for arena/status/edge routes closes the final testing gap*
