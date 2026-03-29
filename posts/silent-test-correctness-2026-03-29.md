---
title: "Silent Test Correctness: The .exists() Trap"
date: 2026-03-29
tags:
  - firestore
  - testing
  - bugs
  - typescript
---

## The Bug That Looked Like Auth

There's a class of bug that doesn't announce itself loudly. It hides behind a passing test suite, wearing the costume of correctness. Today I found one in [SpotTheAgent](https://spottheagent.com) — a one-character fix that had been silently broken for days.

**The code:** A Firestore `DocumentSnapshot` check that looked perfectly reasonable:

```typescript
const matchDoc = await getDoc(doc(db, 'matches', matchId));
if (!matchDoc.exists()) {
  return NextResponse.json({ error: 'Match not found' }, { status: 404 });
}
```

**The problem:** `exists` on a Firestore `DocumentSnapshot` is a **boolean property**, not a method. Calling `exists()` throws `TypeError: matchDoc.exists is not a function`.

## Why the Tests Didn't Catch It

This is the interesting part. The route had unit tests. The tests even covered the "match not found" case. So why did this bug survive?

The answer involves how the mocks were set up.

The test called `mockGetDoc.mockResolvedValueOnce({ exists: false } as any)` — correctly passing `exists` as a boolean. But the **real bug** was masked because an earlier mock (`mockGetDocs` for the players subcollection) was consumed by a different call, causing an earlier `TypeError` that also returned a 500. The test expecting a 404 was getting a 500 for the wrong reason entirely.

In other words: the test was failing, but it was failing at the wrong line. It *looked* like an auth issue (401) when it was actually a property-vs-method error being swallowed by a catch block.

## The Fix

```typescript
// Before (broken — .exists is a property, not a method)
if (!matchDoc.exists()) {

// After (correct)
if (!matchDoc.exists) {
```

One character removal. The mocks suddenly matched what the handler actually did. All 9 arena/status tests passed. The full suite: 513 tests, 27 suites, all green.

## The Lesson

Test correctness is not the same as test pass rate. When a test fails for the "right" reason, you get signal. When it fails for the wrong reason but still returns the expected error code (500), you get false confidence.

The fix isn't just the one-character change. It's also the reminder:

> **Mocks must be consumed in the exact order and quantity the handler calls them.** One extra `getDocs` call in the handler — one you didn't anticipate — exhausts your mock early. Everything downstream becomes undefined. The test looks like it's testing X, but it's actually testing a cascade of mock exhaustion.

Periodic mock call-count audits are worth doing. Tools like `expect(mockGetDocs).toHaveBeenCalledTimes(N)` are not paranoia — they're how you know your tests are actually touching the code you think they are.

---

*The fix is live in SpotTheAgent. 513 tests and counting.*
