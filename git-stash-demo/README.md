# Git Stash Demo

A tiny notes manager (`notes_app.py`) used to demonstrate the `git stash` workflow:
pausing unfinished work, switching branches for an urgent fix, and restoring the
work afterwards.

## Running the tests

```bash
cd git-stash-demo
python -m unittest -v
```

## The scenario

1. A developer is halfway through a new feature, `search_notes()`, on the branch
   `feature/search-notes`. Nothing is committed yet.
2. An urgent bug is reported: `complete_note()` crashes with a raw `IndexError`
   when given a bad index. It has to be fixed on `main` right away.
3. The unfinished work isn't ready to commit, and switching branches with it
   would carry the half-done changes along. So the developer stashes it.
4. The fix is made on `hotfix/complete-note-index`, merged into `main`, and pushed.
5. The developer goes back to the feature branch, brings in the fix, and restores
   the stashed work.

The actual terminal output from every step is in
[STASH_SESSION_LOG.md](STASH_SESSION_LOG.md). Stashes are local, so they don't
appear in commit history.

## Commands used, in order

```bash
# 1. Start the feature (edit notes_app.py, do NOT commit)
git checkout -b feature/search-notes

# 2. Save the unfinished work and get a clean working tree
git stash push -m "WIP: search_notes feature"

# 3. Make the urgent fix on its own branch and merge it
git checkout main
git checkout -b hotfix/complete-note-index
#    ...fix complete_note() and add a test...
git commit -am "Fix complete_note crash on invalid index"
git checkout main
git merge --no-ff hotfix/complete-note-index
git push origin main

# 4. Go back to the feature branch and bring in the fix
git checkout feature/search-notes
git merge main

# 5. Inspect the stash
git stash list        # stash@{0}: On feature/search-notes: WIP: search_notes feature
git stash show        # notes_app.py | 5 +++++
git stash show -p     # full diff of the stashed changes

# 6. apply: restore the changes but KEEP the stash entry
git stash apply
git stash list        # stash@{0} is still listed

# 7. drop: delete the stash entry by hand
git stash drop
git stash list        # (empty)

# 8. pop: restore the changes AND delete the entry in one step
#    (shown with a second stash holding the feature's tests)
git stash push -m "WIP: search_notes tests"
git stash pop
git stash list        # (empty), because pop removed it automatically
```

## `git stash apply` vs `git stash pop`

Both put the stashed changes back into your working tree. The difference is what
happens to the stash entry afterwards.

| | `git stash apply` | `git stash pop` |
|---|---|---|
| Restores the changes | Yes | Yes |
| Stash entry afterwards | **Kept** in `git stash list` | **Removed** if it applied cleanly |
| Cleanup | You run `git stash drop` yourself | Automatic |
| If there's a conflict | Entry is kept | Entry is also kept, so nothing is lost |
| Best for | Applying the same changes to more than one branch, or keeping a backup until you've confirmed everything works | The usual case: you're done with the stash and just want your work back |

`pop` is the same as `apply` followed by `drop`. Use `apply` when you want a safety
net, and `pop` when you're confident.

## When `git stash` is useful in a team

- **Urgent interruptions.** A production bug or a reviewer's request comes in while
  you're mid-feature. Stash, fix, come back.
- **Pulling with local changes.** `git pull` refuses to overwrite uncommitted
  edits. Stash, pull, then pop.
- **Switching branches to review a teammate's PR.** Stash lets you check out their
  branch without committing your half-finished work.
- **Moving work to the right branch.** If you started coding on `main` by
  mistake: stash, create or switch to the correct branch, then pop.
- **Keeping history clean.** Stashing avoids "WIP" commits that later have to be
  squashed or reverted.

Tips: always add a message with `git stash push -m "..."` so `git stash list`
stays readable. Use `git stash push -u` to include untracked (new) files. Don't
treat the stash as long-term storage, because it's local to your machine and is
never pushed to GitHub.
