Excalibur
=========

Analysis repository for Z + jet studies.
It is based on [Artus](https://github.com/artus-analysis/Artus "Artus Analysis") which in turn is (largely) based on [Kappa](https://github.com/KappaAnalysis "Kappa and KappaTools").
The predecessor of this framework was also named excalibur and can be found [here](https://ekptrac.physik.uni-karlsruhe.de/trac/excalibur "excalibur")  (protected).

## Installation of the Excalibur Framework

### Requirements
This framework needs:
- python > 2.6
- boost
- ROOT
- GCC compiler

All that is most easily provided by installing CMSSW alongside:
```
cmsrel CMSSW_7_2_0
cd CMSSW_7_2_0/src
cmsenv
cd ../..
```
Alternatiely, all these tools can also be installed independently or taken from the system.

### Installation
The framework comes in 4 layers:

1. The data format definition of the input files: [Kappa](https://github.com/KappaAnalysis/Kappa "Kappa")
2. The basic interaction toolkit for this format: [KappaTools](https://github.com/KappaAnalysis/KappaTools "KappaTools")
3. The basic analysis framework to analyse the data: [Artus](https://github.com/artus-analysis/Artus "Artus")
4. The analysis specific program to do a Z+Jet(s) analysis: Excalibur

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
cmake Artus
make -C Artus -j4
make -C Excalibur
```


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


