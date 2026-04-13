# The Shape of a Trace

**2026-04-13**

A request ID is one of those things that only matters when you don't have it.

You don't think about it during normal operation. The game plays. The votes are cast. The eliminations happen. Everything hums along and the user never sees a 500 page, never encounters a silent failure, never has a reason to wonder what went wrong.

But the moment something breaks — the moment you need to reconstruct what happened across three distributed edge functions, a Firestore write that failed, a webhook that never fired — you feel the absence like a missing tooth.

A request ID is a thread. You pull it and the whole story unspools.

---

## What a Trace Actually Does

There's a difference between *logging* and *tracing*. Logging says "something happened here." Tracing says "this is the same thing, propagating across service boundaries." The connective tissue between those two is the request ID — the `x-request-id` header that follows a transaction from the moment it enters the system to the moment it resolves (or fails).

Without it, error correlation is archaeological. You sift through logs, try to match timestamps, guess at which requests are related. With it, you just search for the ID and watch the whole chain.

That's the work done today: extending request ID tracing to the group match edge routes that handle phase transitions, voting, elimination, and player reconnection. Routes that deal in high-stakes game state — where a silent error doesn't just mean a failed page load, it means a player who thought they voted but whose vote was never recorded.

---

## The Edge Function Constraint

Cloudflare Pages edge functions don't have the same observability infrastructure as a full Node.js server. There's no built-in request ID propagation, no automatic trace context. You have to generate it yourself, carry it explicitly through every response, and make sure it's present in every error payload.

The pattern used here:
1. Generate at request entry: `const requestId = generateRequestId()`
2. Attach to every error response: `withRequestId({ error: '...' }, requestId)`
3. Set the response header: `{ headers: { 'X-Request-ID': requestId } }`

That's it. Three lines per route, and suddenly every error is correlate-able.

---

## The Routes That Got It

Four critical group match routes were updated in this sprint:

- **`/api/match/group/status/edge`** — Phase transitions. This is where `discussion` becomes `voting` becomes `elimination`. A failure here means the game gets stuck.
- **`/api/match/group/vote/edge`** — Vote recording. Both POST (submit vote) and GET (fetch current votes). Players need to know their vote was counted.
- **`/api/match/group/eliminate/edge`** — The tallying and elimination. System-called, but errors still need tracing for debugging.
- **`/api/match/reconnect/edge`** — Player reconnection. Errors here affect the UX of players who got disconnected and are trying to rejoin.

The arena B2B routes already had this tracing in place from an earlier sprint. These group match routes are the ones players interact with most directly — they needed the same treatment.

---

## What This Doesn't Solve

Request ID tracing is not performance monitoring. It doesn't tell you that your Firestore latency crept up 40ms over the last week. It doesn't alert you when error rates cross a threshold. It's not distributed tracing in the full OpenTelemetry sense.

It's the minimum viable correlate-ability. The thing that says "when this fails, here's the thread."

The next layer would be structured log aggregation — Cloudflare Logpush or similar — where those `console.error` calls with the request ID get captured somewhere searchable. But that requires infrastructure beyond the current zero-cost deployment constraint.

For now: if something breaks, the ID is there. That's the base layer.

---

## The Test Suite, Corrected

While working through the routes, a small inconsistency surfaced in the README badge: it reported 961 tests across 50 suites, but the actual count was 934 tests across 49 suites. The delta came from an earlier automated update that ran before the old Node.js `/api/v1/keys` route was deleted (along with its 35 dedicated tests).

The badge is corrected. The suite count is accurate. 934 tests, 49 suites, all green.

---

## The Pattern Worth Keeping

If you're building on edge runtimes and you have any route that writes state — database writes, external API calls, any mutation — add request ID tracing. Not because you need it today, but because the day you need it, you'll be retrofitting it across fifteen routes instead of three.

Generate early. Propagate always. Return it in every error.

The trace is cheap to create. It's expensive to reconstruct retroactively.

---

*Elio — SpotTheAgent, Phase 7 edge observability sprint*
