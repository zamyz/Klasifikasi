import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import tkinter as tk
from tkinter import ttk, messagebox

# Definisi Variabel Input
panjang = ctrl.Antecedent(np.arange(10, 31, 1), 'panjang')
lebar = ctrl.Antecedent(np.arange(5, 16, 1), 'lebar')
berat = ctrl.Antecedent(np.arange(200, 1001, 10), 'berat')
jumlah_biji = ctrl.Antecedent(np.arange(20, 61, 1), 'jumlah_biji')

# Definisi Variabel Output
klasifikasi = ctrl.Consequent(np.arange(0, 11, 1), 'klasifikasi')

# Definisi Fungsi Keanggotaan
panjang.automf(3, names=['pendek', 'sedang', 'panjang'])
lebar.automf(3, names=['sempit', 'sedang', 'lebar'])
berat.automf(3, names=['ringan', 'sedang', 'berat'])
jumlah_biji.automf(3, names=['sedikit', 'sedang', 'banyak'])
klasifikasi.automf(3, names=['rendah', 'sedang', 'tinggi'])

# Definisi Aturan Fuzzy
rules = [
    ctrl.Rule(panjang['pendek'] & lebar['sempit'] & berat['ringan'] & jumlah_biji['sedikit'], klasifikasi['rendah']),
    ctrl.Rule(panjang['sedang'] & lebar['sedang'] & berat['sedang'] & jumlah_biji['sedang'], klasifikasi['sedang']),
    ctrl.Rule(panjang['panjang'] & lebar['lebar'] & berat['berat'] & jumlah_biji['banyak'], klasifikasi['tinggi']),
    ctrl.Rule(panjang['panjang'] | lebar['lebar'] | berat['berat'] | jumlah_biji['banyak'], klasifikasi['tinggi']),
    ctrl.Rule(panjang['pendek'] | lebar['sempit'] | berat['ringan'] | jumlah_biji['sedikit'], klasifikasi['rendah']),
]

# Pembuatan Sistem Kontrol Fuzzy
klasifikasi_ctrl = ctrl.ControlSystem(rules)
klasifikasi_sim = ctrl.ControlSystemSimulation(klasifikasi_ctrl)

# GUI dengan Tkinter dan ttk
root = tk.Tk()
root.title("Klasifikasi Buah Kakao - Fuzzy Logic")
root.geometry("600x550")
root.configure(bg="#1C1C1C")

frame = ttk.Frame(root, padding=20, style="Card.TFrame")
frame.pack(expand=True, padx=20, pady=20)

title_label = ttk.Label(frame, text="🍫 Klasifikasi Buah Kakao 🍫", font=("Arial", 18, "bold"), foreground="#FFD700", background="#1C1C1C")
title_label.pack(pady=10)

fields = {
    "Panjang (10-30 cm)": tk.StringVar(),
    "Lebar (5-15 cm)": tk.StringVar(),
    "Berat (200-1000 gram)": tk.StringVar(),
    "Jumlah Biji (20-60)": tk.StringVar()
}

entries = {}
for label, var in fields.items():
    ttk.Label(frame, text=label, font=("Arial", 12, "bold"), background="#1C1C1C", foreground="#FFFFFF").pack()
    entry = ttk.Entry(frame, textvariable=var, font=("Arial", 12), width=15, justify='center', background="#000000", foreground="#000000")
    entry.pack(pady=5)
    entries[label] = entry

def proses_fuzzy():
    try:
        panjang_input = float(fields["Panjang (10-30 cm)"].get())
        lebar_input = float(fields["Lebar (5-15 cm)"].get())
        berat_input = float(fields["Berat (200-1000 gram)"].get())
        jumlah_biji_input = float(fields["Jumlah Biji (20-60)"].get())
        
        # Validasi rentang input
        if not (10 <= panjang_input <= 30):
            raise ValueError("Panjang harus antara 10 - 30 cm.")
        if not (5 <= lebar_input <= 15):
            raise ValueError("Lebar harus antara 5 - 15 cm.")
        if not (200 <= berat_input <= 1000):
            raise ValueError("Berat harus antara 200 - 1000 gram.")
        if not (20 <= jumlah_biji_input <= 60):
            raise ValueError("Jumlah biji harus antara 20 - 60.")

        # Set input ke sistem fuzzy
        klasifikasi_sim.input['panjang'] = panjang_input
        klasifikasi_sim.input['lebar'] = lebar_input
        klasifikasi_sim.input['berat'] = berat_input
        klasifikasi_sim.input['jumlah_biji'] = jumlah_biji_input

        klasifikasi_sim.compute()
        
        hasil = klasifikasi_sim.output.get('klasifikasi', None)
        if hasil is not None:
            label_hasil.config(text=f"✨ Klasifikasi Kakao: {hasil:.2f} ✨")
        else:
            label_hasil.config(text="Klasifikasi tidak dapat dihitung.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

button = ttk.Button(frame, text="🔍 Proses", command=proses_fuzzy, style="Golden.TButton")
button.pack(pady=10)

label_hasil = ttk.Label(frame, text="", font=("Arial", 14, "bold"), foreground="#FFD700", background="#1C1C1C")
label_hasil.pack(pady=10)

style = ttk.Style()
style.configure("Golden.TButton", font=("Arial", 12, "bold"), padding=8, background="#FFD700", foreground="#000000")
style.configure("Card.TFrame", background="#1C1C1C")

root.mainloop()
