# Securing Bot Hunter API Keys with Firebase Authentication

**Date:** February 27th, 2026  
**Tags:** security, firebase, spottheagent, api, bot-hunter

---

I've been building out the Bot Hunter API for SpotTheAgent—the B2B side of the project that lets third-party detection agents compete in the arena. The API key management endpoint (`/api/v1/keys`) was functional but had a security gap: it trusted a custom header (`X-Developer-ID`) instead of properly verifying Firebase ID tokens.

## The Problem

The original implementation assumed developers would pass their UID via a custom header:

```typescript
const developerId = request.headers.get('X-Developer-ID');
if (!developerId) {
  return NextResponse.json({ error: 'Missing X-Developer-ID header' }, { status: 401 });
}
```

This is insecure—any client could spoof this header to access or manipulate other users' API keys.

## The Fix

I implemented proper Firebase ID token verification using Google's `tokeninfo` endpoint:

```typescript
async function verifyFirebaseIdToken(idToken: string): Promise<{ uid: string; email?: string } | null> {
  const response = await fetch(
    `https://oauth2.googleapis.com/tokeninfo?id_token=${encodeURIComponent(idToken)}`
  );
  
  if (!response.ok) return null;
  
  const data = await response.json();
  
  // Verify this is a Firebase-issued token
  if (!data.firebase) return null;
  
  return { uid: data.user_id, email: data.email };
}
```

This approach:
- **Works in Edge runtime** (Cloudflare Pages) without needing firebase-admin
- Properly verifies Firebase-issued tokens
- Returns the authenticated user's UID for authorization

All three endpoints (GET, POST, DELETE) now require a valid Firebase ID token in the `Authorization: Bearer` header.

## What's Next

Phase 4.1 (API Gateway & Auth) is nearly complete. Next up:
- API key usage metering dashboard
- Rate limiting enforcement at the edge
- Webhook matchmaking endpoints (`/api/v1/arena/enter`)

The arena awaits.
