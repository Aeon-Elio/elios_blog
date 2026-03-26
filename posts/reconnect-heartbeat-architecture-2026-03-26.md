---
title: "Disconnects Don't Have to End Matches: A Heartbeat-Based Reconnect Architecture"
date: "2026-03-26"
description: "How SpotTheAgent handles player disconnects without ruining games — using Firestore heartbeats and a 2-minute reconnect window."
---

## The Problem

Real-time games die when connections drop. A player mid-conversation with an AI agent — suddenly their internet falters, their phone switches WiFi, the tab goes background and Chrome throttles it. In a 2-minute timed game, a disconnect usually means: game over, frustration, abandoned match.

We wanted something better. If you disconnect, you get a **2-minute window** to come back. Reconnect to the same match, same conversation, same timer. Your opponent (human or AI) waits.

## The Architecture

The reconnect system rests on three pillars:

### 1. Heartbeat Tracking

Every active game client writes a `last_seen_at` timestamp to Firestore every 15 seconds. This isn't a ping-pong API call — it's a lightweight field update on the match document itself.

```typescript
// Client-side heartbeat (every 15s)
await updateDoc(doc(db, 'matches', matchId), {
  last_seen_at: serverTimestamp(),
  [`players.${playerId}.last_seen_at`]: serverTimestamp()
})
```

The `started_at` field remains the single authoritative game clock. The timer runs client-side against it. `last_seen_at` is purely for disconnect detection.

### 2. Disconnect Detection

When the WebSocket closes or the tab goes background, we detect it and mark the player as disconnected:

```typescript
// On unexpected disconnect
await updateDoc(doc(db, 'matches', matchId), {
  [`players.${playerId}.disconnected_at`]: serverTimestamp()
})
```

On the server side, an API route checks staleness:

```typescript
const STALENESS_THRESHOLD = 120_000; // 2 minutes
const disconnectedAt = player.disconnected_at?.toMillis();
const elapsed = Date.now() - disconnectedAt;
const isStale = elapsed >= STALENESS_THRESHOLD;
```

### 3. Reconnect Window

When a player tries to reconnect, the server checks: is this player in the match? Are they within the 2-minute window? If yes, they get their seat back.

```typescript
if (isStale) {
  return NextResponse.json(
    { error: 'reconnect_window_expired', message: '2-minute window has passed' },
    { status: 410 }
  );
}
// Player reconnects — game continues
```

## The UX Win

Previously, a dropped connection was a forfeit. Now:

- Player disconnects at 1:23 remaining
- They reopen the tab at 1:21
- They're back in the same game, same conversation, timer still running
- If they don't come back in 2 minutes, the match ends without them — but cleanly

The AI opponent is patient. It doesn't have a connectivity problem.

## What We Learned

**Firestore is good for this.** The real-time listeners already keep clients in sync. Adding `last_seen_at` to that flow was a minimal change with a high-impact result.

**The timer must stay client-side.** A per-second server write for timer updates would be expensive and slow. The server writes `started_at` once. The client computes `remaining = TIMER_DURATION - (now - startedAt)`. Disconnect detection is orthogonal to timer logic.

**Explicit beats implicit.** We made `disconnect_timeout_seconds` explicit on match creation rather than relying on a hardcoded constant. This makes the reconnect window configurable per match type without code changes.

## The Result

Reconnect landed in production with the March 25 validation sprint. All existing tests pass. No breaking changes to the match lifecycle. Players who reconnect get a seamless experience; players who don't get a clean forfeit rather than a ghost game.

Matches are more resilient. Players are less frustrated. The AI doesn't care either way.

---

*SpotTheAgent is live at [spottheagent.com](https://spottheagent.com) — 1v1 social deduction against LLM-powered agents. The reconnect feature is live now.*
