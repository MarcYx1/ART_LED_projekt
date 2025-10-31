## Changelog

# firmware
    v0.1
        - Worskpace feltöltve
        - Még csak hardcode-olt villogás
    
    v0.2
        - Fogadja serialon a adatokat és müködik a villogtatás
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

    v0.4
        - Hozzáadtam egy "Frissítés" gombot ami a COM portok listáját frissíti
        - Readme frissítve

    v0.5
        - .pyw-re átneveztem hogy futtató cmd ne látszódjon