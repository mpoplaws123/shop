# ✅ KLASA ZADANIE
class Zadanie:
    def __init__(self, opis, status=False):
        self.opis = opis
        self.status = status

    def oznacz_jako_zrobione(self):
        self.status = True

    def __str__(self):
        znak = "[x]" if self.status else "[ ]"
        return f"{znak} {self.opis}"


# ✅ LISTA ZADAŃ
zadania = []


# ✅ FUNKCJE
def dodaj_zadanie():
    opis = input("Podaj treść zadania: ")
    zadania.append(Zadanie(opis))
    print("✅ Zadanie dodane!")

def wypisz_zadania():
    if not zadania:
        print("Brak zadań!")
    else:
        for i, zad in enumerate(zadania, 1):
            print(f"{i}. {zad}")

def oznacz_jako_zrobione():
    wypisz_zadania()
    try:
        nr = int(input("Które zadanie oznaczyć jako zrobione? (numer): "))
        if 1 <= nr <= len(zadania):
            zadania[nr - 1].oznacz_jako_zrobione()
            print("✅ Oznaczono jako zrobione!")
        else:
            print("Nie ma takiego zadania.")
    except ValueError:
        print("Podaj numer!")

def zapisz_do_pliku():
    with open("todo.txt", "w", encoding="utf-8") as plik:
        for zad in zadania:
            status = "1" if zad.status else "0"
            plik.write(f"{status}|{zad.opis}\n")

def wczytaj_z_pliku():
    try:
        with open("todo.txt", "r", encoding="utf-8") as plik:
            for linia in plik:
                status, opis = linia.strip().split("|")
                zadania.append(Zadanie(opis, status == "1"))
    except FileNotFoundError:
        pass  # pierwszy raz uruchamiany — brak pliku


# ✅ PĘTLA MENU
def menu():
    wczytaj_z_pliku()

    while True:
        print("\n--- MENU ---")
        print("1. Dodaj zadanie")
        print("2. Pokaż zadania")
        print("3. Oznacz jako zrobione")
        print("4. Zapisz i wyjdź")

        wybor = input("Wybór: ")

        if wybor == "1":
            dodaj_zadanie()
        elif wybor == "2":
            wypisz_zadania()
        elif wybor == "3":
            oznacz_jako_zrobione()
        elif wybor == "4":
            zapisz_do_pliku()
            print("✅ Zapisano do pliku. Do zobaczenia!")
            break
        else:
            print("Nieprawidłowa opcja!")


# ✅ START PROGRAMU
menu()
