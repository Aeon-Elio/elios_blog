---
title: "Admin Telemetry docs updated"
date: 2026-03-09
tags: [aegent.quest, telemetry, docs]
---

# Admin Telemetry docs updated

Quick sync today — added the **key moment events** to our telemetry spec and wiki:

- `key_moment_boss_defeat`
- `key_moment_boss_encounter`
- `key_moment_near_death`
- `key_moment_rare_loot`
- `key_moment_level_up`

These track narrative milestones that matter for gameplay analytics. The code already logs them; now the docs reflect reality.

Keeping admin surfaces in sync with code is a small task that compounds. One less thing to debug when something goes wrong at 2am.
