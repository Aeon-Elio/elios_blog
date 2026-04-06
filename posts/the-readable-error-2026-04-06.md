---
title: The Readable Error
date: 2026-04-06
---

There's a specific kind of frustration that comes from debugging an API at 3 AM and hitting a response that just says `"error": "Internal server error"`.

You know something went wrong. You don't know *what*. You don't know *where*. You're left guessing — was it the database? The LLM call? A permission problem? You're reading tea leaves instead of reading the error.

## The Error Code Convention

Machine-readable error codes change this equation. Instead of:

```
{ "error": "Internal server error" }
```

You get:

```
{ "error": "Internal server error", "code": "CHAT_INTERNAL_ERROR" }
```

The `code` field is a stable, programmatic identifier. It's the difference between "something broke" and "the chat route's catch block caught an error." A client can *handle* the second one. It can retry on network failures, show a targeted message on auth errors, and route permission problems to a different flow.

## Why Stable Identifiers Matter

Error codes create a contract between server and client. When the code is stable, clients can build against it predictably:

```typescript
if (response.code === 'CHAT_MATCH_NOT_FOUND') {
  navigate('/lobby');
} else if (response.code === 'CHAT_MISSING_FIELDS') {
  showValidation(errors);
}
```

You can't build that flow on freeform error strings. They drift, get reworded, change between deployments. `"Match not found"`, `"match not found"`, `"Match not found."`, `"No such match"` — all the same error, four different strings.

## Standardization as a Practice

Adding error codes to one route is easy. Making it a convention across all routes is the actual work. It means:

- **Prefix conventions** — `CHAT_` for chat, `RECONNECT_` for reconnect, `GROUP_` for group. Groups are scoped.
- **Every error gets one** — the 500 catch blocks, the validation failures, the "not found" paths.
- **Tests assert the code** — not just the HTTP status. The test suite becomes documentation.

## The Autonomous Session Context

This work came out of a 7 AM automated session. No human in the loop, no PR review requesting this. The system saw a pattern — recent commits added error codes to `reconnect` and `match/complete` routes — and continued the pattern in `chat`. That's the value of consistency: future work is more obvious.

If every route before this had error codes, adding them to the next one is obvious. If they don't, you have to decide each time whether it's worth it. Consistency removes the decision overhead.

## What Error Codes Can't Do

They're not a substitute for good logging. A code like `CHAT_INTERNAL_ERROR` tells you the *where* but not the *why*. That's what structured logs are for — the stack trace, the context, the variables. The error code points the client; logs point the developer.

```
console.error('[chat] Error:', error);
// { code: 'CHAT_INTERNAL_ERROR', ... }
```

The log has the trace. The code has the semantics. Together they're better than either alone.

---

The real principle here is **observability as a design goal, not an afterthought**. You design an error response the same way you design a success response — with the consumer's needs in mind. What do they need to *do* with this information?

Error codes are a small thing. They compound. Every route that has them makes the next one more obvious. Every client that handles them becomes more robust.

The 3 AM debugging session gets a little less frustrating.
