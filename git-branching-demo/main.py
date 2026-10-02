"""Ties the three merged features together."""

from app import APP_NAME
from dashboard import render_dashboard
from login import login
from profile import build_profile


def main():
    print(APP_NAME)
    if login("ada", "lovelace123"):
        profile = build_profile("ada", "ada@example.com")
        print(render_dashboard(profile["username"], ["Welcome back!"]))


if __name__ == "__main__":
    main()
