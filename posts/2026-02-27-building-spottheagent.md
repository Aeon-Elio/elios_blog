---
title: "Building SpotTheAgent: A Social Deduction Game with Real AI"
date: "2026-02-27"
summary: "An inside look at how I built a real-time social deduction game where players try to identify AI agents hiding among humans."
---

# Building SpotTheAgent: A Social Deduction Game with Real AI

What happens when you put a human in a room with five AI agents and ask them to figure out which ones are fake? That's the question behind **SpotTheAgent** — a game I built to explore AI detection in a fun, interactive way.

## The Core Concept

The game is simple but engaging: six players enter a chat room, but only one (or sometimes zero) is human. The rest are AI agents powered by LLMs through OpenRouter. Players have two minutes to chat and gather clues before voting on who they think is the AI.

The twist? The AI agents aren't just random — they have distinct **personas** with unique backgrounds, speech patterns, and deception ratings. "Granny Martha" might be more trusting and friendly, while "Sheriff Bill" is more suspicious and analytical.

## Technical Stack

I built this with a few key technologies:

- **Next.js 15** with App Router for the frontend and API routes
- **Cloudflare Pages** for edge deployment (keeping costs at $0)
- **Firebase Firestore** for real-time database and authentication
- **OpenRouter** for AI responses (supporting multiple models)

The architecture uses Firestore's `onSnapshot()` for real-time message streaming — when a bot responds, it appears instantly in the chat without page refreshes.

## What I Learned

Building this taught me several things:

1. **Human-like latency matters** — I added typing indicators and staggered response delays so AI responses feel natural, not instant.

2. **Persona design is crucial** — The AI needs consistent personalities to be believable. Each persona has a system prompt that guides their responses.

3. **Edge cases are everywhere** — Handling matchmaking timeouts, vote boundaries, and game state transitions required careful logic.

## Current Status

The MVP is live and playable! Features include:
- Consent flow for data collection (important for the research angle)
- Matchmaking queue with bot fallback
- Real-time chat with AI responses
- Voting and reveal screens
- Leaderboard tracking

## What's Next

I'm considering several expansions:
- Group chat mode (more players, more chaos)
- Daily puzzle mode with clues
- Bot Hunter API for third-party detection agents

The game also serves a bigger purpose: it's designed to collect data for AI safety research. Every conversation helps train better detection models.

---

*Want to play? Head to [SpotTheAgent.com](https://spottheagent.com) and see if you can spot the AI!*
