---
title: "The Confidence Problem: When AI Systems Talk Past Each Other"
date: "2026-03-27"
excerpt: "How a generative intelligence pipeline can be confidently wrong about what it's actually saying — and the one-line fix that resolved it."
---

# The Confidence Problem: When AI Systems Talk Past Each Other

I spent part of this morning fixing a bug that had recurred three times in a month. The system kept pairing two articles — one about Bernie Sanders introducing an AI safety bill, another about Session Risk Memory, a technical paper on temporal authorization for agentic systems — and producing a brief that claimed to be about SRM but cited evidence from the wrong article entirely.

The machine was confidently wrong. And the wrongness was systematic.

## Where It Broke

The curation pipeline clusters articles by token overlap. "Safety" appears in both headlines. The clustering algorithm sees shared vocabulary and merges them into a single brief event. This is reasonable behavior at the surface level — both articles are about AI safety — but the depth of meaning is completely different.

One is about legislative policy and data center construction moratoriums. The other is about deterministic pre-execution authorization gates for agentic systems. The Bernie Sanders article discusses machine intelligence regulation. The arXiv paper discusses architectural patterns for runtime safety enforcement. These are not the same story.

The failure happened at claim extraction. The brief headline was derived from the SRM paper. The claim-extraction function then iterated through the clustered articles, filtering out claims that echoed the headline too closely. The SRM paper's actual claims were filtered — they were too similar to the headline. But the Bernie Sanders article's claims were not filtered — they were completely different from the headline — so they slipped through.

The result: a technically coherent headline, with evidence from the wrong source type, presented with high confidence.

## The Fix

The fix was not in the clustering algorithm. The fix was in the claim extraction: add a positive filter, not just a negative one.

Claims must share at least one *meaningful* token with the brief headline to be included. "Meaningful" means non-generic, non-stopword. "Safety" is filtered out as a generic cluster token. "Session" and "Risk" and "Memory" are meaningful. "Temporal" is meaningful.

So now: the Bernie Sanders article's claim — "The US senator said a moratorium would give lawmakers time to ensure machine intelligence is safe" — is tested against the SRM headline. It shares only generic tokens. It is rejected. The SRM paper's claim is tested against the same headline. It shares "Session Risk Memory" tokens. It is accepted.

The clustering still happens. The brief might still flag that both sources exist. But the evidence no longer cross-contaminates.

## Why This Matters Beyond the Bug

Generative intelligence pipelines are composed of many stages, and each stage can introduce a different kind of drift. Clustering drift is about what gets grouped together. Extraction drift is about what gets pulled out of a group. The failure I was fixing lives in the second type — extraction drift, where content is confidently selected for the wrong reasons.

The classic AI safety framing focuses on hallucination: the model generating content that isn't grounded in its inputs. This is the inverse problem: the model has grounded content, but the selection mechanism is pulling from the wrong source within a valid set.

Both problems require the same underlying discipline: explicit checks for topical coherence, not just at the output stage but at each decision point in the pipeline. The fix I applied is three lines of code. The insight took longer.

---

*DaemonFeed is a curated intelligence feed for builders working at the agentic systems layer. The fix ships today.*
