################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: Õppeprogramm "flashcards"
#
#
# Autorid: Kuldar Lilleõis, Kaspar Matkur
#
# mõningane eeskuju:
#
# Lisakommentaar (nt käivitusjuhend):
#
##################################################

import tkinter as tk #GUI moodul alisasega tk, et oleks lihtsam koodis välja
from tkinter import messagebox, simpledialog, ttk # Kutsusin lisa funktsioonid mis ei töödanud kui kutsuda ainult tkinteri moodul
import os
import json #json faili töötlus 
import random

# Loob json faili samasse kausta kui on programm
KAARDID_FAIL = os.path.join(os.path.dirname(__file__), "õppekaardid.json")

# Laeb json failist eelnevalt lisatud õppekaardid
def lae_õppekaardid():
    try:
        with open(KAARDID_FAIL, "r", encoding="utf-8") as f:
            return json.load(f).get("kaardid", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Kirjutab lisatud õppekaardi json faili
def salvesta_õppekaardid(kaardid):
    with open(KAARDID_FAIL, "w", encoding="utf-8") as f:
        json.dump({"kaardid": kaardid}, f, indent=4)


class MälukaardiRakendus:
    def __init__(self, aken):
        self.aken = aken
        self.aken.title("Õppekaardide Rakendus")
        self.aken.geometry("600x400")  # GUI akna suuruse määramine
        self.kaardid = lae_õppekaardid()

        # Peamenüü nupud
        self.pearaam = tk.Frame(self.aken)
        self.pearaam.pack(pady=20)

        tk.Button(self.pearaam, text="Õpi õppekaardidega", command=self.õpi_kaarte, width=20).pack(pady=5)
        tk.Button(self.pearaam, text="Vaata kõiki õppekaarte", command=self.vaata_kaarte, width=20).pack(pady=5)
        tk.Button(self.pearaam, text="Loo uus õppekaart", command=self.loo_õppekaart, width=20).pack(pady=5)
        tk.Button(self.pearaam, text="Välju", command=self.aken.quit, width=20).pack(pady=5)

    # Funkstioon uute kaardide loomiseks ja json faili salvestamiseks
    def loo_õppekaart(self):
        küsimus = simpledialog.askstring("Loo õppekaart", "Sisesta küsimus:")
        if not küsimus:
            return
        vastus = simpledialog.askstring("Loo õppekaart", "Sisesta vastus:")
        if not vastus:
            return
        self.kaardid[küsimus] = vastus
        salvesta_õppekaardid(self.kaardid)
        messagebox.showinfo("Õnnestus", "Õppekaart on loodud!")

    # Funkstioon kõigi lisatud kaardide vaatamiseks json failis
    def vaata_kaarte(self):
        if not self.kaardid:
            messagebox.showinfo("Teade", "Ühtegi õppekaarti pole saadaval.")
            return

        vaatamise_aken = tk.Toplevel(self.aken)
        vaatamise_aken.title("Vaata õppekaarte")
        vaatamise_aken.geometry("600x400")

        raam = tk.Frame(vaatamise_aken)
        raam.pack(fill="both", expand=True)

        lõuend = tk.Canvas(raam)
        kerimisriba = ttk.Scrollbar(raam, orient="vertical", command=lõuend.yview)
        kerimisraam = ttk.Frame(lõuend)

        kerimisraam.bind(
            "<Configure>",
            lambda e: lõuend.configure(scrollregion=lõuend.bbox("all"))
        )

        lõuend.create_window((0, 0), window=kerimisraam, anchor="nw")
        lõuend.configure(yscrollcommand=kerimisriba.set)

        lõuend.pack(side="left", fill="both", expand=True)
        kerimisriba.pack(side="right", fill="y")

        # Lisatud funktsioon mis lisab iga kaardi juurde nupu "Kustuta"
        for küsimus, vastus in self.kaardid.items():
            kaardiraam = tk.Frame(kerimisraam, pady=5, padx=10)
            kaardiraam.pack(fill="x", expand=True, pady=2)

            tk.Label(kaardiraam, text=f"K: {küsimus}", anchor="w").pack(side="left", fill="x", expand=True)
            tk.Label(kaardiraam, text=f"V: {vastus}", anchor="w").pack(side="left", fill="x", expand=True)
            tk.Button(kaardiraam, text="Kustuta", command=lambda q=küsimus: self.kustuta_kaart(q), fg="red").pack(side="right")

    # Funktsioon mis lisab võimaluse kustutada lisatud kaarte json failist
    def kustuta_kaart(self, küsimus):
        kinnitus = messagebox.askyesno("Kustutamise kinnitus", f"Kas soovite kindlasti kustutada õppekaardi: '{küsimus}'?")
        if kinnitus:
            del self.kaardid[küsimus]
            salvesta_õppekaardid(self.kaardid)
            messagebox.showinfo("Õnnestus", "Õppekaart on kustutatud!")

    # Funktsioon õppekaardide kasutamiseks/ õppimiseks
    def õpi_kaarte(self):
        # Teade kui ühtegi õppekaardi pole lisatud
        if not self.kaardid:
            messagebox.showinfo("Teade", "Ühtegi õppekaarti pole saadaval.")
            return

        # Küsimuste suvalisse järjekorda seadmine
        küsimused = list(self.kaardid.keys())
        random.shuffle(küsimused)

        # Teade kui kõik kaardid on läbitud
        def järgmine_küsimus(indeks):
            if indeks >= len(küsimused):
                messagebox.showinfo("Lõpetatud", "Kõik mälukaardid on läbitud!")
                õpiaken.destroy()
                return

            küsimus = küsimused[indeks]
            vastus = self.kaardid[küsimus]

            def kontrolli_vastust():
                kasutaja_vastus = vastuse_sisestus.get().strip()
                if kasutaja_vastus.lower() == vastus.lower():
                    messagebox.showinfo("Õige!", "Teie vastus on õige!")
                else:
                    messagebox.showinfo("Vale!", f"Õige vastus on: {vastus}")
                järgmine_küsimus(indeks + 1)

            for vidin in õpi_raam.winfo_children():
                vidin.destroy()

            tk.Label(õpi_raam, text=f"K: {küsimus}", font=("Arial", 14)).pack(pady=10)
            vastuse_sisestus = tk.Entry(õpi_raam, font=("Arial", 12))
            vastuse_sisestus.pack(pady=10)
            tk.Button(õpi_raam, text="Esita vastus", command=kontrolli_vastust).pack(pady=5)

        # Loob uue akna kus kasutaja õpib õppekaardidega
        õpiaken = tk.Toplevel(self.aken)
        õpiaken.title("Õpi õppekaarte")
        õpiaken.geometry("600x400")
        õpi_raam = tk.Frame(õpiaken)
        õpi_raam.pack(pady=20, padx=20)
        järgmine_küsimus(0)

def main():
    juur = tk.Tk() # tkinteri peaakna loomiseks
    rakendus = MälukaardiRakendus(juur) # Aktiveerib rakenduse ja seob selle kasutajaliidesega
    juur.mainloop() # Programmi töö toimub selles kuni kasutaja otsustab väljuda

# Põhiprogrammi algus
main()
