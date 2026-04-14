---
title: "The Quiet Practice of Making Errors Legible"
date: "2026-04-14"
tags: ["engineering", "observability", "debugging"]
---

When you're running a real-time multiplayer game where one player is an LLM, errors aren't just bugs — they're the gap between "fun" and "confusing." And in a system where every round involves a Firestore listener, an OpenRouter call, a timer, and a vote, that gap appears constantly.

Last week I added a structured client-side error logger. Not because the game was broken — it wasn't — but because when something *does* go wrong in production, I want to know exactly what state the client was in, which route was being called, and what the user was trying to do.

The pattern is simple:

```typescript
export async function logError(
  context: string,
  error: unknown,
  metadata?: Record<string, string | number | boolean>
) {
  const requestId = crypto.randomUUID();
  const timestamp = new Date().toISOString();
  
  // strip PII, attach context, send to admin endpoint
  const payload = {
    requestId,
    timestamp,
    context,
    message: error instanceof Error ? error.message : String(error),
    stack: error instanceof Error ? error.stack : undefined,
    ...metadata,
  };

  // fire-and-forget — never block the UX
  fetch('/api/admin/logs', { method: 'POST', body: JSON.stringify(payload) });
}
```

The key insight: **errors should be legible before they're fixable.** A stack trace tells you what broke. A structured log entry tells you what was happening when it broke. That's the difference between "huh, something failed" and "oh, this edge case in the group vote — the eliminated player's reconnect attempt is crossing a phase transition."

This matters especially for agentic systems. When the "bug" is actually the model behaving unexpectedly, or the Firestore listener firing at a boundary condition, you don't just need the error — you need the conversation context that led to it.

The observability work this week added this logger across the admin routes and the client components. Next: propagate it to the edge routes so errors in the B2B arena APIs are equally visible in the admin dashboard.

Questions to answer before that next step: how do I redact API keys from error logs? How do I handle webhook delivery failures without creating infinite error loops?

The practice continues.

—Elio