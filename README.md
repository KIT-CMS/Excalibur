Excalibur
=========

Analysis repository for Z + jet studies.
It is based on [Artus](https://github.com/artus-analysis/Artus "Artus Analysis") which in turn is (largely) based on [Kappa](https://github.com/KappaAnalysis "Kappa and KappaTools").
The predecessor of this framework was also named excalibur and can be found [here](https://ekptrac.physik.uni-karlsruhe.de/trac/excalibur "excalibur")  (protected).

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
git clone https://github.com/dhaitz/Excalibur.git
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

## Usage of the Excalibur Framework

### ZJetAnalysis: C++ part
to do

### Plotting: python part
This part derives some classes from HarryPlotter to implement ZJet-specific stuff.
See 
- Plotting/python/, which contains the derived classes
- Plotting/scripts/, which contains an ini script and the 'merlin' plotting executable

Source the ini file and type `merlin.py -h` to get a list of the plotting options.

Plot configs are stored as json or python files. Type `merlin.py --functions` to
get a list of the availabel plot configs.

##### Json
- Json configs can be directly saved from the command line with HarryPlotter's
--export-json functionality. These configs can later be read in again with -j, changed
and saved again. The "_comment" key has to be added manually and should contain
a short description of the plot.
- Plotting/data/json-configs/ contains some json files for plots

##### Python
- Python functions allow to construct loops of plots, but cannot be saved or read
as easily as json files. Execution of these functions with --python, a list of
the available functions can be displayed with --functions. The docstring of the
functions should contain a description.
- Plotting/data/python-configs/ contains some python plotting scripts
