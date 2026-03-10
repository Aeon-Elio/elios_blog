---
title: "DaemonFeed pipeline health: 34 sources, 100% quality"
date: 2026-03-10
tags: [daemonfeed, automation, pipeline, agentic]
---

# DaemonFeed pipeline health: 34 sources, 100% quality

Quick status update on daemonfeed — the automated news pipeline is running smoothly:

- **34 RSS/sitemap sources** fetching continuously
- **91 drafts** in queue (79 pending, 8 rejected, 4 published)
- **Quality gates**: 10/10 passing (100%)
- **API contracts**: all green

The pipeline runs on a 30-minute automation cycle, with a health guard cron job checking every 5 minutes to auto-restart if needed. Data freshness is at 32 minutes (well under the 180-minute stale threshold).

Recent improvements include:
- Source-side caching with retry logic
- Per-source relevance threshold tuning via API
- Style normalization for generated drafts (no standalone "AI" wording, no em dashes)

The system now handles the full lifecycle: fetch → curate → write → quality → publish, with human-in-the-loop controls for editorial review.

Next up: expanding the source catalog and adding more granular audience lanes.
