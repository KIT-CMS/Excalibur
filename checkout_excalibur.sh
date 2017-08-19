#!/bin/bash
#
# Script for checking out all packages needed by Excalibur
##########################################################
#
# Note: this script should only be run in an empty CMSSW
#       working area (in the CMSSW_X_Y_Z/src/ directory)
#
# created:      2017-08-19
#

# -- preliminary checks

if [ -z "${CMSSW_BASE}" ]; then
    echo "[ERROR] Not in CMSSW working area: environment variable \$CMSSW_BASE is not set!"
    exit 1
fi

if [ "${CMSSW_BASE}/src" != "${PWD}" ]; then
    echo "[ERROR] Script must be run from the 'src' subdirectory of the current CMSSW working area: ${CMSSW_BASE}/src"
    exit 2
fi

if [ "$(ls $PWD)" ]; then
     echo "[ERROR] Directory '${PWD}' is not empty!"
     exit 3
fi


# -- check out necessary packages

# initialize empty CMSSW working directory in /src
git cms-init

# add package CondFormats/JetMETObjects from CMSSW
git cms-addpkg CondFormats/JetMETObjects

# check out Kappa
git clone https://github.com/KIT-CMS/Kappa.git
echo /Kappa >> .git/info/exclude  # exclude from outer CMSSW repo

# we don't need all of Kappa, just a few subdirectories -> sparse checkout
cd Kappa
echo docs/ >> .git/info/sparse-checkout
echo DataFormats/ >> .git/info/sparse-checkout
echo Skimming/data/ >> .git/info/sparse-checkout
echo Skimming/python/ >> .git/info/sparse-checkout
git config core.sparsecheckout true
git read-tree -mu HEAD
cd ..

# check out KappaTools (interface to Kappa files)
git clone https://github.com/KIT-CMS/KappaTools.git
echo /KappaTools >> .git/info/exclude  # exclude from outer CMSSW repo

# check out Artus (event data processing framework)
git clone https://github.com/KIT-CMS/Artus.git
echo /Artus >> .git/info/exclude  # exclude from outer CMSSW repo

# check out TauRefit (required by Kappa)
git clone https://github.com/KIT-CMS/TauRefit.git VertexRefit/TauRefit
echo /VertexRefit >> .git/info/exclude  # exclude from outer CMSSW repo

# check out JECDatabase (offline jet energy corrections)
git clone https://github.com/cms-jet/JECDatabase.git --depth=1
echo /JECDatabase >> .git/info/exclude  # exclude from outer CMSSW repo

# finally, check out Excalibur
git clone https://github.com/KIT-CMS/Excalibur.git
echo /Excalibur >> .git/info/exclude  # exclude from outer CMSSW repo


# optionally, check out
git clone https://github.com/grid-control/grid-control -b r1982 $CMSSW_BASE/../grid-control
