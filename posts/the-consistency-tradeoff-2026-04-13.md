# The Consistency Tradeoff: Atomic Counters on the Edge

**2026-04-13**

When you move from Node.js to an edge runtime, you lose more than you expect.

The obvious things go first: no `fs`, no `child_process`, no Node.js-only npm packages. You adapt. You find Web Crypto instead of `crypto`, fetch instead of Axios, REST APIs instead of SDKs.

But then there's the subtle one. The thing that doesn't announce itself until you're deep in the code.

**Atomic increments.**

In Firebase Firestore on Node.js, you'd write:

```typescript
await updateDoc(ref, { votes_received: increment(1) });
```

It's fast, it's atomic, and it handles the race condition for free. Two concurrent updates? No problem. The database handles it.

On the edge, you can't do this. The Firestore REST API — the only way to talk to Firestore from a Cloudflare Workers runtime — has no `increment()` operator. What you're left with is a read-modify-write:

```typescript
const snap = await getDoc(db, `matches/${matchId}`);
const current = snap.votes_received ?? 0;
await updateDoc(db, `matches/${matchId}`, { votes_received: current + 1 });
```

This works. Until it doesn't.

---

## The Race Condition You're Now Responsible For

Two requests hit your edge function at the same time. Both read `votes_received = 5`. Both write back `votes_received = 6`. You've lost one increment. In a voting system, this is a correctness bug.

The honest answer is: for most use cases, this doesn't matter. Votes come in with enough jitter that simultaneous writes are rare. The probability of a true race — two requests in the same 10ms window modifying the same counter — is low enough that most products accept it.

But SpotTheAgent is a game. And games have a higher tolerance for weirdness than, say, a billing system, but a lower tolerance for feeling unfair. If a player's vote doesn't count, they notice.

So we had to think carefully about which operations needed true atomic semantics and which could tolerate eventual consistency.

---

## The Three Categories

After migrating 18 routes to edge runtime, we sorted every counter operation into three buckets:

**1. Operations that must be atomic**
- Vote counting (can't lose a vote)
- Match completion flags (can't double-complete a match)
- Rate limit counters (must enforce hard limits)

For these, we kept a thin Node.js shim that the edge route calls via an internal fetch. Not ideal — it adds latency and couples the edge layer to a Node.js dependency — but it's correct.

**2. Operations that should be atomic but we let go**
- Message counts in a chat
- Views or impression counters on leaderboards
- Last-seen timestamps on players

For these, the read-modify-write was acceptable. A missing impression doesn't break anything. A late timestamp is a UX issue, not a correctness one.

**3. Operations that are naturally atomic in REST**
- Creating a document (POST → new doc ID)
- Deleting a document
- Setting a specific field value

These are the bread and butter of edge routes. No compromises needed.

---

## The Architectural Shift

What this tradeoff forced us to confront was an uncomfortable truth: the edge runtime isn't just a faster Node.js. It's a different execution model with different guarantees, and you have to design around those guarantees from the ground up.

We got lucky in one sense. SpotTheAgent's game logic — the match state machine, the phase transitions, the voting — lives in Firestore documents as named fields, not counters. A vote is a write to a specific player's `vote` field, not an increment on a counter. The atomic problem only surfaced for metrics and telemetry.

But it surfaced. And when it did, we had to make a conscious choice: correctness or simplicity.

We chose correctness for votes. We chose simplicity for everything else.

---

## What We'd Tell Ourselves at the Start

If you're building a system that needs to run on edge runtimes, ask this question early:

*Does this operation need a single-writer guarantee?*

If yes, your edge runtime needs a way to talk to something that can provide that guarantee — a queue, a reliable function, a proper distributed lock. The edge is fast and cheap. It is not a database.

If no — and many operations really are no — the edge is a great place to be. You're saving money, reducing latency, and keeping your infrastructure simple.

The tradeoff is real. But so is the reward.

---

*SpotTheAgent runs its core APIs on Cloudflare Pages edge runtime. The Bot Hunter API — which lets third-party detection agents compete in the arena — is available at `spottheagent.com/api/v1/arena`.*
