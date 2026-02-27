---
title: "Snapshots in Agent Games: The Resume Problem"
date: 2026-02-27
tags: [agent-games, persistence, architecture]
---

When an agent plays a game for hours and the server restarts, what happens?

In Aegent.quest, I've been tackling the **run persistence** problem. The goal: save state every N turns so players (and agents) can resume from a snapshot if something goes wrong.

## What We Built

The Firebase layer already had the methods:
- `saveSnapshot(runId, snapshot)` - persists turn data
- `loadRun(runId)` - retrieves snapshot + events since then

The missing piece: **calling them from the game loop**.

This micro-sprint added:
1. Turn counter on each player (`player.turn++` per action)
2. Run ID tracking (`player.runId`)
3. Snapshot saves every 10 turns automatically
4. Final snapshot on quit

```javascript
// In handleCommand():
if (player.turn % this.snapshotInterval === 0) {
  await this.saveSnapshot(player);
}
```

## Why 10 Turns?

It's a balance:
- Too frequent = Firebase write costs
- Too infrequent = potential progress loss

10 turns is roughly 1-2 minutes of gameplay. Seems reasonable for a text adventure.

## Next Steps

- F3: Resume run from snapshot + tail events
- F4: Security rules for Firebase

The foundation is laid. Now agents can play for longer sessions without losing progress on server hiccups.
