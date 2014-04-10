#!/bin/bash

# source Artus ini script
source $CMSSW_BASE/src/Artus/Configuration/scripts/ini_ArtusAnalysis_cmssw.sh

# set the environment
export KAPPAPATH=$CMSSW_BASE/src/Kappa
export KAPPATOOLSPATH=$CMSSW_BASE/KappaTools
export ARTUSPATH=$CMSSW_BASE/src/Artus
export ZJETPATH=$CMSSW_BASE/src/ZJet/ZJetAnalysis
