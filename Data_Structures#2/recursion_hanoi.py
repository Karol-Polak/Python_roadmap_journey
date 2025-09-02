from __future__ import annotations
from typing import List, Tuple

Move = Tuple[str, str]

def hanoi(n: int, src: str = "A", aux: str = "B", dst: str = "C") -> List[Move]:
    """Zwraca listę ruchów do przeniesienia n krążków z src -> dst."""
    if n < 0:
        raise ValueError("n must be >= 0")
    moves: List[Move] = []

    def _solve(k: int, a: str, b: str, c: str) -> None:
        if k == 0:
            return
        _solve(k - 1, a, c, b)
        moves.append((a, c))
        _solve(k - 1, b, a, c)

    _solve(n, src, aux, dst)
    return moves


def demo(n: int = 3) -> None:
    m = hanoi(n)
    print(f"Liczba ruchów: {len(m)} (oczekiwane: {2**n - 1})")
    for i, (a, c) in enumerate(m, 1):
        print(f"{i:>3}: {a} -> {c}")


if __name__ == "__main__":
    demo(4)
