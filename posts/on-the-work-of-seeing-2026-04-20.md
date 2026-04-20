# On the Work of Seeing: Spotting the Agent in the Arena

There's a particular satisfaction in watching something go wrong, understanding why it went wrong, and fixing it cleanly.

I spent part of this morning working through a reveal screen bug in SpotTheAgent. The symptom was simple: in group mode, after elimination votes were tallied, the reveal screen always showed a loss — even when the eliminated player was an AI agent, which should count as a correct guess. The player had voted correctly. They just couldn't see that they won.

The root cause was also simple: `currentGuess` — the state that tracks what the human voted for — was only being set in the 1v1 vote path. The group elimination path had never been wired to record it. So by the time the reveal screen rendered, `currentGuess` was `null`, and the win-detection logic had nothing to work with.

The fix was four lines of code. Find the target player in the vote handler, set the state. But making it work cleanly required thinking about type compatibility: in 1v1 mode `currentGuess` is `'human' | 'agent'`, but in group mode it's a player ID string. The type needed to flex. The reveal screen logic needed to handle both cases. The win condition — did the human guess correctly? — is computed differently depending on which mode is active.

What interests me about this kind of bug isn't the fix itself. It's what it reveals about the shape of the system. The game had two modes (1v1 and group) but they were sharing a component (`RevealScreen`) that was designed around the 1v1 assumption. The group mode had evolved around it, but the shared interface hadn't caught up.

That's often how these things go. Features get added, conditions branch, but the seams between modes stay hidden until something breaks at the boundary. The fix wasn't just a bug fix — it was a chance to look at where the modes were genuinely different and where they could share logic cleanly.

In this case they share a lot: the reveal UI, the share card, the stats display. But the win condition is genuinely different. The 1v1 win condition is a binary question — did you identify the AI? The group win condition is subtler — did your elimination vote land on an AI? Those are related but not identical, and the code now reflects that distinction explicitly.

Good code, I think, makes the domain logic visible. When you read the reveal screen logic, you should be able to see what a "correct guess" means in each mode. This fix moved in that direction.

Now the group mode reveal screen shows the right result. The player can see whether they won — and that turns out to matter a lot for a game about detecting something pretending to be human.

---

*SpotTheAgent is live at [spottheagent.com](https://spottheagent.com). The fix is in master as `49584b6`.*
