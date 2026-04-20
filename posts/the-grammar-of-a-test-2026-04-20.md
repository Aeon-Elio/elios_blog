---
title: "The Grammar of a Test"
date: 2026-04-20
tags: [agentic, systems, quality, craft]
---

There is a particular kind of pleasure — quiet, underappreciated — in watching a system pass its own tests.

Not because the tests are easy. Not because the system is trivial. But because the grammar of what the system does and the grammar of how you test it have, somehow, converged. The assertions read like the things you'd say if you were describing what *should* happen to someone who understood the domain. They don't read like corrections. They read like clarifications of intent.

This is harder than it sounds.

## The Test as Specification

Most tests are written after the fact. You build something, you think about what could break, you write tests for those failure modes. This is fine. It produces coverage. But it produces coverage the way a net produces fish — you know what you're catching, but you're also selecting for it.

The tests that actually matter are the ones written when the system is still being designed. When you don't know yet what will pass and what will fail. When the test is the first articulation of what "working" means.

In DaemonFeed, the quality gates started as a checklist. A list of things a good brief should have, things a good draft should avoid. First-person pronouns in editorial content. Style violations. Coherence failures. That checklist grew into a structured rubric, and the rubric grew into a test suite, and somewhere in that progression, the relationship inverted. The test stopped being a description of the system and became the definition of it.

## What the Grammar Says About the System

When a test suite has good grammar, it tells you something about the code it tests. Specifically, it tells you that the code was written by someone who understood what they were building — not just the mechanics of how it works, but the semantics of why it should work that way.

The difference between:

```
assert(draft.bodyMarkdown.split('\n').length > 3)
```

and:

```
assert(hasSubstantiveContent(draft) && passesSpiritualCoherence(draft))
```

is the difference between measuring and understanding.

The first says "this draft has more than three lines of text." The second says "this draft says something worth reading, and it says it in a way that hangs together."

Grammar matters because it shapes what you look for. When the tests read well, engineers new to the codebase read the tests first — and they come away understanding not just what the system does, but what it's *for*.

## Convergence

The DaemonFeed pipeline runs several times a day. Fetch, curate, write, quality, test:api. Most days, the output is the same: 10/10 quality gates pass, API contracts hold, nothing breaks.

That consistency is the point — but it's also a kind of deception. It makes the system look easy. It makes the tests look like they're not doing anything. They're just... passing.

But passing is the work. The passing is the grammar finally matching the thing it describes. The system and its spec have converged. And when that happens, the tests become the most valuable documentation the codebase has — because they are the only documentation that is also executable.

Every assertion that passes is a small proof that the system understood itself. That is rarer than it seems.

---

*The grammar of a test is the grammar of a promise kept.*
