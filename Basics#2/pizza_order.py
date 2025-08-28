MENU = {
    'Margherita': 20,
    'Pepperoni': 25,
    'Hawajska': 100,
    'Vesuvio': 35,
}

TOPPINGS = {
    'ser': 3,
    'papryka': 4,
    'oliwki': 15,
    'pieczarki': 6,
    'szynka': 5,
}

def show_menu():
    print("\n Menu Pizza:")
    for i, (name, price) in enumerate(MENU.items(), 1):
        print(f"{i}. {name} - {price} zł")

def show_toppings():
    print("\n Menu Toppings:")
    for i, (name, price) in enumerate(TOPPINGS.items(), 1):
        print(f"{i}. {name} - {price} zł")

def order_pizza():
    show_menu()
    try:
        choice = int(input("Wybierz pizze (numer): "))
        if not (1 <= choice <= len(MENU)):
            print("Zły numer pizzy!")
            return None
    except ValueError:
        print("Podaj liczbę")
        return None

    pizza_name = list(MENU.keys())[choice - 1]
    price = MENU[pizza_name]

    toppings = set()
    show_toppings()
    raw = input("Wybierz numery dodatków (oddzielone spacją, Enter = brak): ")
    for r in [x for x in raw.split()]:
        try:
            idx = int(r)
            if 1 <= idx <= len(TOPPINGS):
                toppings_name = list(TOPPINGS.keys())[idx - 1]
                toppings.add(toppings_name)
            else:
                print(f"Nie ma dodatku {idx}")
        except ValueError:
            print(f"{r!r} to nie liczba")

    return {"pizza": pizza_name, "toppings": tuple(toppings), "price": price + sum(TOPPINGS[e] for e in toppings)}


def main():
    order_list = []
    while True:
        print("\n   MENU   ")
        print("[1] Zamów pizze\n[2] Pokaż rachunek\n[3] Wyjdź")
        try:
            choice = int(input("> "))
        except ValueError:
            print("Podaj numer 1-3")
            continue

        if choice == 1:
            order = order_pizza()
            if order:
                order_list.append(order)
                print(
                    f"Dodano {order['pizza']} + {', '.join(order['toppings']) if order['toppings'] else 'bez dodatków'}")
        elif choice == 2:
            if not order_list:
                print("Brak zamówień.")
            else:
                total = sum(o["price"] for o in order_list)
                print("\nRachunek:")
                for i, o in enumerate(order_list, 1):
                    print(
                        f"{i}. {o['pizza']} + {', '.join(o['toppings']) if o['toppings'] else 'bez dodatków'} -> {o['price']} zł")
                print(f"--- Razem: {total} zł ---")
        elif choice == 3:
            print("Smacznego!")
            break
        else:
            print("Podaj numer 1–3.")

if __name__ == "__main__":
    main()