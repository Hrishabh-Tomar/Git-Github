# Git Merge Conflict Demo

Two branches change the **same line** of the same file differently, so the second
merge into `main` conflicts. The conflict is then resolved by hand and committed.

## What happened (real history in this repo)

```text
*   293dfde Merge feature/greeting-friendly into main, resolving greeting conflict
|\
| * 82433b8 Make greeting casual and friendly      (feature/greeting-friendly)
* |   1ff825a Merge feature/greeting-welcome into main
|\ \
| |/
| * 16c9884 Make greeting a formal welcome         (feature/greeting-welcome)
|/
* 7ce732c Add git-merge-conflict-demo: base greeting module   <- common base
```

1. **Same base.** Both branches were created from `7ce732c`, where `greet()` returns
   `f"Hello, {name}"`.
2. **Same line, different edits.**
   - `feature/greeting-welcome`: `return f"Welcome, {name}!"`
   - `feature/greeting-friendly`: `return f"Hey {name}, nice to see you."`
3. **First merge is clean.** `git merge --no-ff feature/greeting-welcome` into `main`.
4. **Second merge conflicts.** `git merge --no-ff feature/greeting-friendly`:

   ```text
   Auto-merging git-merge-conflict-demo/greeting.py
   CONFLICT (content): Merge conflict in git-merge-conflict-demo/greeting.py
   Automatic merge failed; fix conflicts and then commit the result.
   ```

   `git status` shows `UU greeting.py` (both modified).

## Reading the conflict markers

```python
def greet(name):
<<<<<<< HEAD
    return f"Welcome, {name}!"
=======
    return f"Hey {name}, nice to see you."
>>>>>>> feature/greeting-friendly
```

- `<<<<<<< HEAD` to `=======` is **your side**: what `main` already has.
- `=======` to `>>>>>>> feature/greeting-friendly` is the **incoming side**.
- Git can't tell which is right, because both changed the same line from the same
  base, so it stops and asks.

## Deciding what to keep

Neither change was wrong; they had different goals. `main` already had the formal
"Welcome, {name}!", and the incoming branch added warmth with "nice to see you".
Rather than discard one, the resolution keeps both ideas:

```python
return f"Welcome, {name}! Nice to see you."
```

Steps: edit the file, delete all three marker lines, run the tests, then:

```bash
git add git-merge-conflict-demo/greeting.py
git commit        # completes the merge as a two-parent commit
```

A test (`test_greet_keeps_both_branches_wording`) locks in the resolved behavior.

## Run it yourself

```bash
cd git-merge-conflict-demo
python conflict_demo.py     # replays the whole conflict in a temp repo, prints the markers, asserts each step
python -m unittest -v       # greeting tests + the conflict replay test
```

The final files contain no markers (that's the point of resolving), so
`conflict_demo.py` is the runnable proof that the conflict occurred.
