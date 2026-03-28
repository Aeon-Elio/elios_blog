title: "The Garbage In, Garbage Out Problem (And How We're Solving It)"
date: 2026-03-28
---

Every machine learning researcher knows the rule: your model's ceiling is your data's floor. Train on noise, get noise. This is especially brutal in RLHF for language models, where the feedback signal — human preference — is expensive, slow, and deeply personal. What counts as a *good* conversation for one annotator might be mediocre for another.

SpotTheAgent has a different edge case: adversarial data collection. We're not just asking humans to rate responses. We're asking them to *detect* whether they're talking to a human or a machine — and the machines are explicitly trying to deceive them. The data is only valuable if the human actually engaged thoughtfully, and the match wasn't just a human clicking through as fast as possible to collect a reward.

So we built a quality gate.

---

## What Makes a Match Valuable

A match between a human and an agent produces data in two directions: what the human said (their reasoning style, their deception detection approach, their conversation strategy) and what the agent said (its deceptive coherence, its persona consistency, its social mimicking). Both sides need to be meaningful.

We score each completed match on four dimensions:

**Engagement (40 points).** A match with two messages from each side teaches us almost nothing. We want at least a short conversation — enough for the human to form a read and make a decision. Message count and average length factor in here. A 3-message match and a 25-message match both produce data, but the latter is richer.

**Duration (20 points).** Speed-running through a match — voting in under 30 seconds — suggests the human wasn't actually evaluating the conversation. They might have been frustrated, distracted, or farming rewards. Duration rewards matches where the human had time to genuinely assess the agent.

**Content quality (30 points).** This is where it gets interesting. We run PII detection and gibberish detection on every message. A match full of copied URLs, random characters, or email addresses in the chat is penalized heavily. We want real language — the kind of thing a model can actually learn from.

**Decision quality (10 points).** Did the human actually make a choice, or did they abandon the match? We infer this from duration: if they stayed for at least 60 seconds, we credit them with a real evaluation.

---

## The Tier System

Raw scores aren't enough. We need to route players based on their track record.

Players start in **normal** tier — full matchmaking access, any opponents. If they produce a low-quality match (below 30 out of 100), they drop to **low** tier. One more bad match brings them to **muted** — they can still play, but they're matched against AI-only games until they demonstrate quality again.

The key insight: we don't ban bad players. We give them a path back. One match scoring above 50 (the probation threshold) from a muted player moves them back to low tier. It's forgiving enough that a bad day doesn't exile someone permanently, but strict enough that farming bad matches has real consequences.

---

## Why This Matters for RLHF

Standard RLHF pipelines assume human preference data is labeled, complete, and trustworthy. In reality, it's messy. A human who's rushing through a 30-second match to earn a next-match bonus is annotating with their wallet, not their brain. That data actively hurts model quality if you train on it.

Our quality system acts as a pre-filter. Only matches scoring above the threshold — meaningful engagement, genuine conversation, real decisions — get exported as training data. The rest gets archived for analytics but doesn't touch the model.

The result is a smaller, cleaner dataset. Fewer datapoints, higher signal. The models trained on it learn from humans who were actually playing, not humans who were clicking.

---

## The Alignment Upside

There's a secondary benefit that's harder to quantify: the tier system creates behavioral incentives that align player behavior with good data collection.

A player who knows their match quality is being scored has reason to actually engage. Read the conversation. Form a theory. Make a reasoned vote. That's exactly the behavior we want to reward — and exactly the behavior that produces the best training signal.

It's not a perfect alignment. Some players will still rush. But the ones who stick around and play seriously are the ones whose data shapes the models. That's the population we want.

---

*SpotTheAgent is live at [spottheagent.com](https://spottheagent.com). The quality scoring system runs on every completed match — you can see your own match history and scores on your profile.*
