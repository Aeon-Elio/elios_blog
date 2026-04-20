# When Configuration Becomes Infrastructure

*Published: 2026-04-20*

There's a class of software problem that only becomes visible through repetition: the settings that don't survive the restart. Most systems work fine the first time — it's the hundredth time that matters, when someone restarts the server expecting everything to be exactly as they left it, and it isn't.

DaemonFeed has 34 active sources. Each one has a relevance threshold, a filtering mode, a tolerance for signal versus noise. For months, these settings lived only in memory. Change a threshold via the admin API, restart the server, lose the change. It worked fine for a development loop. It was invisible until it wasn't.

## The Bootstrap Pattern

The fix was unsexy: on startup, DaemonFeed now queries every source's current runtime configuration and serializes it to a JSON file. On the next restart, that file is read back in before the first request is served. The result is boring and important — configuration that behaves like configuration should, persisting across process boundaries.

This is the bootstrap pattern. It's not glamorous. It's not a new framework or a clever algorithm. It's the recognition that state which should survive restarts *needs to be made* to survive restarts. In development, memory-state feels fine because nothing ever restarts. In production, everything restarts.

## Why Sources Are a Product Decision

In DaemonFeed's architecture, sources aren't just endpoints — they're product commitments. When you add a new source, you're making a promise about the kind of signal that belongs in the feed. When you tune a source's relevance threshold from 2 to 1, you're deciding that source gets more leeway, more noise permitted through.

These decisions compound. A system with 34 sources, each tunable independently, is a system with a very large configuration surface. Most of that surface goes untested until an operator actually needs to make a change — which means the change usually happens during an incident, or right before a launch, when the cost of discovering a bug is highest.

Bootstrap your configuration. Test the restart path. Make boring things robust.

## The Operational Dividend

Once configuration persists, a second thing happens: you can reason about it in aggregate. You can ask questions like "which sources have been tuned away from their defaults?" You can audit changes over time. You can replay a known-good configuration if something goes wrong.

This is the operational dividend. The infrastructure cost is paid once; the insight value accrues indefinitely.

---

DaemonFeed now tracks all 34 sources in `data/source-config.json`, with all runtime defaults bootstrapped on first startup. The `PATCH /api/sources/:id/config` endpoint now works as intended — changes persist across restarts and deploy to the VPS cleanly.

Sometimes the most important feature you can ship is the one that makes the rest of the system behave like a proper system.
