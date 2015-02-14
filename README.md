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
make Excalibur
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

data/json/ contains some json files for plots
python/ contains the derived classes
scripts/ contains an ini script and the 'merlin' plotting executable
python/scripts/ contains some plotting scripts

source the ini file and type "merlin.py -h" to get a list of the plotting options

