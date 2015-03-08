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


# This function creates a folder with links to python directories, like SCRAM
# TODO enable merlin standalone usage without reinventing SCRAM ...
standalone_merlin(){
    export PYTHONLINKDIR=$EXCALIBURPATH/../python-links
    export PYTHONPATH=$PYTHONLINKDIR:$PYTHONPATH
    export PATH=$EXCALIBURPATH/Plotting/scripts:$PATH

    for j in Artus Excalibur; do
        # base dirs
        mkdir -p $PYTHONLINKDIR/$j
        touch $PYTHONLINKDIR/$j/__init__.py
        for i in `ls -d $(dirname $EXCALIBURPATH)/$j/*/python/`; do
            # create links to python dirs
            if [ ! -d $PYTHONLINKDIR/$j/$(basename $(dirname $i)) ]; then
                ln -s $(dirname $i)/python $PYTHONLINKDIR/$j/$(basename $(dirname $i))
            fi
            # create __init__.py in dirs and subdirs
            for k in `find $PYTHONLINKDIR/$j/*/ -type d`; do
                touch $k/__init__.py
            done
        done
    done
    source $EXCALIBURPATH/Plotting/scripts/ini_ZJetharry.sh
}
