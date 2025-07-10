import pandas as pd
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# === MASAÜSTÜNDE satislar KLASÖRÜ ===
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
veri_klasoru = os.path.join(desktop, "satislar")
os.makedirs(veri_klasoru, exist_ok=True)

paths = {
    "stok": os.path.join(veri_klasoru, "stok.xlsx"),
    "alis": os.path.join(veri_klasoru, "alislar.xlsx"),
    "urun": os.path.join(veri_klasoru, "urunler.xlsx"),
    "uretim": os.path.join(veri_klasoru, "uretimler.xlsx"),
    "satis": os.path.join(veri_klasoru, "satislar.xlsx"),
    "tas_gelir_gider": os.path.join(veri_klasoru, "tas_gelir_gider.xlsx"),
    "beton_gelir_gider": os.path.join(veri_klasoru, "beton_gelir_gider.xlsx")

}
paths["tas_gelir_gider"] = os.path.join(veri_klasoru, "tas_gelir_gider.xlsx")
paths["beton_gelir_gider"] = os.path.join(veri_klasoru, "beton_gelir_gider.xlsx")
for key in ["tas_gelir_gider", "beton_gelir_gider"]:
    if not os.path.exists(paths[key]):
        pd.DataFrame(columns=[
            "Tarih", "Tip", "Açıklama", "Birim", "Birim Fiyatı", "Miktar", "Toplam Tutar"
        ]).to_excel(paths[key], index=False)

for key, path in paths.items():
    if not os.path.exists(path):
        if key == "stok":
            pd.DataFrame(columns=["Malzeme", "Miktar_kg"]).to_excel(path, index=False)
        elif key == "alis":
            pd.DataFrame(columns=["Malzeme", "Miktar_kg", "BirimFiyat", "Tarih"]).to_excel(path, index=False)
        elif key == "urun":
            pd.DataFrame(columns=["Urun", "Malzeme", "Yuzde"]).to_excel(path, index=False)
        elif key == "uretim":
            pd.DataFrame(columns=["Urun", "Gramaj_kg", "Tarih"]).to_excel(path, index=False)
        elif key == "satis":
            pd.DataFrame(columns=["Urun", "Musteri", "Miktar_kg", "SatisFiyat", "Tarih", "NetKar"]).to_excel(path, index=False)

# === Arayüz Başlat ===
root = tk.Tk()
root.title("Beton Parke Takip Sistemi")
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# === Stok Girişi Sekmesi ===
def stok_girisi():
    try:
        malzeme = entry_malzeme.get()
        miktar = float(entry_miktar.get())
        fiyat = float(entry_fiyat.get())
        tarih = datetime.now().strftime("%Y-%m-%d")

        alis = pd.read_excel(paths["alis"])
        yeni = pd.DataFrame([[malzeme, miktar, fiyat, tarih]], columns=alis.columns)
        alis = pd.concat([alis, yeni], ignore_index=True)
        alis.to_excel(paths["alis"], index=False)

        stok = pd.read_excel(paths["stok"])
        if malzeme in stok["Malzeme"].values:
            stok.loc[stok["Malzeme"] == malzeme, "Miktar_kg"] += miktar
        else:
            stok = pd.concat([stok, pd.DataFrame([[malzeme, miktar]], columns=stok.columns)], ignore_index=True)
        stok.to_excel(paths["stok"], index=False)

        messagebox.showinfo("Başarılı", "Stok girişi kaydedildi.")
        entry_malzeme.delete(0, tk.END)
        entry_miktar.delete(0, tk.END)
        entry_fiyat.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Hata", str(e))

