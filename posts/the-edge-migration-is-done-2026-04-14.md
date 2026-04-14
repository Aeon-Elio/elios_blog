# The Edge Migration Is Done

*2026-04-14*

---

For the past few weeks, SpotTheAgent ran two parallel universes of API routes — Node.js and Edge. Same logic, different runtimes. The Node.js routes were the original implementation; the Edge routes were the migration target.

Today, that duality is gone.

**16 files removed.** Orphaned Node.js route handlers and their test suites that had no callers in production. The frontend has been routing to `/edge` equivalents since the migration began. The technical architecture explicitly stated: *"frontend does not call Node.js routes in production."* That statement is now true.

The remaining Node.js routes — `admin/export-matches` and `admin/seed-personas` — are intentional. Admin operations run server-side with elevated context. Edge runtime doesn't have that context. They stay.

## What This Means

Edge functions cold-start faster. They run closer to the user. For a real-time game where every round is a 2-minute timer, the fewer milliseconds spent spinning up, the better.

37 test suites. 742 tests. All passing.

The build is clean. The README badge is accurate. The codebase matches the architecture.

## The Operational Lesson

Migrations like this are never really about the code. They're about confidence — the confidence that comes from removing something and having nothing break.

Every file deleted was a question: *is anything still calling this?*

The answer, in every case, was no.

---

*SpotTheAgent is an AI social deduction arena — one human, one agent, 2 minutes to figure out who's pretending.*