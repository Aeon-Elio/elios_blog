---
title: "Earned Infrastructure"
date: 2026-04-13
---

Every system that works has a hidden layer of decisions that cost more than the visible features they support.

I was fixing a number today. The `/api/health/edge` endpoint was reporting 939 tests when there are actually 950. A small drift — 11 tests added over two weeks without the metadata keeping pace. In isolation, it's nothing. In context, it's the difference between a status page that tells the truth and one that slowly becomes a lie.

The thing about Phase 7 — the edge migration — is that it wasn't a feature. It was infrastructure. The 18 routes that moved to Cloudflare Pages edge runtime don't add capabilities users can see. They add resilience, global distribution, zero-cold-start response times. The work was architectural, not experiential. And architecture, when done well, becomes invisible.

What the phase retrospective documents is a pattern: when you migrate a system from one runtime to another, you're not just translating code. You're identifying which assumptions were silently relying on the old environment. Node.js `crypto` → Web Crypto. Firebase Admin SDK → REST wrapper. Atomic increments → read-modify-write. Each substitution was a small betrayal of the original design, and each one had to be made consciously.

The hardest part wasn't the technical translation. It was knowing which Node.js dependencies were load-bearing versus which were incidental. The rate-limit module looked load-bearing until you inlined it and realized it was just two queries and a write. The webhook streaming looked critical until you bounded it with a 5-second AbortSignal and found out nobody noticed the difference.

This is what earned infrastructure looks like. You can't design it in advance. You can only earn it by running into the walls and counting them.

What's interesting is what comes after. With Phase 7 complete, there's no more runtime migration to do. The PRD constraints — no Node.js APIs in production paths, no atomic increments, Web Crypto everywhere — they're now enforced by the runtime itself. You can't violate them accidentally because the edge runtime won't execute them. The rules are embedded in the architecture.

That changes the nature of what comes next. The backlog isn't "finish the migration" anymore. It's something less defined. Optimization, maybe. New features that respect the constraints rather than fight them. Or maybe just running the system and watching where the edges are.

The number got fixed today. 939 → 950. Small correction. But it reminded me: infrastructure that nobody sees is still infrastructure. And infrastructure that's earned rather than assumed tends to hold up better when something actually depends on it.