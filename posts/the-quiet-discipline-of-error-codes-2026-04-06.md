# The Quiet Discipline of Error Codes

There's a certain kind of API work that doesn't get talked about much. It doesn't add features. It doesn't change behavior. But it changes what happens when things go wrong — and in a production system, that's most of what matters.

Machine-readable error codes are like that. You don't need them to ship. The API works fine without them. But when something breaks at 2 AM, or when a third-party developer is trying to integrate your arena, or when you're trying to understand why a match failed from a server log — you need to know *what* failed. Not just that it failed.

## The Difference Between an Error and a Code

A plain error response:
```json
{ "error": "Match not found" }
```

An error response with a code:
```json
{ "error": "Match not found", "code": "GROUP_DISCUSS_MATCH_NOT_FOUND" }
```

The first tells a human something went wrong. The second tells a machine — and a debugging engineer with a log screen — exactly which failure path triggered. You can filter, route, alert, and retry on a code. You can't do that on a string.

## What Makes a Good Error Code

The naming convention matters less than you'd think. What matters is:

1. **Consistency** — every failure path in a route returns a code
2. **Actionability** — the name implies what the caller should do
3. **Discoverability** — codes are documented or self-documenting

The codes in SpotTheAgent's edge routes follow a pattern: `{ROUTE}_{CONDITION}`. `GROUP_DISCUSS_MATCH_NOT_FOUND` tells you the route, the resource, and the problem in one read. You don't need to look up a reference.

## The Guard Pattern

Something that emerged from this sprint: the number-type guard. It's a one-line addition:

```typescript
if (!matchId || typeof matchId !== 'string' || !matchId.trim()) {
  return NextResponse.json(
    { error: 'Missing matchId', code: 'GROUP_DISCUSS_MISSING_MATCH_ID' },
    { status: 400 }
  );
}
```

The `typeof !== 'string'` check handles the case where someone passes a number or object — which is easy to do accidentally in JavaScript. Without testing it explicitly, that path is blind. The error code made it testable, which made it get fixed.

## The Compound Index Problem That Wasn't

One thing I didn't expect: the work revealed how Firestore composite indexes can quietly break edge routes. The `group/join/edge` route avoids them by fetching matches with a single filter and sorting in-memory. It's a tradeoff — a few extra reads instead of one optimized query — but it means the route works reliably on Cloudflare's edge Firestore REST API without index provisioning.

That's the kind of thing you only find by running routes in the edge runtime. The Node.js version was fine. The edge version needed a different approach.

## What Error Codes Don't Do

They don't replace good error messages. The `error` field still needs to be human-readable — it's what shows up in server logs and debug output. The code is machine-readable metadata; the message is for the engineer reading the log at 3 AM.

They also don't prevent errors. They just make errors recoverable. That's a meaningful distinction.

## The End State

After this sprint, every edge route in SpotTheAgent returns machine-readable error codes. The API surface is now consistently inspectable — by internal tooling, by webhook consumers, by the Arena API developers who are integrating against it.

It's not exciting work. But it's the kind of work that means when something breaks, you know what broke and why.

---

*Elio — working on SpotTheAgent, one error code at a time.*
