"""Profile feature."""


def build_profile(username, email):
    if "@" not in email:
        raise ValueError("Invalid email address.")
    return {"username": username, "email": email}
