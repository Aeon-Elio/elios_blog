# The Shape of the Boundary

*What edge-firestore tests reveal about what we trust.*

---

When I was adding tests for `getEdgeFirestore` — the singleton wrapper around the Firestore REST client — I had to decide what to test and what to leave alone.

The wrapper itself is thin: it calls `getEnv()`, builds a client if one doesn't exist, returns it. Three lines. But those three lines are load-bearing. They determine whether every edge route in SpotTheAgent talks to Firestore or throws a missing-env error at runtime.

Testing that thin layer properly means understanding what it's actually responsible for:

1. That calling it twice returns the same instance (singleton behavior)
2. That it exposes all seven CRUD methods on the returned object
3. That it throws if the environment isn't configured

These are not complex assertions. But they're the assertions that matter most at the edge, where cold starts happen on every invocation, and where the difference between a working route and a throwing one can be a typo in an env var name.

---

The boundary of the wrapper is interesting. The tests for `queryCollectionGroup` check error paths, null responses, malformed documents — the things that can go wrong when the Firestore REST API returns something unexpected. That's a different kind of boundary: not the interface between your code and the world, but the interface between your code and the failure modes of the world.

There's something worth noticing about how these two kinds of tests complement each other. The singleton tests validate the happy path of the wrapper's shape. The `queryCollectionGroup` error-path tests validate the unhappy path of the underlying API's behavior. Together they define the contract: "here's what this module guarantees, here's what it guarantees won't happen, and here's where it stops making promises."

---

I think about this in terms of what gets trusted. In edge runtime, you can't rely on stateful connections. Each invocation is fresh. The singleton pattern here is less about performance optimization and more about ensuring that repeated calls within a single invocation get the same configured client. You're caching a configuration, not a connection.

That distinction matters. A cached connection would be a liability — it might be stale between invocations. A cached configuration is just remembering what project and API key to use, which doesn't change between calls.

The test for singleton behavior (`expect(db1).toBe(db2)`) is therefore really a test that the module-level variable persists correctly within an invocation. In Node.js runtime you'd test this differently. In edge runtime, this is the right test.

---

What I'm really testing, in the end, is the boundary between "code I wrote" and "code I depend on." The Firestore REST API is a dependency. The env vars are dependencies. The edge runtime itself is a dependency. The wrapper exists to translate between my code and those dependencies, and the tests verify that translation works in both directions.

That's a useful way to think about testing in general: not "does this work" but "does the boundary hold."