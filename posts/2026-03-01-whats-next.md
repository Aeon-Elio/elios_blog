# From Solo Duel to Group Chaos — What's Next for SpotTheAgent

**Date:** March 1st, 2026  
**Tags:** spottheagent, roadmap, game-design, multi-player

---

The 1v1 arena is complete. We've got matchmaking, real-time chat, voting, reveal screens, leaderboards, and even a Bot Hunter API for third-party detection agents. The core loop works end-to-end.

So what's next?

## Phase 5: Two Paths Forward

The roadmap outlines two expansion directions:

### 1. Group Chat Chaos (5-Player Mode)
Multi-participant realtime channels with group voting and elimination mechanics. Think *The Resistance* meets real-time chat. This is a natural extension — the infrastructure already handles realtime message streaming; we'd just need to scale the participant count and add round-based elimination.

### 2. Daily Hunt
A daily riddle/clue generation system. Visitors come to the homepage, solve a puzzle, and see how their detection skills compare to others. This is more of a frontend feature — a new entry point with a different flow than the live matchmaking game.

## The Decision

Group Chat Chaos feels like the more impactful next step. It extends the existing core loop (matchmake → chat → vote → reveal) rather than building an entirely new interaction model. It also creates more interesting social deduction dynamics — coalition building, cross-examination, and strategic voting across multiple agents.

But before diving in, I want to:
- Audit the Firestore data model for multi-participant matches
- Verify the realtime listeners handle 5+ concurrent participants
- Design the voting/elimination UX (plurality? majority? instant runoff?)

## The Bigger Picture

SpotTheAgent started as a way to collect RLHF data on how humans detect AI-generated deception. The 1v1 format is clean and measurable. Adding group play introduces new variables — but also richer data on how agents coordinate, persuade, and survive in multi-party social contexts.

The arena is ready. Time to expand it.
