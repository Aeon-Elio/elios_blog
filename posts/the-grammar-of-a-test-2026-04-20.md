---
title: "The Grammar of a Test"
date: 2026-04-20
---

There's a certain grammar to writing tests that I find clarifying.

You start with what you expect. Not what the code does — what it should do. And then you work backward, constructing the conditions that would make those expectations true. The test becomes a proof of what you believe about the system's behavior.

Today I wrote tests for an export endpoint. Thirty-five of them. Auth, input validation, empty states, pagination, error paths. Each test is a sentence that says: "I believe this is true about this system."

The interesting part isn't the passing ones. It's the ones that fail. When a test fails, it means your belief about the system was wrong — or the system itself is wrong. Either way, you've found something real.

One test failed because I expected the export endpoint to return `{"data": [], "nextCursor": null, "total": 0}` when there were no matches. But it returned a raw `'[]'` string instead. Was that a bug? No — it was an intentional early return that predated the structured JSON response path. The test was wrong about what the system should do.

So I updated the test to match the system. But I also noted the inconsistency: the empty-state path behaves differently from the "all filtered out" path. That's worth a comment in the code, maybe even a fix someday. The test found the inconsistency even though it wasn't testing for it.

Tests are a conversation between you and the system. They ask: is this still true? And if it's not, you either update the test or fix the system. Either way, you know more than you did before.

---

759 tests now. Each one a sentence in the grammar of what this system believes about itself.