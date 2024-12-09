import tkinter as tk
from tkinter import ttk
import json
import random

KOMPLEKTID_FAIL = "kaardikomplektid.json"

LIGHT_BLUE = "#add8e6"
BUTTON_COLOR = "#87cefa"

# Funktsioonid kaardikomplektide laadimiseks ja salvestamiseks
def lae_komplektid():
    try:
        with open(KOMPLEKTID_FAIL, "r", encoding="utf-8") as f:
            return json.load(f).get("komplektid", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvesta_komplektid(komplektid):
    with open(KOMPLEKTID_FAIL, "w", encoding="utf-8") as f:
        json.dump({"komplektid": komplektid}, f, indent=4, ensure_ascii=False)

class Rakendus(tk.Tk):
    def __init__(self):
        super().__init__()
        self.komplektid = lae_komplektid()

        # Seadista stiilid
        self.seadista_stiilid()

        # Avab rakenduse akna ekraani keskel
        self.update_idletasks()
        width = 800
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Takistab kasutajal akna suurust muuta
        self.resizable(False, False)

        # Rakenduse põhikonteiner
        self.pearaam = ttk.Frame(self, style='TFrame')
        self.pearaam.pack(fill="both", expand=True)

        self.peamenüü()

    def seadista_stiilid(self):
        """Seadista rakenduse stiilid."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure('.', background=LIGHT_BLUE)
        style.configure('TFrame', background=LIGHT_BLUE)
        style.configure('TLabel', background=LIGHT_BLUE)
        style.configure('TButton', background=BUTTON_COLOR, foreground='black')
        style.map('TButton',
                  background=[('active', BUTTON_COLOR)],
                  foreground=[('active', 'black')])

    def näita_sõnumit(self, title, message, callback=None):
        # Kuvab mitteintrusiivse sõnumi rakenduse sees
        overlay = tk.Frame(self, bg="white", highlightbackground="black", highlightthickness=1)
        overlay.place(relx=0.5, rely=0.5, anchor="center", width=300, height=150)

        lbl_title = tk.Label(overlay, text=title, font=("Arial", 12, "bold"), background="white")
        lbl_title.pack(pady=10)
        lbl_msg = tk.Label(overlay, text=message, wraplength=250, justify="center", background="white")
        lbl_msg.pack(pady=10)

        def close_msg(event=None):
            overlay.destroy()
            if callback:
                callback()

        btn_ok = ttk.Button(overlay, text="OK", command=close_msg)
        btn_ok.pack(pady=10)
        btn_ok.focus_set()

        # Lubab Enter klahviga sulgeda sõnumi
        overlay.bind("<Return>", close_msg)
        overlay.focus_set()

    def näita_veateadet(self, title, message, callback=None):
        # Kuvab mitteintrusiivse veateate rakenduse sees
        overlay = tk.Frame(self, bg="white", highlightbackground="red", highlightthickness=1)
        overlay.place(relx=0.5, rely=0.5, anchor="center", width=300, height=150)

        lbl_title = tk.Label(overlay, text=title, font=("Arial", 12, "bold"), background="white", foreground="red")
        lbl_title.pack(pady=10)
        lbl_msg = tk.Label(overlay, text=message, wraplength=250, justify="center", background="white")
        lbl_msg.pack(pady=10)

        def close_msg(event=None):
            overlay.destroy()
            if callback:
                callback()

        btn_ok = ttk.Button(overlay, text="OK", command=close_msg)
        btn_ok.pack(pady=10)
        btn_ok.focus_set()

        # Lubab Enter klahviga sulgeda sõnumi
        overlay.bind("<Return>", close_msg)
        overlay.focus_set()

    def puhasta_raam(self):
        """Puhastab pearaami enne uue sisu lisamist."""
        for widget in self.pearaam.winfo_children():
            widget.destroy()

    def peamenüü(self):
        self.puhasta_raam()

        ttk.Label(self.pearaam, text="Õppekaardide rakendus", font=("Arial", 20, "bold")).pack(pady=20)

        # Peamenüü nupud
        ttk.Button(self.pearaam, text="Hakka harjutama!", command=self.alusta_õpinguid, width=30).pack(pady=5)
        ttk.Button(self.pearaam, text="Katseta oma teadmisi!", command=self.harjuta_juhuslik, width=30).pack(pady=5)
        ttk.Button(self.pearaam, text="Loo kaardikomplekt", command=self.loo_kaardikomplekt, width=30).pack(pady=5)
        ttk.Button(self.pearaam, text="Lisa kaart komplekti", command=self.lisa_kaart, width=30).pack(pady=5)
        ttk.Button(self.pearaam, text="Näita kaardikomplekte", command=self.näita_kaardikomplekte, width=30).pack(pady=5)
        ttk.Button(self.pearaam, text="Vaheta Küsimused ja Vastused", command=self.ava_pööramise_valik, width=30).pack(pady=5)
        ttk.Button(self.pearaam, text="Välju", command=self.quit, width=30).pack(pady=5)

    def alusta_õpinguid(self):
        if not self.komplektid:
            self.näita_sõnumit("Teade", "Ühtegi kaardikomplekti pole saadaval.")
            return

        # Valik, millist komplekti harjutada
        komplekt_nimed = ["— Vali komplekt —"] + list(self.komplektid.keys())  # Lisatud placeholder
        valitud_komplekt = tk.StringVar(value=komplekt_nimed[0])  # Alustab placeholderiga

        def alusta_valitud_komplektiga():
            komplekt_nimi = valitud_komplekt.get()
            kaardid = self.komplektid[komplekt_nimi]["kaardid"]
            if not kaardid:
                self.näita_sõnumit("Teade", "Valitud komplektis pole kaarte.")
                return
            näita_harjutus_režiim(kaardid)

        def näita_harjutus_režiim(kaardid):
            self.puhasta_raam()
            kaardid_list = list(kaardid.items())

            def näita_vastust(vastus, küsimus):
                self.puhasta_raam()
                ttk.Label(self.pearaam, text=küsimus, font=("Arial", 14)).pack(pady=10)
                ttk.Label(self.pearaam, text=vastus, font=("Arial", 14, "bold")).pack(pady=10)
                ttk.Button(self.pearaam, text="Järgmine kaart", command=järgmine_kaart).pack(pady=5)

            def järgmine_kaart():
                if not kaardid_list:
                    self.näita_sõnumit("Õnnestus", "Kõik kaardid on läbitud!", self.peamenüü)
                    return

                küsimus, vastus = kaardid_list.pop(0)
                self.puhasta_raam()
                ttk.Label(self.pearaam, text=küsimus, font=("Arial", 14)).pack(pady=10)
                ttk.Button(self.pearaam, text="Näita vastust", command=lambda: näita_vastust(vastus, küsimus)).pack(pady=5)

            järgmine_kaart()

        self.puhasta_raam()

        ttk.Label(self.pearaam, text="Vali kaardikomplekt harjutamiseks", font=("Arial", 16, "bold")).pack(pady=20)
        ttk.OptionMenu(self.pearaam, valitud_komplekt, *komplekt_nimed).pack(pady=10)
        ttk.Button(self.pearaam, text="Alusta harjutamist", command=alusta_valitud_komplektiga).pack(pady=10)
        ttk.Button(self.pearaam, text="Tagasi", command=self.peamenüü).pack(pady=10)

    def harjuta_juhuslik(self):
        # Harjutus juhuslikult valitud komplektiga.
        if not self.komplektid:
            self.näita_sõnumit("Teade", "Ühtegi kaardikomplekti pole saadaval.")
            return

        # Valige juhuslik kaardikomplekt
        komplekt_nimi = random.choice(list(self.komplektid.keys()))
        kaardid = self.komplektid[komplekt_nimi]["kaardid"]

        if not kaardid:
            self.näita_sõnumit("Teade", "Valitud komplektis pole kaarte.")
            return

        # Juhuslikult järjestatud küsimused
        kaardid_list = list(kaardid.items())
        random.shuffle(kaardid_list)

        def lõpetamise_nupp():
            self.puhasta_raam()
            self.näita_sõnumit("Harjutamine lõpetatud", f"Sa harjutasid komplekti: {komplekt_nimi}", self.peamenüü)

        def näita_vastust(vastus, küsimus):
            self.puhasta_raam()
            ttk.Label(self.pearaam, text=küsimus, font=("Arial", 14)).pack(pady=10)
            ttk.Label(self.pearaam, text=vastus, font=("Arial", 14, "bold")).pack(pady=10)

            ttk.Button(self.pearaam, text="Järgmine küsimus", command=järgmine_kaart).pack(pady=5)
            ttk.Button(self.pearaam, text="Lõpeta", command=lõpetamise_nupp).pack(pady=5)

        def järgmine_kaart():
            if not kaardid_list:
                self.näita_sõnumit("Õnnestus", "Kõik kaardid on läbitud!", lambda: lõpetamise_nupp())
                return

            küsimus, vastus = kaardid_list.pop(0)
            self.puhasta_raam()

            ttk.Label(self.pearaam, text=küsimus, font=("Arial", 14)).pack(pady=10)
            ttk.Button(self.pearaam, text="Näita vastust", command=lambda: näita_vastust(vastus, küsimus)).pack(pady=5)
            ttk.Button(self.pearaam, text="Lõpeta", command=lõpetamise_nupp).pack(pady=5)

        self.puhasta_raam()
        ttk.Button(self.pearaam, text="Lõpeta", command=lõpetamise_nupp).pack(anchor="ne", pady=10, padx=10)
        järgmine_kaart()

    def loo_kaardikomplekt(self):
        self.puhasta_raam()

        ttk.Label(self.pearaam, text="Loo uus kaardikomplekt", font=("Arial", 16, "bold")).pack(pady=20)
        ttk.Label(self.pearaam, text="Komplekti nimi:", font=("Arial", 12)).pack(pady=5)
        nimi_var = tk.StringVar()
        ttk.Entry(self.pearaam, textvariable=nimi_var, width=40).pack(pady=5)

        def loo_komplekt():
            nimi = nimi_var.get().strip()
            if nimi and nimi not in self.komplektid:
                self.komplektid[nimi] = {"kaardid": {}}
                salvesta_komplektid(self.komplektid)
                self.näita_sõnumit("Õnnestus", f"Kaardikomplekt '{nimi}' loodud!", self.peamenüü)
                self.peamenüü()
            else:
                self.näita_veateadet("Viga", "Komplekt selle nimega juba eksisteerib või nimi on tühi.")

        ttk.Button(self.pearaam, text="Loo komplekt", command=loo_komplekt, width=20).pack(pady=10)
        ttk.Button(self.pearaam, text="Tagasi", command=self.peamenüü, width=20).pack(pady=5)

    def lisa_kaart(self):
        # Lisab kaardi olemasolevasse komplekti
        self.puhasta_raam()

        if not self.komplektid:
            self.näita_veateadet("Teade", "Palun loo esmalt kaardikomplekt.", self.peamenüü())
            return

        ttk.Label(self.pearaam, text="Lisa uus kaart", font=("Arial", 16, "bold")).pack(pady=20)

        ttk.Label(self.pearaam, text="Vali kaardikomplekt:", font=("Arial", 12)).pack(pady=5)
        # Valik, millist komplekti harjutada
        komplekt_nimed = ["— Vali komplekt —"] + list(self.komplektid.keys())  # Lisatud placeholder
        valitud_komplekt = tk.StringVar(value=komplekt_nimed[0])  # Alustab placeholderiga
        ttk.OptionMenu(self.pearaam, valitud_komplekt, *komplekt_nimed).pack(pady=5)

        ttk.Label(self.pearaam, text="Küsimus:", font=("Arial", 12)).pack(pady=5)
        küsimus_var = tk.StringVar()
        ttk.Entry(self.pearaam, textvariable=küsimus_var, width=40).pack(pady=5)

        ttk.Label(self.pearaam, text="Vastus:", font=("Arial", 12)).pack(pady=5)
        vastus_var = tk.StringVar()
        ttk.Entry(self.pearaam, textvariable=vastus_var, width=40).pack(pady=5)

        def lisa_kaart_komplekti():
            komplekt = valitud_komplekt.get()
            küsimus = küsimus_var.get().strip()
            vastus = vastus_var.get().strip()
            if küsimus and vastus:
                self.komplektid[komplekt]["kaardid"][küsimus] = vastus
                salvesta_komplektid(self.komplektid)
                self.näita_sõnumit("Õnnestus", f"Kaart lisatud komplekti '{komplekt}'!", self.peamenüü)
            else:
                self.näita_veateadet("Viga", "Küsimus või vastus ei tohi olla tühi.")

        ttk.Button(self.pearaam, text="Lisa kaart", command=lisa_kaart_komplekti, width=20).pack(pady=10)
        ttk.Button(self.pearaam, text="Tagasi", command=self.peamenüü, width=20).pack(pady=5)

    def sorteeri_komplektid(self):
        # Sorteerib komplektid tähestikulises järjekorras nende nimede järgi
        sorteeritud_komplektid = dict(sorted(self.komplektid.items(), key=lambda item: item[0].lower()))
        self.komplektid = sorteeritud_komplektid
        salvesta_komplektid(self.komplektid)  # Salvestab sorteeritud andmed tagasi JSON-faili.
        self.näita_kaardikomplekte()  # Värskendab ekraani

    def pöörata_kaarte(self, komplekt_nimi):
        komplekt_andmed = self.komplektid.get(komplekt_nimi)
        if not komplekt_andmed:
            self.näita_veateadet("Teade", f"Komplekti '{komplekt_nimi}' andmeid ei leitud.")
            return

        kaardid = komplekt_andmed.get("kaardid", {})
        if not kaardid:
            self.näita_veateadet("Teade", f"Komplektis '{komplekt_nimi}' ei ole kaarte, mida pöörata.")
            return

        # Dubleerivate vastuste jälgimine, et vältida võtmekonflikte
        vastused = list(kaardid.values())
        if len(vastused) != len(set(vastused)):
            self.näita_veateadet("Viga", f"Komplekti '{komplekt_nimi}' kaartides on duplikaat vastuseid, mida ei saa pöörata.")
            return

        # Vahetab küsimus ja vastus
        pööratud_kaardid = {vastus: küsimus for küsimus, vastus in kaardid.items()}

        # Uuenda komplekti ümberpööratud kaardid
        self.komplektid[komplekt_nimi]["kaardid"] = pööratud_kaardid

        salvesta_komplektid(self.komplektid)

        # Värskendage kasutajaliidese muutuste kajastamiseks
        self.näita_kaardikomplekte()

        self.näita_sõnumit("Õnnestus", f"Õppekaardid komplektis '{komplekt_nimi}' on edukalt pööratud!")

    def ava_pööramise_valik(self):
        if not self.komplektid:
            self.näita_veateadet("Teade", "Ühtegi komplekti pole saadaval, mida pöörata.")
            return

        self.puhasta_raam()

        ttk.Label(self.pearaam, text="Vali komplekt kaardi pööramiseks", font=("Arial", 16, "bold")).pack(pady=20)

        # clickitava menüü loomine komplektide valimiseks
        komplekt_nimed = ["— Vali komplekt —"] + list(self.komplektid.keys())  # Lisatud placeholder
        valitud_komplekt = tk.StringVar(value=komplekt_nimed[0])  # Alustab placeholderiga

        dropdown = ttk.OptionMenu(self.pearaam, valitud_komplekt, *komplekt_nimed)
        dropdown.pack(pady=10)

        # Raam nuppude jaoks
        button_frame = ttk.Frame(self.pearaam)
        button_frame.pack(pady=10)

        def reverse_selected():
            komplekt = valitud_komplekt.get()
            if komplekt == "— Vali komplekt —":
                self.näita_veateadet("Viga", "Palun vali komplekt, mida pöörata.")
                return
            self.pöörata_kaarte(komplekt)

        ttk.Button(button_frame, text="Pöörata", command=reverse_selected, width=15).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Tagasi", command=self.peamenüü, width=15).pack(side="left", padx=10)

    def näita_kaardikomplekte(self):
        # Kaardikomplektide ja nende kaartide kuvamine koos kerimise ja redigeerimise võimalustega
        self.puhasta_raam()

        ttk.Label(self.pearaam, text="Kaardikomplektid ja nende kaardid", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Frame for Buttons
        button_frame = ttk.Frame(self.pearaam)
        button_frame.pack(pady=10)

        # "Sort" Button
        ttk.Button(button_frame, text="Sort", command=self.sorteeri_komplektid, width=20).pack(side="left", padx=10, pady=30)

        # "Tagasi" Button
        ttk.Button(button_frame, text="Tagasi", command=self.peamenüü, width=20).pack(side="left", padx=10)

        if not self.komplektid:
            ttk.Label(self.pearaam, text="Ühtegi komplekti pole saadaval.", font=("Arial", 12)).pack(pady=10)
            ttk.Button(self.pearaam, text="Tagasi", command=self.peamenüü, width=20).pack(pady=20)
            return

        # Loo Canvas ja kerimisriba
        canvas = tk.Canvas(self.pearaam, bg=LIGHT_BLUE, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        kerimisriba = ttk.Scrollbar(self.pearaam, orient="vertical", command=canvas.yview)
        kerimisriba.pack(side="right", fill="y")

        kerimisraam = ttk.Frame(canvas, style='TFrame')
        scrollable_frame_id = canvas.create_window((0, 0), window=kerimisraam, anchor="nw")

        def muuda_kerimise_ala(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def muuda_canvase_laiust(event):
            canvas.itemconfig(scrollable_frame_id, width=canvas.winfo_width())

        def keri_hiirega(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        # Hiireratta sidumine kerimisega
        canvas.bind_all("<MouseWheel>", keri_hiirega)
        canvas.bind_all("<Button-4>", keri_hiirega)
        canvas.bind_all("<Button-5>", keri_hiirega)
        kerimisraam.bind("<Configure>", muuda_kerimise_ala)
        canvas.bind("<Configure>", muuda_canvase_laiust)

        # Kaardikomplektide lisamine keritavasse raami
        for nimi, andmed in self.komplektid.items():
            frame = ttk.Frame(kerimisraam)
            frame.pack(fill="x", padx=20, pady=5)

            # Sisemine raam, et sättida kustutamis nuppu sildi kõrvale
            komplekt_frame = ttk.Frame(frame)
            komplekt_frame.pack(fill="x", padx=0, pady=0)

            # Kustuta komplekt nupp
            ttk.Button(komplekt_frame, text="Kustuta komplekt", command=lambda n=nimi: self.kustuta_komplekt(n), width=20).pack(side="left", padx=10)

            # Komplekti silt
            ttk.Label(komplekt_frame, text=f"{nimi} ({len(andmed['kaardid'])} kaarti)", font=("Arial", 14, "bold")).pack(side="left")

            if andmed.get("kaardid"):
                for küsimus, vastus in andmed["kaardid"].items():
                    kaart_frame = ttk.Frame(kerimisraam)
                    kaart_frame.pack(fill="x", padx=40, pady=2)

                    ttk.Label(kaart_frame, text=f"K: {küsimus}\nV: {vastus}\n", font=("Arial", 12)).pack(side="left", padx=135)
                    ttk.Button(kaart_frame, text="Kustuta", command=lambda n=nimi, k=küsimus: self.kustuta_kaart(n, k), width=15).pack(side="right", padx=2)
                    ttk.Button(kaart_frame, text="Muuda", command=lambda n=nimi, q=küsimus, v=vastus: self.muuda_kaart(n, q, v), width=15).pack(side="right", padx=2)
            else:
                ttk.Label(kerimisraam, text="  (Pole kaarte)", font=("Arial", 12, "italic")).pack(anchor="w", padx=180)

        canvas.configure(yscrollcommand=kerimisriba.set)

    def muuda_kaart(self, komplekt_nimi, vana_küsimus, vana_vastus):
        self.puhasta_raam()

        ttk.Label(self.pearaam, text=f"Muuda kaarti komplektis '{komplekt_nimi}'", font=("Arial", 16, "bold")).pack(pady=20)

        ttk.Label(self.pearaam, text="Küsimus:", font=("Arial", 12)).pack(pady=5)
        küsimus_var = tk.StringVar(value=vana_küsimus)
        ttk.Entry(self.pearaam, textvariable=küsimus_var, width=40).pack(pady=5)

        ttk.Label(self.pearaam, text="Vastus:", font=("Arial", 12)).pack(pady=5)
        vastus_var = tk.StringVar(value=vana_vastus)
        ttk.Entry(self.pearaam, textvariable=vastus_var, width=40).pack(pady=5)

        def salvesta_muudatused():
            uus_küsimus = küsimus_var.get().strip()
            uus_vastus = vastus_var.get().strip()

            if not uus_küsimus or not uus_vastus:
                self.näita_veateadet("Viga", "Küsimus või vastus ei tohi olla tühi.")
                return

            # Uuenda kaardi andmed
            if uus_küsimus != vana_küsimus:
                # Kui küsimust muudeti, kustuta vana ja lisa uus
                del self.komplektid[komplekt_nimi]["kaardid"][vana_küsimus]
            self.komplektid[komplekt_nimi]["kaardid"][uus_küsimus] = uus_vastus
            salvesta_komplektid(self.komplektid)
            self.näita_sõnumit("Õnnestus", "Kaart on edukalt muudetud!", self.näita_kaardikomplekte)

        ttk.Button(self.pearaam, text="Salvesta", command=salvesta_muudatused, width=20).pack(pady=10)
        ttk.Button(self.pearaam, text="Tühista", command=self.näita_kaardikomplekte, width=20).pack(pady=5)

    def kustuta_komplekt(self, komplekt_nimi):
        if komplekt_nimi in self.komplektid:
            del self.komplektid[komplekt_nimi]
            salvesta_komplektid(self.komplektid)
            self.näita_sõnumit("Õnnestus", f"Kaardikomplekt '{komplekt_nimi}' kustutatud!", self.näita_kaardikomplekte())
            
    def kustuta_kaart(self, komplekt_nimi, küsimus):
        if komplekt_nimi in self.komplektid and küsimus in self.komplektid[komplekt_nimi]["kaardid"]:
            del self.komplektid[komplekt_nimi]["kaardid"][küsimus]
            salvesta_komplektid(self.komplektid)
            self.näita_sõnumit("Õnnestus", f"Kaart '{küsimus}' kustutatud komplektist '{komplekt_nimi}'!", self.näita_kaardikomplekte())
            self.näita_kaardikomplekte()

def main():
    rakendus = Rakendus()
    rakendus.mainloop()

if __name__ == "__main__":
    main()
