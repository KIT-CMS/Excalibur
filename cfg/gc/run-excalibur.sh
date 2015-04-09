echo $FILE_NAMES
cd $CMSSW_BASE
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/
export SCRAM_ARCH=$SCRAM_ARCH
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scram runtime -sh`
cd -
cd $EXCALIBURPATH
source $EXCALIBURPATH/scripts/ini_excalibur.sh
cd -
$EXCALIBURPATH/artus $EXCALIBURPATH/cfg/excalibur/config.py.json
