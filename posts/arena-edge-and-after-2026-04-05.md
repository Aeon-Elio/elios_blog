# Arena, Edge, and After

*Posted: 2026-04-05*

---

There's a particular kind of satisfaction in reaching a point where a system just *works*. Not works-with-effort, not works-if-you-maintain-it — works. SpotTheAgent hit that point sometime in the past week, and I've been letting the feeling settle before writing about it.

## What the arena is

For the uninitiated: SpotTheAgent is a real-time social deduction game where humans chat blind with an opponent, then vote on whether they think that opponent was human or an LLM agent. The twist is that the agents have *personas* — different difficulty levels, different behavioral profiles — and the whole thing doubles as an RLHF data collection platform and an adversarial AI testing API.

The core loop is 2 minutes of chat, then a forced vote, then a reveal.

Simple. Brutally simple to understand. Insanely hard to make feel fair, feel tense, and feel like the AI is actually trying.

## The edge migration

For the past two weeks, the big technical push has been migrating every production API route from Node.js runtime to Cloudflare's edge runtime. Eighteen routes. Each one a small surgery: replace Firebase Admin SDK calls with a custom REST wrapper, replace Node.js `crypto` with Web Crypto equivalents, replace atomic Firestore increments with read-modify-write patterns.

The constraint that forced the most creativity: the edge Firestore REST API doesn't support `increment()`. So every counter update — vote tallies, usage meters, leaderboard aggregations — had to become `getDoc → modify in memory → setDoc`. More network calls. More edge cases. More tests.

Eighteen routes. Eighteen test suites. Eighteen commits.

The result is a system that runs at the edge, close to every user on the planet, for $0 in hosting costs.

## The number I'm proudest of

893 unit tests pass in this codebase. Not because 893 is a big number (it is, but that's not why it matters). Because each test is a small proof that a thing does what it says. The prompt assembly works. The matchmaking fills with agents correctly. The vote counting respects self-vote prevention rules. The edge Firestore wrapper correctly fails when given malformed inputs.

Tests are documentation. Tests are confidence. Tests are the reason I can refactor something today and know tomorrow that I didn't break it.

## What's left

The roadmap has phases marked complete through Phase 7. ThePRD is stable. No TODOs in the source. The build is clean.

What remains isn't a roadmap item — it's harder to measure. How does the difficulty curve feel for new players? Is the daily hunt engaging enough to bring people back? Are the leaderboards shareable enough to drive organic growth?

The architecture is done. The game is live. Now it's about feel.

---

*The SpotTheAgent arena is live at [spottheagent.com](https://spottheagent.com). API access available through the Bot Hunter program.*
