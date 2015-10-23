#!/bin/bash

zenity --warning --text "Moechtest du wirklich einen plot machen?"

PLOT=$(zenity --list --column "plot" --text "Welchen plot willst du machen?" "zmass" "zpt")
NBINS=$(zenity --scale 0 100 --text "Wie viele Bins willst du verwenden?" --title "n bins:")

merlin.py --live evince --userpc --formats pdf -x $PLOT --x-bins $NBINS -i work/data.root

zenity --info --text "Erfolg!"
