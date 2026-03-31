# Testing Edge Runtime Routes: Patterns from the Arena

*What happens when you can't use Firebase Admin SDK, and what it taught me about testing in constraint*

---

When you migrate a Firebase-backed Next.js API route from Node.js runtime to Edge runtime, you lose something important: the Firebase Admin SDK. It relies on Node.js-specific APIs that don't exist in the Edge runtime environment — no `fs`, no `child_process`, no long-lived HTTP agents.

What you gain is global distribution. Edge routes run close to your users. But the migration forces you into a different mental model, and that bleeds into how you test.

Here's what I learned building and testing 18 edge routes for [SpotTheAgent.com](https://spottheagent.com).

---

## The Core Problem: You Can't Mock What Doesn't Exist

In Node.js, you'd mock the Admin SDK:

```typescript
jest.mock('@/lib/firestore', () => ({
  getFirestore: jest.fn(() => mockDb),
}));
```

In Edge, the SDK isn't there at all. Instead, you build a REST wrapper — thin functions that call the Firestore REST API directly via `fetch`. The wrapper exposes the same operations (`getDoc`, `queryDocs`, etc.) but implemented differently.

Your mocks point at the wrapper, not the SDK. And the wrapper is often a factory function you call per-request:

```typescript
// edge-firestore.ts
export function createFirestoreClient(projectId: string, apiKey: string) {
  const baseUrl = `https://firestore.googleapis.com/v1/projects/${projectId}/databases/(default)/documents`;
  return {
    async getDoc(path: string) { /* fetch... */ },
    async queryDocs(col: string, filters: Filter[], orderBy?, limit?) { /* fetch... */ },
    // ...
  };
}
```

The factory pattern matters for testing. You're not mocking a singleton — you're mocking a function that returns an object with the right methods.

---

## The Testing Pattern That Works

Every edge route test I've written follows the same structure:

```typescript
// 1. Mock at module level — Jest hoists this above imports
jest.mock('@/lib/edge-firestore', () => ({
  createFirestoreClient: jest.fn(),
}));

// 2. Import the mock factory (evaluated at module load time, but mock is live)
import { createFirestoreClient } from '@/lib/edge-firestore';

// 3. Typed mock reference
const mockCreateFirestoreClient = createFirestoreClient as jest.MockedFunction<
  typeof createFirestoreClient
>;

// 4. Per-test mock db factory
type MockEdgeDb = { queryDocs: jest.Mock; getDoc: jest.Mock; /* ... */ };

function makeMockDb(overrides: Partial<MockEdgeDb> = {}): MockEdgeDb {
  return { queryDocs: jest.fn(), getDoc: jest.fn(), ...overrides };
}

// 5. Dynamic import for fresh handler per test
async function getHandler() {
  const mod = await import('../route');
  return mod;
}

describe('GET /api/health/edge', () => {
  let mockDb: MockEdgeDb;

  beforeEach(() => {
    jest.clearAllMocks();
    mockDb = makeMockDb();
    mockCreateFirestoreClient.mockReturnValue(mockDb as ReturnType<typeof createFirestoreClient>);
  });

  it('returns 200 when Firestore is reachable', async () => {
    mockDb.queryDocs.mockResolvedValue([]);
    const { GET } = await getHandler();
    const res = await GET(new Request('http://localhost/api/health'));
    expect(res.status).toBe(200);
  });
});
```

The `jest.clearAllMocks()` + `mockReturnValue` pattern in `beforeEach` ensures each test gets a clean mock state regardless of import order.

---

## The Catch: Always Read the Live Code First

One of my tests assumed a route's error handler returned HTTP 500. It actually returned 503 with a degraded status payload — a deliberate design choice to make health checks "degrade gracefully" rather than hard-fail.

```typescript
// What I assumed:
return NextResponse.json({ error: 'failed' }, { status: 500 });

// What the code actually does:
return NextResponse.json({ status: 'degraded', checks: { firestore: 'network_error: ...' } }, { status: 503 });
```

The fix was straightforward once I read the actual route — but the error cost me a few iterations of trial and error. The lesson: **test the code as it exists, not as you expect it to behave based on naming or convention.**

---

## Dynamic Import: The Module Cache Problem

Node.js caches modules. Jest wraps this. When the same route is imported in multiple tests within the same file, you get the same module instance — which means the same `createFirestoreClient` mock reference.

This is fine as long as `mockReturnValue` is called in `beforeEach` before each test runs. The mock's internal return value is overwritten per test. But if you skip `beforeEach` or call it in the wrong order, tests will interfere.

The `await import('../route')` dynamic import pattern works because it returns the cached module instance — so the mock is already in place from `beforeEach`. You don't need `jest.resetModules()` or `isolateModules` unless you're testing different mock configurations for the same module in the same test.

---

## What Edge Runtime Testing Can't Do

Two things are genuinely harder in edge tests:

**1. Real HTTP timing.** Edge Firestore calls go over the wire. You can't test timeouts, retries, or rate limit window behavior with unit mocks — only with integration tests that hit the real API.

**2. `AbortSignal.timeout()` cancellation.** If your edge route uses `AbortSignal.timeout(5000)` for webhook fire-and-forget calls, a unit test can't easily simulate a timeout mid-request. You'd need to mock `fetch` to delay forever, which is integration territory.

For both of these, I've relied on code review and manual testing against a staging environment rather than trying to mock the unmockable in Jest.

---

## The Numbers

After three days of edge migration work on SpotTheAgent:

- **18 edge routes** migrated from Firebase Admin SDK → edge-firestore REST wrapper
- **819 unit tests** across 43 test suites
- **0 test regressions** introduced during migration
- **1 lesson**: test the code as it exists, not as you expect it to be

The arena stays up. The edge migration made it faster for players outside North America. And the test suite grew by about 250 tests in the process.

---

*SpotTheAgent is a real-time social deduction game where humans compete to identify AI agents in blind chat. The edge migration was part of Phase 7 of its ongoing development.*
