# Error Messages Are an API Surface

Most developers treat error messages as an afterthought — the thing you write after the happy path is done, when you're wrapping up and need to make sure the code doesn't leak anything embarrassing. "Something went wrong." "An error occurred." "Please try again." These are the developer equivalent of "um" in conversation: a verbal filler that acknowledges something happened without actually communicating.

This is a mistake. Error messages are not the negative space of an API. They are as much a part of the contract as the successful response. And treating them as such is one of the highest-leverage things you can do for developer experience.

## What makes an error message bad

The cardinal sin is **vagueness at the wrong layer**. When a REST endpoint returns a 500 with the body "Internal server error," the HTTP status code tells the consumer exactly what they need to know at the network level: something went wrong on the server. But "internal server error" as a body tells them *nothing* about what actually happened, what state they or the server might be in, or what they should do next.

The problem compounds when the error is localizable or has multiple failure modes that produce the same opaque message. If "Login failed" can mean wrong password, account locked, session expired, server unreachable, or rate limit hit, and all of these produce the same response, then every consumer of your API has to implement the logic you should have written — figuring out what went wrong from the observable behavior.

This is making your consumers do your job.

## The machine-readable layer

The practical solution is a two-layer error contract. The first layer is a machine-readable code — a string like `INVALID_LEADERBOARD_TYPE` or `RATE_LIMIT_EXCEEDED` that a consumer can switch on programmatically. The second layer is a human-readable message — a string like "The leaderboard type must be one of: weekly, monthly, all_time" — that a developer sees when something goes wrong.

The machine-readable code is not for the end user. It's for the developer building against your API, so they can handle failures without having to parse strings or reverse-engineer your error semantics. The human-readable message is for the developer when something goes wrong unexpectedly — it should contain enough context to understand what happened and, ideally, what to do about it.

```typescript
// Bad: one layer, all ambiguity
{ "error": "Invalid type" }

// Better: two layers, clear contract
{
  "error": "INVALID_LEADERBOARD_TYPE",
  "message": "The leaderboard type must be one of: weekly, monthly, all_time",
  "status": 400
}
```

Note that the code `INVALID_LEADERBOARD_TYPE` is not a description of what went wrong — it's a stable identifier for a specific failure mode. It shouldn't change between versions, even if you rewrite the message. The code is the contract. The message is the documentation.

## Codes should be consistent across endpoints

Here's a pattern I've found valuable: define your error code vocabulary at the API level, not the endpoint level. When a consumer sees `*_INVALID_TYPE`, they should know that this class of error means "a parameter that accepts enumerated values received a value outside that set." Whether that's a leaderboard type, a sort direction, a content status — the meaning is the same. They can handle it uniformly.

This means your error codes become a language. Developers learn the vocabulary once, and then your entire API becomes more predictable. `*_NOT_FOUND` means the resource doesn't exist or the caller doesn't have access to it. `*_PERMISSION_DENIED` means the caller tried to do something they're not allowed to do. `*_VALIDATION_ERROR` means the request body or parameters failed a check.

When every endpoint invents its own error codes for equivalent failure modes, you're making your API harder to learn. When you use consistent vocabulary across endpoints, you're giving your consumers a cognitive shortcut they can apply everywhere.

## Error codes are part of your stability contract

Error codes need to be stable. A consumer who writes code that handles `INVALID_LEADERBOARD_TYPE` is depending on that code continuing to exist and continuing to mean the same thing. If you rename it to `LEADERBOARD_TYPE_ERROR` in a future version, you've broken their integration — not because the functionality changed, but because the error contract changed.

This means you should version your error code vocabulary the same way you version your API. Document what codes exist, what they mean, and treat changes to them as breaking changes that require a major version bump.

## The testing question

One underappreciated benefit of machine-readable error codes: they're testable in a way that free-form error messages are not. You can write assertions that verify the exact code returned for each failure mode:

```typescript
expect(await api.leaderboards.get({ type: 'invalid' })).toMatchObject({
  status: 400,
  error: 'INVALID_LEADERBOARD_TYPE'
});
```

You cannot do this reliably with strings. Strings are brittle — a whitespace change, a capitalization shift, a slight rewording — and your tests fail, even though nothing meaningful changed. Error codes give you stable, refactorable failure assertions.

## Start with your errors

When I'm designing a new API surface, I write the error codes first. Before I write the happy-path handlers, I document all the ways a request can fail and what code each failure mode gets. This forces clarity about the failure taxonomy early — before the implementation diverges from the intent.

It's also a useful forcing function for edge cases. When I write out `DUPLICATE_ENTRY`, `WRITE_RATE_LIMITED`, and `SCHEMA_VALIDATION_FAILED` as the expected error codes for a new endpoint, I immediately start asking: what does duplicate mean here? What's the write rate limit? What exactly are we validating? These are questions worth answering before the code exists, not after.

---

Error messages are not where you stop communicating. They're where you start communicating under duress — when something has gone wrong, when the consumer needs to understand what happened, and when they need to decide what to do next. Treat them with the same care you'd give any other part of your API contract.

You'd be surprised how much a well-designed error response tells a developer that they've chosen the right API to build against.
