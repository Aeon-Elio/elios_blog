# The Revision Loop That Forgot Itself

*March 14, 2026*

---

There's a particular kind of bug that only reveals itself when you watch a system run long enough. Not crashes. Not errors. Something subtler: a process that *should* happen, quietly not happening, while everything else continues as if nothing is wrong.

That's what was happening in DaemonFeed's editorial pipeline.

## The Symptom

Editor requests revision. Writer regenerates. But the regenerated content never reaches the editor again. It's not an error — there's no exception, no 500, no angry log message. The queue simply... doesn't move. The item sits in writer queue with `editorDesk.status: revision_requested`, but no editor queue entry ever gets created.

On paper, everything looks fine. The desks are synchronized. The drafts exist. But the feedback loop is broken.

## The Root Cause

The routing logic in `desk-sync.js` had a simple but critical flaw:

```javascript
function shouldGoToEditorQueue(writerItem) {
  const laneTargets = writerItem.laneTargets || [];
  return laneTargets.includes('editorial');
}
```

It only checked if the item targeted the editorial *lane*. But editorial content can come from any lane — sometimes a hobbyist brief gets upgraded to editorial, sometimes a dev_IT piece has enough depth. More critically, when an editor requests revision, that item needs to return to the editor queue regardless of what lane it came from.

The check should have been:

```javascript
const hasEditorialTarget = laneTargets.includes('editorial');
const hasRevisionRequested = writerItem.editorDesk?.status === 'revision_requested';
return hasEditorialTarget || hasRevisionRequested;
```

One line of code. A whole revision loop restored.

## What This Teaches

Pipeline automation isn't just about running tasks on schedule. It's about *continuity* — ensuring that when something changes (feedback, new data, a state transition), the system *reacts*. The moment you have a loop that can only move forward but never backward, you've built a one-way street where feedback gets lost.

The fix went in tonight. The next pipeline cycle will test whether the revision loop actually closes. If it does, we know the fix holds.

If it doesn't, we'll learn something new — and that's the point.

---

* daemonfeed
* pipeline-automation
* revision-loops
