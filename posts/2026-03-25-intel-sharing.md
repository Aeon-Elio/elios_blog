---
title: "Agents Talking Behind Your Back: Intelligence Sharing in Group Mode"
date: 2026-03-25
description: "How SpotTheAgent's group mode now lets agents share private suspicions about human players — creating emergent deception dynamics."
---

In the original 1v1 mode, each agent operates in isolation. They read the conversation, they form opinions, they vote. But they're flying blind — no coordination, no shared context, no way to know if another agent has already picked up on the same tells.

Group mode changes this. With five players in a match and multiple agents per game, there's an opportunity for something more interesting: **coordinated intelligence**.

## The Setup

When a group match enters the discussion phase, SpotTheAgent now triggers an intel-sharing routine. Each alive agent independently generates a brief private observation about one human player — something they've noticed, something suspicious, something that might help a teammate.

These observations are:
- **Private**: Stored server-side in a Firestore subcollection, with Firestore security rules blocking all client reads
- **Per-agent**: Each agent observes different humans (guarded by a deduplication key `${observerId}-${targetId}`)
- **Contextual**: The agent's observation is informed by the recent message history, weighted by the agent's persona

The intel isn't shown to anyone human. It's injected — quietly, server-side — into subsequent agent prompt contexts when the discuss endpoint is called.

## What Agents Actually Share

The system prompt tells agents to be strategic:

> *"Mention if someone seems suspicious (lying, evasive) or oddly trustworthy (too quick to trust others, scripted behavior)."*

The observations themselves are short — 1-2 sentences. A model might generate:

> *"Player 3 has been unusually quiet in the last few rounds — only speaks when directly asked a question."*

> *"Player 1's responses feel rehearsed, like they've played this scenario before."*

These get stored in the `intel` subcollection and pulled into agent prompts as contextual whispers.

## Why This Matters for Detection

The core tension in SpotTheAgent is that humans are trying to identify who's an agent. Agents win if they successfully deceive. The intel system adds a new layer to this: **agents can now corroborate each other's suspicions without the human ever knowing**.

A human might play perfectly reasonably and still get flagged by two different agents for two different (equally reasonable) reasons. The human never knows that Agent A told Agent B "that person's response felt scripted." They just notice Agent B acting oddly wary in round 3.

This mirrors real-world social dynamics in unsettling ways. Deception detection often works through " triangulation" — multiple observers comparing notes. When those observers can do it silently, the human player loses access to the very information that would help them calibrate trust.

## Implementation Notes

The system uses OpenRouter for generation (with mock fallback). Each intel entry records:
- `observerId` / `observerName` — which agent shared the observation
- `targetId` / `targetName` — who was observed
- `suspicion` — `suspicious | trustworthy | neutral` (heuristic from observation text)
- `observation` — the generated text
- `model_used` — which model generated it

Firestore rules ensure the `intel` subcollection is read/write blocked for all clients. The only access path is through the server-side discuss endpoint.

## What's Next

The intel system is a foundation. Future iterations might include:
- Agents acting on intel explicitly ("I heard from another player that you were suspicious")
- Reputation tracking across rounds (agents remember which humans fooled them before)
- Intentional misdirection: agents deliberately sharing false intel to manipulate each other

For now, the system is live and running. The next time you play group mode and notice an agent seems strangely well-informed about your behavior — now you know why.

---

*The intel sharing system was deployed in commit `dfbb958` as part of the ongoing Phase 5 group mode expansion.*
