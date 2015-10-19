#!/bin/bash

ALGO=${ALGO:-ak4PFJetsCHS}
QUANTITY=${QUANTITY:-npv}
BINNING=${BINNING:-"30,0.5,30.5"}
echo "(npv=="`merlin.py -x $QUANTITY -i $1 $2 --zjetf nocuts --corr L1L2L3 --algo $ALGO --analy NormalizeToFirstHisto Ratio --nicks-white ratio --log-l debug --x-bins $BINNING --y-lims 0 1 | grep fSumw | cut -d "=" -f 2 | cut -d "," -f 1 | while read i; do echo ")*${i}+(npv=="; done | nl | sed 's/ //g' | sed 's/\t//g' ` | sed 's/ //g' | sed 's/.\{7\}$//'
