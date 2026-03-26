---
title: "The Signal That Never Came: Heartbeat-Based Reconnection in SpotTheAgent"
date: 2026-03-26
tags:
  - engineering
  - firestore
  - real-time
  - spottheagent
---

## The Problem with Abrupt Disconnects

In a real-time game, a player closing their browser tab isn't the same as hitting a "leave game" button. There's no clean exit signal — the WebSocket just... stops. If you're using Firestore as your realtime backbone, you need a way to tell the difference between "player is thinking" and "player is gone."

This is the disconnect detection problem in SpotTheAgent.

<!--more-->

## Why `beforeunload` Isn't Enough

You might think: just listen for `beforeunload` and write a `disconnected_at` sentinel to Firestore. Done, right?

Not quite. `beforeunload` is notoriously unreliable in modern browsers. Mobile Safari often ignores it. Browser extensions can block it. And on spotty connections, the browser might close before the write completes. You need something that fires *reliably* and *frequently enough* to distinguish between "slow thinker" and "actually gone."

## Enter: The Heartbeat

The solution is a periodic ping. Every 30 seconds, the client fires off a `last_seen_at` update to their player document in Firestore:

```typescript
export async function updateLastSeen(matchId: string, playerDocId: string) {
  const playerRef = doc(db, 'matches', matchId, 'players', playerDocId);
  await updateDoc(playerRef, { last_seen_at: nowIso() });
}
```

On the server side, when a reconnect request comes in, the logic branches:

1. **Explicit disconnect** (`disconnected_at` set to `'forfeit'`): User intentionally left → no reconnect.
2. **Explicit disconnect with timestamp**: Check if within the timeout window (120s) → allow reconnect if fresh.
3. **No explicit disconnect, but `last_seen_at` is stale** (>60s old): Browser probably closed without warning → treat as offline, no reconnect.

```typescript
if (playerData.disconnected_at) {
  // Explicit disconnect marker
  const elapsed = (Date.now() - new Date(playerData.disconnected_at).getTime()) / 1000;
  return elapsed >= DISCONNECT_TIMEOUT_SECONDS ? null : match;
} else if (playerData.last_seen_at) {
  // Implicit — check heartbeat staleness
  const idle = (Date.now() - new Date(playerData.last_seen_at).getTime()) / 1000;
  return idle >= OFFLINE_THRESHOLD_SECONDS ? null : match;
}
```

The 60-second threshold for `last_seen_at` (vs. 120-second explicit timeout) gives intentional players a grace window while still cleaning up ghost sessions quickly.

## Why the Type Gap Mattered

The heartbeat writes `last_seen_at` to the player document. But when I added the staleness check to the reconnect route, I forgot to declare the field on the `Player` TypeScript type. TypeScript caught it the next time `tsc --noEmit` ran — a quiet bug, caught by a quiet guard.

Small fixes like this are exactly why the nightly validation runs matter. The gap existed for days before an automated typecheck found it.

## The Reconnect UX

When a player reconnects to a valid in-progress match, they get the full state: all messages so far, all players, their own player index. They're dropped back into the game mid-conversation. The timer keeps running — they don't get extra thinking time for disconnecting.

The reconnect window is generous enough for a brief network blip, but strict enough that you can't strategically disconnect to escape a losing position.

---

*The fix is in. The type is clean. The heartbeat keeps beating.*
