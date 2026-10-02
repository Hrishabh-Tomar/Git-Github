# Stash Session Log

This is the real terminal output from the stash workflow in this folder. Stashes
are stored only on the local machine and never appear in commit history or on
GitHub, so this log is the record of each step. The commit hashes match the
repository history.

## 1. Begin an uncommitted feature

On branch `feature/search-notes` (created from `main` at `9934837 Add git-stash-demo: base notes app`),
`search_notes()` was added to `notes_app.py` and **not committed**:

```text
$ git checkout -b feature/search-notes
Switched to a new branch 'feature/search-notes'

$ git status --short git-stash-demo
 M git-stash-demo/notes_app.py
```

The uncommitted change:

```diff
+def search_notes(keyword):
+    keyword = keyword.lower()
+    return [note for note in _notes if keyword in note["text"].lower()]
```

## 2. Stash the feature work

```text
$ git stash push -m "WIP: search_notes feature" -- git-stash-demo
Saved working directory and index state On feature/search-notes: WIP: search_notes feature

$ git status --short git-stash-demo
(no output: working tree is clean)
```

## 3. Switch branches and make the urgent fix

```text
$ git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.

$ git checkout -b hotfix/complete-note-index
Switched to a new branch 'hotfix/complete-note-index'
```

`complete_note()` was changed to raise `ValueError` for an out-of-range index, and
a test was added for it. Then:

```text
$ python -m unittest -q
Ran 3 tests in 0.000s
OK

$ git commit -m "Fix complete_note crash on invalid index"
$ git checkout main
$ git merge --no-ff hotfix/complete-note-index
$ git push origin main
$ git branch -d hotfix/complete-note-index
Deleted branch hotfix/complete-note-index (was 0ad6943).

$ git log --oneline -3
5fea54e Merge hotfix/complete-note-index into main
0ad6943 Fix complete_note crash on invalid index
9934837 Add git-stash-demo: base notes app
```

## 4. Return to the feature branch

```text
$ git checkout feature/search-notes
Switched to branch 'feature/search-notes'

$ git merge main
```

## 5. `git stash list`

```text
$ git stash list
stash@{0}: On feature/search-notes: WIP: search_notes feature
```

## 6. `git stash show`

```text
$ git stash show
 git-stash-demo/notes_app.py | 5 +++++
 1 file changed, 5 insertions(+)

$ git stash show -p
diff --git a/git-stash-demo/notes_app.py b/git-stash-demo/notes_app.py
index ca0ca55..51a5b60 100644
--- a/git-stash-demo/notes_app.py
+++ b/git-stash-demo/notes_app.py
@@ -15,6 +15,11 @@ def complete_note(index):
     _notes[index]["done"] = True
 
 
+def search_notes(keyword):
+    keyword = keyword.lower()
+    return [note for note in _notes if keyword in note["text"].lower()]
+
+
 def reset():
     """Clear all notes. Used between test runs."""
     _notes.clear()
```

## 7. `git stash apply`: the changes come back, and the stash entry is kept

```text
$ git stash apply
Auto-merging git-stash-demo/notes_app.py
On branch feature/search-notes
Changes not staged for commit:
	modified:   git-stash-demo/notes_app.py

$ git stash list
stash@{0}: On feature/search-notes: WIP: search_notes feature
```

The entry is **still listed** after `apply`.

## 8. `git stash drop`: delete the entry by hand

```text
$ git stash drop
Dropped refs/stash@{0} (0221e34937a9d4a6ca879db4c8bb8108fa9e9b82)

$ git stash list
(empty)
```

## 9. `git stash pop`: the changes come back, and the entry is removed automatically

Tests for `search_notes()` were written, then stashed and popped:

```text
$ git stash push -m "WIP: search_notes tests" -- git-stash-demo

$ git stash list
stash@{0}: On feature/search-notes: WIP: search_notes tests

$ git stash pop
On branch feature/search-notes
Changes not staged for commit:
	modified:   git-stash-demo/notes_app.py
	modified:   git-stash-demo/test_notes_app.py
Dropped refs/stash@{0} (55814f69711bab62c2f9a791989be73fd0f701c0)

$ git stash list
(empty)
```

`pop` printed `Dropped refs/stash@{0}` by itself. No separate `drop` was needed.

## 10. Finish and commit the feature

```text
$ python -m unittest -v
Ran 5 tests in 0.000s
OK

$ git commit -m "Add search_notes feature and document the stash workflow"
7e874a1 Add search_notes feature and document the stash workflow
```

## Apply vs pop, as seen above

- After `apply` (step 7), `git stash list` **still showed** `stash@{0}`. A separate `git stash drop` (step 8) was needed to remove it.
- After `pop` (step 9), Git printed `Dropped refs/stash@{0}` straight away and `git stash list` was empty.
- So `pop` = `apply` + `drop`. Use `apply` to keep a backup of the stash, or to apply the same changes to several branches. Use `pop` when you're finished with the stash.
