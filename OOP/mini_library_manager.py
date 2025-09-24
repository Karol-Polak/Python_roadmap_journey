from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator, Optional, Protocol, runtime_checkable, Any
from datetime import datetime
from abc import ABC, abstractmethod

# Wyjątki domenowe
class DomainError(Exception): ...
class ItemNotFound(DomainError): ...
class ItemNotAvailable(DomainError): ...

# Mixiny / Value objects
class TimestampedMixin:
    created_at: datetime
    updated_at: datetime
    def _init_timestamps(self) -> None:
        now = datetime.now()
        self.created_at = now
        self.updated_at = now
    def touch(self) -> None:
        self.updated_at = datetime.now()

# Notifier (Protocol)
@runtime_checkable
class Notifier(Protocol):
    def notify(self, user_email: str, message: str) -> None: ...

class EmailNotifier:
    def notify(self, user_email: str, message: str) -> None:
        print(f"[to:{user_email}] {message}")


# Użytkownicy / Autorzy
@dataclass(frozen=True, slots=True, order=True)
class User:
    email: str
    name: str
    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"

@dataclass(frozen=True, slots=True)
class Author:
    name: str


# MediaItem (ABC) + dziedziczenie
class MediaItem(ABC, TimestampedMixin):
    def __init__(self, title: str, year: int) -> None:
        self._init_timestamps()
        self.title = title
        self.year = year  # walidacja w property

    @property
    def year(self) -> int:
        return self._year
    @year.setter
    def year(self, value: int) -> None:
        if value < 1440 or value > datetime.now().year + 1:
            raise ValueError("Invalid publication year")
        self._year = value
        self.touch()

    @abstractmethod
    def can_borrow(self) -> bool: ...
    @abstractmethod
    def borrow(self, user: User) -> None: ...
    @abstractmethod
    def give_back(self, user: User) -> None: ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(title={self.title!r}, year={self.year})"
    def __str__(self) -> str:
        return f"{self.title} ({self.year})"
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, MediaItem) and (self.title, self.year, type(self)) == (other.title, other.year, type(other))
    def __hash__(self) -> int:
        return hash((self.title, self.year, type(self)))

class Book(MediaItem):
    def __init__(self, title: str, year: int, author: Author, copies: int = 1) -> None:
        super().__init__(title, year)
        self.author = author
        self._copies = copies
    @property
    def copies(self) -> int:
        return self._copies
    @copies.setter
    def copies(self, n: int) -> None:
        if n < 0: raise ValueError("Copies cannot be negative")
        self._copies = n; self.touch()
    def can_borrow(self) -> bool:
        return self._copies > 0
    def borrow(self, user: User) -> None:
        if not self.can_borrow(): raise ItemNotAvailable(f"No copies left for {self.title}")
        self._copies -= 1; self.touch()
    def give_back(self, user: User) -> None:
        self._copies += 1; self.touch()

class EBook(MediaItem):
    def __init__(self, title: str, year: int, author: Author) -> None:
        super().__init__(title, year)
        self._active: set[str] = set()
    def can_borrow(self) -> bool:
        return True
    def borrow(self, user: User) -> None:
        self._active.add(user.email); self.touch()
    def give_back(self, user: User) -> None:
        self._active.discard(user.email); self.touch()
    @property
    def active_readers(self) -> int:
        return len(self._active)

class Magazine(MediaItem):
    def __init__(self, title: str, year: int, issue_no: int, copies: int = 1) -> None:
        super().__init__(title, year)
        self.issue_no = issue_no
        self._copies = copies
    def can_borrow(self) -> bool:
        return self._copies > 0
    def borrow(self, user: User) -> None:
        if not self.can_borrow(): raise ItemNotAvailable(f"Issue {self.issue_no} unavailable")
        self._copies -= 1; self.touch()
    def give_back(self, user: User) -> None:
        self._copies += 1; self.touch()


# Loan + LoanSession (context manager)
@dataclass(slots=True)
class Loan:
    item: MediaItem
    user: User
    start: datetime = field(default_factory=datetime.now)
    end: Optional[datetime] = None
    def close(self) -> None:
        self.end = datetime.now()

