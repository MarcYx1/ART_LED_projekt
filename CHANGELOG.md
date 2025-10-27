## Changelog

# firmware

# GUI
    v0.1
        - Alap GUI felépítve tkinterrel
        - GUI elemek elhelyezve még funkció nélkül
        - BPM átszámolása bekapcs kikapcs időbe függvény
        - README.md frissítve
    
    v0.2
        - Serial kapcsolat implementálva
        - COM port választó input
        - Státusz label a serial kapcsolat alapján frissül
        - Threading-el több szálon futtatás mivel a tkinter loopban elindított serial kapcsolat timeout-hoz vezet
    
    v0.3
        - Mostmár csak számokat lehet beírni a mezőkbe
        - Readme frissítve (v0.2 és v0.3 változásokkal)