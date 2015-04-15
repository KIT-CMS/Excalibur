# Are we running on SLC6?
cat /etc/redhat-release

# List of files to be processed by Excalibur
echo $FILE_NAMES

# Set up CMSSW environment
cd @CMSSW_BASE@
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/
export SCRAM_ARCH=@SCRAM_ARCH@
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scram runtime -sh`
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:@WORKPATH@/lib

# Create worker node specific JSON file with correct list of input files
cd -
@WORKPATH@/json_modifier.py @WORKPATH@/@ARTUS_CONFIG@ $PWD

# Run analysis with config from worker node tmp dir
@WORKPATH@/artus @ARTUS_CONFIG@
