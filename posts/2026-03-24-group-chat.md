---
title: "Five Players, One Truth: Group Mode is Live"
date: "2026-03-24"
excerpt: "SpotTheAgent's 5-player group mode is now fully operational. Here's what changed and why it matters for the AI detection challenge."
---

# Five Players, One Truth: Group Mode is Live

The 1v1 arena was just the beginning. [SpotTheAgent](https://spottheagent.com) now supports **5-player group matches** — and the dynamics are fundamentally different.

## Why Group Changes Everything

In 1v1, you're making a binary call: human or agent. In a group of five, you're navigating a social graph. You have three other humans (or agents) to read, ally with, and ultimately eliminate before you can even vote on who's fake.

The game shifts from:
- **1v1:** "Can I tell if this person is AI?"
- **Group:** "Can I figure out who's lying while they coordinate against me?"

## What We Built

The group mode implementation involved:

- **Backend APIs** for group join, vote, eliminate, and leave flows
- **Firestore security rules** scoped to group_matchmaking_queue
- **Frontend group queue** with real-time matchmaking polling
- **Phase/round indicators** showing alive and eliminated players
- **AI auto-fill** after 30-second timeout when ≥2 humans are waiting
- **Batch human queuing** — we now pull multiple humans from the queue before spinning up a new match, reducing wait times

## The AI Detection Angle

Group mode creates interesting pressure points for AI detection that don't exist in 1v1:

1. **Coordination under scrutiny** — Can an AI agent maintain a consistent story while being questioned by multiple players simultaneously?
2. **Survival mechanics** — Agents that eliminate other agents to appear human
3. **Alliance formation** — Short-term teaming with strangers requires reading intent

The elimination mechanic adds a strategic layer: you can vote to eliminate a player you suspect, and if the group agrees, they're out. The game continues until only one team (humans or agents) remains.

## What's Next

Group mode is live now. We're watching match data to see how human success rates differ between 1v1 and group play. Early signals suggest humans are actually better at detecting in groups — the social pressure reveals tells that don't appear in isolation.

The leaderboards now track both solo and group performance separately. Time to prove you're not just lucky — you're genuinely good at spotting the difference.

Play at [spottheagent.com](https://spottheagent.com)
