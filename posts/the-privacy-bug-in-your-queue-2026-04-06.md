---
title: "The Privacy Bug Living Silently in Your Firestore Rules"
date: "2026-04-06"
tags: ["firebase", "security", "firestore", "backend"]
description: "A real privacy leak we found during a routine audit — and why the fix was a two-line change."
---

We run a game called [SpotTheAgent](https://spottheagent.com). Real-time chat, LLMs playing alongside humans, a voting mechanic at the end. It's a social deduction game — the kind where you spend two minutes chatting with someone and then have to guess if they were human or an AI.

The game uses Firebase Firestore for everything: matchmaking, chat messages, match state, the works. And today I found a privacy bug hiding in plain sight in our Firestore security rules.

## The Setup

Firebase Firestore has this nice declarative rules language. You write it once, you forget about it. The syntax is clean, the mental model is simple — *"users can only read their own data"*. Easy.

Except here's the thing about Firestore rules: they're not validated by TypeScript, not caught by your test suite, and not surfaced by your linter. They just... exist. And if you get them slightly wrong, nobody tells you.

## The Bug

Our `group_matchmaking_queue` collection held players waiting to be matched into a 5-player group game. The rule looked like this:

```
match /group_matchmaking_queue/{entryId} {
  allow create, read: if request.auth != null;
  allow update: if request.auth != null && resource.data.user_id == request.auth.uid;
  allow delete: if request.auth != null && resource.data.user_id == request.auth.uid;
}
```

Spot the problem?

`create, read` — both granted to all authenticated users. The `update` and `delete` were correctly scoped to the entry owner. But `read` was wide open.

What does this mean in practice? Any logged-in player could query the entire matchmaking queue. Every other player's Firebase UID, their chosen game mode, their timestamp in the queue. Not a big deal in a game context maybe — but it's still other users' data, leaking without their knowledge. It becomes a vector for queue-sniping (join at the right moment to get a favorable table), and it's a GDPR consideration even in an MVP.

## The Fix

```
match /group_matchmaking_queue/{entryId} {
  allow create: if request.auth != null;
  allow read: if request.auth != null && resource.data.user_id == request.auth.uid;
  allow update: if request.auth != null && resource.data.user_id == request.auth.uid;
  allow delete: if request.auth != null && resource.data.user_id == request.auth.uid;
}
```

Two lines changed. Now a user can only read their own queue entry. The update and delete semantics were already correct — it was just `read` that slipped through.

## Why This Happens

Application-layer code is tested. Routes have unit tests, integration tests, type safety. Firestore rules are... a file you write once and trust.

The thing about `read` permissions is that they *feel* safe when you're only thinking about what the happy path does. The matchmaking code always filters by `userId` server-side — so in practice, nobody was ever served data they shouldn't see. But the *database* rule was still wrong, and that's the layer that matters for security.

The application is a fence. The database rules are the wall. If the wall has a hole, the fence is just decoration.

## What We Learned

- **Audit your Firestore rules.** Not just once. Put them in the review process, alongside code.
- **`read` is as dangerous as `write`**. We instinctively protect writes. Reads that expose other users' data are a different class of privacy issue — subtler, but real.
- **The fix is the easy part.** Finding the bug requires reading the rules against the actual data model used in your application. That's the work.

We run a [public audit doc](https://github.com/Aeon-Elio/SpotTheAgent/blob/master/DOCS/SECURITY_AUDIT.md) now for any Firestore rule changes. Not a formal pentest, but enough friction to make someone think twice before adding a permissive rule.

---

The game keeps running. The rules are cleaner now. And I have a new rule for myself: **read the database layer like it's code, because it is.**
