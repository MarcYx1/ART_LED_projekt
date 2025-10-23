import tkinter as tk
# import pyserial  # Ha már kitaláltuk miként és hogyan lesz serial kommunikáció

# tkinter ablak inicializálása
window = tk.Tk()
window.title("LED Villogtató")
window.geometry("300x330")
window.resizable(False, False)

# --------------------------Függvények--------------------------

def refresh(bpm_ertek):
    # BPM kiszámólása alapján frissíti a bekapcs és kikapcs mezőket
    kikapcs_ido = bekapcs_ido = round(60000 / (int(bpm_ertek) * 2)) if bpm_ertek.isdigit() and int(bpm_ertek) > 0 else 0
    bekapcs.delete(0, tk.END)
    kikapcs.delete(0, tk.END)
    bekapcs.insert(0, bekapcs_ido)
    kikapcs.insert(0, kikapcs_ido)
    
def ido_kuldes():
    bekapcs_ido = bekapcs.get()
    kikapcs_ido = kikapcs.get()

    # Amíg nincs serialos téma addig csak kiíratom a konzolra
    print(f"Bekapcsolt idő: {bekapcs_ido} ms")
    print(f"Kikapcsolt idő: {kikapcs_ido} ms")

# --------------------------GUI elemek--------------------------

# Cím
label = tk.Label(window, text="LED villogtató", font=("Comic Sans MS", 16))
label.pack(pady=20)

# Két oszlop létrehozása
columns = tk.Frame(window)
columns.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# --------------------------oszlopok--------------------------

# LED sebesség beállítások oszlopa
left_frame = tk.Frame(columns, width=140, height=240)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

# Állapot és küldés gomb oszlopa
right_frame = tk.Frame(columns, width=140, height=240)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

#--------------------------bal oszlop--------------------------

# LED sebesség beállítások bal oldalon
tk.Label(left_frame, text="LED Sebesség", font=("Comic Sans MS", 10, "bold")).pack(padx=8, pady=8)

# Bekapcsolt idő mező
tk.Label(left_frame, text="Bekapcs. idő (ms)", font=("Comic Sans MS", 10)).pack(pady=4)
bekapcs = tk.Entry(left_frame, width=10) # Bekapcs mező
bekapcs.pack(pady=4)

# kikapcsolt idő mező
tk.Label(left_frame, text="Kikapcs. idő (ms)", font=("Comic Sans MS", 10)).pack(pady=4)
kikapcs = tk.Entry(left_frame, text="kikapcs", width=10) # Kikapcs mező
kikapcs.pack(pady=4)

# BPM mező
tk.Label(left_frame, text="BPM", font=("Comic Sans MS", 10)).pack(pady=4)
bpm_var = tk.StringVar() # Tkinter StringVar a BPM érték tárolására (ennek segítségével tudom frissíteni a másik két mezőt)
bpm = tk.Entry(left_frame, width=10, textvariable=bpm_var) # BPM mező
bpm_var.trace_add("write", lambda *args: refresh(bpm_var.get())) # Automatikus frissítse a bekapcs és kikapcs mezőt a BPM alapján
bpm.pack(pady=4)

# --------------------------jobb oszlop--------------------------

# Állapot és küldés gomb jobb oldalon
tk.Label(right_frame, text="Állapot", font=("Comic Sans MS", 10, "bold")).pack(padx=8, pady=8)
allapot = tk.Label(right_frame, text="Lecsatlakozva", font=("Comic Sans MS", 10), fg="#ff0000") # Állapot címke
allapot.pack(pady=4)
tk.Button(right_frame, text="Küldés", font=("Comic Sans MS", 10), command=ido_kuldes).pack(pady=20) # Küldés gomb

window.mainloop()