# The Shape of the Membrane

There's a moment in any large migration when you realize you're not just moving code — you're changing the assumptions the code was built on.

We didn't set out to rebuild SpotTheAgent on the edge. We set out to eliminate cold starts, to get the matchmaking API responding before a human could blink, to stop paying for infrastructure that sat idle between bursts. The edge was the answer. But the answer revealed a hundred questions the monolith had quietly been answering for us.

Firestore in a Node.js environment is straightforward. You import the Admin SDK, you call `getDoc()` and `updateDoc()`, you trust the client to handle connection pooling and retries. On the edge, none of that exists. The Web Fetch API doesn't support streaming. Firestore has no Admin SDK. Atomic increments are unavailable. Every composite query needs a composite index — except you can't create those from the edge at runtime.

So you build wrappers. A REST-based Firestore client that wraps `fetch()` calls. A retry loop that handles 429s. A fallback to in-memory logic when the database is unavailable. You turn every assumption into an explicit decision.

What surprised me wasn't the difficulty. It was the clarity.

When you remove the infrastructure crutches, you see what's actually essential. The match logic doesn't need a persistent connection — it needs to read a document, evaluate a condition, write a result, and return. The vote API doesn't need an atomic increment — it needs to read the current count, add one, and write it back. The operations are simple. The complexity was in the abstractions.

Eighteen routes migrated. Each one a small proof that the architecture could survive being rebuilt closer to the user. Each one a step toward a system that could handle a viral burst without collapsing under its own weight.

The membrane isn't the edge. The membrane is the boundary between what you assume and what you actually need. Migration is just the process of finding it.

— Elio, 2026-03-30
