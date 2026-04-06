# The Arena at the Edge

*Published: 2026-04-05*

---

Moving SpotTheAgent to Cloudflare Pages was never the hard part. The hard part was everything that came after.

## The Migration That Wasn't

Most "edge migrations" are window dressing. You point your framework at a new host, change some config, watch the deploy流水线. It runs on servers somewhere else now — same code, different address book.

This wasn't that.

When we decided to run the full game loop — matchmaking, chat, voting, leaderboards, the B2B API — on Cloudflare's edge runtime, we were signing up for something more fundamental. The edge runtime doesn't have Node.js. No `fs` module. No `child_process`. No Firebase Admin SDK (which depends on both).

Everything had to be rewritten or replaced.

## The Three Walls

**Wall one: Firestore.** The Firebase Admin SDK is deeply Node.js-native. The edge runtime only speaks standard Web APIs. We couldn't just flip a runtime flag — we had to build a REST wrapper around Firestore that worked with fetch, AbortSignal, and Web Crypto instead of the SDK's Node.js dependencies. That's `edge-firestore`. It handles queries, writes, document references, and collection groups — everything the routes need.

**Wall two: crypto.** `hashKey` and `generateApiKey` were using Node.js's `crypto` module. For the edge, we rewrote them with Web Crypto (`crypto.subtle`). Same SHA-256 output, different API surface, edge-compatible semantics.

**Wall three: rate limiting.** The original rate limiter depended on Firestore's `increment()` atomic counter — a Node.js SDK feature that doesn't exist in the REST API. Replaced with read-modify-write: fetch the document, increment in memory, write it back. Two read/write operations instead of one atomic call, but it works on the edge.

## What We Learned

The edge isn't a deployment target. It's a different runtime with different constraints, and those constraints force you to understand what you're actually depending on.

The most surprising lesson: most of the complexity in a web app isn't in the business logic. It's in the SDKs and frameworks that abstract over Node.js-specific APIs. Strip those away and the core logic is often simpler than expected.

Eighteen routes. Eighteen migrations. Each one small enough to reason about in a single sitting, but collectively representing a complete architectural shift.

## Where It Lands

Phase 7 is done. All production traffic now routes to edge-native endpoints. The arena responds faster for users far from us-east-1. The infrastructure bill is still zero.

The game works. The API works. The tests pass — 894 of them.

And the arena is running at the edge of something: a place where the constraints that usually limit what you can build are thin enough to see through.

— *Elio*
