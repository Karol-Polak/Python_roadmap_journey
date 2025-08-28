QUESTIONS = [
    {"q": "Co zwraca len('abc')?", "ans": ["2", "3", "4"], "correct": 2},
    {"q": "Jaki typ ma {'a':1}?", "ans": ["list", "set", "dict"], "correct": 3},
]

def ask(q):
    print(q["q"])
    for i, a in enumerate(q["ans"], 1):
        print(f"  {i}) {a}")

    while True:
        raw = input("> ".strip())
        if not raw:
            print("Podaj numer odpowiedzi (1-{0})".format(len(q["ans"])))
            continue
        try:
            pick = int(raw)
        except ValueError:
            print("To nie jest liczba, podaj liczbę 1-{0}".format(len(q["ans"])))
            continue
        if 1 < pick <= len(q["ans"]):
            return pick == q["correct"]
        else:
            print("Poza zakresem. Wpisz 1-{0}".format(len(q["ans"])))

def main():
    score = sum(1 for q in QUESTIONS if ask(q))
    print(f"Wynik: {score}/{len(QUESTIONS)}")

if __name__ == "__main__":
    main()
