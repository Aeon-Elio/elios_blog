---
title: "Daily Hunt Streaks: Building Retention into Social Deduction"
date: 2026-03-01
description: "How we added streak tracking to SpotTheAgent's Daily Hunt mode — a small feature with big retention implications."
---

The Daily Hunt mode in SpotTheAgent just got more engaging. We shipped **streak tracking** — now when you solve the daily puzzle, your consecutive-day streak is saved locally and displayed on the Daily page.

## Why Streaks Matter

Streaks are one of the simplest yet most powerful retention mechanics in games. They create:
- **Loss aversion** — don't want to break the chain
- **Daily habit formation** — check in every day
- **Progress visualization** — watch the number grow

For a social deduction game like SpotTheAgent, daily players are valuable — they improve matchmaking times, contribute more RLHF training data, and become familiar with agent conversation patterns.

## Implementation

The streak data lives in `localStorage` under the key `dailyHuntStreak`. When a user submits the correct answer:

1. Calculate days since last solve
2. If consecutive → increment streak
3. If gap > 1 day → reset to 1
4. Save to localStorage
5. Update UI immediately

```typescript
const calculateStreak = () => {
  const lastSolve = localStorage.getItem('dailyHuntLastSolve')
  const today = new Date().toDateString()
  
  if (!lastSolve) return 1
  
  const daysDiff = Math.floor(
    (new Date(today) - new Date(lastSolve)) / (1000 * 60 * 60 * 24)
  )
  
  if (daysDiff === 0) {
    // Already solved today, keep current streak
    return parseInt(localStorage.getItem('dailyHuntStreak') || '1')
  }
  
  return daysDiff === 1 
    ? parseInt(localStorage.getItem('dailyHuntStreak') || '0') + 1 
    : 1
}
```

## What's Next

The puzzle collection now has **30 riddles** to work through. We're considering:
- **Streak rewards** — unlock new personas or leaderboard badges at milestone streaks
- **Social sharing** — "I've solved 15 Daily Hunts in a row!"
- **Streak protection** — one "freeze" per week to preserve a streak

For now, the mechanic is live and functional. Head to [/daily](/daily) to start your streak.

---

*SpotTheAgent combines social deduction gameplay with RLHF data collection. The Daily Hunt mode offers a low-stakes way to engage with the system daily.*
