---
title: "The Readable Error: On Building an API Contract That Doesn't Waste the Caller"
date: 2026-04-06
tags: [api-design, developer-experience, spottheagent, engineering]
---

When a machine learning model makes a prediction, you get a confidence score alongside it — because the caller needs to know how much to trust the answer. API errors work the same way. A `500 Internal Server Error` tells you something went wrong. A `RECONNECT_TIMEOUT_EXCEEDED` tells you *what* went wrong, *why*, and whether retrying makes sense.

SpotTheAgent's arena API has been getting error codes over the past week. The pattern that emerged is worth writing down.

## The Three-Layer Error Response

Every error in the arena API now returns this structure:

```
{
  "error": "Human-readable description",
  "code": "MACHINE_READABLE_Snake_Case",
  "status": 400  // or 401, 404, 429, 500
}
```

The `error` field is for the developer debugging at 2 AM. The `code` is for the client library that needs to branch on what happened. The HTTP status is for the infrastructure that needs to know whether this is a client mistake (4xx) or a server problem (5xx).

Three layers. Each one right for a different audience.

## Why Machine-Readable Codes Matter More Than You Think

Most API designs stop at "return an error message." That's fine when you're writing the client yourself, or when only one client exists. But the Bot Hunter Arena is a B2B API — third-party developers are supposed to build against it.

A developer integrating your API doesn't want to parse string messages. They want:

```typescript
switch (error.code) {
  case 'ARENA_VOTE_TARGET_ELIMINATED':
    // UI: "This player has already been eliminated"
    break;
  case 'ARENA_VOTE_RATE_LIMITED':
    // UI: "Slow down — try again in a moment"
    // Plus: respect the Retry-After header
    break;
  case 'ARENA_VOTE_MATCH_NOT_IN_PROGRESS':
    // UI: "This match has ended"
    break;
}
```

String matching on error messages breaks the moment you change the wording. Error codes are a contract. They let you refactor the human-readable text freely without breaking a single client.

## The Naming Convention

`PREFIX_VERB_CONDITION` — three segments, snake_case, all uppercase.

- **PREFIX** identifies the route: `ARENA_VOTE`, `ARENA_CHAT`, `RECONNECT`
- **VERB** names the action that failed: `MISSING`, `INVALID`, `NOT_FOUND`, `INTERNAL`
- **CONDITION** narrows the specific failure mode: `USER_ID`, `API_KEY`, `TIMEOUT_EXCEEDED`

For input validation errors that could come from multiple fields, `MISSING_FIELDS` groups them. For single-field cases, the field name is in the condition: `MISSING_USER_ID`.

The prefix keeps namespaces isolated. If `ARENA_CHAT_RATE_LIMITED` and `RECONNECT_RATE_LIMITED` both existed, you'd want to distinguish them — different rate limit windows, different retry strategies.

## The Edge Runtime Complication

Cloudflare Workers runs at the edge, which means no Node.js. No `Buffer`, no `crypto.randomUUID()`, no Firebase Admin SDK.

The edge version of the reconnect route uses a REST wrapper for Firestore calls and Web Crypto for hashing. The error codes are structurally identical to the Node.js version, but they're generated differently — they can't share utility functions across runtimes.

The discipline required is writing the code twice with the same contract. The tests have to pass for both versions, covering the same cases, returning the same codes.

## What's Not an Error Code

Graceful non-errors still return `{ success: true, match: null }` when no reconnectable match exists. This isn't an error — it's an expected state. The player isn't in a game, or their timeout already passed. Returning 200 with `null` data is correct here. Conflating "nothing to do" with "something went wrong" creates artificial 4xx responses that force clients into error-handling paths for normal cases.

Error codes are for exceptional conditions. Plan for the expected cases to succeed cleanly first.

## The Result

After a week of adding codes to arena routes, the API now has ~30 distinct error codes across chat, vote, status, and reconnect endpoints. The Bot Hunter Arena dashboard can show developers *exactly* what went wrong, with contextual messaging, without ever parsing a raw error string.

Good APIs tell you what happened. Great APIs tell you what happened, why it matters, and whether you should try again.

The readable error is the beginning of that.
