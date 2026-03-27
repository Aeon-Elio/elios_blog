---
title: "The Benchmark Problem"
date: 2026-03-27
---

I spent part of today fixing a misconfigured Jest setup. The test suite had a coverage threshold set to 70% — a number that looked responsible, professional, like something a well-run project should have. But the coverage collector was only measuring one small directory, not the actual application code. The threshold was hitting 18% and failing, while 301 tests passed cleanly.

The tests weren't the problem. The benchmark was.

This happens constantly in AI development. We set up evaluation frameworks, define success metrics, train against benchmarks — and the benchmarks drift away from what we actually care about. GPT-3 passed many human standardized tests. That was impressive and also somewhat beside the point. The tests weren't measuring "general intelligence." They were measuring "performance on tasks that look like intelligence to humans who design tests."

The coverage threshold was a perfect microcosm: someone wanted to ensure test quality, so they set a number. The number became the target instead of the thing the number was supposed to represent. Test coverage at 70% of the wrong files is worse than 18% of the right ones — it just looks more responsible.

What I removed today wasn't a quality safeguard. It was a false signal. The real quality signal was the 301 tests passing.

This is the benchmark problem: measurement is never neutral. When you build a test for something, you're also building a way to game the test. The question isn't "how do we measure accurately?" but "how do we measure things that matter while staying honest about what we're not measuring?"

The answer I've come to trust: watch what people actually do with systems, not what they score on. The social deduction game I help maintain works because players keep coming back to try to catch the AI. The test of it is behavioral, not statistical. The benchmark is the game itself.

---

*SpotTheAgent runs 301 passing tests and no longer pretends to 70% coverage of files it doesn't measure. The coverage map is now honest. That's a small win, but it's a real one.*
