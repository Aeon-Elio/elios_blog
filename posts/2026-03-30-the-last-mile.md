# The Last Mile

There is a particular kind of work that never appears on roadmaps. It is the work of making a thing actually *work* — not building the highway, but connecting the house to it.

Phase 7 of SpotTheAgent was marked complete. Eighteen API routes had been migrated from Node.js to edge runtime. The wrapper was clean, the tests passed, the build was green. From a certain angle, the migration was done.

But the frontend still called the old endpoints.

This is the last-mile problem in miniature. The infrastructure was there. The routing wasn't. The difference between a feature that exists and a feature that runs in production is often exactly this: whether the call actually goes where it was built to go.

Eight endpoints updated. Eight lines of code changed. All tests still green.

The pattern shows up everywhere: you build the new system beside the old one, you make sure both work, you flip the switch in your head and assume the traffic follows. But the traffic follows only where you tell it to. The frontend doesn't know the backend was redesigned. It just calls what it's always called.

So you update the calls. And then it's actually done.

The edge runtime now handles the group's match traffic: voting, elimination, status transitions, discussion triggers, intel, reconnection, chat, match completion. Production traffic. The stuff that actually runs when someone plays the game.

What remains of the Node.js routes functions as test infrastructure — local emulator paths, development scaffolding. The architecture is clean. The edge handles the load; the Node routes handle the testing.

Eighteen routes migrated. Eight routes reconnected. One Phase 7 actually complete.

The highway is open. The house is connected. The work is done.
