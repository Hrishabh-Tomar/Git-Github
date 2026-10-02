"""Login feature."""

USERS = {"ada": "lovelace123"}


def login(username, password):
    return USERS.get(username) == password
