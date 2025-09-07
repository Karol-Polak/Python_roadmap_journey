from __future__ import annotations
import random
import string
from functools import wraps
from typing import Iterator

# --- Dekoratory walidujące ---
def validate_length(fn):
    @wraps(fn)
    def wrapper(length: int = 12, *args, **kwargs):
        if length < 8:
            raise ValueError("Password length must be >= 8")
        return fn(length, *args, **kwargs)
    return wrapper

def require_types(fn):
    @wraps(fn)
    def wrapper(length: int = 12, *, use_lower=True, use_upper=True,
                use_digits=True, use_symbols=True):
        kinds = [use_lower, use_upper, use_digits, use_symbols]
        if sum(bool(k) for k in kinds) < 2:
            raise ValueError("Enable at least two character categories")
        return fn(length, use_lower=use_lower, use_upper=use_upper,
                  use_digits=use_digits, use_symbols=use_symbols)
    return wrapper

# --- Funkcyjny generator hasła ---
@validate_length
@require_types
def generate_password(length: int = 12, *,
                      use_lower: bool = True,
                      use_upper: bool = True,
                      use_digits: bool = True,
                      use_symbols: bool = True) -> str:
    pools = []
    if use_lower:   pools.append(string.ascii_lowercase)
    if use_upper:   pools.append(string.ascii_uppercase)
    if use_digits:  pools.append(string.digits)
    if use_symbols: pools.append("!@#$%^&*()-_=+[]{};:,.?/")
    rng = random.SystemRandom()
    # co najmniej 1 znak z każdej wybranej puli
    out = [rng.choice(pool) for pool in pools]
    all_chars = "".join(pools)
    out += [rng.choice(all_chars) for _ in range(length - len(out))]
    rng.shuffle(out)
    return "".join(out)

# --- Iterator klasowy: nieskończony strumień haseł ---
class PasswordStream:
    def __init__(self, length: int = 12):
        if length < 8:
            raise ValueError("length must be >= 8")
        self.length = length
        self._rng = random.SystemRandom()
        self._chars = string.ascii_letters + string.digits

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        return "".join(self._rng.choice(self._chars) for _ in range(self.length))

# --- DEMO ---
def demo():
    print("One-off:", generate_password(12, use_symbols=False))
    print("Strong :", generate_password(16, use_symbols=True))
    print("\nStream of 3 passwords:")
    stream = PasswordStream(12)
    for i, pwd in zip(range(3), stream):
        print(f"{i+1}: {pwd}")

if __name__ == "__main__":
    demo()
