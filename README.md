Kantinens infoskærmssystem
==========================

`kantinfo.py` kører i en tmux på `infoscreen`-maskinen og `cokepc`-maskinen i
K@ntinen -- og måske andre steder?

Se https://github.com/datalogisk-kantineforening/infoscreen og
https://github.com/datalogisk-kantineforening/cokepc for de to vigtigste
systemer der bruger `kantinfo`-programmet.


Indhold
-------

Understøttede filtyper og deres handlinger:

  * `.html`, `.gif`: Vises i en browser
  * `.jpg`, `.png`: Vises i en billedfremviser
  * `.url`: Linket i filen åbnes enten i en browser eller i en videoafspiller,
    afhængigt af hvordan stien ser ud
  * `.sh`: Programmet køres
  * `.<noget>.eval`: Programmet køres, og dets uddata gemmes i en midlertidig fil
    med navnet `etellerandet.<noget>`, hvorefter dén fil køres
  * `.terminal`: Programmet køres i en grafisk terminal på infoskærmen


Konfiguration af slides
-----------------------

Hvert slide kan have en konfigurationsfil.  Hvis et slide hedder
`et-slide.endelse`, skal konfigurationsfilen hedde `et-slide.endelse.yaml`.
Filen skrives i YAML-formatet.  Følgende felter er understøttet:

  * `duration`: Tager et tal i sekunder og beskriver hvor lang tid et slide skal
    vises.  Standard er 20 sekunder.  Hvis `duration` er -1, vil scriptet ikke
    terminere slidet, men i stedet vente på at slidet terminerer sig selv.
  * `start_at` og `end_at` (begge skal gives): Beskriver det tidspunkt på dagen
    hvor et slide skal vises.
  * `probability`: Beskriver sandsynligheden for at et slide vises.  Standard er
    at et slide altid vises.  Angiv i intervallet 0 til 1.

Eksempel på konfigurationsfil der sørger for at et slide bliver vist i kun 10
sekunder:

    duration: 10

Eksempel på konfigurationsfil der sørger for at et slide bliver vist kun mellem
13 og 14:

    start_at: 13:00
    end_at: 14:00

Eksempel på konfigurationsfil, som tilbyder afspilning af vilkårlige udsnit af et filmslide.
Funktionen virker både med tidspunkter og hele sekunder.

    intervals: [['0:00' , '0:23'] , ['1:04', '1:30'] , [0, 500]]

Eksempel på konfigurationsfil, som tilbyder afspilning af bestemt udsnit af et filmslide:

    start_pos: 0:10
    end_pos: 1:40

eller

    start_pos: 41
    end_pos: 100


Ordre-sending
-------------

Man kan sende ordrer til en kørende `kantinfo.py` ved at køre
`kantinfo-order.py` og give ordrer på standard in.  `kantinfo.py` forstår
følgende ordrer:

  * `goto <slide>`: afbryd hvadend der foregår og skift så hurtigt som muligt
    til `<slide>`.


Afhængigheder
-------------

`kantinfo` afhænger af følgende programmer:

  + `python`
  + `pyyaml`: YAML-bibliotek til Python
  + `surf`: Simpel browser -- brug evt. https://github.com/Jobindex/surf
    for pænere skift mellem slides
  + `feh`: Simpel billedfremviser


Kodekopiering
-------------

Copyright © 2014-2015 Infoskærms-gruppen <infoskaerm@dikumail.dk>

This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See the COPYING file for more details.


Infoskærms-gruppen
------------------

Mest kodet af Troels og Niels.