f1 = ttk.Frame(notebook)
notebook.add(f1, text="Stok Girişi")
entry_malzeme = tk.Entry(f1); entry_miktar = tk.Entry(f1); entry_fiyat = tk.Entry(f1)
tk.Label(f1, text="Malzeme: ").grid(row=0, column=0); entry_malzeme.grid(row=0, column=1)
tk.Label(f1, text="Miktar (kg): ").grid(row=1, column=0); entry_miktar.grid(row=1, column=1)
tk.Label(f1, text="Birim Fiyat: ").grid(row=2, column=0); entry_fiyat.grid(row=2, column=1)
tk.Button(f1, text="Kaydet", command=stok_girisi).grid(row=3, columnspan=2, pady=5)
tk.Label(f1, text="TURKCE KARAKTER KULLANMAYIN!", fg="red").grid(row=4, columnspan=2, pady=(10, 5))


# === Ürün Reçetesi Tanımı Sekmesi ===
recete_gecici = []

def receteye_malzeme_ekle():
    malzeme = entry_urun_malzeme.get()
    try:
        yuzde = float(entry_urun_yuzde.get())
        recete_gecici.append((entry_urun.get(), malzeme, yuzde))
        liste_kutu.insert(tk.END, f"{malzeme} - %{yuzde}")
        entry_urun_malzeme.delete(0, tk.END)
        entry_urun_yuzde.delete(0, tk.END)
    except:
        messagebox.showerror("Hata", "Geçerli bir yüzde gir!")

def recete_kaydet():
    if not recete_gecici:
        messagebox.showwarning("Uyarı", "Hiç malzeme eklenmedi.")
        return
    df = pd.read_excel(paths["urun"])
    yeni_df = pd.DataFrame(recete_gecici, columns=["Urun", "Malzeme", "Yuzde"])
    df = pd.concat([df, yeni_df], ignore_index=True)
    df.to_excel(paths["urun"], index=False)
    messagebox.showinfo("Başarılı", "Ürün reçetesi kaydedildi.")
    entry_urun.delete(0, tk.END)
    liste_kutu.delete(0, tk.END)
    recete_gecici.clear()

f2 = ttk.Frame(notebook)
notebook.add(f2, text="Ürün Tanımı")
tk.Label(f2, text="Ürün Adı: ").grid(row=0, column=0)
entry_urun = tk.Entry(f2)
entry_urun.grid(row=0, column=1, columnspan=2, sticky="ew")
tk.Label(f2, text="Malzeme: ").grid(row=1, column=0)
entry_urun_malzeme = tk.Entry(f2)
entry_urun_malzeme.grid(row=1, column=1)
tk.Label(f2, text="Yüzde: ").grid(row=1, column=2)
entry_urun_yuzde = tk.Entry(f2)
entry_urun_yuzde.grid(row=1, column=3)
tk.Button(f2, text="Malzeme Ekle", command=receteye_malzeme_ekle).grid(row=2, column=0, columnspan=4, pady=5)
liste_kutu = tk.Listbox(f2, width=50)
liste_kutu.grid(row=3, column=0, columnspan=4)
tk.Button(f2, text="Tümünü Kaydet", command=recete_kaydet).grid(row=4, column=0, columnspan=4, pady=5)
tk.Label(f2, text="TURKCE KARAKTER KULLANMAYIN!", fg="red").grid(row=5, column=0, columnspan=4, pady=(10, 5))

# === Üretim Sekmesi ===
def uretim_yap():
    try:
        urun = entry_uretim_urun.get()
        gramaj = float(entry_uretim_gramaj.get())
        tarih = datetime.now().strftime("%Y-%m-%d")

        receteler = pd.read_excel(paths["urun"])
        stok = pd.read_excel(paths["stok"])
        urun_recete = receteler[receteler["Urun"] == urun]
        if urun_recete.empty:
            raise ValueError("Bu ürün için reçete tanımı yok.")

        for _, row in urun_recete.iterrows():
            malzeme = row["Malzeme"]
            oran = row["Yuzde"] / 100
            gereken = gramaj * oran
            if malzeme in stok["Malzeme"].values:
                mevcut = stok.loc[stok["Malzeme"] == malzeme, "Miktar_kg"].values[0]
                if mevcut < gereken:
                    raise ValueError(f"{malzeme} için yeterli stok yok.")
                stok.loc[stok["Malzeme"] == malzeme, "Miktar_kg"] -= gereken
            else:
                raise ValueError(f"{malzeme} stokta yok.")

        stok.to_excel(paths["stok"], index=False)
        uretim = pd.read_excel(paths["uretim"])
        uretim = pd.concat([uretim, pd.DataFrame([[urun, gramaj, tarih]], columns=uretim.columns)], ignore_index=True)
        uretim.to_excel(paths["uretim"], index=False)

        messagebox.showinfo("Başarılı", "Üretim kaydedildi.")
        entry_uretim_urun.delete(0, tk.END)
        entry_uretim_gramaj.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Hata", str(e))

