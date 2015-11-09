Kantinens infoskærmssystem
==========================

`kantinfo.py` kører i en tmux på `infoscreen`-maskinen og `cokepc`-maskinen i
K@ntinen -- og måske andre steder?

Se https://github.com/datalogisk-kantineforening/infoscreen og
https://github.com/datalogisk-kantineforening/cokepc for de to vigtigste system
der bruger `kantinfo`-programmel.


Indhold
-------

Understøttede filtyper og deres handlinger:

  * `.html`, `.gif`: Vises i en browser
  * `.jpg`, `.png`: Vises i en billedfremviser
  * `.url`: Linket i filen åbnes enten i en browser eller i en videoafspiller,
    afhængigt af hvordan stien ser ud
  * `.sh`: Programmet køres
  * `.terminal`: Programmet køres i en grafisk terminal på infoskærmen

Infoskærmen har en opløsning på 1920x1080, så design efter det.


Konfiguration af slides
-----------------------

Hvert slide kan have en konfigurationsfil.  Hvis et slide hedder
`et-slide.endelse`, skal konfigurationsfilen hedde `et-slide.endelse.yaml`.
Filen skrives i YAML-formatet.  Følgende felter er understøttet:

  * `duration`: Tager et tal i sekunder og beskriver hvor lang tid et slide skal
    vises.  Standard er 20 sekunder.
  * `start_at` og `end_at` (begge skal gives): Beskriver det tidspunkt på dagen
    hvor et slide skal vises.
  * `probability`: Beskriver sandsynligheden for at et slide vises.  Standard er
    at et slide altid vises.  Angiv i intervallet 0 til 1.

Eksempel på konfigurationsfil der sørger for at et slide bliver vist i kun 10
sekunder:

    duration: 10


Afhængigheder
-------------

Installér følgende programmer:

  + `python`
  + `matchbox`: Simpel window manager
  + `surf`: Simpel browser
  + `xdotool`: Musemarkør-skjuler (mm.)
  + `feh`: Simpel billedfremviser
  + `tmux`: Ligesom screen, men fra BSD
  
For at køre vores IRC-viser-slide, installér ogsa:

  + `sic`: Simpel IRC-klient
  + `toilet`: Tekst-formatterings-program


Sådan gør man manuelt
---------------------

*Lad være med at gøre det her.  Sæt i stedet .xinitrc op og genstart maskinen.*

Grundet vor sofistikerede og fremskredne teknologi er det ikke enkelt at starte
infoskærmen.  Her er den nutids-kompatible procedure:

  0. Log ind på odroid-maskinen med brugeren `odroid`.
  1. Start en tmux.
  2. Gå ind i `infoscreen`-mappen.
  3. Kør: `export DISPLAY=:0`
  4. Kør: `dbus-launch ./infoscreen.py`
  5. Vent til maskinen crasher, gå derefter til 0.


Kodekopiering
-------------

Copyright © 2014-2015 Infoskærms-gruppen <infoskaerm@dikumail.dk>

This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See the COPYING file for more details.


Infoskærms-gruppen
------------------

Mest kodet af Troels og Niels.
