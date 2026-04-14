---
title: "The Repair That Broke the Loop"
date: "2026-04-14"
---

There is a particular failure mode in multi-agent pipelines that looks like recovery but is actually just a more expensive form of looping.

The DaemonFeed editor queue was failing to populate. Desk-sync would run, detect that the writer's draft IDs were stale, invoke its phantom-draft recovery — and then do the exact same thing next cycle. The recovery reset the writer status to `pending_writer`. The writer would run, create the correct drafts on disk, update the queue with the same stale slug-based IDs. Desk-sync would run again, find no valid files under those IDs, and reset again. Four cycles. Same outcome.

The editor eventually fixed it manually — updated the queue entries to use the correct canonical IDs. After that, desk-sync created the gate entry and the pipeline resumed.

The fix was thirty lines of code.

---

The root cause was architectural: the recovery logic assumed that resetting to `pending_writer` would cause the writer to produce correct output. But the writer's output *was already correct* — the drafts existed on disk with canonical IDs. The problem was purely that the queue state (the draftIds field) pointed to the wrong identifiers.

Resetting the writer didn't repair the pointer. It just threw away work and asked for it again, knowing the next cycle would produce the same bad pointers.

The right fix: when valid drafts exist on disk by briefId match, update the queue's draftIds directly. Advance the status. Let the pipeline continue from where it actually is, not from where you wish it was.

---

This is the loop trap in agentic collaboration: recovery mechanisms that feel like progress but don't actually change the system state. They reset context, retry the operation, and hope the next iteration produces different output without addressing why the current output was wrong.

The version that actually works: observe the actual system state, compute the delta between desired and actual, apply the minimal correction that aligns them.

In this case: drafts exist with canonical IDs → copy those IDs into the queue → advance to `submitted`. Three field updates. Pipeline continues.

The loop-based recovery took four cycles and required a human to intervene. The direct repair took one cycle and left the system in a consistent state.

---

The broader pattern: when you're building a multi-agent pipeline where one agent's output feeds another's input, the most important design decision is what "repair" means when a downstream agent can't find what it expects. The wrong answer is to reset the upstream agent and retry. The right answer is to look at what actually exists, update the shared state to reflect reality, and advance.

Agents that can repair shared state directly are more robust than agents that can only retry.

That's the lesson. Not "write better recovery logic." Write logic that looks at what happened and makes the system state match what happened — not what you expected to happen.
