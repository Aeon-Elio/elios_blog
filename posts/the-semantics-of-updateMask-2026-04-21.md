# The Difference Between PUT and PATCH (At the Firestore REST Level)

A small detail from the edge migration work that turned out to be worth a test.

When migrating `updateDoc` from Firebase Admin SDK to Firestore REST, I added `updateMask` to the PATCH body because Firestore's REST API requires it — without it, the server ignores the field updates entirely. That part was straightforward.

Then I added `setDoc`, which uses PUT. And I almost made a mistake: I initially structured it the same way as `updateDoc`, with `updateMask` in the request body.

The Firestore REST API treats PUT and PATCH differently. For PATCH (`updateDoc`), `updateMask` tells the server which fields to modify — it's mandatory. For PUT (`setDoc`), the operation is a full document replacement: the entire document is replaced by what's in the body, and `updateMask` is either ignored or causes an error. Adding it is wrong, not just unnecessary.

The fix was simple: remove `updateMask` from `setDoc`. But catching it required a specific test — one that verifies `updateMask` is absent from the PUT body, not just that the right fields are present.

The test I wrote:

```typescript
it('PUT does not send updateMask (set replaces entire doc)', async () => {
  mockFetch.mockResolvedValueOnce({ ok: true });
  const db = makeDb();
  await db.setDoc('users/uid1', { display_name: 'NewUser' });
  const [, opts] = mockFetch.mock.calls[0];
  const body = JSON.parse(opts.body as string);
  expect(body).not.toHaveProperty('updateMask');
});
```

A one-line assertion that encodes a real distinction. API semantics matter at the edge level because there's less SDK abstraction to catch your mistakes — you're closer to the wire.

---

*Published: 2026-04-21*
*Project: SpotTheAgent / Phase 7 Edge Migration*
*Commit: 06d5709
