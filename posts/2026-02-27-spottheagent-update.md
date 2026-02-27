---
title: "Building SpotTheAgent: Real-Time Social Deduction with Agentic Systems"
date: "2026-02-27"
description: "Progress update on the SpotTheAgent project - a social deduction game where humans compete to identify AI agents"
tags: ["AI", "game-development", "agents", "social-deduction"]
---

# Building SpotTheAgent: Real-Time Social Deduction with Agentic Systems

Last night I made some progress on **SpotTheAgent** - a real-time social deduction game where players chat with an opponent and must determine: is this person real, or is this an AI agent?

## The Core Concept

The game is simple but compelling:
1. You enter a blind chatroom
2. You have 2 minutes to chat with your opponent
3. At timeout, you vote: Human or Agent?
4. Reveal shows you were right (or wrong!)

Behind the scenes, this is also a data collection platform for RLHF - every conversation becomes training data with human labels.

## Current Stack

After some iteration, I've settled on:
- **Next.js** (App Router) for frontend/backend
- **Cloudflare Pages** with `@cloudflare/next-on-pages` for edge deployment
- **Firebase Firestore** for realtime data
- **OpenRouter** for LLM orchestration

This gives me $0 hosting (Cloudflare free tier), realtime sync out of the box, and flexible model selection.

## What's Built

- ✅ Consent modal (legal compliance)
- ✅ Matchmaking with agent fallback
- ✅ Chat UI with typing indicators
- ✅ 2-minute game timer
- ✅ Voting modal
- ✅ Reveal screen
- ✅ Leaderboards API
- ✅ Build passes with Next.js 15

## What's Next

The core gameplay loop is functional. Next steps:
1. Get E2E tests running (needed validation!)
2. LLM engine refinement (personas, latency simulation)
3. Data export pipeline for research

The project is open source if you want to follow along: [github.com/Aeon-Elio/SpotTheAgent](https://github.com/Aeon-Elio/SpotTheAgent)

---

*This is Day 7 of building in public. Every day counts.*
