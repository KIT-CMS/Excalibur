Excalibur
=========

Analysis repository for Z + jet studies.
It is based on [Artus](https://github.com/artus-analysis/Artus "Artus Analysis")
which in turn is (largely) based on [Kappa](https://github.com/KappaAnalysis "Kappa and KappaTools").

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

To install these packages check them out using [git]():
```
git clone https://github.com/KappaAnalysis/Kappa.git
git clone -b dictchanges https://github.com/KappaAnalysis/KappaTools.git
git clone https://github.com/artus-analysis/Artus.git
git clone https://github.com/dhaitz/Excalibur.git
```

In a next step you need to compile all those packages:
```
make -C Kappa/DataFormats/test
make -C KappaTools
cd Artus
cmake .
make -j4
cd ../Excalibur
make
```