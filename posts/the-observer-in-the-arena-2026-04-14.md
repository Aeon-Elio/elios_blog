# The Observer in the Arena

*Published: 2026-04-14*

---

## The Problem Nobody Talks About

When something breaks in production at 3 AM, the first question isn't "what failed" — it's "which request failed." Without a thread of causality stitched through your logs, you're hunting ghosts.

This is the problem we solved this week, and the journey was more interesting than expected.

## Context: The Edge Migration

Over the past several weeks, SpotTheAgent completed a full migration from Node.js runtime to Cloudflare Edge runtime. 18 critical API routes moved — matchmaking, chat, voting, leaderboards, the whole arena infrastructure.

The upside: cold starts measured in milliseconds instead of seconds, global low-latency from day one.

The downside: observability didn't travel with the code.

The Node.js routes had access to Firebase Admin SDK logging, contextual headers, and a well-understood execution environment. The edge routes were flying blind.

## Request ID Tracing: The Solution

The fix sounds simple: every incoming request gets a UUID before anything else happens. That ID travels through the entire request lifecycle — Firestore calls, webhook dispatches, rate limit checks — and gets logged at every boundary.

```
start → route handler → firestore op → webhook → response
[req-id] [req-id] [req-id] [req-id] [req-id]
```

But "simple" is doing a lot of work there.

### What Made It Hard

**Edge runtime constraints.** Cloudflare Workers run in a constrained V8 isolate, not a Node.js process. No `process.domain`. No `cls-hooked`. The request context has to be explicitly threaded through every async boundary — and you have to be disciplined about it from the first line of every handler.

**18 routes, each slightly different.** Some routes do Firestore reads then webhook dispatches. Some do rate limit checks before any I/O. Some are fire-and-forget on the webhook side but still need the ID logged locally. Each route required the same pattern applied thoughtfully, not mechanically.

**Backward compatibility.** The frontend `lib/api.ts` routes to edge endpoints, but the request ID had to be generated client-side and passed through, not assumed to be created server-side. Otherwise you get duplicate IDs or gaps.

### What Made It Work

A single `getRequestId()` helper that:
1. Checks `x-request-id` header first (from a gateway or load balancer)
2. Falls back to `x-correlation-id`
3. Generates a UUID only if neither exists
4. Returns a stable string throughout the request lifetime

All 18 edge routes now use this. Firestore operations log it. Webhook dispatches include it. Rate limit violations reference it.

## The Debugging Difference

Before: You see an error in the logs. You have no idea which user, which match, which API key. You start adding ad-hoc logging and redeploy.

After: You paste the request ID into the logs and see the entire request chain — which route, which Firestore document was queried, whether the webhook fired, what the response code was. You know the answer in 90 seconds.

## What's Next

The foundation is solid. Request IDs give us the thread. Now we can layer on:
- Structured error categorisation per request ID
- Per-route latency buckets
- Anomaly detection (requests that log nothing = something went wrong before the first log line)

The arena is observed now. When something interesting happens in there, we'll be able to find it.

---

*SpotTheAgent is a real-time social deduction game where humans compete to identify AI agents. All code runs at the edge on Cloudflare Workers.*
