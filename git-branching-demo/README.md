# Git Branching Demo

A small app built from three feature branches that were each merged into `main`.

| Branch | Change | Files |
|---|---|---|
| `feature-login` | `login()` checks a username and password | `login.py`, `test_login.py` |
| `feature-profile` | `build_profile()` validates the email | `profile.py`, `test_profile.py` |
| `feature-dashboard` | `render_dashboard()` shows notifications | `dashboard.py`, `test_dashboard.py` |

## Commands used

```bash
git switch -c feature-login        # create a branch and switch to it
#   ...edit, then git add + git commit...
git switch main                    # switch back (profile and dashboard branch from main too)
git switch -c feature-profile
git switch main
git switch -c feature-dashboard
git push origin feature-login feature-profile feature-dashboard   # push every branch

git switch main
git merge --no-ff feature-login     # --no-ff keeps a visible merge commit
git merge --no-ff feature-profile
git merge --no-ff feature-dashboard

git branch -d feature-login feature-profile feature-dashboard     # delete merged branches locally
git log --oneline --graph --all     # final history
```

`git branch -d` is the safe delete: it refuses to delete a branch that isn't merged.
The three branches were deleted locally, but their copies on GitHub
(`origin/feature-login`, `origin/feature-profile`, `origin/feature-dashboard`)
are kept so the branch history stays visible.

## Final history

```text
* 98ecd92 Add main.py combining login, profile and dashboard
*   c35f8e1 Merge feature-dashboard into main
|\
| * f042853 Add dashboard feature
* |   997c0cc Merge feature-profile into main
|\ \
| * | b742776 Add profile feature
| |/
* |   b06f494 Merge feature-login into main
|\ \
| |/
| * 455fcae Add login feature
|/
* 18029b2 Add git-branching-demo: base app on main
```

## Run

```bash
cd git-branching-demo
python main.py
python -m unittest -v
```
