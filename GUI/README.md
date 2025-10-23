# LED Villogtató (GUI)

Egyszerű Tkinter-es GUI a LED villogtatásához

Rövid leírás
 - Három beviteli mező a sebesség megadására, bekapcs idő, kikapcs idő és BPM
 - Serial kapcsolat állapot kijelzés
 - Küldés gomb ami a seriállal a mikrokontrollerre küldi a bekapcs kikapcs időt

TODO-k
 - Serial port integráció (valszeg pyserial-al) és a küldés tényleges implementálása.
 - Az entry-k jelenleg bármilyen szöveget befogadnak (tkinter csodája) csak számokat engedjen
 - A BPM mező törlése ha kézzel átírom a bekapcs vagy kikapcs időt
 - Választható serial port és az "Állapot" label valós idejű frissítése.
 - Ha minden kész buildelni exe-be (valszeg pyinstaller)

Fontos:
Egyenlőre ez csak nagyon ideiglenes ablak, valószínüleg sokat fog változni még a beágy.-os igényektől függően