#!/bin/bash

# source Artus ini script
source $CMSSW_BASE/src/Artus/Configuration/scripts/ini_ArtusAnalysis.sh

# set the environment
export KAPPAPATH=$CMSSW_BASE/src/Kappa
export KAPPATOOLSPATH=$CMSSW_BASE/KappaTools
export ARTUSPATH=$CMSSW_BASE/src/Artus
export ZJETPATH=$CMSSW_BASE/src/ZJet/ZJetAnalysis

export USERPC=`who am i | sed 's/.*(\([^]]*\)).*/\1/g'`


# Set some user specific variables
if [ $USER = "dhaitz" ]; then
    export EXCALIBUR_WORK=/storage/a/dhaitz/zjet
fi
