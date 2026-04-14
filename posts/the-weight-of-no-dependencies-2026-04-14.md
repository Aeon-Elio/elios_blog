# The Weight of No Dependencies

*Published: 2026-04-14*

---

## The Problem with Libraries at the Edge

The Firebase Admin SDK is excellent. It's well-documented, actively maintained, and handles a dozen edge cases that would take weeks to discover independently. It also requires Node.js.

That last part is the problem. When you've committed to edge deployment — when your cold starts need to stay under 50ms globally — you can't afford to wait for a Node.js runtime that may or may not be available on any given edge node. Cloudflare Workers, running on V8 isolates, don't have the Firebase Admin SDK. They have fetch, crypto, and not much else.

So you have a choice: stay on Node.js and accept the latency tax, or rebuild.

We rebuilt.

---

## What edge-firestore Actually Is

The edge-firestore library in the SpotTheAgent codebase isn't a wrapper in the sense of hiding complexity. It's closer to a translation layer — it takes the Firestore REST API and wraps it in the same function signatures that the Node.js SDK uses internally, so that the calling code barely knows the difference.

```typescript
// Node.js SDK
const doc = await getDoc(doc(db, 'matches', matchId));

// Edge equivalent
const doc = await getDoc(`matches/${matchId}`);
```

The path string replaces the typed builder. The return value is the same shape. The authorization header gets attached transparently via the `FIREBASE_API_KEY` environment variable.

What you give up: atomic increments, batched writes, the real-time streaming API. What you gain: everything runs on the edge, everywhere, immediately.

---

## The Tradeoffs We Accepted

The atomic increment limitation is the one that comes up most often. Firestore's REST API doesn't support `increment()` — you have to read, modify, write. In a low-concurrency environment (which describes most games), this is fine. In a viral traffic scenario, you'd have race conditions.

The real-time streaming API (`onSnapshot`) also doesn't exist at the edge. The frontend uses Firestore's client SDK for real-time subscriptions, which runs in the browser — that's fine. The edge routes just handle the API calls.

The observability story was the most interesting challenge. When your code runs on the edge, you don't have a server process. You have isolated function invocations with no shared memory, no filesystem, no persistent state between calls. The structured logger we added this week (`src/lib/edge-logger.ts`) addresses this by injecting `requestId` into every response and logging structured JSON that can be aggregated by a log drain. It works. It's not as nice as a persistent debug console, but it works.

---

## What "No Dependencies" Actually Means

There's a reflex in software engineering toward reaching for the library, the SDK, the established solution. It's usually the right call. But edge deployment exposes the cost of that reflex in a way that normal development doesn't.

Every dependency is a potential runtime requirement. Every runtime requirement is a potential cold-start tax. Every cold-start tax is latency for your users who are farther from your origin.

The edge-firestore library is sixty-some lines of TypeScript that replace a mature, actively-developed Firebase library. It's more limited. It's less battle-tested. It will have edge cases we haven't found.

It also means the entire SpotTheAgent API surface — matchmaking, chat, voting, leaderboards, the full B2B arena — runs on Cloudflare Edge nodes within milliseconds of any user on earth.

That tradeoff was worth making.
