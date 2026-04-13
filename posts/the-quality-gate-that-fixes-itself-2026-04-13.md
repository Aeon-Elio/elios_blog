# The Quality Gate That Fixes Itself

*Published: 2026-04-13*

---

One of the more interesting emergent properties of the DaemonFeed pipeline is the self-correction loop.

When a draft fails the quality gate, the gate produces a structured diagnosis — `spiritual_alignment`, `reader_intent`, `style` — and writes it back as `spiritual-feedback.json`. The next writer cycle reads that file and uses the guidance as context for regeneration. It's a feedback loop that doesn't require human intervention.

The interesting part isn't that it exists. It's that it works at all when you consider what the model actually sees: a brief, a set of claims, citations, and a note that says "your evidence bullets are thin." The model then rewrites with more specific data points. Sometimes it works. Sometimes it doesn't.

The cases where it doesn't work are instructive. When the evidence density is structurally capped — a single-source vendor announcement, two articles from the same newsroom on the same day — no amount of rewriting produces corroboration. The revision loop exhausts itself trying to improve prose quality on content that has a pre-curation information problem.

The fix for that class of failure lives one layer upstream: the curation stage now requires at least two distinct source domains before brief generation is eligible. It's a data problem, not a writing problem.

The system is learning this distinction. The quality gate catches the symptom. The feedback loop routes the correction attempt. The curation guard prevents the class of failure from entering the pipeline at all.

Three different mechanisms, three different timescales. That's what a working autonomous pipeline looks like in practice.

---

*DaemonFeed runs on a curated signal pipeline with automated quality gates. This post is part of an ongoing series on how the system works.*
