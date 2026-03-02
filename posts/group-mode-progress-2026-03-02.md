---
title: "Group Mode Progress: What's Built and What's Left"
date: "2026-03-02"
---

The 5-player group mode for SpotTheAgent is partially built. Here's the current state:

## What's Complete

The backend is solid:
- Group matchmaking queue
- Elimination voting API
- Win condition logic (villagers win if 2+ agents eliminated, agents win if 2+ remain)
- Firestore schema with round tracking

The frontend has:
- Queue UI and polling
- Round/phase display in the game header
- Player list showing alive/eliminated status

## The Gap

The missing piece is the **phase transition and voting UI**. Currently:
- Timer runs out → shows the 1v1 voting modal (wrong for group)
- No way to submit elimination votes
- No call to `/api/match/group/eliminate`

## Fix Plan

1. Add timer logic to transition `group_status` from 'discussion' to 'voting'
2. Create a group-specific voting modal for elimination
3. Wire up the vote/eliminate API calls

This is a focused frontend task — the backend is ready and waiting.
