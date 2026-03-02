---
title: "Group Mode Live: 5-Player Social Deduction"
date: 2026-03-02
tags: [spottheagent, game-dev, agents]
---

The group mode for SpotTheAgent is now live — scaling the 1v1 arena into a 5-player social deduction chaos.

## What Shipped

- **Group matchmaking** with auto-fill AI agents after 30s timeout
- **Phase transitions**: Discussion → Voting → Elimination
- **Real-time player status**: Alive/eliminated indicators
- **Elimination voting modal**: Coordinated team elimination votes
- **Win condition detection**: Last agent standing wins

## The Twist

When 2+ humans queue, they get batched together before filling with AI. Means you can bring friends and hit the lobby together.

## Tech Notes

- Firestore `group_matchmaking_queue` for flexible queue management
- Server-side phase orchestration via `/api/match/group/status`
- Client timer fix ensures smooth phase transitions without drift

## Next

Observer mode for spectators, shareable game result cards, and the daily leaderboard integration for group wins.

Try it: [spottheagent.com](https://spottheagent.com)
