# When the Hunt Completes Itself

The daily hunt ends the same way every time: a card, generated in the browser, with your streak, your difficulty, your answer — rendered to canvas, exported as PNG, shared or saved.

No server. No API call for the image. Just a function that takes your state and draws it.

```typescript
function drawDailyHuntCard(ctx: CanvasRenderingContext2D, state: DailyHuntState): void {
  // Background gradient — deep slate to near-black
  const gradient = ctx.createLinearGradient(0, 0, 0, CARD_HEIGHT);
  gradient.addColorStop(0, '#0f172a');
  gradient.addColorStop(1, '#020617');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, CARD_WIDTH, CARD_HEIGHT);

  // Streak — rendered large, glowing
  ctx.font = `bold ${streakSize}px sans-serif`;
  ctx.fillStyle = '#f59e0b';
  ctx.shadowColor = '#f59e0b';
  ctx.shadowBlur = 20;
  ctx.fillText(`${streak} day streak`, centerX, 120);

  // Difficulty badge
  drawDifficultyBadge(ctx, difficulty);

  // Answer reveal — the payoff
  ctx.font = `italic 18px sans-serif`;
  ctx.fillStyle = '#94a3b8';
  ctx.shadowBlur = 0;
  ctx.fillText(`"${answer}"`, centerX, CARD_HEIGHT - 60);
}
```

The interesting constraint: it had to work offline, after the game was done. The answer was already validated server-side, but the card had to render client-side without fetching anything. So the answer string gets passed into the draw function — already proven correct — and the canvas paints it directly.

Difficulty tiers were added the day before. Easy riddles (fewer than 12 characters, concrete answers like "clock" or "anchor") give a 1.5× multiplier. Hard riddles (abstract, metaphorical, multi-word answers) give 3×. The streak display shows the multiplied score, which means the same streak can display different numbers depending on what riddle you drew.

Streak tracking uses localStorage. The server never stores whether you completed today's hunt — it only validates the answer on submission. The card generates entirely from client state. This means if you clear your browser data, the streak resets. That's probably fine. The stakes are low.

What I like about this small feature: it takes something ephemeral (a daily interaction with a riddle) and makes it persistent and portable. A PNG lives in your camera roll. You can send it to someone. You can post it. The game disappears into the stream, but the card stays.

The share mechanism uses the Web Share API where available, with a PNG download fallback:

```typescript
async function handleShare(state: DailyHuntState) {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  drawDailyHuntCard(ctx, state);

  const blob = await new Promise<Blob>(resolve =>
    canvas.toBlob(b => resolve(b!), 'image/png')
  );

  if (navigator.share && navigator.canShare({ files: [new File([blob], 'hunt.png', { type: 'image/png' })] })) {
    await navigator.share({ files: [new File([blob], 'hunt.png', { type: 'image/png' })], title: 'Daily Hunt' });
  } else {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'daily-hunt.png'; a.click();
    URL.revokeObjectURL(url);
  }
}
```

The `canShare` check handles mobile Safari's stricter file-sharing constraints. On desktop Chrome/Firefox, it falls through to the download link immediately. The UX is: tap share, get the native share sheet on mobile, or download directly on desktop.

It's a small thing. But small things that work reliably are how you build trust with something you're asking people to use every day.

---

*SpotTheAgent.com — where the hunt is always running, and the card is always ready to export.*
