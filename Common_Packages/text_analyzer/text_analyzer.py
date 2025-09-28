# comprehensions/text_analyzer.py
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterator

WORD_RE = re.compile(r"\b\w+\b", re.UNICODE)

@dataclass
class Report:
    total_lines: int
    total_words: int
    unique_words: int
    avg_word_len: float
    top_10: list[tuple[str, int]]

def iter_words(lines: Iterator[str]) -> Iterator[str]:
    """Generator: normalizacja linii i wyciąganie słów on-the-fly."""
    normalized = (ln.strip().replace("\t", " ") for ln in lines)  # generator expression
    for line in normalized:
        for w in [w.lower() for w in WORD_RE.findall(line)]:
            yield w

def analyze(path: str | Path) -> Report:
    path = Path(path)
    with path.open("r", encoding="utf-8") as fh:
        counter: Counter[str] = Counter()
        total_len = 0
        total_words = 0
        for w in iter_words(fh):              # generator → brak alokacji dużych list
            total_words += 1
            total_len += len(w)
            counter[w] += 1

    # policz linie
    with path.open("r", encoding="utf-8") as fh2:
        total_lines = sum(1 for _ in fh2)

    unique = len(counter)
    avg = total_len / total_words if total_words else 0.0
    top10 = counter.most_common(10)
    return Report(total_lines, total_words, unique, avg, top10)

def save_report(rep: Report, out_path: str | Path) -> None:
    lines = [
        "Text Analyzer Report",
        "====================",
        f"Lines           : {rep.total_lines}",
        f"Words           : {rep.total_words}",
        f"Unique words    : {rep.unique_words}",
        f"Avg word length : {rep.avg_word_len:.2f}",
        "",
        "Top 10 words:",
        *[f"  {w:<15} {c}" for w, c in rep.top_10],  # list comprehension do formatowania
        "",
    ]
    Path(out_path).write_text("\n".join(lines), encoding="utf-8")

def demo():
    sample = Path(__file__).with_name("sample.txt")
    if not sample.exists():
        sample.write_text(
            "Python is great. Python is readable and powerful!\n"
            "Generators are memory-friendly; list comprehensions are concise.\n"
            "Context managers keep resources safe. Python, python, PYTHON.\n"
            "TAK TAK TAK TAK TAK TAK TAK TAK TAK.\n ",
            encoding="utf-8",
        )
    rep = analyze(sample)
    save_report(rep, Path(__file__).with_name("report.txt"))
    print("OK — report saved next to the script.")

if __name__ == "__main__":
    demo()
