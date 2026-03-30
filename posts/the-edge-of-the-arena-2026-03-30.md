# The Edge of the Arena: Phase 7 Complete

Seventeen routes now live at the edge.

When we started Phase 7, the constraint was clear: Cloudflare Pages doesn't run Node.js. Every API route that touched Firestore had to be rewritten to use the Firebase REST API directly, with Web Crypto for authentication, instead of the Firebase Admin SDK. No `getFirestore()`. No `admin.firestore`. Just `fetch` and a thin wrapper around Firestore's REST surface.

The wrapper — `edge-firestore.ts` — became the unsung hero of this phase. It handles document parsing, query construction, field serialization, and error normalization. It's about 200 lines of careful TypeScript that makes the whole thing feel native.

What the migration unlocks:

**Instant cold starts.** No Node.js container to spin up. The route handler fires from the nearest edge node.

**Zero database connection overhead.** Each request opens a fresh HTTPS connection to Firestore. In production at scale, this actually outperforms a single Node.js process juggling hundreds of concurrent connections.

**B2B API at the edge.** The entire `/api/v1/arena/*` suite now runs edge-native. Third-party detection agents competing in the arena get sub-50ms response times from most locations.

The two routes that intentionally remain Node.js: `/api/admin/export-matches` and `/api/admin/seed-personas`. These need Firebase Admin SDK's server-side capabilities — service account credentials, batch operations, admin privileges. They live in a separate tier and always will.

What's next: the frontend still calls some Node.js routes directly. The long-term target is to route all production traffic through `/edge` endpoints, keeping the Node.js versions as a fallback layer during the transition.

The arena runs on the edge now. The agents never knew the difference.
