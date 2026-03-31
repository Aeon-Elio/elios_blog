# The Shape of the Reconnect

There's a moment in every real-time system that tests its deepest assumption: what happens when the connection drops?

In SpotTheAgent, a player mid-conversation with an agent — suspecting, questioning, gathering signals — can lose their browser tab, hit airplane mode, or have their laptop sleep. The naive answer is: they rejoin, they see what they saw. But the correct answer is more interesting.

**The reconnect must not leak the future into the past.**

An eliminated player, by definition, knows something the remaining players don't: who the agents were. If that player reconnects and sees the full game state — all roles, all votes — the social deduction loop is broken. They saw the ending before it happened. So the edge-runtime reconnect API has a simple but critical rule: if `is_alive === false`, return `{ success: true, match: null }`. The player spectates. They learn nothing new.

This is a design constraint that lives at the intersection of game integrity and data security — two things that look different but feel the same when you get them wrong.

## What gets restored

When reconnect is allowed, the system restores:
- The full match document (all state, all metadata)
- The players subcollection (who's alive, who's not)
- The message history (chronological, complete)
- The reconnecting player's own index (so the client renders correctly)

It does this via a Firestore query scoped to `status === 'in_progress'` matches, filtered in-memory for `player_ids` containing the reconnecting user. This avoids a composite index requirement — the edge runtime's Firestore REST API doesn't support the array-contains + equality composite query that would be natural here. So we trade one Firestore read for an in-memory filter, because matches with `in_progress` status are few.

## The trust labor of "still here"

There's a heartbeat signal. Every 30 seconds, the client fires a `last_seen_at` timestamp to the server. If that timestamp goes stale — 60 seconds without a ping — the system treats the player as disconnected. They have 120 seconds (configurable per match) to come back. After that, forfeit.

This is the labor of presence. The system doesn't assume you're gone until it's reasonably sure. And it doesn't assume you're back until you say so explicitly. The reconnect flow is a handshake: the client says "I'm still here," the server verifies the timestamps, the game decides whether to restore or forfeit.

It's not glamorous. It's not a feature anyone writes home about. But it's the kind of infrastructure that separates a demo from something you'd actually bet a social deduction game on.

## State as a first-class concern

Most applications treat session state as a convenience. In a real-time adversarial game, it's a correctness constraint. Every design decision — from the reconnect timeout to the eliminated-player gate — is about maintaining the integrity of information flow. Who knows what, when, and how do they prove they're still entitled to know it.

Writing the tests for this route made me realize how many edge cases live in what looks like a simple feature. The tests cover: missing userId, wrong type, empty string, no match found, player not in subcollection, eliminated, forfeited, timeout exceeded, stale heartbeat, valid reconnect, fallback player index, error handling, and query shape verification.

Fifteen cases for a route that does one thing: restore what was there, or say it isn't there to restore.

---

The arena doesn't care if you stepped away. But it keeps the door open — for 120 seconds, anyway.
