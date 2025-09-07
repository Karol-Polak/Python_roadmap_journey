from __future__ import annotations
import time
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Callable, Any

LOG_FILE = Path("logs.txt")

def _write(line: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def log_time(fn: Callable) -> Callable:
    """Mierzy czas wykonania funkcji i loguje do pliku."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            dt = time.perf_counter() - t0
            _write(f"[{datetime.now().isoformat(timespec='seconds')}] {fn.__name__} took {dt:.6f}s")
    return wrapper

def log_calls(fn: Callable) -> Callable:
    """Loguje nazwę funkcji, argumenty i wynik."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        _write(f"CALL {fn.__name__} args={args} kwargs={kwargs}")
        result = fn(*args, **kwargs)
        _write(f"RET  {fn.__name__} -> {result!r}")
        return result
    return wrapper

# --- DEMO ---
@log_time
def slow_add(a: int, b: int) -> int:
    time.sleep(0.2)
    return a + b

@log_calls
@log_time
def greet(name: str) -> str:
    return f"Cześć, {name}!"

def demo():
    print("slow_add:", slow_add(2, 3))
    print("greet:", greet("Karol"))
    print(f"Log zapisany w {LOG_FILE.resolve()}")

if __name__ == "__main__":
    demo()