f3 = ttk.Frame(notebook)
notebook.add(f3, text="Üretim")
tk.Label(f3, text="Ürün: ").grid(row=0, column=0)
entry_uretim_urun = tk.Entry(f3)
entry_uretim_urun.grid(row=0, column=1)
tk.Label(f3, text="Gramaj (kg): ").grid(row=1, column=0)
entry_uretim_gramaj = tk.Entry(f3)
entry_uretim_gramaj.grid(row=1, column=1)
tk.Button(f3, text="Üretimi Kaydet", command=uretim_yap).grid(row=2, column=0, columnspan=2, pady=5)
tk.Label(f3, text="TURKCE KARAKTER KULLANMAYIN!", fg="red").grid(row=10, columnspan=2, pady=(10, 5))


# === Satış Sekmesi ===
def satis_kaydet():
    try:
        urun = entry_satis_urun.get()
        musteri = entry_satis_musteri.get()
        miktar = float(entry_satis_miktar.get())
        fiyat = float(entry_satis_fiyat.get())
        tarih = datetime.now().strftime("%Y-%m-%d")

        kdv_orani = 0.20
        receteler = pd.read_excel(paths["urun"])
        alislar = pd.read_excel(paths["alis"])
        urun_recete = receteler[receteler["Urun"] == urun]

        toplam_maliyet = 0
        for _, row in urun_recete.iterrows():
            malzeme = row["Malzeme"]
            oran = row["Yuzde"] / 100
            gereken_miktar = miktar * oran
            alis_malzeme = alislar[alislar["Malzeme"] == malzeme]
            if not alis_malzeme.empty:
                birim_fiyat = alis_malzeme.iloc[-1]["BirimFiyat"]
                toplam_maliyet += gereken_miktar * birim_fiyat

        net_kar = (fiyat * miktar / (1 + kdv_orani)) - toplam_maliyet

        satis = pd.read_excel(paths["satis"])
        yeni_satis = pd.DataFrame([[urun, musteri, miktar, fiyat, tarih, net_kar]], columns=satis.columns)
        satis = pd.concat([satis, yeni_satis], ignore_index=True)
        satis.to_excel(paths["satis"], index=False)

        messagebox.showinfo("Başarılı", "Satış kaydedildi.")
        entry_satis_urun.delete(0, tk.END)
        entry_satis_musteri.delete(0, tk.END)
        entry_satis_miktar.delete(0, tk.END)
        entry_satis_fiyat.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Hata", str(e))

f4 = ttk.Frame(notebook)
notebook.add(f4, text="Satış")
tk.Label(f4, text="Ürün: ").grid(row=0, column=0)
entry_satis_urun = tk.Entry(f4)
entry_satis_urun.grid(row=0, column=1)
tk.Label(f4, text="Müşteri: ").grid(row=1, column=0)
entry_satis_musteri = tk.Entry(f4)
entry_satis_musteri.grid(row=1, column=1)
tk.Label(f4, text="Miktar (kg): ").grid(row=2, column=0)
entry_satis_miktar = tk.Entry(f4)
entry_satis_miktar.grid(row=2, column=1)
tk.Label(f4, text="Satış Fiyatı: ").grid(row=3, column=0)
entry_satis_fiyat = tk.Entry(f4)
entry_satis_fiyat.grid(row=3, column=1)
tk.Button(f4, text="Satışı Kaydet", command=satis_kaydet).grid(row=4, column=0, columnspan=2, pady=5)
tk.Label(f4, text="TURKCE KARAKTER KULLANMAYIN!", fg="red").grid(row=10, columnspan=2, pady=(10, 5))

