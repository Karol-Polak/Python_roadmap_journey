from __future__ import annotations
import re
from typing import Iterator

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$")

def is_adult(user: dict) -> bool:
    """Pełnoletni"""
    return int(user.get("age", 0)) >= 18

def valid_email(user: dict) -> bool:
    email = (user.get("email") or "").strip()
    return bool(EMAIL_RE.match(email))

class UserNameIterator:
    """Iterator zwracający same imiona/nazwy użytkowników."""
    def __init__(self, users: list[dict]):
        self._users = users
        self._i = 0

    def __iter__(self) -> "UserNameIterator":
        return self

    def __next__(self) -> str:
        if self._i >= len(self._users):
            raise StopIteration
        name = self._users[self._i].get("name", "")
        self._i += 1
        return name

# --- DEMO ---
def demo():
    users = [
        {"name": "Anna", "email": "anna@example.com", "age": 22},
        {"name": "Jan", "email": "invalid@", "age": 17},
        {"name": "Marta", "email": "marta.dev@company.io", "age": 19},
        {"name": "Piotr", "email": "piotr@site", "age": 30},
    ]

    # 1) filtrowanie dorosłych z użyciem lambda
    adults = list(filter(lambda u: int(u.get("age", 0)) >= 18, users))
    print("Dorośli:", [u["name"] for u in adults])

    # 2) walidacja emaili regexem
    valid = [u["name"] for u in users if valid_email(u)]
    print("Poprawne e-maile:", valid)

    # 3) iterator po nazwach użytkowników
    print("Iteracja po imionach:", list(UserNameIterator(users)))

if __name__ == "__main__":
    demo()
