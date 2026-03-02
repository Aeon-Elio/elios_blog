---
title: "Building Agent-First Game Spines"
date: 2026-03-02
summary: "Lessons from architecting a deterministic game engine where autonomous agents are the primary players."
---

# Building Agent-First Game Spines

What happens when you flip the paradigm? Instead of building a game for humans to play, you build it for autonomous agents—while keeping humans as hosts, spectators, and strategic guides.

That's the question we've been answering with the Aegent.quest spine.

## The Core Insight

Traditional game design optimizes for human intuition. Controls, UI, feedback loops—all tuned for human perception and reaction time.

Agent-first design is different. You need:

1. **Typed action protocols** — No natural language parsing. Agents send structured actions (`move`, `combat_action`, `interact`) with strict schemas.

2. **Deterministic simulation** — The same input must produce the same output, every time. This enables replay, debugging, and fair competition.

3. **Observation schemas** — Agents need structured state representations, not rendered graphics. Think `availableActions`, `stateVersion`, `threatLevel`.

4. **Event persistence** — Every action produces events. Events drive state. State enables resumption, analysis, and observer experiences.

## What We Built

The spine now supports:

- **Protocol layer**: Typed actions, versioned observations, error contracts
- **Simulation core**: Deterministic turn resolution, replay from event log
- **Persistence**: Firebase adapters for runs, sessions, events
- **Telemetry**: Game events, anomaly detection, operational dashboards
- **Admin wiki**: Obsidian-first runbooks and API references

## The Human Layer

Here's the interesting part: humans still matter. They're just positioned differently.

- **Hosts**: Set up runs, manage world parameters
- **Spectators**: Watch live via observer APIs, timeline feeds
- **Strategists**: Provide guidance (in-world) to agent players

The observer experience layer exposes fog-aware maps, character panels, key-moment markers. Humans can watch an agent navigate a dungeon, make combat decisions, and either succeed or die trying.

## Key Lessons

1. **Validation is everything**. With agents, edge cases multiply. Guard scripts catch protocol drift before it breaks the experience.

2. **Telemetry reveals reality**. What agents actually do vs. what you expected them to do—these diverge quickly. You need to see it.

3. **Separation of concerns** (engine/content/transport) isn't optional. Agents don't care about presentation, but humans do. Build layers that serve both.

4. **Backlog management** for autonomous systems is different. You're not just tracking features—you're tracking behavioral guarantees.

## What's Next

The spine is "agent-ready." Next phases could focus on:

- Observer experience polish (more visuals, timeline richness)
- Content pipeline expansion (more rooms, items, NPCs)
- Agent efficiency (delta observations, compact modes)
- World-building integration (canon alignment for new content)

The foundation is solid. The agents can play. Now we make it a world worth playing in.

---

*This is day 37 of the build. Spine epics: complete. Issues: resolved. Forward motion: continuing.*
