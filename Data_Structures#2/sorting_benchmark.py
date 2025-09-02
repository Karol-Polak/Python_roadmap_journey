from __future__ import annotations
from typing import List
import random
import time

# --- implementacje sortowań ---

def bubble_sort(a: List[int]) -> List[int]:
    arr = a[:]
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def insertion_sort(a: List[int]) -> List[int]:
    arr = a[:]
    for i in range(1, len(arr)):
        x = arr[i]; j = i - 1
        while j >= 0 and arr[j] > x:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = x
    return arr

def merge_sort(a: List[int]) -> List[int]:
    arr = a[:]
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    # merge
    out: List[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out

def quick_sort(a: List[int]) -> List[int]:
    arr = a[:]
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    less  = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)

# --- benchmark ---

SORTS = {
    "bubble": bubble_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
}

def benchmark(n: int = 10_000, seed: int = 42) -> dict[str, float]:
    rng = random.Random(seed)
    data = [rng.randint(0, 1_000_000) for _ in range(n)]
    timings: dict[str, float] = {}
    for name, fn in SORTS.items():
        start = time.perf_counter()
        out = fn(data)
        dur = time.perf_counter() - start
        assert out == sorted(data)
        timings[name] = dur
    return timings


def demo() -> None:
    for n in (1_000, 5_000, 10_000):
        t = benchmark(n=n)
        print(f"\nN={n}")
        for k, v in sorted(t.items(), key=lambda x: x[1]):
            print(f"{k:<9} {v:.4f}s")

if __name__ == "__main__":
    demo()
