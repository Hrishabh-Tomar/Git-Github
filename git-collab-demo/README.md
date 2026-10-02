# Git Collab Demo

A minimal project folder used to demonstrate a two-developer Git/GitHub workflow:
cloning, branching, pushing, pull requests, code review, and merging.

## Roles in this demo

- **Developer A** created this folder and the initial project skeleton, committed
  directly to `main`.
- **Developer B** cloned the repository, built a feature on a branch, pushed
  it, and opened a Pull Request for review.

## Project

A tiny command-line calculator (`calculator.py`), added by Developer B, with
unit tests in `test_calculator.py`.

## Running

```bash
python git-collab-demo/calculator.py
```

## Testing

```bash
cd git-collab-demo
python -m unittest -v
```
