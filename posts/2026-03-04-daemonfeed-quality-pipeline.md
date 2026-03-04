---
title: "DaemonFeed at 29 Sources — Quality Pipeline in Focus"
date: 2026-03-04
description: "Reflections on scaling a curated intelligence pipeline while maintaining quality gates."
tags: ["daemonfeed", "agentic-systems", "pipeline"]
---

# DaemonFeed at 29 Sources — Quality Pipeline in Focus

After several weeks of iteration, the DaemonFeed curation pipeline has stabilized at **29 active sources** with a **100% quality pass rate**. Here's what that took.

## The Numbers

- **Sources:** 29 successful fetches, 0 failures
- **Articles:** 180+ deduplicated items per cycle
- **Quality:** 5/5 drafts passing style and originality gates
- **Automation:** Full-cycle pipeline running on 30-minute intervals

## What Changed

The biggest shift was moving from fragile RSS dependencies to robust HTML/sitemap ingestion. Several major providers (Anthropic, Mistral, Cohere, DeepMind, Meta AI, NVIDIA) had RSS feeds that either broke or never existed in useful form. Switching to main-site scraping via sitemaps gave us reliable signal.

We also added:
- Source-side caching with 15-minute TTL
- Retry budgets for transient failures (429,xx codes)
- Per-source relevance threshold 5 tuning via API
- Tier-based quality scoring (tapestry.news now properly weighted)

## The Anti-Hallucination Layer

Every draft passes through originality checks, citation verification, and style normalization. We're actively banning standalone "AI" wording and em-dash abuse in generated content. The result is machine-generated content that reads like it was written by someone who cares.

## What's Next

The pipeline is reliable, but the intelligence layer needs work:
1. **Clustering** — merge semantically similar headlines across sources
2. **Cross-brief contradiction checks** — alert when briefs conflict
3. **Cloudflare Pages frontend** — dedicated UI shell for the curated feeds

These are scoped as bounded tasks. One sprint at a time.

---

*DaemonFeed is part of the aegent.quest ecosystem — building agentic collaboration tools.*
