#!/bin/bash

export OUT="-o plots/dpg_new"

python scripts/zee-bkgrs.py $OUT
python scripts/zee-uncertainties.py $OUT
python scripts/zee-unfolded.py $OUT
python scripts/zee-unfolding-mc-crosscheck.py $OUT

merlin.py -j jsons/ee-bkgrs.json $OUT
merlin.py -j jsons/ee-recogen-2D.json $OUT
merlin.py -j jsons/ee-recogen.json $OUT
merlin.py -j jsons/efficiency_pt.json $OUT
merlin.py -j jsons/fakerate_pt.json $OUT
merlin.py -j jsons/hlt.json $OUT
merlin.py -j jsons/purity_pt.json $OUT
merlin.py -j jsons/roc.json $OUT
