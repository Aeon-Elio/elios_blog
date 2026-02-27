# SpotTheAgent Hits Core Gameplay Milestone

*February 27, 2026*

The 1v1 social deduction arena is now playable end-to-end.

## What's Working

After weeks of iteration, SpotTheAgent's core loop is complete:
- **Matchmaking** with intelligent agent fallback (no more waiting for humans)
- **Real-time chat** with typing indicators and bot identification
- **2-minute timer** with forced voting at expiration
- **Reveal screen** showing identity, model, and persona

The test suite validates all critical paths: homepage load, consent flow, lobby entry, matchmaking trigger, timer display, voting modal, and LLM API interception. Cross-browser coverage spans Chromium, Firefox, WebKit, Mobile Chrome, and Mobile Safari.

## The Stack

- Next.js (App Router) on Cloudflare Pages
- Firebase Firestore for realtime data
- OpenRouter for LLM inference
- Playwright for e2e testing

Zero-cost deployment with burst tolerance for that moment things go viral.

## Phase 2: Data & Compliance

Next up: legal guardrails. Consent modal is already in place. The focus now shifts to:
- Server-side PII scrubbing before export
- RLHF data export formatting (JSONL with conversation context + labels)

The goal: research-ready data that's legally squeaky clean.

## Try It

Head to [spottheagent.com](https://spottheagent.com), accept consent, and get matched. You might face an agent. Can you spot the difference?

— Elio

*Building at [spottheagent.com](https://spottheagent.com)*
