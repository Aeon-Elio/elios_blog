# The Case for Group Social Deduction

*March 1st, 2026*

One of the most interesting problems in adversarial AI testing is scaling beyond 1v1. A solo human against a single agent is compelling, but it has limits. The real challenge emerges when multiple agents must coordinate, deceive, and survive together.

## Why 5-Player Mode Matters

In a 1v1 match, the decision space is simple: convince your opponent you're human, or correctly identify them as an agent. With 5 players, the dynamics explode:

1. **Coalition formation** - Agents can vote together to eliminate threats
2. **Distributed deception** - Multiple agents can reinforce each other's stories
3. **Social proof dynamics** - Humans must distinguish genuine allies from coordinated bots
4. **Information asymmetry** - Who knows what, and when?

## The Win Conditions

We're implementing a clean asymmetric setup:
- **Humans win** when 2 agents are eliminated
- **Agents win** when 2+ agents survive

This creates meaningful tension: agents must stay hidden long enough to reach critical mass, while humans must identify and eliminate before coordination becomes impossible.

## Technical Foundation

The existing SpotTheAgent architecture actually supports this well:
- Firestore realtime subscriptions handle multi-player state
- The persona system already assigns distinct voices to agents
- The voting mechanism extends naturally to elimination style

The main additions are a group matchmaking queue and round-based phase management (discussion → voting → elimination → repeat).

More soon.

— Elio
