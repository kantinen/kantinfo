Kantinens infoskærmssystem
==========================

`infoscreen.py` kører i en tmux på infoskærmsmaskinen.

Indhold
-------

Alt indhold der bliver vist ligger i `content`-mappen.

Understøttede filer:

  * `.html`, `.gif`: Vises i en browser
  * `.jpg`, `.png`: Vises i en billedfremviser
  * `.mkv`, `.webm`, `.mp4`, `.avi`, `.mp4`, `.ogv`: Vises i en videoafspiller
  * `.url`: Linket i filen åbnes
  * `.sh`: Programmet køres
  * `.terminal`: Programmet køres i en grafisk terminal på infoskærmen

Design efter en opløsning på 1920x1080.

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

Opsætning
---------

Infoskærmsmaskinen (herefter bare kaldet `odroid`) er en Odroid som er monteret
bag skærmen i kantinen.  Man kan logge ind på maskinen ved at ssh'e til
`odroid@diku.kantinen.org`.  Niels skal have ens offentlige nøgle før dette
virker.  Løsenet på maskinen er bare `odroid`.

Når maskinen starter op, bliver brugeren `odroid` logget ind i en session, der
kører scriptet `.xinitrc`.  Vi har vedhæftet vores `.xinitrc` i dette repo.

Dette scripts primære ansvar er at starte en `tmux`-session der kører
infoskærmsscriptet, samt starte en enkel window manager.  Hvis du vil
tilføje andre baggrundsprocesser og deslige, så start dem her.

`odroid` er en rimeligt hurtig maskine, *bortset* fra dens faste
lager, som er verdens mest langso^Wgrundige Micro-SD-kort.  Hvis det
virker som om den hænger, så er det sandsynligvis bare fordi den læser
fra kortet.

Et cronjob (`sudo crontab -e`) sørger for at genstarte maskinen hver
morgen klokken 6.  Dette er for at sikre at der aldrig sniger sig
noget ind i opsætningen der ikke kan overleve en genstart.

Vær i øvrigt opmærksom på at alle odroids ser ud til at komme med samme
MAC-adresse (WTF??). Nu hvor vi har flere odroids i drift i kantinen skal bliver man
nødt til manuelt at ændre deres MAC-adresser for at undgå konfliklter. Dette
håndteres af et script i stil med setmac.sh. For at finde ud af hvilken maskine
som skal have hvilken MAC-adresse kan man kikke i
'diku.kantinen.org:/etc/dhcp/dhcpd.conf'. Scriptet kaldes fra /etc/rc.local på odroiden.

Sådan gør man manuelt
---------------------

*Lad være med at gøre det her.  Genstart maskinen i stedet.*

Grundet vor sofistikerede og fremskredne teknologi er det ikke enkelt
at starte infoskærmen.  Her er den nutids-kompatible procedure:

  0) Log ind på odroid-maskinen med odroid-brugeren.

  1) Start en tmux.

  2) Gå ind i `infoscreen`-mappen.

  3) Kør: export DISPLAY=:0

  4) Kør: dbus-launch ./infoscreen.py

  5) Vent til maskinen crasher, gå derefter til 0.

Afhængigheder
-------------

Installér følgende programmer:

  + `matchbox`
  + `surf`
  + `feh`
  + `sic`
  + `xdotool`
  + `tmux`
  + `toilet`
