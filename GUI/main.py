import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import serial
import serial.tools.list_ports
import threading # utálom nagyon rossz de muszáj ha tkinterrel akarom csinálni, külön szálon kell futtnia a serial kezelésnek és a tkinter loopnak

serial_port = None
serial_port_lock = threading.Lock()

def set_status(text, color="#000000"):
    # külön szálon frissítse az állapot labelt
    window.after(0, lambda: allapot.config(text=text, fg=color))

def show_exception(message, title="Hiba"):
    # A hiba ablak besorolása
    window.after(0, lambda: messagebox.showerror(title, message))

def connect_serial(asd=None):
    # Serial kapcsolat kezelés külön szálon
    def worker():
        global serial_port
        port = port_var.get()

        # már nyitott portot zárjuk
        with serial_port_lock:
            if serial_port and serial_port.is_open:
                try:
                    serial_port.close()
                except Exception:
                    pass
                serial_port = None

        if not port:
            set_status("Lecsatlakozva", "#ff0000")
            return

        try:
            sp = serial.Serial(port, baudrate=9600, timeout=1)
        except Exception as e:
            with serial_port_lock:
                serial_port = None
            # hiba popup
            show_exception(str(e), "Soros csatlakozás hiba")
            set_status("Lecsatlakozva", "#ff0000")
            return

        # nyitott port mentése
        with serial_port_lock:
            serial_port = sp
        set_status(f"Csatlakoztatva: {port}", "#008000")

    threading.Thread(target=worker, daemon=True).start()

def refresh(bpm_ertek):
    # BPM kiszámólása alapján frissíti a bekapcs és kikapcs mezőket
    kikapcs_ido = bekapcs_ido = round(60000 / (int(bpm_ertek) * 2)) if bpm_ertek.isdigit() and int(bpm_ertek) > 0 else 0
    # update StringVars instead of direct Entry manipulation
    bekapcs_var.set(str(bekapcs_ido))
    kikapcs_var.set(str(kikapcs_ido))
    
def ido_kuldes():
    # Meg lesz változtatva arra hogy ne is lehessen betűket beírni, addíg ez van
    try:
        bekapcs_ido = int(bekapcs_var.get())
        kikapcs_ido = int(kikapcs_var.get())
    except ValueError:
        set_status("Érvénytelen szám", "#ff0000")
        return

    # A serial adatküldés kezelése
    def worker():
        with serial_port_lock:
            sp = serial_port

        if sp and sp.is_open:
            try:
                line = f"{bekapcs_ido},{kikapcs_ido}\n"
                sp.write(line.encode("utf-8"))
                set_status("Elküldve", "#008000")
            except Exception as e:
                show_exception(str(e), "Küldési hiba")
                set_status("Lecsatlakozva", "#ff0000")
        else:
            set_status("Nincs csatlakoztatva port", "#ff0000")

    threading.Thread(target=worker, daemon=True).start() # nem tudom hogyan de mukodik

# tkinter ablak inicializálása
window = tk.Tk()
window.title("LED Villogtató")
window.geometry("300x350")
window.resizable(False, False)

# numeric input validator (allow only digits or empty)
def validate_numeric(P):
    return P == "" or P.isdigit()

# register validator with the Tk window
vcmd = window.register(validate_numeric)

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

# use StringVar for bekapcs and kikapcs so we can set them from code
bekapcs_var = tk.StringVar()
kikapcs_var = tk.StringVar()

# Bekapcsolt idő mező (numeric only)
tk.Label(left_frame, text="Bekapcs. idő (ms)", font=("Comic Sans MS", 10)).pack(pady=4)
bekapcs = tk.Entry(left_frame, width=10, textvariable=bekapcs_var, validate='key', validatecommand=(vcmd, '%P'))
bekapcs.pack(pady=4)

# kikapcsolt idő mező (numeric only)
tk.Label(left_frame, text="Kikapcs. idő (ms)", font=("Comic Sans MS", 10)).pack(pady=4)
kikapcs = tk.Entry(left_frame, width=10, textvariable=kikapcs_var, validate='key', validatecommand=(vcmd, '%P'))
kikapcs.pack(pady=4)

# BPM mező (numeric only)
tk.Label(left_frame, text="BPM", font=("Comic Sans MS", 10)).pack(pady=4)
bpm_var = tk.StringVar() # Tkinter StringVar a BPM érték tárolására (ennek segítségével tudom frissíteni a másik két mezőt)
bpm = tk.Entry(left_frame, width=10, textvariable=bpm_var, validate='key', validatecommand=(vcmd, '%P')) # BPM mező
bpm_var.trace_add("write", lambda *args: refresh(bpm_var.get())) # Automatikus frissítse a bekapcs és kikapcs mezőt a BPM alapján
bpm.pack(pady=4)

# --------------------------jobb oszlop--------------------------

# Állapot és küldés gomb jobb oldalon
tk.Label(right_frame, text="Állapot", font=("Comic Sans MS", 10, "bold")).pack(padx=8, pady=8)
allapot = tk.Label(right_frame, text="Lecsatlakozva", font=("Comic Sans MS", 10), fg="#ff0000") # Állapot címke
allapot.pack(pady=4)

tk.Button(right_frame, text="Küldés", font=("Comic Sans MS", 10), command=ido_kuldes).pack(pady=20) # Küldés gomb
tk.Label(right_frame, text="Soros Port:", font=("Comic Sans MS", 8)).pack(pady=4)

# port lista (dinamikusan frissíti elérhető portok alapján)
ports = [p.device for p in serial.tools.list_ports.comports()]
if not ports:
    ports = ["Nincs elérhető port"]
port_var = tk.StringVar(value=ports[0] if ports else "")
port_combo = ttk.Combobox(right_frame, textvariable=port_var, values=ports, state="readonly", width=10) # Soros port legördülő menü
port_combo.pack(pady=4)
port_combo.bind("<<ComboboxSelected>>", connect_serial)
tk.Button(right_frame, text="Frissít", font=("Comic Sans MS", 8), command=lambda: port_combo.configure(values=[p.device for p in serial.tools.list_ports.comports()])).pack(pady=4) # COM port lista frissítéséhez
# Egyszer próbálkozik csak, ne tartson sok időbe ha nem sikerül
connect_serial()

window.mainloop()