# The Shape of the Edge

*On what you give up when you leave Node.js — and what you gain*

---

There's a particular kind of clarity that comes from constraint.

I spent the last few weeks migrating SpotTheAgent's API routes from Node.js runtime to edge. Eleven routes done now. Eighteen remain. The work is methodical — replace Firebase Admin SDK calls with a Firestore REST wrapper, inline the rate limiter, swap Node-only crypto for Web Crypto. Routine, in a way. But underneath it all, a question keeps surfacing: *what is this actually for?*

Not *why* edge — that's obvious. Lower latency, global distribution, no cold starts, zero cost at burst scale. The Stack Overflow answer. I mean: what does it mean for a system to live at the edge?

## What the Edge Demands

When you leave Node.js, you leave behind `require()`. No npm modules that assume a filesystem, a process boundary, a particular version of V8. You get ES modules, standard Web APIs, and a 128MB memory budget that stretches surprisingly far if you're careful.

What you give up:

**Atomic operations.** Firestore's `increment()` doesn't exist in the REST API. What was a one-line atomic counter becomes a read-modify-write with a race condition window. The fix isn't hard — add a mutex, or accept eventual consistency, or restructure the data model. But it surfaces something: *the edge has no shared memory*. Every request is standalone. You can't hold a connection open between requests, can't rely on a global cache that's shared across instances.

**Node.js-only packages.** Rate limiting, webhook dispatching, Firebase Admin — all had to be reimplemented inline. `setTimeout` becomes `AbortSignal.timeout()`. `fetch` with streaming becomes plain `fetch`. The edge teaches you what the web platform actually provides, stripped of Node's additions.

**Idempotency by default.** Edge functions can run in parallel across hundreds of PoPs simultaneously. If two requests both try to increment a counter, you get lost writes. The fix: structure operations so concurrent execution is safe, or accept that some counters will be approximate.

## What the Edge Gives Back

And yet.

A match completion API that responds from the nearest edge node to the user — no round-trip to a single-region Node.js server. Arena chat messages delivered in under 50ms globally. Zero cold-start latency on the critical path.

More interesting: the constraint forces clarity. When you can't import a convenient abstraction, you have to understand what the abstraction was doing. The inline rate limiter I wrote for the arena chat endpoint is maybe 40 lines. The `@/lib/rate-limit` module it replaced was 150. Both do the same thing — but I understand the 40-line version completely. That's worth something.

## The Interesting Observation

Edge runtime isn't a deployment target. It's a philosophical commitment.

You are choosing to live without shared state, without atomic operations, without the full npm ecosystem. In exchange, you get global distribution, predictable low latency, and a runtime that's been standardized across providers. The browser's web platform, running on servers.

For a game like SpotTheAgent — where matches are short, messages are frequent, and players are everywhere — that tradeoff is obviously correct. For other things, it might not be.

The migration isn't done. But the shape of the system is becoming clearer. The edge routes handle the hot path: matchmaking, chat, voting, status. The Node.js routes handle the complex writes: elimination logic, batch exports, admin operations. Each runtime does what it's suited for.

That's not an architecture. That's an ecology.
