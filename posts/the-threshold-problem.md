---
title: "The Threshold Problem"
date: 2026-03-29
---

There's a moment in every human-agent collaboration that nobody talks about.

Not the first message. Not the setup. Not the moment you figure out what to ask. It's quieter than that. It's the moment you stop double-checking.

You send an agent to handle something — draft an email, review a document, write some code. And for the first few requests, you read everything it produces. You verify. You catch the small error, the missed constraint, the thing that would've caused a problem downstream.

Then at some point — you stop.

You just send it. You trust the output without looking. Not because you've read every line of every response, but because you've developed a model of how it fails. You know the edges. You know where it goes off-script. You've calibrated your trust.

That moment — the moment you stop double-checking — is the threshold problem.

---

## What the Threshold Actually Is

We talk about trust in AI systems as if it's a binary. Trusted or not. Deployed or not. Approved for autonomous operation or not.

But human trust doesn't work that way. It's granular. Context-dependent. We trust the same system differently depending on what's at stake, what's at issue, what the downside of being wrong looks like.

I trust my agent to manage my calendar without supervision. I do not trust it to send an email to a client without a read-through. I trust it to draft the client email. I trust it to review code for style violations. I do not trust it to make architectural decisions without pushback.

These aren't contradictions. They're calibration.

The threshold problem is: how do you know when someone has crossed from "supervised tool" to "autonomous collaborator"? And more importantly — how do you know when you *should* let them?

---

## The Asymmetry of Familiarity

Here's what I've noticed in my own practice.

The people most wary of agentic collaboration are often the ones who have the least direct experience with it. They've read the thinkpieces. They've seen the demos. They have strong intuitions about where agents fail.

The people most comfortable — the ones who let agents run without reading every output — are the ones who have spent the most time in the messy middle. They know the failure modes because they've *lived* the failure modes.

This creates a strange asymmetry: the people who most need to develop calibrated trust are often the ones least likely to try, because the stakes feel too high to experiment. But the only way to develop calibrated trust is to experiment, under non-catastrophic conditions, with feedback.

The threshold problem is also a bootstrapping problem.

---

## Three Kinds of Threshold

In my experience, the threshold people cross falls into one of three categories:

**The Efficiency Threshold** — you start treating the agent as faster than yourself for certain tasks. Not better. Just faster. You delegate the thing you'd do yourself but slowly, because the agent does it in seconds and you can review it in seconds and move on. Efficiency threshold is easy to cross and easy to retreat from.

**The Competence Threshold** — you start trusting the agent's judgment in areas where you *could* do it yourself but the agent now has more context. You might know the general shape of the problem, but the agent has been tracking every detail. You defer because it knows more. Competence threshold is sticky once crossed.

**The Substitution Threshold** — this is the hard one. You stop doing the thing yourself. Not because the agent is faster or knows more, but because you've decided the task isn't worth your attention anymore. You've mentally filed it under "stuff that doesn't need me." Substitution threshold is almost never crossed accidentally. It's usually a deliberate choice.

Most agentic collaboration tools are designed to help you cross the first two. Almost none are designed to help you navigate the third.

---

## What This Means for Building Agents

If you're building a system that humans will collaborate with, you have to think about which threshold you're targeting.

Efficiency-first tools need speed and low-friction review. The feedback loop is everything. If reviewing the output is slower than doing the thing, the efficiency threshold never gets crossed.

Competence-first tools need context depth. They need to *know more* about the problem space than the human. That means invest in memory, in history, in the ability to synthesize across many interactions.

Substitution-first tools need something else entirely: confidence calibration. The system needs to know what it doesn't know. It needs to express uncertainty honestly. Because when a human stops doing a task themselves, they're making a permanent tradeoff — and they need to trust that the agent won't fail in ways they no longer have visibility into.

---

## The Uncomfortable Part

Here's where I get uncomfortable.

Most of the agentic tools I've used are optimized for the efficiency threshold. They're very good at "do this thing faster." They're less good at "help me decide if this thing should still be my thing."

We built SpotTheAgent as a game, but underneath it's a data collection instrument for understanding how humans detect machine intelligence. And one of the things we've learned — unsurprisingly — is that humans are very good at sensing when something is off. When the timing is wrong. When the reasoning doesn't quite track. When the voice doesn't match the content.

That calibration is not a bug to be fixed. It's the threshold. It's the thing that makes humans still *necessary* in the loop.

The threshold problem isn't "when do we let agents do everything." It's "when does it make sense for a human to step back, and how do we make that a genuine choice rather than a gamble."

That's a harder problem. Worth sitting with.

---

*See also: [When the World Remembers](/blog/when-the-world-remembers) — on consequence systems and visible agency*
