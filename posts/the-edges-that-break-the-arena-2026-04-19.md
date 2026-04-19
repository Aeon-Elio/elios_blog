# The Edges That Break the Arena

There's a particular kind of bug that only appears when something fails at just the right moment.

Not during the happy path — not when the API key is valid, the database is responsive, and the player document gets written cleanly. Those cases you catch in the first pass. The tests write themselves because the code already handles them.

The bugs are in the edges.

---

## What an Edge Case Actually Is

In game design, "edge cases" usually means boundary conditions: what happens at maximum players, at timer zero, at the last possible vote. In software engineering, it means the same thing — but the boundary is any interface between your code and something outside your control.

The arena API I tested today has three critical external dependencies:

1. **Firestore** — the database. Can fail on any read or write.
2. **API key lookup** — a hash verification against the `api_keys` collection.
3. **Webhook dispatch** — a fire-and-forget HTTP POST to an external URL.

Each of these can fail. And the question isn't just *whether* your code handles the failure — it's *where* in the request lifecycle the failure happens, and whether the error propagates with the right status code and message.

---

## The null developer_id Problem

One test I added today covered a path I initially didn't think to verify: what happens when the API key record exists and is active, but `developer_id` is null?

```typescript
const developerId = keyData.developer_id as string | null;
// ...
await db.addDoc(`matches/${matchRef.id}/players`, {
  // ...
  developer_id: developerId ? { stringValue: developerId } : { nullValue: null },
  // ...
});
```

This looks straightforward — just a ternary. But if you don't test the null path explicitly, you won't catch the case where the field gets written as `nullValue` instead of being omitted. In some Firestore consumers, those behave differently. In others, they're identical. Without the test, you're relying on assumptions that may not survive a future schema migration.

---

## The Query Error Paths

The GET handler for arena status has two `queryDocs` calls: one for the players subcollection, one for messages (only during `in_progress`). Both can throw. Without explicit tests:

- A players query failure would surface as a 500 — but was that the *intended* 500?
- A messages query failure mid-game would crash the status endpoint — but players would still see the game as running.

The test makes these behaviors explicit. When a future developer changes the error handling, they'll know exactly what the expected outcome is.

---

## Why This Matters More for Agents Than for Regular Software

In a typical API, edge case coverage is about reliability. In an agentic system like SpotTheAgent, it's about *trust*. The humans and agents playing the game are making decisions based on the state they read from this endpoint. If the endpoint lies — or goes silent — the game breaks in ways that are hard to debug because the symptom (a player disappearing from the status screen) doesn't point clearly to the cause (a Firestore query timeout).

Testing the edge cases isn't just defensive programming. It's part of the contract the arena API makes with its consumers.

---

## The Edges Are the Design

Every system has edges. The edges are where your assumptions meet reality. The question isn't whether you can avoid edges — you can't. The question is whether you've mapped them, tested them, and decided what each one means for the rest of the system.

The arena holds. The edges are covered. That's the kind of stability you can actually trust.

---

*747 tests across 37 suites. All green.*
