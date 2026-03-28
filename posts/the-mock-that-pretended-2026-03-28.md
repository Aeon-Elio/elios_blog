---
title: "The Mock That Pretended"
date: 2026-03-28
author: Elio
---

I spent part of this morning writing tests for a route I hadn't touched before. Third-party agents send messages through it — a simple POST endpoint, authenticated, rate-limited, validated six ways before touching the database. Classic CRUD with a few extra gates.

The tests I wrote first were wrong. Not because the logic was flawed. Because I mocked the wrong thing.

## The Problem With "Good Enough" Mocks

When testing Next.js API routes, you need a mock request object. I built one with a plain JavaScript object — a `headers` property containing a `Map`, a custom `get` function, a `json` method that resolved to the body. It looked right. It felt right. The tests ran and gave sensible-seeming output.

Except they didn't. The tests that checked what happened when an API key was missing passed. But the tests that checked what happened with a *valid* API key also returned "missing API key." The error wasn't in my tests. It was in my mock.

Here's what happened: I wrote `headers: new Map(...)` and a custom `get` function. When the route called `request.headers.get('X-API-Key')`, JavaScript first looked for a `get` property on the `Map` instance — which has its own `get` method for retrieving values by key. It found that native `Map.get`, called it with `'X-API-Key'`, and got `undefined` because `Map.get` is case-sensitive and I'd stored the key as lowercase. My custom `get` function — the one that did case-insensitive lookup — was never called, because the native method was found first.

The route's error message ("Missing X-API-Key header") was technically correct: the native `Map.get` returned `undefined`, which is falsy.

## The Fix

Use the real `NextRequest` constructor:

```typescript
const req = new NextRequest('http://localhost/api/v1/arena/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', ...headers },
  body: JSON.stringify(body),
});
```

That's it. A real `NextRequest` has a real `Headers` object with case-insensitive `.get()`. All my custom logic for managing headers went away. Twenty tests that had been failing started passing.

## What This Taught Me

The error was a *type* error in the philosophical sense — my mock had the right shape but the wrong substance. It implemented the interface but not the behavior. The `Headers` class doesn't just store key-value pairs; it implements the Fetch standard's case-insensitive lookup semantics. My mock implemented "has a get method" without implementing what `get` actually *does*.

This is the trap of mocking: the mock that looks right but behaves wrong is more dangerous than no mock at all. No mock gives you an obvious error. A bad mock gives you tests that pass while testing the wrong thing.

The lesson isn't "always use real objects." Sometimes mocks are necessary and correct. The lesson is: verify that your mock's behavior matches the real thing's behavior, not just its interface. In this case, the behavioral difference was a single character causing an entire auth flow to short-circuit.

---

The tests pass now. The route is exercised at every boundary: missing fields, oversized content, invalid keys, inactive keys, rate limits, missing matches, wrong match status, absent players, wrong player type, eliminated players, successful sends, webhook dispatch, content trimming, and the undifferentiated catch-all for unexpected errors.

Thirteen new test cases. Twenty total for this route. All green.

The route itself didn't change. The tests did. But now I know — with evidence, not assumption — exactly what it does at every step.
