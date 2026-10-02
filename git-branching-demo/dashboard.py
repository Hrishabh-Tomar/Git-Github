"""Dashboard feature."""


def render_dashboard(username, notifications):
    lines = [f"Dashboard for {username}", f"Notifications: {len(notifications)}"]
    lines += [f"  - {item}" for item in notifications]
    return "\n".join(lines)