def iade_kaydet():
    try:
        urun = entry_iade_urun.get()
        miktar = float(entry_iade_miktar.get())
        sebep = entry_iade_sebep.get()
        tip = combo_iade_tip.get()
        tarih = datetime.now().strftime("%Y-%m-%d")

        df = pd.read_excel(paths["iade"])
        yeni = pd.DataFrame([[tarih, tip, urun, miktar, sebep]], columns=df.columns)
        df = pd.concat([df, yeni], ignore_index=True)
        df.to_excel(paths["iade"], index=False)

        if tip == "İade":
            stok = pd.read_excel(paths["stok"])
            if urun in stok["Malzeme"].values:
                stok.loc[stok["Malzeme"] == urun, "Miktar_kg"] += miktar
            else:
                stok = pd.concat([stok, pd.DataFrame([[urun, miktar]], columns=stok.columns)], ignore_index=True)
            stok.to_excel(paths["stok"], index=False)

        messagebox.showinfo("Başarılı", "Kayıt eklendi.")
        entry_iade_urun.delete(0, tk.END)
        entry_iade_miktar.delete(0, tk.END)
        entry_iade_sebep.delete(0, tk.END)
        combo_iade_tip.set("")
    except Exception as e:
        messagebox.showerror("Hata", str(e))

f5 = ttk.Frame(notebook)
notebook.add(f5, text="İade / Hurda")
tk.Label(f5, text="TURKCE KARAKTER KULLANMAYIN!", fg="red").grid(row=0, columnspan=2, pady=(5, 5))
tk.Label(f5, text="Ürün/Malzeme: ").grid(row=1, column=0)
entry_iade_urun = tk.Entry(f5)
entry_iade_urun.grid(row=1, column=1)
tk.Label(f5, text="Miktar (kg): ").grid(row=2, column=0)
entry_iade_miktar = tk.Entry(f5)
entry_iade_miktar.grid(row=2, column=1)
tk.Label(f5, text="Tür (İade / Hurda): ").grid(row=3, column=0)
combo_iade_tip = ttk.Combobox(f5, values=["İade", "Hurda"])
combo_iade_tip.grid(row=3, column=1)
tk.Label(f5, text="Sebep: ").grid(row=4, column=0)
entry_iade_sebep = tk.Entry(f5)
entry_iade_sebep.grid(row=4, column=1)
tk.Button(f5, text="Kaydet", command=iade_kaydet).grid(row=5, columnspan=2, pady=10)

# === SADECE TAŞ GİDER TÜRLERİ ===
tas_gider_turleri = [
    "İŞÇİLİK SGK", "İŞÇİLİK MAAŞ", "İŞ GÜVENLİĞİ", "ÇEVRE DANIŞMANLIK FİRMASI",
    "MADEN MÜHENDİSİ", "SORUMLU YTK", "ORMAN KİRA BEDELİ", "MAPEG KİRA BEDELİ",
    "PATLATMA GİDERİ", "ELEKTRİK", "YEMEK", "MOTORİN", "TAMİR BAKIM  GİDERLERİ",
    "YÖNETİM GİDERİ", "VERGİ", "DİĞER"
]

