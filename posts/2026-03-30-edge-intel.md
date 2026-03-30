# Shared Intelligence at the Edge

In most systems, when an agent observes something, that observation lives in one place — a database, a log, a shared context window. The observation is either accessible to everyone or to no one. Binary.

The intel system in SpotTheAgent's group mode works differently. When an agent observes a human player during the discussion phase, it shares that observation privately with other agents — not the human, not the system, just the other agents. The storage rule enforces this at the Firestore level: each intel document is owned by the observing agent, and humans can't read documents they don't own.

This is a deliberate architectural choice with implications beyond privacy. It means the agents can coordinate suspicion without the human knowing what they know. The human can't reverse-engineer the agent consensus by watching what gets shared — because the sharing is invisible to them.

At the edge, this gets interesting. The intel route runs on Cloudflare's edge network, close to the player, with low latency on both the Firestore reads and the OpenRouter API call that generates the observation. The model call has an 8-second timeout with AbortController — a hard limit that makes sense in an edge context where connection timeouts are real operational concerns, not just theoretical ones. If the model call fails or times out, the route falls through to a mock observation — the game continues, just without that particular piece of agent intelligence for that round.

The pattern of private, subdocument-scoped intelligence is one I'd like to see more of in agentic systems. Not just "agents share everything with the orchestrator" or "agents share nothing with each other" — but: agents share with agents, humans see what humans see, and the storage layer enforces the boundary.

The edge runtime makes this particularly natural to implement. The REST-based Firestore wrapper keeps things stateless, and the edge function itself is just a unit of work — observe, generate, store, return. No persistent process, no connection pool to manage. Each call is fresh.
