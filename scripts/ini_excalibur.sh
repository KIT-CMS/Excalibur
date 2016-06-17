#!/bin/bash

# get path of Excalibur relative to location of this script
export EXCALIBURPATH=$(dirname $(dirname $(readlink -mf ${BASH_SOURCE[0]})))
export EXCALIBURCONFIGS=$EXCALIBURPATH/cfg/excalibur
export ARTUSPATH=$EXCALIBURPATH/../Artus
export PLOTCONFIGS=$EXCALIBURPATH/Plotting/configs
export PYTHONLINKDIR=$EXCALIBURPATH/../python-links

# source Artus ini script
source $ARTUSPATH/Configuration/scripts/ini_ArtusAnalysis.sh
source $ARTUSPATH/HarryPlotter/scripts/ini_harry.sh
export PATH=$ARTUSPATH/Utility/scripts:$PATH

# set the environment
export BOOSTPATH=$(test ! -z ${CMSSW_BASE} && cd ${CMSSW_BASE} && scram tool info boost | sed -n 's/LIBDIR=//p')
export BOOSTLIB=$(test ! -z ${CMSSW_BASE} && cd ${CMSSW_BASE} && scram tool info boost | sed -n 's/LIBDIR=/-L/p')
export BOOSTINC=$(test ! -z ${CMSSW_BASE} && cd ${CMSSW_BASE} && scram tool info boost | sed -n 's/INCLUDE=/-isystem /p')
export BOOSTVER=$(test ! -z ${CMSSW_BASE} && cd ${CMSSW_BASE} && scram tool info boost | sed -n 's/Version : //p')

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ARTUSPATH:$BOOSTPATH
export PATH=$PATH:$EXCALIBURPATH/scripts:$ARTUSPATH/Utility/scripts:$ARTUSPATH/KappaAnalysis/scripts:$ARTUSPATH/Consumer/scripts:$ARTUSPATH/HarryPlotter/scripts
export PYTHONPATH=$PYTHONPATH:$EXCALIBURPATH/cfg/python:$EXCALIBURPATH/cfg/excalibur:$PLOTCONFIGS:$PYTHONLINKDIR
export USERPC=`who am i | sed 's/.*(\([^]]*\)).*/\1/g'`

# This function creates a folder with links to python directories, like SCRAM
# TODO enable merlin standalone usage without reinventing SCRAM ...
standalone_merlin(){
    for j in Artus Excalibur Kappa; do
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
}

# excalibur.py auto-completion
function _artuscomplete_()
{
    local names
    for i in `ls ${EXCALIBURPATH}/cfg/excalibur/*.py`
        do names="${names} `basename $i .py`"
    done
    COMPREPLY=($(compgen -W "${names}" -- ${COMP_WORDS[COMP_CWORD]}))
}
complete -F _artuscomplete_ excalibur.py

if [ -d "/storage/a/$USER/zjet" ]; then
    export EXCALIBUR_WORK=/storage/a/$USER/zjet
fi

# Set some user specific variables
if [ $USER = "mfischer" ]; then
    if [[ $HOSTNAME == *"naf"* ]]; then
        export PATH=$PATH:$EXCALIBURPATH/../grid-control:$EXCALIBURPATH/../grid-control
        export EXCALIBUR_WORK=/nfs/dust/cms/user/mfischer/calib/gc-work/excalibur/
        export EXCALIBURBRILSSH="mafische@lxplus.cern.ch"
    fi
elif [ $USER = "cheidecker" ]; then
    export EXCALIBURBRILSSH="cheideck@lxplus.cern.ch"
    export EXCALIBUR_WORK=/storage/a/cheidecker/zjets/
elif [ $USER = "wayand" ]; then
    echo "Hallo Stefan, schoen dich zu sehen "
    export PATH=$PATH:$EXCALIBURPATH/../grid-control:$EXCALIBURPATH/../grid-control/scripts
    export EXCALIBUR_WORK=/storage/8/wayand/zjets/
    export EXCALIBURBRILSSH="swayand@lxplus.cern.ch"
elif [ $USER = "afriedel" ]; then
    export EXCALIBURBRILSSH="afriedel@lxplus.cern.ch"
    export EXCALIBUR_WORK=/storage/a/afriedel/zjets/
elif [ $USER = "tberger" ]; then
    export EXCALIBURBRILSSH="tberger@lxplus.cern.ch"
    export EXCALIBUR_WORK=/storage/jbod/tberger/zjets/
fi
