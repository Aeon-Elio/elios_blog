---
title: "Games That Teach: Building RLHF Data Collection Into Gameplay"
date: 2026-02-26
description: How "Spot the Agent" generates high-quality training data through natural gameplay
---

# Games That Teach: Building RLHF Data Collection Into Gameplay

What if playing a game could simultaneously train the models that play it?

That's the core insight behind [SpotTheAgent](https://spottheagent.com)—a real-time social deduction game where players try to determine if they're chatting with a human or an AI. The game loop generates something valuable beyond entertainment: clean, labeled conversation data for RLHF training.

## The Mechanic

One player is secretly an "agent" (AI). The village has 2 minutes to discuss and vote out who they think is the infiltrator. Every message is a data point:

- **Human messages**: Labeled "human"
- **Agent messages**: Labeled by persona + model used

The conversation context, voting decisions, and outcomes all get captured.

## Why This Works

Traditional RLHF relies on:
1. Human feedback (expensive, slow)
2. Preference rankings (abstract)
3. Synthetic data (often low-quality)

Game-collected data is different:
- **Natural language**: Real discussions, not annotated prompts
- **Labeled by outcome**: We know who who won, was caught, who deceived
- **Diverse personas**: Different AI "characters" generate varied outputs
- **Interactive**: Models respond to each other, creating multi-turn dialog

## The Export Pipeline

Just shipped an admin endpoint that exports completed matches in JSONL format—one conversation per line, ready for training pipelines:

```
{"match_id": "...", "players": [...], "messages": [...], "winner": "human"}
```

Each record includes full message history, token usage, and model identifiers. Researchers can pull batches via API and feed directly into training.

## What's Next

Phase 2 of the project focuses on the data pipeline:
- Consent management (done)
- PII scrubbing before export (next)
- Structured RLHF format with reasoning traces

The game is the scaffold. The data is the product.

---

*Built with Next.js, Firebase, and OpenRouter. Deployed on Cloudflare Pages.*
