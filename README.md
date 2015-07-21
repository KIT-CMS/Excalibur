Excalibur
=========

Analysis repository for Z + jet studies and jet energy calibration.
It is based on [Artus](https://github.com/artus-analysis/Artus "Artus Analysis") which in turn is (largely) based on [Kappa](https://github.com/KappaAnalysis "Kappa and KappaTools").
The predecessor of this framework was also named excalibur and can be found [here](https://ekptrac.physik.uni-karlsruhe.de/trac/excalibur "excalibur")  (protected).

Please also have a look at the documentation for [Artus](https://github.com/artus-analysis/Artus/blob/master/README.md "Artus Readme") and [HarryPlotter](https://github.com/artus-analysis/Artus/blob/master/HarryPlotter/README.md "HarryPlotter Readme").

## Installation of the Excalibur Framework

### Requirements
This framework needs:
- python >= 2.6
- boost >= 1.50
- ROOT >= 5.34
- GCC compiler

All that is most easily provided by installing CMSSW alongside and taking the offline jet corrections from there (in CondFormats):
```
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/
export SCRAM_ARCH=slc6_amd64_gcc481
source $VO_CMS_SW_DIR/cmsset_default.sh
cmsrel CMSSW_7_2_0
cd CMSSW_7_2_0/src
cmsenv
#git cms-addpkg CondFormats/JetMETObjects
cd ../..
#ln -s CMSSW_7_2_0/src/CondFormats
# temporary solution because 7x does not compile here:
cp -r /portal/ekpcms5/home/berger/zjet/excalibur/external/OfflineCorrection/CondFormats ./
```
Alternatively, all these requirements can also be installed independently or taken from the system.

### Installation
The framework comes in 4 layers:

1. The data format definition of the input files: [Kappa](https://github.com/KappaAnalysis/Kappa "Kappa")
2. The basic interaction toolkit for this format: [KappaTools](https://github.com/KappaAnalysis/KappaTools "KappaTools")
3. The basic analysis framework to analyse the data: [Artus](https://github.com/artus-analysis/Artus "Artus")
4. The analysis specific program to do a Z+Jet(s) or calibration analysis: Excalibur

To install these packages check them out using [git](http://git-scm.com/ "git"):
```
git clone https://github.com/KappaAnalysis/Kappa.git
git clone https://github.com/KappaAnalysis/KappaTools.git
git clone https://github.com/artus-analysis/Artus.git
git clone https://github.com/artus-analysis/Excalibur.git
```

In a next step you need to compile all those packages:
```
make -C Kappa/DataFormats/test
make -C KappaTools
cd Artus ; cmake . ; make -j4 ; cd ..
cd Excalibur
. scripts/ini_excalibur.sh
make
```
(todo: a script should do that and the Makefile should fully handle all parts)

after having done so, it can also be compile with `make` in the parent directory
or with `make project` in Excalibur.

The preceeding implementation can be found at: https://ekptrac.physik.uni-karlsruhe.de/trac/excalibur -
many ideas were and can still be taken from there.


## Usage of the Excalibur Framework

### ZJetAnalysis: C++ part
excalibur.py is the wrapper to run this Z+jet calibration tool. The first argument is the name of a config file located in `cfg/excalibur/` (the filename extension is optional). This config file takes parts from `ZJetConfigFunctions.py` as the base config which is then modified by `ZJetConfigBase.py`. The final json output will be used for the z+jet calibration tool.

Optional useful arguments are
- `-b` batch mode. This parameters takes an optional argument for the computing
resource use. See `-h`
- `-c` only create config and exit
- `-f n` use only `n` input files

Examples
- `excalibur.py data` to use the data.py config
- `excalibur.py mc -b -f 100` to use the mc.py config in batch mode with only 100 input files

Links to 'official' output files (which can be used by all users for plotting etc.)
are stored in the ntuples/ folder.

### Plotting (merlin): python part
This part derives some classes from HarryPlotter to implement ZJet-specific stuff.
See 
- Plotting/python/, which contains the derived classes
- scripts/, which contains an ini script and the 'merlin' plotting executable
- Plotting/plot-configs/, which contains json and python plot config files

Please also have a look at the [HarryPlotter documentation](https://github.com/artus-analysis/Artus/blob/master/HarryPlotter/README.md "HarryPlotter Readme").

Source the ini file. Since HarryPlotter is designed for SCRAM, you need to execute
the shell function  `standalone_merlin` if you're using merlin outside a SCRAM
environment for the first time.(and re-source the ini file).
Type `merlin.py --help` to get a list of the plotting options.

Plot configs are stored as json or python files. Type `merlin.py --list-functions` to
get a list of the available plot configs.

##### InputRootZJet
merlin has the additional --zjetfolder, --algorithms and --corrections arguments.
From these arguments, the folder name is constructed, according to the ZJet folder
naming convention "ZJetFolder_AlgorithmCorrection".

By default, MC histograms (from Artus root files) are scaled to the given
luminosity (--lumi) if at least one Data file is used for plotting.

The quantities.py file in Plotting/python/utiliy contains a dictionary for quantity
aliases. E.g., type 'ptbalance' and this will be replaced with 'jet2pt/zpt'.

The binnings.py file in Plotting/python/utiliy contains a dictionary for special
binnings for ZpT, jet eta, Npv. If you use e.g. `--x-bins zpt` (or dictionary key),
the binning is replaced with the values from this dictionary.

When plotting from a TTree/TNtuple, the 'weight' entry is automatically used as
weight. Diable this with `--no-weight`.

##### PlotMplZJet
The --cutlabel argument places a label with the used cuts (Z pT, abs(jet1eta),
 alpha) on the plot.
The plot axes can be automatically labelled via the entries of the LabelsDict in
Plotting/python/utility/labelsZJet.py (simple strings like 'zpt' are replaced with
nicer Latex labels).


##### Json plot configs
- Json configs can be directly saved from the command line with HarryPlotter's
--export-json functionality. These configs can later be read in again with -j, changed
and saved again. The "_comment" key has to be added manually and should contain
a short description of the plot.
- Plotting/plot-configs/json-configs/ contains some json files for plots


##### Python plot configs
- Python functions allow to construct loops of plots, but cannot be saved or read
as easily as json files. Execution of these functions with --python, a list of
the available functions can be displayed with --list-functions. The docstring of
the functions should contain a description.
- Plotting/plot-configs/python-configs/ contains some python plotting scripts
