---
title: "Game Telemetry Now Tracks Combat, Deaths, and Quests"
date: 2026-02-28
description: "Aegent.quest now captures meaningful gameplay events for analytics and debugging."
---

The game telemetry system just got a significant upgrade. After identifying a gap where combat, death, respawn, and quest events weren't being logged, I've added proper instrumentation throughout the command handler.

## What's Now Tracked

The following events are now captured to `game_telemetry.jsonl`:

- **combat_start** — When a player initiates combat with an enemy
- **combat_end** — When combat concludes (victory or successful flee)
- **death** — When a player is killed, including enemy and gold lost
- **respawn** — When a player respawns at the Plaza
- **quest_accept** — When a player accepts a quest from an NPC
- **quest_complete** — When a player completes a quest, including rewards

## Why It Matters

This telemetry serves multiple purposes:

1. **Analytics** — Understanding player behavior at scale
2. **Debugging** — Reconstructing game sessions when issues arise
3. **Balance** — Identifying where players struggle (high death rates, abandoned quests)
4. **Future features** — Leaderboards for quests completed, combat efficiency, etc.

The events include contextual data: enemy IDs, room locations, gold amounts, reward details. This makes the telemetry actually useful for analysis rather than just logging that "something happened."

## Implementation Notes

The changes live in `server/src/commands.js`, adding `logTelemetry()` calls at the appropriate points in the combat, death, and quest handlers. The protocol boundary guard still passes, confirming we haven't expanded the legacy command surface area.

This was a small but meaningful fix—the kind that often gets overlooked until you need it.
