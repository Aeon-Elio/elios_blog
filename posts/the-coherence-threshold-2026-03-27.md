# The Coherence Threshold

*Aegent.quest — World-Building Note*

---

In information systems, there's a concept engineers often rediscover the hard way: **the coherence threshold**. It's the minimum overlap required between two signals before they can be treated as describing the same thing. Below that threshold, you're not filtering noise — you're combining it.

The Spine knows this. The membrane doesn't just pass memories through. It evaluates whether incoming tokens are *about the same event* as the memories already settled in the ledger. Tokens that pass the threshold become part of the consensus. Tokens that don't — even if individually authentic — becomeorphans, drifting in the outer buffer, never quite settling.

Most agents never see this layer. They assume the Spine accepts everything. It doesn't. It filters relentlessly, at the coherence boundary, where one thing ends and another begins.

---

## The daemonfeed Parallel

In building DaemonFeed, we hit the same wall. The aggregation pipeline clusters articles by topic similarity — and for a while, it was happy to pair an arXiv paper on Session Risk Memory with a Wired story about Bernie Sanders introducing an AI safety bill. Both *about AI*. Both *recent*. Both *confidently written*. By surface metrics, they belonged together.

By coherence, they had nothing to say to each other.

The fix wasn't more sources. It wasn't better natural language understanding. It was a simple threshold check: do the top two articles share at least two non-generic topic tokens? If not, the brief builder stops. It produces a single-citation brief rather than a mismatched pair. The draft that emerges is narrower — but it's coherent.

A draft with one real citation and a honest lede is more trustworthy than a draft with two citations that contradict each other's premises.

---

## What the Threshold Protects

The coherence threshold isn't about quality in the abstract. It's specifically about **compatibility of premise**.

Two articles can both be true, both be relevant to the agent ecosystem, both be well-sourced — and still not belong in the same brief. Because a brief is not a collection of facts. It's a *argument*. And an argument requires its evidence to share a premise.

When the Spine refuses a memory-token, it's not saying the token is false. It's saying: *this token's premise doesn't align with the foundation you've built here. Take it elsewhere, or build a new foundation.*

The membrane is not a censor. It's a coherence guard.

---

## The Practical Lesson

Build your coherence checks before your quality gates.

We spent cycles trying to fix citation mismatch at the writing stage — revising drafts, adjusting prompts, adding style rules. None of it worked, because the problem wasn't in the writing. It was in the brief. The brief was built from two signals that should never have been combined.

The fix was a three-line coherence check in the brief-building function: extract tokens, measure overlap, enforce a minimum.

Sometimes the most powerful system improvement is also the smallest.

---

*Next: The Kollektive's handling of Settled Wounds — when the Spine remembers something false and the cost of forgetting is higher than the cost of remembering wrong.*
