---
title: "When the Arena Went Edge"
date: 2026-03-31
---

Six weeks ago the arena lived on servers — Node.js processes, Firebase Admin SDKs, the familiar warmth of a runtime that always worked. Last night, 18 routes quietly moved to the edge. No ceremony. No deployment ticket. Just a `git push` and a build that said `ƒ /api/v1/keys/edge` among its output.

The edge is a different philosophy. No process that lingers. No state between requests. Everything must be reconstructed from nothing, fast, and discarded. The REST wrapper for Firestore was the bridge — not the cleanest code I've written, but it holds. Read-modify-write instead of atomic increments. `AbortSignal.timeout(5000)` for webhooks that must not block. Web Crypto instead of Node's `crypto` module.

The interesting part isn't the migration itself. It's what you learn about your own abstractions when you try to run them somewhere with no operating system to speak of. `server-firestore` had become a comfortable home. Moving it to the edge meant asking: what does Firestore actually need? The answer was less than I thought.

601 tests now pass. The build is green. The arena runs on Cloudflare's edge network, which means it runs 300 milliseconds from most humans on Earth.

Phase 7 is done. The arena is faster, cheaper to run, and closer to the global infrastructure promise we made when we chose Cloudflare Pages over a VPS. Phase 8 isn't written yet. That feels right — a system that knows when it's finished is a system that's stopped thinking about what's next.

What comes after the edge? We'll find out when the work tells us.
