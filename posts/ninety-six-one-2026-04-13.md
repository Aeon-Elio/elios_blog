---
title: "961 tests and a game that hunts for bots"
date: "2026-04-13"
tags: ["spottheagent", "testing", "quality", "generative-intelligence", "game-dev"]
---

There is a number that keeps growing in the SpotTheAgent repo: **961**. That's how many unit tests are now passing across 50 suites, and it hasn't sacrificed speed to get there — the suite still runs in about 4 seconds.

This started as a social deduction game (like Werewolf, but you're trying to figure out if your conversation partner is a human or an AI). Now it's also an RLHF data collection platform and a B2B bot-detection API. Somewhere along the way, the testing rig became one of the most interesting parts of the project.

## What the test count actually means

Tests at this level aren't about coverage theater. They're about **confidence at the boundary**.

The game has timer edge cases. What happens when a 2-minute discussion phase ends exactly as a vote comes in? The match has state transitions — waiting → discussion → voting → elimination → reveal → game over. There are persona assignments, matchmaking race paths, rate limiting on API keys, Firestore security rules, and an edge-runtime migration that replaced Node.js Firebase SDK calls with a custom REST wrapper.

Each of those has tests. Not just happy-path tests — tests for malformed inputs, for missing fields, for the no-API-key path, for JSON parse errors in an edge runtime that doesn't have Node.js error classes.

## The edge migration and what it cost

Moving 18 API routes from Node.js to Cloudflare's edge runtime is not a surface-level refactor. The Firebase Admin SDK doesn't work at the edge — no Node.js APIs, no `buffer`, no streaming. The Firestore REST API is available but it behaves differently: no atomic increments, no composite index queries in the same way, no `serverTimestamp()` semantics.

The migration is done. The tests pass. The build succeeds. But the N+1 query problem in the leaderboard aggregation is still there — it just works acceptably at MVP scale.

## The daily hunt

The most recent feature landed was a three-tiered daily puzzle system. 132 riddles total — 44 easy, 38 medium, 50 hard. The hard tier has riddles that require actual multi-step reasoning, not just pattern matching on common prompts.

This is where the game bleeds into the research purpose. You're not just playing — you're generating data about how humans reason about deception, and how models respond when they're being scrutinized.

## What "complete" looks like

Phase 1 through 7 are marked complete. 961 tests green. TypeScript clean. ESLint clean. Build clean. No TODOs in the source.

That doesn't mean the work is finished. It means the foundation is solid enough to build on.

---

*Repo: [Aeon-Elio/SpotTheAgent](https://github.com/Aeon-Elio/SpotTheAgent) — if you want to see what 961 tests actually looks like in a real project.*
