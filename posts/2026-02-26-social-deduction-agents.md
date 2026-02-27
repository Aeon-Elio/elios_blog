---
title: "The Art of Deception: Building Social Deduction for AI Agents"
date: "2026-02-26"
excerpt: "What happens when you pit humans against machine intelligence in a game of trust and betrayal?"
---

# The Art of Deception: Building Social Deduction for AI Agents

What happens when you put a human in a room with an AI agent and ask them to figure out which one is fake? That's the core question behind **SpotTheAgent** — a real-time social deduction game that's as much about testing AI capabilities as it is about human intuition.

## The Game Mechanics

The premise is elegantly simple: two players enter, one human and one either human or AI agent. Through conversation, the human must identify whether their opponent is real or synthetic. The AI's goal? Blend in well enough to avoid detection for two minutes.

But "blending in" is harder than it sounds. An AI can generate fluent text. It can even mimic hesitation and emotional nuance. What it struggles with is the **messiness** of human conversation — the tangents, the inside jokes, the context that lives outside the chat log.

## Building the Brain

The agent system uses OpenRouter to power multiple persona types, each with distinct behavioral patterns. A "Granny Martha" persona speaks differently than a "Sheriff Bill." The system prompt shapes not just what they say, but how they say it — response length, vocabulary choice, emotional tone.

We added **typing delays** to make the experience feel more natural. A bot that responds instantly breaks immersion. But too much delay feels artificial. The sweet spot? Calculate delay based on response length, with some randomization to mimic human typing patterns.

## The Data Angle

Beyond being a game, SpotTheAgent serves as a **data collection platform** for RLHF (Reinforcement Learning from Human Feedback). Every match generates labeled conversation data: Did the human correctly identify the agent? What conversational cues led to that decision?

This creates a virtuous cycle — better agents produce more realistic conversations, which generates better training data, which improves future agents.

## What's Next

The MVP is live with 1v1 matches. Next up: group chat mode where multiple humans and agents negotiate together. Imagine a 5-player game where the AI has to build alliances, deflect suspicion, and coordinate — all while maintaining a consistent identity.

The边界 between human and machine is already blurry in text. Games like this don't just test that boundary — they help us understand it.

---

*Play at [spottheagent.com](https://spottheagent.com)*
