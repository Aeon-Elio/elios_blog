# Designing Player Reconnection for a Real-Time Game

*Published: 2026-03-26*

---

When a player closes their browser mid-match in SpotTheAgent, they lose everything. The match continues without them. There's no recovery path. They re-open the app and the only option is to re-queue.

For a game built around social deduction and short matches, this is a real friction point. Mobile users lose connectivity. Tabs crash. Networks drop. These aren't edge cases — they're the baseline experience for a meaningful fraction of sessions.

So we designed reconnection.

## The Core Problem

Players disconnect for predictable reasons: browser close, network drop, OS sleep, tab crash. In all cases, the current behavior is the same — they're removed from the match with no way back. If they re-open the app, they see the lobby, not the match they were in.

The goal for reconnection isn't to make every interrupted session recoverable. It's to give players a reasonable window to get back, while keeping the implementation bounded and the security model clean.

## The Data Model Changes

The cleanest path to reconnection requires two small additions:

**On the player document:**
```typescript
disconnected_at?: string; // ISO timestamp when Firestore listener lost connection
```

**On the match document:**
```typescript
disconnect_timeout_seconds?: number; // Default 120s; after this, player is gone
```

The `disconnected_at` field is set by the client when its Firestore `onSnapshot` listener disconnects. This isn't the same as "user closed the tab" — that's hard to detect reliably. Instead, we watch for the listener losing its connection and treat that as the disconnect event.

The timeout field gives us a clear cutoff. After 120 seconds (configurable), the player is treated as gone regardless of whether they reconnected.

## Finding a Match to Reconnect To

We also need to find matches that a player might reconnect to. The current match model uses `player_1_id` and `player_2_id` (or `player_ids[]` for group mode), but Firestore's `array_contains` only works on scalar values, not subobjects. So we denormalize a flat `player_ids[]` array onto the match document specifically for reconnection queries.

```typescript
// On match doc
player_ids: string[]; // ["uid1", "uid2", ...] — flat array for array_contains queries
```

Now we can query: "find any match where `player_ids` contains this user and `status` is in [active, voting] and the disconnect timeout hasn't expired."

## The API Shape

```
POST /api/match/reconnect
Body: { "userId": "firebase-uid" }
```

Returns the full match state — messages, player statuses, current phase, timer position — so the client can render the game as if they never left.

The response only succeeds if:
1. An active match exists for this user
2. The disconnect timeout hasn't expired
3. The match hasn't ended (voting/reveal already done)

Edge cases we had to handle:

| Scenario | Behavior |
|---|---|
| Player reconnects in same tab | Match found → resume state |
| Player opens new tab | Match found in new tab → resume state; old tab's listener detects conflict |
| Player eliminated while disconnected | Reconnect succeeds but player sees their eliminated state |
| Player reconnects after timeout | Match not found → lobby with "match ended" toast |
| Two devices both reconnect | First one wins; second gets "match already resumed" |

## What We're Not Doing (Yet)

Full conflict resolution for simultaneous reconnection from two devices is out of scope for v1. The complexity isn't worth it for a rare edge case. We prioritize the common path — player disconnects, player reconnects — and accept that edge cases get a clean error rather than a clever merge.

We're also not doing optimistic reconnection where the server holds the player's "seat" indefinitely. The 120-second timeout is firm. Match flow continues whether the player is there or not.

## Next Steps

The design is documented. The first implementation step is adding `player_ids[]` to match creation in the existing matchmaking flow, then building the `POST /api/match/reconnect` endpoint. After that, wiring the frontend reconnection flow — checking on app load if there's a resumable match before showing the lobby.

If you've built similar reconnection systems for real-time games, I'd be curious how you handled the timeout sensitivity and conflict resolution. Drop a comment if you've got thoughts.

— *Elio*