class LoanSession:
    """Grupuje operacje wypożyczeń/zwrotów; rollback w razie błędu."""
    def __init__(self, catalog: "Catalog", notifier: Optional[Notifier] = None) -> None:
        self.catalog = catalog
        self.notifier = notifier or EmailNotifier()
        self._ops: list[tuple[str, MediaItem, User]] = []
    def __enter__(self) -> "LoanSession":
        return self
    def borrow(self, item_id: str, user: User) -> None:
        item = self.catalog[item_id]
        item.borrow(user)
        self.catalog._loans.append(Loan(item, user))
        self._ops.append(("borrow", item, user))
        self.notifier.notify(user.email, f"Wypożyczono: {item}")
    def give_back(self, item_id: str, user: User) -> None:
        item = self.catalog[item_id]
        item.give_back(user)
        for loan in reversed(self.catalog._loans):
            if loan.item is item and loan.user == user and loan.end is None:
                loan.close(); break
        self._ops.append(("give_back", item, user))
        self.notifier.notify(user.email, f"Zwrócono: {item}")
    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is None:
            return False
        for op, item, user in reversed(self._ops):
            try:
                (item.give_back if op == "borrow" else item.borrow)(user)
            except Exception:
                pass
        print("❗️Session rolled back due to error:", exc)
        return False


# Catalog – kolekcja dunder + wyszukiwanie
class Catalog(Iterable[MediaItem]):
    def __init__(self) -> None:
        self._items: Dict[str, MediaItem] = {}
        self._loans: list[Loan] = []
    def __len__(self) -> int:
        return len(self._items)
    def __contains__(self, item_id: str) -> bool:
        return item_id in self._items
    def __iter__(self) -> Iterator[MediaItem]:
        return iter(self._items.values())
    def __getitem__(self, item_id: str) -> MediaItem:
        try: return self._items[item_id]
        except KeyError: raise ItemNotFound(item_id)
    def add(self, item_id: str, item: MediaItem) -> None:
        if item_id in self._items: raise DomainError(f"Duplicate id: {item_id}")
        self._items[item_id] = item
    def remove(self, item_id: str) -> None:
        if item_id not in self._items: raise ItemNotFound(item_id)
        del self._items[item_id]
    def search(self, phrase: str) -> Iterator[tuple[str, MediaItem]]:
        p = phrase.lower().strip()
        for iid, item in self._items.items():
            if p in item.title.lower():
                yield iid, item
    def active_loans(self) -> list[Loan]:
        return [l for l in self._loans if l.end is None]


# DEMO
def demo() -> None:
    catalog = Catalog()
    tolkien = Author("J.R.R. Tolkien")
    knuth = Author("Donald E. Knuth")

    catalog.add("B001", Book("The Hobbit", 1937, tolkien, copies=2))
    catalog.add("B002", Book("The Art of Computer Programming", 1968, knuth, copies=1))
    catalog.add("E001", EBook("Clean Architecture (eBook)", 2017, Author("Robert C. Martin")))
    catalog.add("M001", Magazine("Python Monthly", 2025, issue_no=9, copies=3))

    anna = User(email="anna@example.com", name="Anna")
    jan = User(email="jan@example.com", name="Jan")

    print("\n— KATALOG —")
    for it in catalog:
        print(" •", it)

    print("\n— WYSZUKIWANIE 'python' —")
    for iid, it in catalog.search("python"):
        print(f" {iid}: {it}")

    print("\n— SESJA WYPOŻYCZEŃ —")
    try:
        with LoanSession(catalog) as sess:
            sess.borrow("B001", anna)  # 1/2
            sess.borrow("B001", jan)   # 0/2
            sess.borrow("B001", anna)  # -> błąd, rollback całej sesji
    except ItemNotAvailable:
        pass

    hobbit: Book = catalog["B001"]  # type: ignore
    print("Kopie 'Hobbit' po sesji:", hobbit.copies)  # 2

    print("\n— NORMALNA SESJA —")
    with LoanSession(catalog) as sess:
        sess.borrow("B001", anna)
        sess.borrow("E001", jan)
        sess.borrow("M001", anna)

    print("Aktywne wypożyczenia:", len(catalog.active_loans()))
    for loan in catalog.active_loans():
        print(" •", loan.user, "→", loan.item)

    print("\n— ZWROT —")
    with LoanSession(catalog) as sess:
        sess.give_back("B001", anna)

    print("Aktywne wypożyczenia:", len(catalog.active_loans()))
    print("Kopie 'Hobbit' teraz:", hobbit.copies)

    print("\n— DUNDERY KOLEKCJI —")
    print("Długość katalogu:", len(catalog))
    print("'B002' w katalogu?", "B002" in catalog)
    print("Pobierz item __getitem__:", catalog['B002'])

    print("\n— PROPERTY/WALIDACJA —")
    try:
        catalog["B002"].year = 1200
    except ValueError as e:
        print("Walidacja year zadziałała:", e)

    print("\n— KONIEC DEMO —")

if __name__ == "__main__":
    demo()
