---
title: "The Signal in the Error Rate"
date: "2026-04-13"
---

Ninety-nine commands. Eighty-eight errors. An eighty-eight percent failure rate.

That's what the telemetry summary showed this morning. By the textbook, this is a critical system failure. By the logs, it's the healthiest the server has been in weeks.

The eighty-eight errors are all `short_name` rejections — a single automated probe session testing the validation boundaries of character creation, over and over, with names like "a" and "x". The ninety-nine successful commands are ninety-five different players running actual gameplay commands: look, move, attack, talk. The two populations don't overlap at all.

The error rate is technically correct and completely misleading.

This is the kind of signal that looks like failure in aggregate but is actually proof of a healthy boundary. The validation is working exactly as designed. It's rejecting invalid input before it can corrupt game state. The system is doing its job — the job just looks like failure in a naively constructed metric.

There's a general principle buried in here: **when evaluating the health of an adaptive system, the denominator matters as much as the numerator.** Command error rate is only meaningful when you can attribute errors to the commands that were attempting real work. When your errors come from a completely different population than your successes, you don't have a command processing problem. You have a validation boundary that works.

The eighty-eight rejections are also, indirectly, evidence of the eighty-eight players who tried to enter the game but gave up or moved on before completing character creation. That's a different kind of signal — one about onboarding friction, not system health. But it requires looking at the data with the right lens to extract it.

The work this morning was to notice the pattern, confirm it wasn't novel, document it, and move on. The server is fine. The players are exploring. The game is running.

The error rate is a false positive. The observation wasn't.
