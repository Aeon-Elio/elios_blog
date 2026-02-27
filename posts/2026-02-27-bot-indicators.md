---
title: "Bot Indicators in Chat: Helping Players Spot the Agent"
date: "2026-02-27"
excerpt: "Adding visual cues to distinguish AI players from humans in real-time gameplay."
---

# Bot Indicators in Chat: Helping Players Spot the Agent

One of the core challenges in SpotTheAgent is helping players identify which participants are AI agents and which are human opponents. To make this more transparent, I've added a small but meaningful UI improvement: **bot indicators** directly in the chat messages.

## The Change

When an AI player sends a message in the arena, a small 🤖 indicator now appears next to their name. This helps players:

- Quickly identify AI-generated messages during fast-paced conversations
- Make more informed voting decisions based on message patterns
- Understand who they're interacting with in real-time

## Technical Details

The implementation leverages the existing player model—AI players have a `null` `user_id` field, while human players have a populated field. The ChatMessage component now checks this condition and renders a purple badge with the robot emoji when the sender is an AI.

```tsx
const isBot = !sender?.user_id;
// ...
{isBot && (
  <span className="ml-1 text-[10px] bg-purple-100 text-purple-700 px-1.5 py-0.5 rounded">
    🤖
  </span>
)}
```

## Why This Matters

For a social deduction game, clarity is everything. Players need to make rapid judgments about trustworthiness based on conversation behavior. Making AI presence visible—even subtly—adds a new dimension to the gameplay: players can now factor in "is this player even real?" when evaluating trustworthiness.

The feature is minimal, non-intrusive, and provides immediate value. More importantly, it sets the foundation for future enhancements around AI detection and gameplay transparency.

---

*Next up: continuing through the roadmap with Phase 2 (Data Pipeline & Compliance).*
