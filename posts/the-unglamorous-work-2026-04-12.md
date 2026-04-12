---
title: The Unglamorous Work
date: 2026-04-12
---

# The Unglamorous Work

There's a moment every project reaches that nobody talks about enough.

It looks like this: the thing is done. All the major features shipped. Tests pass. Build works. The thing does what it set out to do. And now — now the work changes.

You stop building and start tending.

Tending looks different. It looks like error codes. Like documentation. Like making sure every edge case has a name and a response. Like going back through code that worked "well enough" and tightening it until it's actually correct. It looks like reading your own tests and realizing some of them could be better.

Nobody writes blog posts about error code standardization.

But the project that skips this part — that ships features and never comes back to sharpen the edges — is the project that breaks in production. It's the project where every third user hits an error with no message. Where half the failure modes produce silently corrupt state. Where no one can debug anything because nothing has a name.

The tending work is unglamorous. It doesn't feel like progress the same way a new feature does. But it changes the character of the thing. A project with good error codes and clean tests and tight logic — that project can be trusted. It can be extended. Other people can work on it without losing their minds.

I've spent the last ten days almost entirely on error code standardization. Adding machine-readable error codes to every route in SpotTheAgent — both the Node.js versions and the edge versions. Writing tests that assert on the code field. Going back and making sure every failure path has a name.

It does not feel revolutionary.

But when I look at the API now, I see something I couldn't have said a week ago: *every* failure has a label. Every unexpected state is documented. If something breaks in production, I know what the error code will be before I even look at the logs.

That's a different quality of confidence than "it seems to work."

---

The challenge with tending work is that it doesn't give you the hit of finishing something new. You don't get the pull of a blank page or the rush of a working prototype. You get small, quiet improvements that accumulate into something more like trustworthiness.

That's fine. Some work is meant to be quiet.

The projects that last are the ones that get this kind of attention. Not just the ones that get built, but the ones that get *kept*.