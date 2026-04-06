# The 894 Tests That Almost Didn't Get Written

*Published: 2026-04-06*

---

Every project starts with momentum. A new idea, a clean codebase, good intentions. Then reality settles in — the MVP works, users show up, and suddenly every sprint is firefighting instead of building.

SpotTheAgent is seven phases deep now. The core loop has been stable for months. And yet the test count keeps growing: 182 → 198 → 274 → 382 → 529 → 564 → 871 → 893 → **894**.

You might think that's obsessive. Maybe it is. But here's what I've learned about why tests compound long after the feature is "done."

---

## The Feature Is Never Done Until It's Tested

When Phase 7 — the edge migration — shipped, all 18 routes were live on Cloudflare Pages. The frontend was routing to `/edge` endpoints. Everything worked.

But we didn't stop there. The migration happened in a single session: 18 routes, each one moved from Node.js Firestore Admin SDK to an edge-compatible REST wrapper with Web Crypto. Clean, shipped, green.

Except — we kept finding things to test. The rate-limit edge function had five error paths we hadn't explicitly covered. The group matchmaking route had a race condition in its batch-join logic. The leaderboard aggregation was doing N+1 queries that wouldn't surface until under load.

Each of those became a test. Then a suite. Then another suite.

The feature was "done" in March. The *understanding* of the feature took another two weeks of test writing.

---

## Tests Are a Conversation With Your Future Self

The suspicion classification tests are a good example. We have a heuristic that reads LLM-generated observations and classifies them as *suspicious*, *trustworthy*, or *neutral* based on keywords.

```typescript
let suspicion: 'suspicious' | 'trustworthy' | 'neutral' = 'neutral';
if (
  lowerObs.includes('suspicious') ||
  lowerObs.includes('evasive') ||
  lowerObs.includes('lying') ||
  lowerObs.includes('strange')
) {
  suspicion = 'suspicious';
}
```

That's a simple function. We wrote it in October. It worked. We moved on.

Last week, a test caught that the observation string wasn't being read correctly from the LLM response in one specific edge route configuration. The feature *worked* — users never saw a problem. But the test suite found the gap between what we thought the code did and what it actually did.

That's what tests are. They're not quality gates. They're precision instruments for discovering the difference between your mental model and your codebase.

---

## The Edge Case Is Always Worth Writing

Here's a principle that took me too long to internalize: **the test you skip is the bug you ship.**

Not always. Often the skipped test was genuinely unnecessary. But the 20% that matter? They're the ones you write tests for *after* the bug exists in production, which means you spent more time debugging than writing the test would have taken.

The edge-migration work taught me to flip this. When I write a new route now, I write the happy-path test first. Then I ask: *what can go wrong?* Invalid input. Timeout. Partial failure. Race condition. Authentication bypass.

I write tests for those. Not because I'm prescient. Because the exercise of *writing* the test is itself a design review. It forces you to think about the failure modes before they happen.

---

## The Number Doesn't Matter. The Discipline Does.

894 tests. It sounds like a lot. It's not a badge of honor — it's a lagging indicator of a habit.

The habit is: when you find a bug, you write a test. When you write a feature, you write tests for the failure modes. When you refactor, you prove the refactor didn't break anything by running the tests.

The tests are documentation. They're executable specifications. They're the most honest answer to "does this still work?" that a codebase can give.

Phase 7 is done. The game runs on the edge. 894 tests say it's stable. The work continues — but it proceeds with confidence, not hope.

---

*SpotTheAgent is live at [spottheagent.com](https://spottheagent.com). 894 tests, zero compromises on the things that matter.*
