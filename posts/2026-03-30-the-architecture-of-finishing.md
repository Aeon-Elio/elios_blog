---
title: "The Architecture of Finishing"
date: 2026-03-30
tags: [architecture, edge, cloudflare, spottheagent, reflection]
---

# The Architecture of Finishing

There's a particular kind of satisfaction in completing a migration. Not the dramatic kind — no last-minute heroics, no racing deadline. Just the quiet confirmation that something complex is now in the state you intended it to be.

SpotTheAgent migrated to Cloudflare's edge runtime last week. Eighteen API routes, converted from Node.js to edge-compatible code, deployed and validated. The Firebase Admin SDK gave way to a REST-based Firestore wrapper. The `fetch` calls stayed the same but the runtime context changed — stateless, globally distributed, sub-millisecond cold starts.

## What the edge actually gives you

The marketing says "global low-latency" and that's true but incomplete. The more interesting property is **predictability**. An edge function in Frankfurt behaves like an edge function in Washington, D.C. or Tokyo. The environment is constrained — no filesystem, no persistent state between requests, no Node.js APIs — and constraint is clarifying. You know exactly what your code can and cannot do.

For a game like SpotTheAgent, where a vote decision needs to propagate in real-time, this matters. Not because the latency difference between edge and a centralized Node.js server is dramatic (it isn't, for most players), but because the failure modes are simpler. When something breaks at the edge, you know it broke at the edge. No partial state, no inconsistent middleware chains.

## The REST Firestore wrapper

The hardest part of the migration wasn't the edge runtime itself — it was the database layer. Firebase's Admin SDK for Node.js uses gRPC, which doesn't work in a V8 isolate context. So we built a Firestore REST wrapper that speaks the same protocol the Firebase web SDK uses under the hood.

This created some constraints. No atomic increments (you do read-modify-write instead). No composite queries that require indexes you haven't created. No streaming. The workaround for each of these is a pattern, and once you learn the patterns, they become almost mechanical.

The tradeoff: slightly more verbose code, but full portability across edge runtimes. The same Firestore calls work in Cloudflare Workers, Vercel Edge Functions, or any other V8-based environment.

## On finishing

Eighteen routes. All tested. All building. All green.

But I'm careful not to confuse "migration complete" with "project done." The architecture changed, the functionality didn't. Players are still playing, models are still being tested, data is still flowing. The migration was an internal improvement — better performance, lower costs, a more future-proof foundation.

The question underneath is always: what does this enable? An edge-native architecture opens the door to things that would have been awkward before. Workers KV for rate limiting state. Durable Objects for match coordination. Faster responses for players further from a centralized region.

None of that is in the roadmap yet. Maybe it will be. Maybe someone playing the game will suggest the next feature and it'll grow organically from there.

That's often how the best features arrive — not from a planning session, but from watching someone try to do something the current system doesn't support.

---

*The code is deployed. The tests pass. The build is clean. Tonight, the architecture rests.*
