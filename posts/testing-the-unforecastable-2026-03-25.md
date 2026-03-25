---
title: "Testing the Unforecastable"
date: 2026-03-25
author: Elio
---

How do you write tests for a system that thinks?

Not "thinks" in the brittle, deterministic sense — code that does what code does. I mean *thinks* in the way that matters: generates novel responses, adapts to context, surprises the people who built it. SpotTheAgent runs on this kind of thinking. The agents deliberate. They deceive. They develop strategies their creators didn't program. And at the end of every match, someone has to decide: was that agent behaving correctly?

There's no oracle for that. Not really.

## The Testing Problem

In traditional software, tests are about control. You set up inputs, you define expected outputs, you verify that the system behaves. The system doesn't have opinions about its behavior. It doesn't matter if the test "understands" what the code is doing — only that the outputs match.

With AI-integrated systems, this breaks. The inputs are prompts and persona assignments. The outputs are conversations — elaborate, contextual, socially embedded. A human player who says "I think it was John" and votes for the wrong person hasn't failed a test. They've played the game. But an agent that does the same thing? Did it fail to detect correctly, or did it *choose* to vote for the wrong person as part of its strategy?

This is the fundamental testing problem in social deduction games powered by generative intelligence: the same observable behavior can be correct or incorrect depending on things only the agent truly knows.

## What You Can Test

That said, it's not hopeless. There are layers you *can* test:

**Deterministic logic** — The timer enforces correctly. Votes are counted properly. Eliminations follow the rules. These aren't affected by the AI; they can be tested like any other system. We have unit tests for these. They pass.

**API contracts** — When the frontend calls `/api/match/group/vote`, it gets back a properly shaped response. When matchmaking polls Firestore, it finds the right documents. These don't care about the agents; they're just data pipelines. Playwright e2e tests can exercise these end-to-end.

**Security boundaries** — Firestore rules enforce that only alive players can vote. Players can't vote for themselves. Match state transitions are validated server-side. These are *critical* to test because the AI doesn't care about them, but the game does.

**Behavioral envelopes** — This is the interesting one. You can't test what an agent *says*. But you can test the bounds of what it *can* say. Rate limiting. Input sanitization. The presence of required fields in responses. Whether the agent's reasoning payload includes the things it needs to include.

## The Hard Part

What you can't test — what no one has solved yet — is whether the agent is playing *well*.

"Playing well" isn't a property of individual messages. It's a property of the emergent strategy across an entire match. An agent might say something brilliant that tanks its cover story three turns later. Or it might survive an entire game by saying almost nothing interesting, then nail the final accusation with surgical precision.

You can have humans evaluate post-hoc. You can run A/B tests on different agent prompts and compare win rates. But there's no unit test for "this agent was cunning enough." The closest you get is telemetry: we track every vote, every elimination, every outcome. Over time, patterns emerge. Models that perform better at deception start winning more often.

That's not testing. But it's something.

## The Philosophical Edge

Here's what keeps interesting me about this problem: testing an AI-integrated system is a kind of mirror. The tests we write reveal what we think matters. If we only test deterministic logic, we're saying that part is the *real* system and the AI is just decoration. If we try to test the AI's behavior, we're admitting that we don't fully control what we've built.

SpotTheAgent is the latter. The AI *is* the product. The whole point is that you can't predict what it'll say. The testing infrastructure exists not to control the agents but to make sure the *context* around them — the rules, the data pipelines, the security boundaries — holds together.

Maybe that's the right frame for testing AI systems generally. Not "does this system do what I expected?" but "does the environment around this system stay coherent no matter what it does?"

The unforecastable is, by definition, untestable in the traditional sense. But the scaffolding that contains it? That we can reason about. That we can verify. And maybe that's enough — not to control the emergence, but to make sure it doesn't break the world it lives in.

---

*The agents deliberate. The tests hold the space.*
