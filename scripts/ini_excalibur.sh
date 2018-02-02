#!/bin/bash

# get path of Excalibur relative to location of this script
export EXCALIBURPATH=$(dirname $(dirname $(readlink -mf ${BASH_SOURCE[0]})))
export EXCALIBURCONFIGS=$EXCALIBURPATH/cfg/excalibur
export ARTUSPATH=$EXCALIBURPATH/../Artus
export PLOTCONFIGS=$EXCALIBURPATH/Plotting/configs
export PYTHONLINKDIR=$EXCALIBURPATH/../python-links
export PATH=$PATH:$CMSSW_BASE/../grid-control:$CMSSW_BASE/../grid-control/scripts
source /cvmfs/grid.cern.ch/emi3ui-latest/etc/profile.d/setup-ui-example.sh

# source Artus ini script
source $ARTUSPATH/Configuration/scripts/ini_ArtusAnalysis.sh
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
if [ $USER = "cheidecker" ]; then
    export EXCALIBURBRILSSH="cheideck@lxplus.cern.ch"
    export EXCALIBUR_WORK=/portal/ekpbms2/home/cheidecker/zjets/
elif [ $USER = "wayand" ]; then
    echo "Hallo Stefan, schoen dich zu sehen "
    #export EXCALIBUR_WORK=/storage/8/wayand/zjets/
    export EXCALIBUR_WORK=/portal/ekpbms1/home/wayand/JEC/
    export EXCALIBURBRILSSH="swayand@lxplus.cern.ch"
elif [ $USER = "swayand" ]; then
    echo "Hallo Stefan, schoen dich auf der NAF zu sehen "
    export EXCALIBUR_WORK=/nfs/dust/cms/user/swayand/JEC/
    export EXCALIBUR_SE="srm://dgridsrm-fzk.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/dcms/disk-only/store/user/swayand/excalibur/"
    export EXCALIBURBRILSSH="swayand@lxplus.cern.ch"
    export HARRY_REMOTE_USER="wayand"
    export HARRY_USERPC="ekplx23.physik.uni-karlsruhe.de"
elif [ $USER = "afriedel" ]; then
    export EXCALIBURBRILSSH="afriedel@lxplus.cern.ch"
    export EXCALIBUR_WORK=/storage/a/afriedel/zjets/
    export EXCALIBUR_SE="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/afriedel/Excalibur"
elif [ $USER = "tberger" ]; then
    export EXCALIBURBRILSSH="tberger@lxplus.cern.ch"
    if [[ $HOSTNAME = *ekpbms* ]]; then 
        #export EXCALIBUR_WORK=/home/tberger/excalibur_work/
        export EXCALIBUR_WORK=/storage/c/tberger/excalibur_work/
    else 
        export EXCALIBUR_WORK=~/storage/working/
    fi
    export HARRY_REMOTE_USER="tberger"
    export HARRY_USERPC="ekplx32.ekp.kit.edu"
    #export EXCALIBUR_SE="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/tberger/Excalibur"
    export EXCALIBUR_SE="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/tberger/Excalibur"
    #export EXCALIBUR_SE="srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/tberger/Excalibur"
elif [ $USER = "dsavoiu" ]; then
    export EXCALIBURBRILSSH="dsavoiu@lxplus.cern.ch"
    #export EXCALIBUR_WORK=/portal/ekpbms1/home/dsavoiu/excalibur_work
    export EXCALIBUR_WORK=/storage/c/dsavoiu/excalibur_work
    #export EXCALIBUR_SE="srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/dsavoiu/Excalibur"
    export EXCALIBUR_SE="srm://cmssrm-kit.gridka.de:8443/srm/managerv2?SFN=/pnfs/gridka.de/cms/disk-only/store/user/dsavoiu/Excalibur"
    export HARRY_REMOTE_USER="dsavoiu"
    export HARRY_USERPC="ekplx32.ekp.kit.edu"
fi
source $ARTUSPATH/HarryPlotter/scripts/ini_harry.sh
alias cs='sh $EXCALIBURPATH/scripts/condor_status.sh'