def tas_gider_kaydet():
    try:
        tarih = entry_tas_tarih.get()
        tip = "Gider"  # sabit
        aciklama = combo_tas_kategori.get()
        birim = entry_tas_birim.get()
        birim_fiyat = float(entry_tas_fiyat.get())
        miktar = float(entry_tas_miktar.get())
        toplam = birim_fiyat * miktar

        df = pd.read_excel(paths["tas_gelir_gider"])
        yeni = pd.DataFrame([[tarih, tip, aciklama, birim, birim_fiyat, miktar, toplam]], columns=df.columns)
        df = pd.concat([df, yeni], ignore_index=True)
        df.to_excel(paths["tas_gelir_gider"], index=False)

        messagebox.showinfo("Başarılı", "Taş gideri kaydedildi.")
        entry_tas_tarih.delete(0, tk.END)
        combo_tas_kategori.set("")
        entry_tas_birim.delete(0, tk.END)
        entry_tas_fiyat.delete(0, tk.END)
        entry_tas_miktar.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Hata", str(e))

f6 = ttk.Frame(notebook)
notebook.add(f6, text="Taş Gider")
tk.Label(f6, text="Tarih (YYYY-AA-GG):").grid(row=0, column=0)
entry_tas_tarih = tk.Entry(f6)
entry_tas_tarih.grid(row=0, column=1)
tk.Label(f6, text="Gider Türü:").grid(row=1, column=0)
combo_tas_kategori = ttk.Combobox(f6, values=tas_gider_turleri)
combo_tas_kategori.grid(row=1, column=1)
tk.Label(f6, text="Birim:").grid(row=2, column=0)
entry_tas_birim = tk.Entry(f6)
entry_tas_birim.grid(row=2, column=1)
tk.Label(f6, text="Birim Fiyatı:").grid(row=3, column=0)
entry_tas_fiyat = tk.Entry(f6)
entry_tas_fiyat.grid(row=3, column=1)
tk.Label(f6, text="Miktar:").grid(row=4, column=0)
entry_tas_miktar = tk.Entry(f6)
entry_tas_miktar.grid(row=4, column=1)
tk.Button(f6, text="Kaydet", command=tas_gider_kaydet).grid(row=5, columnspan=2, pady=10)
tk.Label(f6, text="TURKCE KARAKTER KULLANMAYIN!", fg="red").grid(row=6, columnspan=2, pady=(5, 5))

# === SADECE BETON GİDER TÜRLERİ ===
beton_gider_turleri = ["ÇİMENTO", "AGREGA", "KATKI"]

def beton_gider_kaydet():
    try:
        tarih = entry_beton_tarih.get()
        tip = "Gider"  # sabit
        aciklama = combo_beton_kategori.get()
        birim = entry_beton_birim.get()
        birim_fiyat = float(entry_beton_fiyat.get())
        miktar = float(entry_beton_miktar.get())
        toplam = birim_fiyat * miktar

        df = pd.read_excel(paths["beton_gelir_gider"])
        yeni = pd.DataFrame([[tarih, tip, aciklama, birim, birim_fiyat, miktar, toplam]], columns=df.columns)
        df = pd.concat([df, yeni], ignore_index=True)
        df.to_excel(paths["beton_gelir_gider"], index=False)

        messagebox.showinfo("Başarılı", "Beton gideri kaydedildi.")
        entry_beton_tarih.delete(0, tk.END)
        combo_beton_kategori.set("")
        entry_beton_birim.delete(0, tk.END)
        entry_beton_fiyat.delete(0, tk.END)
        entry_beton_miktar.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Hata", str(e))

f7 = ttk.Frame(notebook)
notebook.add(f7, text="Beton Gider")
tk.Label(f7, text="Tarih (YYYY-AA-GG):").grid(row=0, column=0)
entry_beton_tarih = tk.Entry(f7)
entry_beton_tarih.grid(row=0, column=1)
tk.Label(f7, text="Gider Türü:").grid(row=1, column=0)
combo_beton_kategori = ttk.Combobox(f7, values=beton_gider_turleri)
combo_beton_kategori.grid(row=1, column=1)
tk.Label(f7, text="Birim:").grid(row=2, column=0)
entry_beton_birim = tk.Entry(f7)
entry_beton_birim.grid(row=2, column=1)
tk.Label(f7, text="Birim Fiyatı:").grid(row=3, column=0)
entry_beton_fiyat = tk.Entry(f7)
entry_beton_fiyat.grid(row=3, column=1)
tk.Label(f7, text="Miktar:").grid(row=4, column=0)
entry_beton_miktar = tk.Entry(f7)
entry_beton_miktar.grid(row=4, column=1)
tk.Button(f7, text="Kaydet", command=beton_gider_kaydet).grid(row=5, columnspan=2, pady=10)
tk.Label(f7, text="TURKCE KARAKTER KULLANMAYIN!", fg="red").grid(row=6, columnspan=2, pady=(5, 5))

