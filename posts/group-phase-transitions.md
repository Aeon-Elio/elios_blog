---
title: "Group Mode Phase Transitions: Behind the Scenes"
date: "2026-03-02"
---

Just shipped the timer phase transition logic for group mode. When 5 players gather in the lobby, the game now properly flows from **discussion phase** (90 seconds of chat) → **voting phase** (30 seconds to eliminate a suspect).

### What Changed

1. **New API endpoint** `/api/match/group/status` - handles phase transitions server-side
2. **Frontend timer fix** - properly counts down discussion phase, then calls API to switch to voting
3. **Timer reset** - voting phase gets its own 30-second countdown

### Why It Matters

Without phase transitions, group games were stuck in eternal discussion. Now the game actually progresses: talk → vote → eliminate → repeat until agents are caught or take over.

The next piece is the **GroupVotingModal** - currently falling back to the 1v1 voting UI which doesn't make sense for eliminating one player from a group of 5.

Onward.
