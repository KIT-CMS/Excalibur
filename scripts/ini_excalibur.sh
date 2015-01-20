#!/bin/bash

# source Artus ini script
source ../Artus/Configuration/scripts/ini_ArtusAnalysis.sh

# set the environment
export EXCALIBURPATH=$(readlink -e .)
export KAPPAPATH=$EXCALIBURPATH/../Kappa
export KAPPATOOLSPATH=$EXCALIBURPATH/../KappaTools
export ARTUSPATH=$EXCALIBURPATH/../Artus

export USERPC=`who am i | sed 's/.*(\([^]]*\)).*/\1/g'`


# Set some user specific variables
if [ $USER = "dhaitz" ]; then
    export EXCALIBUR_WORK=/storage/a/dhaitz/zjet
fi
