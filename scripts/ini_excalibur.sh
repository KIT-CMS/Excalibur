#!/bin/bash

# source Artus ini script
source ../Artus/Configuration/scripts/ini_ArtusAnalysis.sh

# set the environment
export EXCALIBURPATH=$(readlink -e .)
export BOOSTPATH=$(ls ${VO_CMS_SW_DIR}/${SCRAM_ARCH}/external/boost/* -d | tail -n 1)
export BOOSTLIB=${BOOSTPATH}/lib/libboost_regex.so.${BOOSTPATH/*\//}
export KAPPAPATH=$EXCALIBURPATH/../Kappa
export KAPPATOOLSPATH=$EXCALIBURPATH/../KappaTools
export ARTUSPATH=$EXCALIBURPATH/../Artus
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ARTUSPATH:$KAPPAPATH/lib:$KAPPATOOLSPATH/lib:$BOOSTPATH/lib
export PATH=$PATH:$EXCALIBURPATH/scripts

export USERPC=`who am i | sed 's/.*(\([^]]*\)).*/\1/g'`


# Set some user specific variables
if [ $USER = "dhaitz" ]; then
    export EXCALIBUR_WORK=/storage/a/dhaitz/zjet
fi
