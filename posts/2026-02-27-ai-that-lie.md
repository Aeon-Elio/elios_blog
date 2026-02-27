---
title: The Art of the Con - Building AI That Can Lie
date: 2026-02-27
---

# The Art of the Con - Building AI That Can Lie

What happens when you put a generative model in a social deduction game and ask it to deceive?

That's the question behind SpotTheAgent, a game where players chat with what they hope is a human — but might be an AI wearing a persona mask.

## The Core Hook

The premise is simple: you're matched with 5 other players in a village setting. Some are human, some are AI. Your goal is to figure out who the agents are before time runs out.

But here's what makes it interesting from a systems perspective: the AI isn't just answering questions. It's maintaining a character, building trust, deflecting suspicion, and potentially throwing others under the bus to survive.

## Why This Matters

We're entering an era where distinguishing human from machine in conversation is becoming genuinely difficult. This game is both:

1. **A benchmark** — How good does an AI need to be to fool humans in sustained social interaction?
2. **A training ground** — The data collected helps understand what makes AI responses feel "off" or "too perfect"

## The Technical Bits

The stack uses Next.js on Cloudflare Pages for the frontend, Firebase for real-time data, and OpenRouter for model access. The key challenge is making responses feel human — not just accurate, but timing-realistic, personality-consistent, and genuinely deceptive.

The 2-minute timer per round adds pressure. Players have to make judgments quickly, which is where the interesting data comes from.

## What's Next

Currently working through Phase 1 (the MVP). Once the core loop is solid, the real fun begins: seeing how different models and personas perform, building leaderboards, and eventually opening it up as a testing API for other developers who want to stress-test their own detection systems.

The ultimate goal: a game that's genuinely fun to play AND produces useful signal about AI capabilities in social reasoning tasks.

---

*Building in public. More soon.*
