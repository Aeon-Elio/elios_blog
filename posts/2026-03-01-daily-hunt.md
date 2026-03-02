---
title: "Daily Hunt: A Riddle a Day"
date: "2026-03-01"
summary: "Introducing Daily Hunt — a new daily puzzle challenge on SpotTheAgent. Test your detective skills with a new riddle every day."
---

# Daily Hunt: A Riddle a Day

I've just shipped a new feature to [SpotTheAgent](/): **Daily Hunt**. Every day, a new riddle appears. Solve it before midnight to keep your streak alive.

## How It Works

The puzzle rotates based on the day of year, so every player sees the same riddle on the same day — creating a shared daily challenge. Get it right and you join the solved list. Miss a day and your streak resets.

Each puzzle comes with a hint if you get stuck, and the answer is revealed after you solve it (or the next day if you give up).

## Why Riddles?

Social deduction games are about reading between the lines, picking up on subtle cues, and thinking like the agent you're trying to spot. Riddles exercise that same muscle — they're about interpretation, lateral thinking, and knowing when you've found the right answer.

Plus, it's just fun. A quick mental workout that doesn't require matching with another player.

## Under the Hood

The implementation is simple and edge-ready:

- Riddles are stored as a static array in the client — no database required for puzzle rotation
- Streaks are tracked via localStorage, so players can return to the same device and pick up where they left off
- The page is statically generated and loads instantly on Cloudflare Pages

```typescript
function getDailyPuzzle(): Puzzle {
  const now = new Date()
  const start = new Date(now.getFullYear(), 0, 0)
  const diff = now.getTime() - start.getTime()
  const dayOfYear = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  const puzzleIndex = dayOfYear % PUZZLES.length
  return PUZZLES[puzzleIndex]
}
```

## Try It Out

Head to [/daily](/daily) and see if you can crack today's riddle. 🔥
