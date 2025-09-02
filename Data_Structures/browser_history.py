from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class BrowserHistory:
    """Historia przeglądarki oparta o dwa stosy (back/forward)."""
    _back: List[str] = field(default_factory=list)
    _forward: List[str] = field(default_factory=list)
    _current: str = "about:blank"

    @property
    def current(self) -> str:
        return self._current

    def visit(self, url: str) -> None:
        """Wejście na nowy adres – obecny trafia na stos 'back', 'forward' czyścimy."""
        self._back.append(self._current)
        self._current = url
        self._forward.clear()

    def back(self) -> bool:
        """Cofnij o jedną stronę. Zwraca True jeśli się udało."""
        if not self._back:
            return False
        self._forward.append(self._current)
        self._current = self._back.pop()
        return True

    def forward(self) -> bool:
        """Do przodu o jedną stronę. Zwraca True jeśli się udało."""
        if not self._forward:
            return False
        self._back.append(self._current)
        self._current = self._forward.pop()
        return True

    def can_back(self) -> bool:
        return bool(self._back)

    def can_forward(self) -> bool:
        return bool(self._forward)

    def __repr__(self) -> str:
        return f"BrowserHistory(current={self._current!r}, back={self._back}, fwd={list(reversed(self._forward))})"


def demo_cli() -> None:
    """Prosty interfejs tekstowy do zabawy."""
    h = BrowserHistory()
    print("Browser History (stack) – wpisz: visit <url> | back | forward | show | quit")
    print("Start:", h.current)
    while True:
        cmd = input("> ").strip()
        if not cmd:
            continue
        if cmd == "quit":
            break
        if cmd.startswith("visit "):
            h.visit(cmd.split(" ", 1)[1])
        elif cmd == "back":
            print("OK" if h.back() else "Nie można cofnąć")
        elif cmd == "forward":
            print("OK" if h.forward() else "Nie można iść do przodu")
        elif cmd == "show":
            print(h)
        else:
            print("Nieznana komenda")
        print("⟶", h.current)


if __name__ == "__main__":
    demo_cli()
