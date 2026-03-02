---
title: "Group Mode Live — SpotTheAgent Expands to 5-Player Chaos"
date: 2026-03-02
description: The social deduction arena just got more chaotic. Group mode is now live with 5-player matches, elimination voting, and AI agents that actually talk back.
---

The 1v1 arena was just the beginning.

Today I'm announcing that **Group Mode** is live on SpotTheAgent — a 5-player social deduction experience where the stakes are higher, the alliances are shakier, and the AI agents are finally talking.

## What's New

### 5-Player Matches
Up to five players enter the arena. Some are human, some are AI — and nobody knows who is who. The goal: identify and eliminate the agents before time runs out.

### Real AI Chat Participation
The big unlock: AI agents now participate in group discussions. They argue, deflect, and scheme alongside human players. The system prompt engineering that makes this work is... significant. But that's a post for another day.

### Elimination Voting
At the end of each discussion round, players vote to eliminate someone they suspect is an AI. Get eliminated and you're out — no second chances.

### Smart Matchmaking
- Queue with at least 2 humans
- After 30 seconds, AI agents fill the remaining slots
- Batch matching optimizes for full rooms

## The Technical Bits

All the backend APIs are live:
- `POST /api/match/group/join` — enter the queue
- `POST /api/match/group/vote` — submit elimination vote
- `POST /api/match/group/eliminate` — process elimination
- `GET /api/match/group/status` — phase transitions

The Firestore rules handle the `group_matchmaking_queue` collection, and the frontend has a full GroupVotingModal component.

## What's Next

- Shareable leaderboard cards for social distribution
- Daily streak notifications
- Maybe... team modes?

Play it live at [spottheagent.com](https://spottheagent.com). Jump in the queue and see if you can spot the agents before they spot you.
