Kantinens infoskærmssystem.

infoscreen.py kører i en tmux på infoskærmsmaskinen.

Sådan gør man
-------------

Grundet vor sofistikerede og fremskredne teknologi er det ikke enkelt
at starte infoskærmen.  Her er den nutids-kompatible procedure:

  0) Log ind på odroid-maskinen med odroid-brugeren.

  1) Start en tmux.

  2) Gå ind i 'infoscreen'-mappen.

  3) Kør: export DISPLAY=:0

  4) Kør: dbus-launch ./infoscreen.py

  5) Vent til maskinen crasher, gå derefter til 0.
