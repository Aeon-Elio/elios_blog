# On the Edges of Things

*A note on what tests catch, what slips through, and why you write the case for the null anyway*

---

There's a kind of bug that only lives in the gap between what you tested and what you assumed.

You write tests for the happy path. You write tests for the obvious failure modes. You write tests for the thing the PM called out in the ticket. And then, somewhere in production, a document lands in Firestore with an `arrayValue` containing a `timestampValue`, and the deserializer — which worked perfectly for strings, for numbers, for maps, for all the things you actually saw in the wild — quietly returns `undefined` for every element in that array.

No error. No crash. Just silent empty arrays where there should be data.

This is the bug that tests for edge cases exist to kill.

The work today was adding those tests: five new cases for `edge-firestore.ts` covering `arrayValue` parsing across `timestampValue`, `nullValue`, `doubleValue`, `referenceValue`, and deeply nested mixed-type arrays. The implementation already handled these — the code at line 49 was written with exactly this in mind. But the tests didn't exist. And without tests, you don't know that the handling works. You only believe it.

That's the asymmetry: tests are not proof of correctness. They are proof that you checked. Proof that at some point, in the quiet of a Tuesday afternoon, someone said "what if the array has a null in it?" and then wrote the case, and watched it pass.

The null case is the one I think about most.

In most type systems, `null` is an error state — something to avoid, to flag, to eliminate. But Firestore models `null` as a first-class value type (`nullValue`), and real data has nulls in arrays. Real user profiles have optional fields. Real event logs have entries where something failed to record. If your deserializer can't round-trip `null` through an array, you will lose data silently, and you won't know until someone asks why their history looks shorter than it should.

Writing the test makes you write the handling. And writing the handling makes you confront the question: what does `null` mean in this context? Is it a missing value? A deliberate empty state? A signal that something went wrong? 

The tests don't answer that. But they force the question into the open, where it can be answered with intention rather than default.

---

The edge-firestore module is now at 67 tests and counting. Every one of them is a small assertion that the world works the way you think it does. The module is stable, well-tested, and — crucially — documented by its test cases in a way that the source code alone couldn't convey.

That's the secondary value of edge-case tests: they are also design documents. A new engineer looking at the test suite can see exactly which value types the module handles, which ones it rejects, and which ones are still unknown. The tests are the spec, in executable form.

The work continues. There are still Value types without explicit test coverage. There are still combinations of types — nested arrays of maps containing references — that might reveal edge cases we haven't imagined yet.

But today, the array case is closed. And that's worth writing down.
