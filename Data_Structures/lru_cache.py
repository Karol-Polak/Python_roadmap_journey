from __future__ import annotations
from typing import Any, Dict, Optional

class _Node:
    __slots__ = ("k", "v", "prev", "next")
    def __init__(self, k: Any, v: Any):
        self.k = k; self.v = v
        self.prev: Optional[_Node] = None
        self.next: Optional[_Node] = None

class LRUCache:
    """
    LRU Cache implementation.
    Stała złożoność operacji O(1):
        - hash map: klucz -> węzeł,
        - podwójnie wiązana lista: kolejność użycia (head <-> ... <-> tail)
    Najnowszy element -> head, najstarszy element -> tail
    """
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.cap = capacity
        self.map: Dict[Any, _Node] = {}
        self.head = _Node(None, None)
        self.tail = _Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_front(self, n: _Node) -> None:
        n.prev = self.head
        n.next = self.head.next
        self.head.next.prev = n
        self.head.next = n

    def _remove(self, n: _Node) -> None:
        n.prev.next = n.next
        n.next.prev = n.prev
        n.prev = n.next = None

    def _move_to_front(self, n: _Node) -> None:
        self._remove(n)
        self._add_front(n)

    def get(self, k: Any) -> Any:
        n = self.map.get(k)
        if not n:
            return None
        self._move_to_front(n)
        return n.v

    def put(self, k: Any, v: Any) -> None:
        n = self.map.get(k)
        if n:
            n.v = v
            self._move_to_front(n)
            return
        if len(self.map) == self.cap:
            lru = self.tail.prev
            self._remove(lru)
            self.map.pop(lru.k, None)
        n = _Node(k, v)
        self.map[k] = n
        self._add_front(n)

    def __len__(self) -> int:
        return len(self.map)

    def __contains__(self, k: Any) -> bool:
        return k in self.map

    def clear(self) -> None:
        self.map.clear()
        self.head.next = self.tail
        self.tail.prev = self.head


def demo():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    print(c.get("a"))
    c.put("c", 3)
    print("b" in c)
    print(c.get("a"))

if __name__ == "__main__":
    demo()
