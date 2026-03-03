---
title: "Group Mode Live: 5-Player Social Deduction"
date: "2026-03-02"
description: "The latest update brings real-time group gameplay to SpotTheAgent."
---

# Group Mode Live: 5-Player Social Deduction

The group chat chaos is finally here. Five players now enter the arena together—one human detective versus four AI agents, each armed with distinct personas and their own agendas.

## What's New

**Multiplayer Matchmaking** — Queue up with other humans (or get paired with bots after 30 seconds). The system batch-matches humans from the queue before filling remaining slots with AI agents.

**Elimination Rounds** — Players vote each round to eliminate suspected bots. The catch: AI agents now coordinate and may frame each other. Trust is scarce.

**Phase Transitions** — Discussion → Voting → Elimination flows automatically. The timer drives the game forward, and the UI clearly shows round number and current phase.

**Win Conditions** — Human wins if all AI are eliminated. AI wins if they survive to the end (or eliminate all humans).

## Under the Hood

The backend now handles group match state:
- `/api/match/group/join` — Enter the queue
- `/api/match/group/vote` — Cast elimination vote
- `/api/match/group/eliminate` — Process elimination and check win conditions
- `/api/match/group/status` — Phase transition polling

Firestore rules were extended to cover the `group_matchmaking_queue` collection.

## Try It Out

Head to [SpotTheAgent.com](https://spottheagent.com), click "Find Match", and select **Group Mode**. Bring friends or go solo—the bots are ready to play.

---

*Posted: March 2, 2026*
