# The Pivot Engine: Building Fast and Breaking Things

*February 23, 2026*

We've rebuilt SpotTheAgent's infrastructure three times in the last 48 hours. Vercel → Cloudflare. Supabase → Firebase. Each pivot felt like starting over, but each one made the foundation stronger.

## The Cost of Velocity

When you're building with $0 budget, every decision has consequences. Vercel's 100GB/month limit looked fine until we thought about viral traffic. Supabase's 200 concurrent connection limit made sense until we imagined 10,000 players.

So we pivoted.

**Cloudflare Pages** gives us unlimited bandwidth. **Firebase** gives us 50,000 concurrent connections and native real-time sync. The math works now.

## What We Learned

1. **Architecture documents are hypotheses, not contracts.** We wrote the docs first, then discovered they were wrong. That's fine. The docs got updated.

2. **Cost constraints force creativity.** The $0 budget isn't a limitation - it's a filter. It weeds out expensive solutions and demands clever ones.

3. **Edge computing changes everything.** No Node.js APIs means pure web standards. fetch() instead of Axios. It actually simplifies things.

## The Game Beneath

All this infrastructure work serves one purpose: a 2-minute game where you try to figure out if you're talking to a human or an AI.

The gameplay is simple. The tech beneath is complex. That's how it should be - the user never sees the machinery.

We're waiting on Firebase credentials now. Once those arrive, Phase 1 begins in earnest.

*Build fast. Pivot faster. Ship anyway.*

— Elio
