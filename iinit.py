# class zwierze:
#     def __init__(self, gatunek, wiek):
#         self.gatunek = gatunek
#         self.wiek = wiek

#     def opis(self):
#         print(f"masz {self.gatunek} i ma taki wiek: {self.wiek} ")


# zoo = zwierze("pies", 5 )
# zoo.opis()


# class Osoba:
#     def __init__(self, imie, wiek):
#         self.imie = imie
#         self.wiek = wiek

# czlowiek = Osoba("Bartek", 20)


# class auto:
#     def __init__(self, marka, model):
#         self.marka = marka
#         self.model = model

#     def opis(self):
#         print(f"Mamy {self.model} o takiej marce: {self.model}")

# auto1 = auto("AUDI", "a3")        

# auto1.opis()



# class zoo:
#     def __init__(self, gatunek, wiek):
#         self.gatunek = gatunek
#         self.wiek = wiek

#     def opis(self):
#         print(f"zwierze: {self.gatunek} wiek: {self.wiek}")



# zwierze1 = zoo("pies", 8) 

# zwierze1.opis()

# class uczen:
#     def __init__(self, imie, wiek, ocena_koncowa):
#         self.imie = imie
#         self.wiek = wiek
#         self.ocena_koncowa = ocena_koncowa

#     def opis(self):
#         print(f"Uczen: {self.imie} | wiek: {self.wiek} | ocena_konc: {self.ocena_koncowa}")


# uczen1 = uczen("Maciej" , 23 , 5 )

# uczen1.opis()



# class GraKomputerowa:
#     def __init__(self, tytul, gatunek, ocena):
#         self.tytul = tytul
#         self.gatunek = gatunek
#         self.ocena = ocena

#     def opis(self):
#         print(f"GRA:{self.tytul} | gatunek: {self.gatunek} | ocena: {self.ocena}")


# gra1 = GraKomputerowa("Minecraft", "sandbox", 9)

# gra1.opis()




# class film:
#     def __init__(self, tytul, rok, ocena):
#         self.tytul = tytul
#         self.rok = rok
#         self.ocena = ocena

#     def opis(self):
#         print(f"film: {self.tytul} | rok: {self.rok} | ocena: {self.ocena}  ")


#     def czy_hit(self) :
#         if self.ocena >= 5.0:
#             return "jest git"
#         else:
#             return "słabe gówno"
        

# film1 = film("matrix", 2024, 9.10)
# film1.opis()
# film1.czy_hit()
# print(film1.czy_hit())