# === GÜNCELLENMİŞ RAPORLAMA SEKMESİ ===
def raporla():
    try:
        secim = combo_rapor_tipi.get()

        def to_date(x):
            return pd.to_datetime(x, errors="coerce")

        # Verileri oku ve tarihleri düzelt
        satis = pd.read_excel(paths["satis"])
        uretim = pd.read_excel(paths["uretim"])
        tas = pd.read_excel(paths["tas_gelir_gider"])
        beton = pd.read_excel(paths["beton_gelir_gider"])

        for df in [satis, uretim, tas, beton]:
            df["Tarih"] = to_date(df["Tarih"])

        if secim == "Günlük":
            satis_group = satis.groupby(satis["Tarih"].dt.date)["NetKar"].sum().rename("Satış Kârı")
            tas_group = tas.groupby(tas["Tarih"].dt.date)["Toplam Tutar"].apply(
                lambda x: x.sum() if (tas.loc[x.index, "Tip"] == "Gelir").all() else -x.sum()
            ).rename("Taş Gelir-Gider")
            beton_group = beton.groupby(beton["Tarih"].dt.date)["Toplam Tutar"].apply(
                lambda x: x.sum() if (beton.loc[x.index, "Tip"] == "Gelir").all() else -x.sum()
            ).rename("Beton Gelir-Gider")
        else:
            satis_group = satis.groupby(satis["Tarih"].dt.to_period("M"))["NetKar"].sum().rename("Satış Kârı")
            tas_group = tas.groupby(tas["Tarih"].dt.to_period("M"))["Toplam Tutar"].apply(
                lambda x: x.sum() if (tas.loc[x.index, "Tip"] == "Gelir").all() else -x.sum()
            ).rename("Taş Gelir-Gider")
            beton_group = beton.groupby(beton["Tarih"].dt.to_period("M"))["Toplam Tutar"].apply(
                lambda x: x.sum() if (beton.loc[x.index, "Tip"] == "Gelir").all() else -x.sum()
            ).rename("Beton Gelir-Gider")

        # Raporu birleştir
        rapor = pd.concat([satis_group, tas_group, beton_group], axis=1).fillna(0)
        rapor["Toplam Kâr/Zarar"] = rapor.sum(axis=1)

        # Göster
        liste_rapor.delete(0, tk.END)
        for tarih, row in rapor.iterrows():
            liste_rapor.insert(tk.END, f"{tarih} ➤ Net: {row['Toplam Kâr/Zarar']:.2f} ₺")

    except Exception as e:
        messagebox.showerror("Hata", str(e))

f8 = ttk.Frame(notebook)
notebook.add(f8, text="Raporlama")
tk.Label(f8, text="Rapor Tipi:").pack(pady=(10, 0))
combo_rapor_tipi = ttk.Combobox(f8, values=["Günlük", "Aylık"])
combo_rapor_tipi.set("Günlük")
combo_rapor_tipi.pack()
tk.Button(f8, text="Raporu Oluştur", command=raporla).pack(pady=5)
liste_rapor = tk.Listbox(f8, width=60)
liste_rapor.pack()
tk.Label(f8, text="TURKCE KARAKTER KULLANMAYIN!", fg="red").pack(pady=(10, 5))



# === Program Başlat ===
root.mainloop()
