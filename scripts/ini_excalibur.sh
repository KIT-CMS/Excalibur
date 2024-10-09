#!/bin/bash

if [ ! -z "$ZSH_VERSION" ]; then
    this_file="${(%):-%x}"
else
    this_file="${BASH_SOURCE[0]}"
fi

# get path of Excalibur relative to location of this script
export EXCALIBURPATH="$(dirname $(dirname $(readlink -mf "$this_file")))"
export EXCALIBURCONFIGS="$EXCALIBURPATH/cfg/excalibur"
export ARTUSPATH="$EXCALIBURPATH/../Artus"
export PLOTCONFIGS="$EXCALIBURPATH/Plotting/configs"
export PYTHONLINKDIR="$EXCALIBURPATH/../python-links"
export PATH="$PATH:$CMSSW_BASE/../grid-control:$CMSSW_BASE/../grid-control/scripts"

# source Artus ini script
source "$ARTUSPATH/Configuration/scripts/ini_ArtusAnalysis.sh"
export PATH="$ARTUSPATH/Utility/scripts:$PATH"

# set the environment
export BOOSTPATH="$(test ! -z ${CMSSW_BASE} && cd ${CMSSW_BASE} && scram tool info boost | sed -n 's/LIBDIR=//p')"
export BOOSTLIB="$(test ! -z ${CMSSW_BASE} && cd ${CMSSW_BASE} && scram tool info boost | sed -n 's/LIBDIR=/-L/p')"
export BOOSTINC="$(test ! -z ${CMSSW_BASE} && cd ${CMSSW_BASE} && scram tool info boost | sed -n 's/INCLUDE=/-isystem /p')"
export BOOSTVER="$(test ! -z ${CMSSW_BASE} && cd ${CMSSW_BASE} && scram tool info boost | sed -n 's/Version : //p')"

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$ARTUSPATH:$BOOSTPATH"
export PATH="$PATH:$EXCALIBURPATH/scripts:$ARTUSPATH/Utility/scripts:$ARTUSPATH/KappaAnalysis/scripts:$ARTUSPATH/Consumer/scripts:$ARTUSPATH/HarryPlotter/scripts"
export PYTHONPATH="$PYTHONPATH:$EXCALIBURPATH/cfg/python:$EXCALIBURPATH/cfg/excalibur:$PLOTCONFIGS:$PYTHONLINKDIR"
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
    _base_dir="${EXCALIBURPATH}/cfg/excalibur/"
    local names
    for i in `find "$_base_dir" -name "*.py"`; do
        # strip away common prefix
        _relative_path="${i#${_base_dir}}"
        # strip away '.py' extension and add as autocomplete candidate
        names="${names} ${_relative_path%.py}"
    done
    COMPREPLY=($(compgen -W "${names}" -- ${COMP_WORDS[COMP_CWORD]}))
}
complete -F _artuscomplete_ excalibur.py

if [ -d "/storage/a/$USER/zjet" ]; then
    export EXCALIBUR_WORK=/storage/a/$USER/zjet
fi


# Set some user specific variables
if [ "$USER" = "tberger" ]; then
    export EXCALIBURBRILSSH="tberger@lxplus.cern.ch"
    export HARRY_REMOTE_USER="tberger"
    export HARRY_USERPC="ekplx32.ekp.kit.edu"
    if [[ $HOSTNAME = *bms* ]]; then 
        #export EXCALIBUR_WORK=/storage/8/tberger/excalibur_work/
        export EXCALIBUR_WORK=/ceph/tberger/excalibur_work/
        export WEB_PLOTTING_MKDIR_COMMAND="mkdir -p /etpwww/web/${HARRY_REMOTE_USER}/public_html/plots_archive/{subdir}"
        export WEB_PLOTTING_COPY_COMMAND="rsync -u {source} /etpwww/web/${HARRY_REMOTE_USER}/public_html/plots_archive/{subdir}"
    else 
        export EXCALIBUR_WORK=~/storage/working/
    fi
    #export EXCALIBUR_SE="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Excalibur"
    export EXCALIBUR_SE="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Excalibur"
    #export EXCALIBUR_SE="srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/tberger/Excalibur"


elif [ "$USER" = "mschnepf" ]; then
    echo "Profile: mschnepf"
    export EXCALIBUR_WORK=/ceph/mschnepf/excalibur_work/
    export EXCALIBUR_SE="root://cmsdcache-kit-disk.gridka.de//store/user/mschnepf/Excalibur"
    GCPATH=/home/mschnepf/htcondor/grid-control
    export PATH=$PATH:$GCPATH:$GCPATH/scripts

    export HARRY_REMOTE_USER="mschnepf"
    export HARRY_USERPC="ekplx7.ekp.kit.edu"
    if [[ $HOSTNAME = *bms* ]]; then
         export WEB_PLOTTING_MKDIR_COMMAND="mkdir -p /ekpwww/web/mschnepf/public_html/plots_archive/{subdir}"
         export WEB_PLOTTING_COPY_COMMAND="rsync -u {source} /ekpwww/web/mschnepf/public_html/plots_archive/{subdir}"
    fi

elif [ "$USER" = "cverstege" ]; then
    echo "Profile: cverstege"
    export EXCALIBUR_WORK=/work/cverstege/gc_work/
    export EXCALIBUR_SE="root://cmsdcache-kit-disk.gridka.de//store/user/cverstege/Excalibur"

elif [ "$USER" = "mhorzela" ]; then
    echo "Profile: mhorzela"
    export EXCALIBUR_WORK=/work/mhorzela/ZJet/excalibur_work
    export EXCALIBUR_SE="root://cmsdcache-kit-disk.gridka.de//store/user/mhorzela/Excalibur"
fi

# source $ARTUSPATH/HarryPlotter/scripts/ini_harry.sh
alias cs='sh $EXCALIBURPATH/scripts/condor_status.sh'
