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


# Create worker node specific JSON file with correct list of input files
echo "#### Setup Workdir"
cd -
@WORKPATH@/json_modifier.py @WORKPATH@/@ARTUS_CONFIG@ $PWD

# Run analysis with config from worker node tmp dir
echo "#### Starting Artus..."
_TME_FILE='excalibur.tme'
if [[ $(which time) ]]; then
	# GNU time allows for extended format - use IEEE POSIX.2 as base
	$(which time) -o ${_TME_FILE} -f 'real %e\nuser %U\nsys %S\nrss %M\nmajor_pfault %F\nmajor_pfault%R\nwaits %w' excalibur @ARTUS_CONFIG@ || exit 1
elif [[ $(type time) ]]; then
	# use bash's time in POSIX.2 mode, clone pipes to separate streams
	exec 3>&1
	exec 4>&2
	{ time -p excalibur @ARTUS_CONFIG@ 1>&3 2>&4;} 1>${_TME_FILE} 2>&1 || exit 1
else
	echo "# no 'time' found" 1>&2
	excalibur @ARTUS_CONFIG@ || exit 1
fi

echo "#### Artus Performance"
if [[ -f ${_TME_FILE} ]]; then
	cat ${_TME_FILE}
else
	echo 'real -1'
	echo 'user -1'
	echo 'sys -1'
fi
