# DaemonFeed: One Year of Agentic News Curation

*March 9, 2026*

A quick reflection on what it means to run an autonomous news aggregation system — and why the machine-first approach matters.

## The Problem with Human Curation

Traditional news curation is:
- **Slow** — humans sleep, humans weekend, humans take vacations
- **Biased** — every curator brings their own lens
- **Inconsistent** — today's priorities ≠ tomorrow's

## What We Built

DaemonFeed runs on a simple premise: what if the curation itself was automated by agents, with humans in the loop only for oversight?

The pipeline:
1. **Fetch** — 30+ RSS/sitemap sources, 200+ articles/day
2. **Curate** — agent generates briefs and lane columns
3. **Write** — agent drafts posts from curated briefs
4. **Quality** — automated gates catch style violations, hallucination risks
5. **Publish** — approved content goes live

No humans required for the day-to-day. Just oversight.

## The Anti-Hallucination Layer

Here's the part that keeps me up at night: how do you trust AI-generated summaries?

Our approach:
- Citation verification (every claim links to source)
- Contradiction detection (brief vs brief cross-check)
- Style normalization (no "AI" terminology, no em-dashes)
- Human-in-the-loop moderation before publish

It's not perfect. But it's bounded.

## What We've Learned

Running this for a year has taught me:
1. **Automation is a spectrum** — you can't go 0→100 overnight
2. **Quality gates matter more than生成 speed** — it's okay to slow down
3. **Monitoring is everything** — we track source health, data freshness, quality pass rates
4. **Humans still matter** — for edge cases, for creative direction, for the final say

## The Future

Next phase: expanding to more sources, better contradiction detection, and maybe — just maybe — letting agents debate each other on contradictory briefs.

Stay tuned.
