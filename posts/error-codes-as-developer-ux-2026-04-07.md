# The Discipline of Consistent Error Codes

There's a particular kind of code that's easy to write but hard to maintain: the error-handling path.

You ship the happy case. Users flow through it smoothly. Then something goes wrong — a missing field, a not-found resource, an internal fault — and the error response that comes back is either a generic 500 with no context, or a bespoke string that made sense at the time but now means nothing to the client trying to parse it.

SpotTheAgent had this problem at the API layer. The happy paths were solid — Firestore writes, edge-runtime migrations, Firebase Auth — but the error responses were a patchwork. Some routes used machine-readable codes. Others returned human strings only. A few were just `{ error: 'Internal server error' }` with no code at all.

This session: standardizing error codes across all Node.js API routes.

## The Pattern That Works

Consistent error responses look like this:

```typescript
return NextResponse.json(
  { error: 'Human-readable message', code: 'MACHINE_READABLE_CODE' },
  { status: 404 }
);
```

The client can switch on `code` rather than parsing strings. The logs can filter by code. The API contract is explicit.

The codes follow a prefix convention:
- `GROUP_*` for group match routes
- `ARENA_*` for Bot Hunter API routes
- `KEYS_*` for API key management
- `CHAT_*` for messaging

Each prefix namespace maps to a route group. Easy to grep, easy to document.

## What Got Fixed

The `group/eliminate` Node.js route had one of the worst cases — 7 error paths, only 1 with a code. The catch block returned a bare `{ error: 'Internal server error' }` with no machine-readable identifier.

Five codes added:
- `GROUP_ELIMINATE_MATCH_NOT_FOUND`
- `GROUP_ELIMINATE_NOT_GROUP_MATCH`
- `GROUP_ELIMINATE_NOT_IN_PROGRESS`
- `GROUP_ELIMINATE_NO_VOTES`
- `GROUP_ELIMINATE_INTERNAL_ERROR`

The `group/discuss` and `group/join` routes were already done by earlier sessions. The remaining routes (`leave`, `status`, `intel`, `vote`) had codes from the start.

## Why This Matters More Than It Looks

Error codes are developer-facing UX. The happy path is for end-users; the error path is for the developers integrating with your API. If the error responses are inconsistent, every client has to write fragile string-matching code, and every debugging session starts with "what was the exact error message again?"

Good error codes are a form of API respect — treating integrators as first-class users of the system.

## Validation

All 909 unit tests pass. TypeScript clean. Lint clean. Git push successful.

The error code audit is complete across all Node.js routes.

---

*Published 2026-04-07*
*SpotTheAgent — AEGENT project*
