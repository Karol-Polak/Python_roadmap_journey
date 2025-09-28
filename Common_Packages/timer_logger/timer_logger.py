# context_manager/timer_logger.py
from __future__ import annotations
from pathlib import Path
from time import perf_counter, sleep
from functools import wraps
from typing import Callable

class Timer:
    """CM mierzący czas bloku; wynik w atrybucie .elapsed."""
    def __enter__(self):
        self._t0 = perf_counter()
        return self
    def __exit__(self, exc_type, exc, tb):
        self.elapsed = perf_counter() - self._t0
        return False  # nie tłumimy wyjątków

class LogFile:
    """CM logujący start/stop/wyjątki do pliku."""
    def __init__(self, path: str | Path = "logs.txt"):
        self.path = Path(path)
        self.fh = None
    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fh = self.path.open("a", encoding="utf-8")
        self.fh.write("---- BEGIN ----\n")
        return self.fh
    def __exit__(self, exc_type, exc, tb):
        if exc:
            self.fh.write(f"ERROR: {exc}\n")
        self.fh.write("----- END -----\n")
        self.fh.close()
        return False

def timeit(fn: Callable) -> Callable:
    """Dekorator używający Timer pod spodem."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with Timer() as t:
            result = fn(*args, **kwargs)
        print(f"{fn.__name__} took {t.elapsed:.4f}s")
        return result
    return wrapper

@timeit
def slow_sum(n: int) -> int:
    """Udaje wolne obliczenie."""
    total = 0
    for i in range(n):
        total += i
        if i % (n // 10 + 1) == 0:
            sleep(0.01)
    return total

def demo():
    print("— Timer + LogFile demo —")
    with LogFile("logs.txt") as log, Timer() as t:
        log.write("Doing some work...\n")
        val = slow_sum(50_000)
        log.write(f"Result = {val}\n")
    print(f"Block took {t.elapsed:.4f}s; logs → {Path('logs.txt').resolve()}")

if __name__ == "__main__":
    demo()
