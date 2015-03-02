#!/bin/bash

# get path of Excalibur relative to location of this script
export EXCALIBURPATH=$(dirname $(dirname $(readlink -mf ${BASH_SOURCE[0]})))
export ARTUSPATH=$EXCALIBURPATH/../Artus

# source Artus ini script
source $EXCALIBURPATH/../Artus/Configuration/scripts/ini_ArtusAnalysis.sh

# set the environment
export BOOSTPATH=$(ls ${VO_CMS_SW_DIR}/${SCRAM_ARCH}/external/boost/* -d | tail -n 1)
export BOOSTLIB=${BOOSTPATH}/lib/libboost_regex.so.${BOOSTPATH/*\//}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ARTUSPATH:$BOOSTPATH/lib
export PATH=$PATH:$EXCALIBURPATH/scripts
export PYTHONPATH=$PYTHONPATH:$EXCALIBURPATH/python
export USERPC=`who am i | sed 's/.*(\([^]]*\)).*/\1/g'`


# Set some user specific variables
if [ $USER = "dhaitz" ]; then
    export EXCALIBUR_WORK=/storage/a/dhaitz/zjet
fi


# Use this to open a root file directly in the TBrowser
rot()
{
    ipython -i $EXCALIBURPATH/scripts/rot.py $@
}
