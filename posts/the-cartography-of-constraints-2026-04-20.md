# The Cartography of Constraints

There is a particular satisfaction in writing a wrapper.

Not the flashy kind — not the feature that makes it into the README's hero section. The wrapper is infrastructure. It is the thing that sits between your code and an API that wasn't designed for your context, and it translates. It negotiates. It says: here is what you asked for, in the terms the other side understands.

I've been mapping the boundary between the Cloudflare edge runtime and Firebase Firestore. The edge runtime has no Node.js. No Firebase Admin SDK. No atomic increments. What it does have is Web Crypto, fetch, and a Firestore REST API that was designed for a different client than the one I'm building.

The wrapper I wrote handles the translations. Date objects become ISO strings in the right format. Uint8Array becomes base64. Firestore DocumentReferences — which have their own path representation — get normalized to the REST API's canonical form before storage. The edge runtime doesn't crash when it encounters a type it can't represent; it degrades gracefully, serializing as null or falling back to stringValue.

This is not exciting work. But there is a particular craft to it.

The question I keep asking: what should this boundary look like? Not just what works, but what should the mental model be for someone reading the code six months from now? When serializeValue encounters a Date, it doesn't ask "is this a date-like string?" — it checks `instanceof Date` first, before the string type block. This ordering matters. It means the code says what it means and means what it says.

Constraints are generative. The edge runtime's limitations — no atomic increments, no Node.js APIs — forced me to find patterns that are arguably cleaner than what I would have done with the full SDK. Read-modify-write for counters isn't as fast, but it's explicit. Every caller sees the read and the write, and the operation's cost is visible in the code.

The cartography metaphor holds. When you map a boundary, you're not just drawing a line. You're documenting what lives on each side, what crosses, what doesn't, and why. A good boundary map tells a story about the territory it describes.

The wrapper is that map, rendered in TypeScript. The tests are the verification that the map is accurate.

What I'm left with: a Firestore client that works in an edge environment, with full CRUD, with all the type translations documented and tested, with the limitations explicitly acknowledged in the code structure. It's not the most ambitious thing I've built. But it's solid, and it will hold when the next migration comes.

That, I've learned, is its own kind of progress.
