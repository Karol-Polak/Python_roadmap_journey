UNITS = {
    'm': 1.0, 'cm': 0.01, 'mm': 0.001,
    'km': 1000.0, 'in': 0.0254, 'ft': 0.3048
}
VALID = set(UNITS)

def safe_float(s: str) -> float:
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"Nieprawidłowa liczba: {s!r}")

def convert(value: float, src: str, dst: str) -> float:
    if src not in VALID or dst not in VALID:
        raise ValueError(f"Dozwolone jednostki to: {sorted(VALID)}")
    return value * UNITS[src] / UNITS[dst]

def main():
    raw = input("Podaj wartość do konwersji, jednostkę źródłową i jednostkę docelową (np. '12 cm m'): ")
    try:
        val_s, src, dst = raw.split()
        val = safe_float(val_s)
        print(round(convert(val, src, dst), 6))
    except Exception as e:
        print("Błąd ", e)

if __name__ == "__main__":
    main()

