from abc import ABC, abstractmethod

class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar  # Az ár
        self.szobaszam = szobaszam  # A szobaszám

    @abstractmethod
    def get_tipus(self):
        pass  # Absztrakt metódus, amit a származtatott osztályoknak kell implementálni

class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar, szobaszam)
        self.tipus = "Egyágyas"

    def get_tipus(self):
        return self.tipus  # Visszaadja a szoba típusát

class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar, szobaszam)
        self.tipus = "Kétágyas"

    def get_tipus(self):
        return self.tipus  # Visszaadja a szoba típusát

class Szalloda:
    def __init__(self, nev):
        self.nev = nev  # A szálloda neve
        self.szobak = []  # A szállodában található szobák listája

    def szoba_hozzaadasa(self, szoba):
        self.szobak.append(szoba)  # Hozzáad egy szobát a szállodához

    def foglalas(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                if not hasattr(szoba, 'foglalasok'):
                    szoba.foglalasok = []  # Ha a szobának még nincs foglalása, hozzunk létre egy üres listát
                for foglalas in szoba.foglalasok:
                    if foglalas.datum == datum:
                        return False  # A szoba már foglalt ezen a napon
                uj_foglalas = Foglalas(szoba, datum)
                szoba.foglalasok.append(uj_foglalas)  # Hozzáadjuk az új foglalást a szoba foglalásaihoz
                return True  # Sikeres foglalás
        return False  # Nem találtuk a szobát

    def foglalas_ar(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                if not hasattr(szoba, 'foglalasok'):
                    szoba.foglalasok = []
                for foglalas in szoba.foglalasok:
                    if foglalas.datum == datum:
                        return False, None  # A szoba már foglalt ezen a napon
                uj_foglalas = Foglalas(szoba, datum)
                szoba.foglalasok.append(uj_foglalas)
                return True, szoba.ar  # Sikeres foglalás és visszaadja a szoba árát
        return False, None  # Nem találtuk a szobát

    def foglalas_lemondasa(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam and hasattr(szoba, 'foglalasok'):
                for foglalas in szoba.foglalasok:
                    if foglalas.datum == datum:
                        szoba.foglalasok.remove(foglalas)  # Eltávolítjuk a foglalást a listából
                        return True  # Sikeres lemondás
        return False  # Nem találtuk a foglalást

    def foglalasok_listazasa(self):
        osszes_foglalas = []
        for szoba in self.szobak:
            if hasattr(szoba, 'foglalasok'):
                for foglalas in szoba.foglalasok:
                    osszes_foglalas.append(f"Szoba {szoba.szobaszam}, Dátum: {foglalas.datum}")
        return osszes_foglalas  # Visszaadja az összes foglalást

    def szabad_szobak(self, datum):
        szabad_szobak = []
        for szoba in self.szobak:
            if not hasattr(szoba, 'foglalasok'):
                szabad_szobak.append(szoba.szobaszam)
            else:
                foglalt = False
                for foglalas in szoba.foglalasok:
                    if foglalas.datum == datum:
                        foglalt = True
                        break
                if not foglalt:
                    szabad_szobak.append(szoba.szobaszam)
        return szabad_szobak  # Visszaadja a szabad szobák számát adott dátumra

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba  # A foglalt szoba
        self.datum = datum  # A foglalás dátuma

def felhasznaloi_felulet():
    szalloda = Szalloda("Példa Szálloda")
    szalloda.szoba_hozzaadasa(EgyagyasSzoba(10000, 101))
    szalloda.szoba_hozzaadasa(EgyagyasSzoba(10000, 102))
    szalloda.szoba_hozzaadasa(KetagyasSzoba(15000, 201))
    szalloda.szoba_hozzaadasa(KetagyasSzoba(15000, 202))

    # Előre lefoglalt szobák
    szalloda.foglalas(101, "2024-06-01")
    szalloda.foglalas(102, "2024-06-02")
    szalloda.foglalas(201, "2024-06-03")
    szalloda.foglalas(202, "2024-06-04")
    szalloda.foglalas(201, "2024-06-05")

    while True:
        print("1. Szoba foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        valasztas = input("Választás: ")

        if valasztas == "1":
            datum = input("Dátum (YYYY-MM-DD): ")
            szabad_szobak = szalloda.szabad_szobak(datum)
            if szabad_szobak:
                print("Szabad szobák:", szabad_szobak)
                szobaszam = int(input("Szobaszám (válasszon a szabad szobák közül): "))
                sikeres, ar = szalloda.foglalas_ar(szobaszam, datum)
                if sikeres:
                    print(f"Foglalás sikeres! A szoba ára: {ar} Ft")
                else:
                    print("A szoba már foglalt ezen a napon, vagy a szobaszám nem létezik.")
            else:
                print("Nincs szabad szoba ezen a napon.")

        elif valasztas == "2":
            szobaszam = int(input("Szobaszám: "))
            datum = input("Dátum (YYYY-MM-DD): ")
            if szalloda.foglalas_lemondasa(szobaszam, datum):
                print("Foglalás lemondva!")
            else:
                print("Nincs ilyen foglalás.")

        elif valasztas == "3":
            foglalasok = szalloda.foglalasok_listazasa()
            if foglalasok:
                for foglalas in foglalasok:
                    print(foglalas)
            else:
                print("Nincsenek foglalások.")

        elif valasztas == "4":
            break

        else:
            print("Érvénytelen választás, próbálja újra.")

# Uncomment the following line to run the user interface
felhasznaloi_felulet()
