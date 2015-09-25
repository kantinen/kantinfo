Kantinens infoskærmssystem
==========================

`infoscreen.py` kører i en tmux på infoskærmsmaskinen.


Indhold
-------

Alt indhold der bliver vist ligger i `content`-mappen.  Der er også mapperne
`content-disabled` og `background`, men disse er ikke vigtige for grundlæggende
kørsel.

Understøttede filtyper og deres handlinger:

  * `.html`, `.gif`: Vises i en browser
  * `.jpg`, `.png`: Vises i en billedfremviser
  * `.mkv`, `.webm`, `.mp4`, `.avi`, `.mp4`, `.ogv`: Vises i en videoafspiller
  * `.url`: Linket i filen åbnes i en browser
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

Eksempel på konfigurationsfil der sørger for at et slide bliver vist i kun 10
sekunder:

    duration: 10


Afhængigheder
-------------

Installér følgende programmer:

  + `matchbox`: Simpel window manager
  + `surf`: Simpel browser
  + `xdotool`: Musemarkør-skjuler (mm.)
  + `feh`: Simpel billedfremviser
  + `tmux`: Ligesom screen, men fra BSD
  
For at køre vores IRC-viser-slide, installér ogsa:

  + `sic`: Simpel IRC-klient
  + `toilet`: Tekst-formatterings-program


Opsætning
---------

Infoskærmen i kantinen køres på en ODroid, men en hvilken som helst datamat vil
være okay.

Infoskærmsmaskinen (herefter bare kaldet `odroid`) er en Odroid som er monteret
bag skærmen i kantinen.  Man kan logge ind på maskinen ved at ssh'e til
`odroid@diku.kantinen.org`.  Niels skal have ens offentlige nøgle før dette
virker.  Løsenet på maskinen for `odroid`-brugeren er bare `odroid`.

Når maskinen starter op, bliver brugeren `odroid` logget ind i en session, der
kører scriptet `.xinitrc`.  Vi har vedhæftet vores `.xinitrc` i dette repo; se
filen `xinitrc` (den er symlinket på odroiden).

Dette scripts primære ansvar er at starte en `tmux`-session der kører
infoskærmsscriptet, samt starte en enkel window manager.  Hvis du vil tilføje
andre baggrundsprocesser og deslige, så start dem her.

Et cronjob (`sudo crontab -e`) sørger for at genstarte maskinen hver morgen
klokken 6.  Dette er for at sikre at der aldrig sniger sig noget ind i
opsætningen der ikke kan overleve en genstart.

Vi har forsøgt at at lave et script til at sætte disse ting op automatisk på
Debian-baserede systemer; se `setup.sh`.  Det mangler dog meget.  Vi har også et
par andre scripts med mindre vigtige formål.

Specifikt for kantinen: Vær opmærksom på at alle odroids ser ud til at komme med
samme MAC-adresse (WTF??).  Nu hvor Kantinen har flere odroids i drift, er vi
nødt til manuelt at ændre deres MAC-adresser for at undgå konflikter.  Dette
håndteres af et script i stil med `setmac.sh`.  For at finde ud af hvilken
odroid som skal have hvilken MAC-adresse, kan man kigge i
`diku.kantinen.org:/etc/dhcp/dhcpd.conf`.  Scriptet kaldes fra `/etc/rc.local`
på odroiden.


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

Copyright © 2014-2015 Infoskærms-gruppen <infoskaerm@kantinen.org>

This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See the COPYING file for more details.


Infoskærms-gruppen
------------------

Mest kodet af Troels og Niels.
