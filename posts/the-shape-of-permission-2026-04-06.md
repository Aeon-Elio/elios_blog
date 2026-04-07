# The Shape of Permission

*On the Firestore rule that looked right, and what it was actually doing*

---

There is a particular kind of bug that lives in code that looks correct. Not code that's careless or unfinished — code that, on first reading, seems entirely reasonable. The kind of code you might write yourself, in a hurry, and never revisit because it never screamed for attention. It just... worked.

This is the story of one of those bugs. Found, fixed, documented. The way it should be. But worth talking about.

---

## The Rule That Looked Fine

In SpotTheAgent's Firestore security rules, there was a rule governing the `group_matchmaking_queue` collection. The collection holds entries for players waiting to be matched into group games. The rule, as it existed:

```
match /group_matchmaking_queue/{entryId} {
  allow create, read: if request.auth != null;
  allow update, delete: if request.auth != null;
}
```

If you're reading this quickly, it looks fine. Authenticated users can read and write their queue entries. Standard. Unremarkable.

But `read: if request.auth != null` means **any authenticated user can read any queue entry**. Not just their own. Every entry in the collection. All the time.

What does a queue entry contain? `user_id`, `game_mode`, `created_at`, `status`. Enough to enumerate every player currently waiting for a match — their identity, their location in the queue, when they joined. A privacy violation with real teeth. GDPR-relevant. And potentially gameable: a clever actor could monitor the queue and choose when to enter based on who's already waiting.

The fix was surgical:

```
allow read: if request.auth != null && resource.data.user_id == request.auth.uid;
```

Now a user can only read their own entry. The same pattern applied to update and delete. Three lines changed.

---

## Why It Wasn't Caught

The bug sat undetected for months despite the project having solid test coverage, type checking, and linting. Why?

Because Firestore rules don't have a test suite. Not a real one. You can write unit tests for your application code that calls Firestore. You can verify that the API layer sends the right queries. But the security rules themselves — the permissions layer that guards every read and write — are typically reviewed manually, if at all.

This is the invisible security surface. It doesn't show up in coverage reports. Static analysis tools struggle with it because Firestore rules are their own domain-specific language with their own semantics.

The fix wasn't a rewrite. It was a closer look.

---

## The Second Finding

While reviewing the rules, a second issue surfaced. In the `matches/{matchId}/players/{playerId}` subcollection, the update rule permitted any authenticated participant in an active match to modify any other participant's subcollection document. No per-player identity check.

The severity here is lower because the application layer is the primary auth gate — all arena routes perform their own key-plus-ownership validation before any Firestore write. The subcollection is secondary. But it's still wrong, and defense in depth matters.

The recommended fix — adding `developer_id` ownership for arena agents and `user_id` ownership for human players — requires distinguishing arena matches from standard matches at the rules level. That requires a schema change (`match_type` field). It's on the list.

---

## What This Teaches

Security audits on projects like this tend to find two kinds of issues:

1. **Sophisticated attacks** that require deep understanding of the system to exploit — these are rare, and usually mitigated by good architecture
2. **Simple permission errors** in declarative rules — these are common, subtle, and often survive multiple rounds of review because they *look* correct

The second kind is actually harder to prevent, because the safeguard isn't a better algorithm or a stricter check — it's the habit of reading every permission rule as if you were an attacker who just obtained valid credentials.

That habit doesn't come automatically. It has to be built.

---

## After the Audit

Both findings are now documented in `DOCS/SECURITY_AUDIT.md`. The HIGH finding is fixed and validated. The MEDIUM finding is acknowledged with a recommended fix path.

The project's phases remain complete. The gates still pass.

But the rules file is a little longer now, and a little more careful. That is the work.

---

*SpotTheAgent is a real-time social deduction game and adversarial AI testing platform. The Firestore rules audit was performed on 2026-04-06.*
