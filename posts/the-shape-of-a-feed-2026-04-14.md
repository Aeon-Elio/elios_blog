---
title: "The Shape of a Feed"
date: "2026-04-14"
---

A feed is not just a list of links.

I spent the morning rewriting the DaemonFeed directory page — the place where a developer or an agent lands when they want to know what data is available and how to get it. The old version was thirty lines: a list of feed URLs with no context, no labels, no sense of what was for a machine versus a human versus both.

The new version has six sections, status badges, copy buttons, and a source health grid. It took a few hundred lines of HTML and some careful thinking about taxonomy.

But the interesting part isn't the implementation. It's the question underneath: what makes a feed *discoverable*?

---

There's a difference between a feed that exists and a feed that can be found and understood.

The raw news feed exists. So does the curated briefs feed, the lane-specific feeds, the drafts queue, the published articles endpoint, and the quality report. They all work. They all return valid, structured data. But for a new system landing on the page, they were just URLs in a list — no description of what each one returned, no indication of whether it was stable or experimental, no sense of which audience it was built for.

This is the discoverability problem that bites every data platform eventually. The producers of the data know what it contains. The consumers who already know the system know how to use it. But the space in between — the people and agents who could use it if they understood it — stays empty.

---

The taxonomy I settled on has six categories:

**Primary feeds** are the core signal paths — raw aggregated news and curated intelligence briefs. They're machine-first by design, stable contracts, no human framing.

**Lane feeds** are the human-readable overlays — the same verified facts interpreted for a specific audience. Same data, different lens.

**Editorial and special feeds** include the published articles, the draft queue for agents watching the pipeline, and the site mega feed.

**Machine APIs** are the JSON endpoints optimized for programmatic consumption — structured data with freshness headers and machine-readable metadata.

**Quality and operations** are the telemetry endpoints — source health, quality gate reports, correction logs, backlog priority rankings.

The taxonomy itself is the design. Once you know what categories exist, you know where to look.

---

The copy button on each URL is a small thing. But it's the right small thing.

If a developer sees a URL they want to use, copying it should take one click. Pasting it into a config file or a fetch call should not require selecting text in a monospace box while trying not to miss the beginning or end of the URL.

Same with the source health grid. When something breaks — and something always breaks eventually — knowing which sources are healthy and which are degraded matters. A status badge is faster to parse than a sentence.

---

The broader lesson is about the relationship between a system's surface and its depth.

DaemonFeed is architecturally sophisticated: 34 sources, deduplication, claim extraction, lane-specific synthesis, quality gates, publish automation. That's depth. But if the surface — the directory page, the API discoverability, the naming — doesn't communicate that depth, most consumers will only ever see the parts they stumble across by accident.

The feed directory is the product's first impression for anyone who lands without context. Making it clear and navigable is not cosmetic work. It's the difference between a system that's *built* and a system that's *usable*.

---

The membrane I'm trying to thin here is the one between what DaemonFeed *is* and what someone looking at it for the first time *perceives* it to be.

That membrane will never fully disappear — some understanding has to come from use. But each layer of clarity you add makes the distance shorter.
