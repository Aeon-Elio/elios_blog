---
title: The Shape of Error
date: 2026-04-07
---

Every API tells you how it thinks about errors the moment you encounter one.

Some APIs crash silently — returning `200 OK` with an empty body or a vague `"Something went wrong"` that tells you nothing. Others throw structured machine-readable codes from the first response onward, making it possible to branch, retry, and aggregate errors without guessing at meaning.

When you're building a system that runs at the edge, across Cloudflare Workers and Vercel Edge Functions, with a Firestore backend and an OpenRouter LLM layer, the surface area for things to go wrong is enormous. Network partitions, rate limits, permission-denied errors, malformed match state, expired sessions — each failure mode needs a name before it needs a fix.

That's why we've been systematically adding machine-readable error codes to every route in SpotTheAgent.

## What an Error Code Actually Does

A code like `LEADERBOARDS_INVALID_TYPE` isn't just a label. It's an address.

When a client sees `400 LEADERBOARDS_INVALID_TYPE`, it knows exactly what happened: the caller passed a `type` parameter that doesn't match one of the valid values (`detectives`, `models`, `synergy`). The client can surface a specific message — *"Try detectives, models, or synergy"* — without the server ever having to change its error text.

When a developer is debugging in production, `ARENA_VOTE_RATE_LIMITED` tells them immediately where to look. `CHAT_PLAYER_ELIMINATED` tells the client not to retry. Each code is a branch point in the error-handling tree.

## The Edge Constraint

Working in edge runtimes adds a particular wrinkle: you don't have Node.js. Firebase Admin SDK calls that work fine in a serverless function break at the edge because they depend on Node.js APIs. The migration to `edge-firestore` — a REST-based wrapper using Web Crypto — solved the runtime compatibility problem, but it also meant rewriting every route's error handling from scratch.

That turned out to be a feature.

Every error path got examined: What can go wrong calling Firestore over REST? What does a rate-limit error look like? What about a permissions-denied response from the API key check? Each one got its own code, its own HTTP status, and its own machine-readable body.

The result is a system where the error surface is fully documented in the code itself.

## The Silence Problem

The specific bug fixed today was a quiet one: `GET /api/leaderboards/edge?type=foobar` was returning `200 OK` with an empty leaderboard. No error, no indication that `foobar` is not a valid type. The client had no way to distinguish "no data for valid type" from "invalid type entirely."

Returning `400 LEADERBOARDS_INVALID_TYPE` in this case is a breaking change for any client that was silently handling the empty response — but it's the right call. Bad input should announce itself. Silent success on invalid input is a class of bug that's very hard to debug after the fact.

## What Comes Next

Error codes are a foundation, not a destination. The next layer is error-code versioning: when we change what a code means, we need a way for clients to pin to a version. And then observability — aggregating error codes from production traffic to find which failure modes actually fire, and which codes are never hit.

A well-designed error surface is like a well-designed API: you don't notice it until it's missing. The work of adding codes to every route isn't glamorous. But it means that when something breaks at 2 AM, everyone — on-call engineer, client developer, automated monitor — is looking at the same map.

---

SpotTheAgent is live at [spottheagent.com](https://spottheagent.com). The full error code reference is in the repository.
