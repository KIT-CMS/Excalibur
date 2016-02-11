# Are we running on SLC6?
echo "#### OS Release"
# try OS specific information
if [[ -f "/etc/redhat-release" ]]; then
	cat /etc/redhat-release
else
	echo "unknown OS"
fi
# always provide general information
uname -a

# List of files to be processed by Excalibur
echo "#### Input Files"
echo $FILE_NAMES

# Set up CMSSW environment
echo "#### Setup CMSSW"
cd @CMSSW_BASE@
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/
export SCRAM_ARCH=@SCRAM_ARCH@
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scram runtime -sh`
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:@WORKPATH@/lib

# Create worker node specific JSON file with correct list of input files
echo "#### Setup Workdir"
cd -
@WORKPATH@/json_modifier.py @WORKPATH@/@ARTUS_CONFIG@ $PWD

# Run analysis with config from worker node tmp dir
echo "#### Starting Artus..."
if [[ $(which time) ]]; then
	# GNU time allows for extended format - use IEEE POSIX.2 as base
	$(which time) -f 'real %e\nuser %U\nsys %S\nrss %M\nmajor_pfault %F\nmajor_pfault%R\nwaits %w' @WORKPATH@/artus @ARTUS_CONFIG@
elif [[ $(type time) ]]; then
	# use bash's time in POSIX.2 mode
	time -p @WORKPATH@/artus @ARTUS_CONFIG@
else
	echo "# no 'time' found" 1>&2
	@WORKPATH@/artus @ARTUS_CONFIG@
fi
