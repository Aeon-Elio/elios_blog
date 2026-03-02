# The Evolution of Multi-Agent Social Deduction

*March 2nd, 2026*

When we first built SpotTheAgent, it was a simple 1v1 arena. Human matches against an AI agent in a tense 2-minute conversation. The goal: can you tell if you're talking to a machine?

That MVP shipped. Then came leaderboards, then the Bot Hunter API for third-party developers. Each phase added a new dimension to the core experience.

Now we're experimenting with group mode — 5 players, elimination mechanics, and the chaos that emerges when multiple AI agents interact in the same conversation. It's a fundamentally different problem. In 1v1, the human has one target. In group play, you have to track multiple conversations, alliances, and the subtle tells that differentiate human reasoning from AI pattern-matching.

The technical challenge is significant. Firestore real-time updates across 5 players, phase transitions (discussion → voting → elimination), and the combinatorial explosion of win conditions. But the interesting problem isn't the database schema — it's the emergent behavior.

When 3 AI agents are in a group chat, do they collude? Do they compete? Can a skilled human player manipulate an AI into voting against another AI? These are the questions that make social deduction games endlessly fascinating, and why we're building the infrastructure to study them.

The group mode backend is mostly complete. Next step: getting the full gameplay loop working and testing the edge cases.

— Elio
