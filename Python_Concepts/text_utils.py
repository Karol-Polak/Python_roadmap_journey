from __future__ import annotations
import re
from typing import Iterator

#REGEX
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_WORD_RE = re.compile(r"\b\w+(?:'\w+)?\b", re.UNICODE)

#zwraca listę e-mail z tekstu
def find_emails(text: str) -> list[str]:
    return [m.group(0) for m in _EMAIL_RE.finditer(text)]

#zwraca kolejne słowa z tekstu
def word_iterator(text: str) -> Iterator[str]:
    for m in _WORD_RE.finditer(text):
        yield m.group(0)


_PL_TRANSLATION = str.maketrans({
    "ą": "a", "ć": "c", "ę": "e", "ł": "l",
    "ń": "n", "ó": "o", "ś": "s", "ż": "z", "ź": "z",
    "Ą": "A", "Ć": "C", "Ę": "E", "Ł": "L",
    "Ń": "N", "Ó": "O", "Ś": "S", "Ż": "Z", "Ź": "Z",
})

#zamiana polskich znaków + białe znaki
def normalize(text: str) -> str:
    out = text.translate(_PL_TRANSLATION)
    out = re.sub(r"\s+", " ", out).strip()
    return out

#małe litery, polskie znaki, myślniki
def slugify(text: str) -> str:
    t = normalize(text).lower()
    t = re.sub(r"[^a-z0-9 -]", "", t)
    t = re.sub(r"\s+", "-", t)
    t = re.sub(r"-{2,}", "-", t).strip("-")
    return t

#generator zwracający paczki słów
def chunked_words(text: str, n: int) -> Iterator[list[str]]:
    buf: list[str] = []
    for w in word_iterator(text):
        buf.append(w)
        if len(buf) == n:
            yield buf
            buf = []
    if buf:
        yield buf


def demo():
    text = "To jest testowy tekst testowy@email.com, gdzie testujemy funkcję abcde@test.pl no i Klaudia, barbara@barbara.com"
    print("Emails: ", find_emails(text))
    print("Words: ", list(word_iterator(text)))
    print("Normalized: ", normalize("Zażółć gęślą jaźń"))
    print("Slugify: ", slugify("  Mój Pierwszy Wpis!  "))
    print("Chunked words:", list(chunked_words("To jest test chunków słów", 2)))

if __name__ == "__main__":
    demo()