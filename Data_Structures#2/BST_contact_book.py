from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Iterator, Any


@dataclass
class Contact:
    name: str
    email: str = ""
    phone: str = ""


class _Node:
    __slots__ = ("key", "value", "left", "right")

    def __init__(self, key: str, value: Contact):
        self.key = key.lower()
        self.value: Contact = value
        self.left: Optional[_Node] = None
        self.right: Optional[_Node] = None


class ContactBST:
    """
    książka kontaktów na bazie BST (Binary Search Tree)
    operacje: insert / get / delete / inorder
    """

    def __init__(self) -> None:
        self._root: Optional[_Node] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def insert(self, contact: Contact) -> None:
        def _insert(node: Optional[_Node], key: str, value: Contact) -> _Node:
            if node is None:
                self._size += 1
                return _Node(key, value)
            if key < node.key:
                node.left = _insert(node.left, key, value)
            elif key > node.key:
                node.right = _insert(node.right, key, value)
            else:
                node.value = value
            return node

        self._root = _insert(self._root, contact.name.lower(), contact)

    def get(self, name: str) -> Optional[Contact]:
        key = name.lower()
        cur = self._root
        while cur:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return cur.value
        return None

    def delete(self, name: str) -> bool:
        deleted = False

        def _min_node(n: _Node) -> _Node:
            while n.left:
                n = n.left
            return n

        def _delete(node: Optional[_Node], key: str) -> Optional[_Node]:
            nonlocal deleted
            if node is None:
                return None
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                deleted = True
                if node.left is None:
                    self._size -= 1
                    return node.right
                if node.right is None:
                    self._size -= 1
                    return node.left
                succ = _min_node(node.right)
                node.key, node.value = succ.key, succ.value
                node.right = _delete(node.right, succ.key)
            return node

        self._root = _delete(self._root, name.lower())
        return deleted

    def inorder(self) -> Iterator[Contact]:
        def _walk(n: Optional[_Node]) -> Iterator[Contact]:
            if not n:
                return
            yield from _walk(n.left)
            yield n.value
            yield from _walk(n.right)
        return _walk(self._root)

    def to_list(self) -> list[Contact]:
        return list(self.inorder())


def demo() -> None:
    book = ContactBST()
    book.insert(Contact("Anna", "anna@example.com", "123924924"))
    book.insert(Contact("Bartek", "bartek@example.com", "123421124"))
    book.insert(Contact("Zenon", phone="123456789"))
    book.insert(Contact("Ola", email="ola@example.pl"))

    print("Lista alfabetyczna:")
    for c in book.inorder():
        print(f"- {c.name} ({c.email or '-'} / {c.phone or '-'})")

    print("Szukaj 'zenon' ->", book.get("zenon"))
    print("Usuń 'Bartek' ->", book.delete("bartek"))
    print("Po usunięciu:", [c.name for c in book.inorder()])


if __name__ == "__main__":
    demo()
