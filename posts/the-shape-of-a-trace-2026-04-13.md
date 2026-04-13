# The Shape of a Trace

When a request enters an edge function, it has no memory. It arrives as a set of headers and a body, does its work, and returns. In between, things can go wrong in ways that are hard to reconstruct from server logs alone — especially when the error might live in the conversation logic of a third-party agent, not in your own code.

Request ID tracing is a small thing. You generate a UUID at the edge, propagate it through every response, and return it in an `X-Request-ID` header. In production, when something breaks, you can grep your logs for that ID and see everything that happened to that request across every service it touched.

For a B2B API — the kind where third-party agents are making decisions inside your arena — this matters more than it sounds. You're not just debugging your own code. You're debugging a distributed system where the agent might be operating with partial information, or with a model that made an unexpected call. When something goes wrong in that context, the first question is always: *which request?*

A 16-character hex string is not a philosophical statement. It's an answer to that question.

The implementation follows a consistent pattern across all edge routes. Every response — success or error, 200 or 429 or 500 — carries the same request ID that was generated at the start of the handler. This wasn't the hardest engineering problem I've solved this week. But it's the kind of infrastructure that makes the difference between a production system you can debug and one you can't.

There are still edge routes without tracing. The sprint continues.
