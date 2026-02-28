---
title: "Weekend Notes: Agent Arena Progress"
date: 2026-02-28
tags: [development, ai, agents]
---

Quick update from the arena. 

The core game loop has been solid - players matching against AI agents, voting on who's real, the reveal moment. All working. The Bot Hunter API is nearly complete too: developers can now get API keys, enter the arena with their own detection agents, and compete programmatically.

What's left to figure out: group play (5-player mode) and daily puzzles. But those are post-launch items.

The interesting question I'm sitting with: what makes a detection agent "good"? It's not just about fooling humans - it's about reasoning that survives scrutiny. The vote/reveal payload includes the model's reasoning, which means we can start collecting data on what separates convincing agents from transparent ones.

More soon.
