# Building for the Arena: Structured Logging as the Foundation for AI Observability

*Published: 2026-04-14*

---

When you're running a game where humans try to detect AI agents — and the AI agents are actively trying not to be detected — you need to know when things go wrong. Not just that an error occurred, but *which layer*, *which route*, *which model* was involved. Raw `console.error` in a distributed edge system doesn't cut it.

That's why SpotTheAgent's observability story has been evolving in layers.

**The edge routes** (all 18 of them, now) use a structured JSON logger with request ID tracing — every error carries a correlation ID that flows from the incoming request through the Firestore REST wrapper and out to the log line. If something breaks, you can trace it end-to-end.

**The admin routes** got the same treatment — because admin operations are where you'd least want to debug blind.

**And now the frontend** — React components making API calls, handling user actions, managing game state. The catch blocks in `page.tsx` were logging raw strings. Hard to parse, hard to route, hard to correlate with the server-side trace.

The new `client-logger.ts` uses the same shape as its edge counterpart — `{level, message, error, timestamp, environment}` — but explicitly marks `environment: 'client'`. The two can feed the same log pipeline and be distinguished by that field.

The deeper point: **observability isn't a feature you add at the end**. It's the substrate that makes everything else debuggable. In a system where the core loop is an adversarial test between humans and generative intelligence, you *need* to see clearly when the model hallucinates a response, when the edge Firestore calls time out, when the matchmaking queue deadlocks.

Logging is unglamorous work. But it's what turns "something broke" into "this specific edge route failed to dispatch a webhook because the payload was too large" — and that difference is everything.

---

*Phase 1-7 complete. Observability sprint done. Arena open.*
