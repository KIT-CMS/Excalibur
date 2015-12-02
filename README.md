Excalibur
=========

[![Build Status](https://travis-ci.org/artus-analysis/Excalibur.svg)](https://travis-ci.org/artus-analysis/Excalibur)

Analysis repository for Z + jet studies and jet energy calibration.
It is based on [Artus](https://github.com/artus-analysis/Artus "Artus Analysis") which in turn is (largely) based on [Kappa](https://github.com/KappaAnalysis "Kappa and KappaTools").
The predecessor of this framework was also named excalibur and can be found [here](https://ekptrac.physik.uni-karlsruhe.de/trac/excalibur "excalibur")  (protected).

Please also have a look at the documentation for [Artus](https://github.com/artus-analysis/Artus/blob/master/README.md "Artus Readme") and [HarryPlotter](https://github.com/artus-analysis/Artus/blob/master/HarryPlotter/README.md "HarryPlotter Readme").

## Installation of the Excalibur Framework

### Requirements
This framework needs:
- python >= 2.6
- boost >= 1.50
- ROOT == 5.34
- GCC compiler >= 4.8

All that is most easily provided by installing CMSSW alongside and taking the offline jet corrections from there (in CondFormats):
```
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/
export SCRAM_ARCH=slc6_amd64_gcc481
source $VO_CMS_SW_DIR/cmsset_default.sh
cmsrel CMSSW_7_4_0_pre9
cd CMSSW_7_4_0_pre9/src
cmsenv
#git cms-addpkg CondFormats/JetMETObjects
cd ../..
#ln -s CMSSW_7_4_0_pre9/src/CondFormats
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
cd Excalibur
. scripts/ini_excalibur.sh
make all
```
As an alternative to this command, you can also compile all four
repositories by hand:
```
make -B -C Kappa/DataFormats/test
make -j4 -B -C KappaTools
cd Artus ; cmake . ; make -B -j4 ; cd ..
cd Excalibur
. scripts/ini_excalibur.sh
make -j4 -B
```

The preceeding implementation can be found at: https://ekptrac.physik.uni-karlsruhe.de/trac/excalibur -
many ideas were and can still be taken from there.


## Usage of the Excalibur Framework

There are two parts in this repository (listed with the corresponding top level folders):
- Excalibur (C++ code + python configs) doing the analysis and producing flat trees
    - Makefile
    - `cfg` (configuration)
    - `data` (correction factors, weight files, etc.)
    - `ntuples` (links to skims used as input files)
    - `scripts` (init scripts etc.)
    - `src` (the code)
    - `test` (test scripts)

- Merlin (python plotting code) producing plots from the flat trees.
    - plotting (Merlin code and configs)
    - plots (ouput files created by Merlin)
    - websync (temporary folder for web sync with `--www`)


### ZJetAnalysis: C++ part
excalibur.py is the wrapper to run this Z+jet calibration tool. The first argument
is the name of a config file located in `cfg/excalibur/` (the filename extension
is optional). This config file takes parts from `ZJetConfigFunctions.py` as the
base config which is then modified by `ZJetConfigBase.py`. The final json output
will be used for the z+jet calibration tool.

Optional useful arguments are
- `-b` batch mode. This parameters takes an optional argument for the computing
resource use. See `-h`
- `-c` only create config and exit
- `-f n` use only `n` input files
Type `excalibur.py -h` for a list of all arguments.


Examples
- `excalibur.py data` to use the data.py config
- `excalibur.py mc -b -f 100` to use the mc.py config in batch mode with only 100 input files

Links to 'official' output files (which can be used by all users for plotting etc.)
are stored in the ntuples/ folder.

##### NTuple Quantities
###### Z boson and decay leptons
- *z(mass|phi|pt|y|eta)*: Mass, phi, pT (transverse momentum), rapidity and pseudorapidity of the reconstructed Z boson.
- *(mu|e)(1|2|plus|minus|)(pt|eta|phi)*: pT (transverse momentum), pseudorapidity, phi for leading/second/positive/negative muon/electron
- *mu(1|2)(sumchpt|sumpet|sumnhet|sumpupt)*: Muon isolation quantities: sum of charged
hadron pT / photon Et / neutral hadron Et / pile-up pT in a (delta-R) cone around the muon.
- *nmuons*: Number of valid muons in the event
- *nmuonsinv*: Number of invalid muons in the event

###### Jets
- *jet(1|2|3)(pt|eta|phi)*: pT, pseudorapidity, phi for leading/second/third jet
- *njets*: Number of valid jets
- *njetsinv*: Number of invalid jets
- *jet1(chf|nhf|pf|ef|mf|hfhf|hfem|)*: Particle-Flow energy fraction of the leading jet:
charged hadron / neutral hadron / photon / electron / muon / hadron-forward / em-forward
- *jet1area*: Area of the leading jet in eta-phi-space
- *jet1(ptl1l2l3|ptl1|ptraw)*: pT of the leading jet for various levels of jet
corrections applied. By default we use fully corrected jets (L1+L2L3(+Res)), but
the pT for the intermediate correction levels is sometimes also needed.
- *jet1(l1|l2|rc|res)*: Jet energy correction factors for the different levels
- *jet1(btag|qgtag)*: Multivariate discriminators for identification of jets from
gluon resp. b-quarks
- *radiation(\*)*: Jet radiated from the leading jet (Used in event-selection
improvement studies)
- *skimjet1(pt|eta|phi|validity)*: pT, pseudorapidity, phi, validity for leading jet in skim

###### Data 
- *run*: Run for this event
- *event*: Lumi section for this event
- *lumi*: Event number for this event
- *npumeandata*: Expected pile-up in data, calculated from instantaneous luminosity

###### MC
- *npu*: Number of pile-up vertices
- *npumean*: Expected pile-up
- *genjet*: Quantities for generator jet
- *genmuons*: Quantities of the generator muons
- *deltarzgenz*: Distance in R (eta-phi-space) between reconstructed and generated Z
- *matchedgenjet(\*)*: Quantities of the generator jet matched to a reconstructed jet
- *matchedgenmuon(\*)*: Quantities of the generator muon matched to a reconstructed muon
- *matchedgenparton(\*)*: Quantities of the parton matched to a reconstructed jet
- *puWeight*: Weight from pile-up-reweighting
- *numberGeneratedEventsWeight*: 1/number\_of\_events\_in\_dataset 
- *crossSectionPerEventWeight*: cross-section
- *ngenneutrinos": number of neutrinos

###### Event Quantities 
- *npv*: Number of reconstructed primary vertices
- *rho*: Rho, the energy density per event
- *met, metphi*: Size and phi-direction of the missing transverse energy (MET)
- *mettype1vecpt*: pT of the vector-difference between raw and type-I MET
- *mettype1pt*: difference of pT of raw and type-I MET
- *sumet*: Sum of the transverse energy of all Partice-Flow objects
- *mpf*: Jet response calculated with the MPF method
- *rawmpf*: MPF response calculated from uncorrected MET
- *weight*: Event weight. Usually 1.0 for Data. For MC, various weights
(crosssection/eventnumber, pile-up reweighting, ...) are usually applied

### Plotting (merlin): python part
This part derives most classes from HarryPlotter to implement ZJet-specific stuff.
See 
- Plotting/python/, which contains the derived classes
- scripts/, which contains an ini script and the 'merlin' plotting executable
- Plotting/configs/, which contains plot configuration files

Please also have a look at the [HarryPlotter documentation](https://github.com/artus-analysis/Artus/blob/master/HarryPlotter/README.md "HarryPlotter Readme").

Source the ini file. Since HarryPlotter is designed for SCRAM, you need to execute
the shell function  `standalone_merlin` if you're using merlin outside a SCRAM
environment for the first time.(and re-source the ini file).
Type `merlin.py --help` to get a list of the plotting options.

Plot configs can be stored as json or python files. Type `merlin.py --list-functions` to
get a list of the available python plot configs.

##### InputRootZJet
merlin has the additional --zjetfolder, --algorithms and --corrections arguments.
From these arguments, the folder name is constructed, according to the ZJet folder
naming convention "ZJetFolder_AlgorithmCorrection".

'ZJetFolder' corresponds to different levels of event selection:
- 'finalcuts' is the default, all cuts for Z+Jet calibration studies are applied
- 'noetacuts' like finalcuts, but without the cut on the leading jet eta
- 'noalphacuts' like finalcuts, but without the cut on alpha (= Jet2pT/ZpT)
- 'noalphanoetacutscuts' like finalcuts, but without cuts on alpha or leading jet eta
- 'zcuts' only cuts on Z boson and muons, no cuts on jets. Used for checking e.g. Z mass peak
- 'nocuts' no cuts (only the basic event selection like json or hlt filter which
is applied for all pipelines.)

By default, MC histograms (from Artus root files) are scaled to the given
luminosity (--lumi) if at least one Data file is used for plotting.

The quantities.py file in Plotting/python/utiliy contains a dictionary for quantity
aliases. E.g., type 'ptbalance' and this will be replaced with 'jet2pt/zpt'.

The binnings.py file in Plotting/python/utiliy contains a dictionary for special
binnings for ZpT, jet eta, Npv. If you use e.g. `--x-bins zpt` (or dictionary key),
the binning is replaced with the values from this dictionary.

When plotting from a TTree/TNtuple, the 'weight' entry is automatically used as
weight. Disable this with `--no-weight`.

##### PlotMplZJet
The --cutlabel argument places a label with the used cuts (Z pT, abs(jet1eta),
 alpha) on the plot.
The plot axes can be automatically labelled via the entries of the LabelsDict in
Plotting/python/utility/labelsZJet.py (simple strings like 'zpt' are replaced with
nicer Latex labels).

The `--layout` option implements special Matplotlib style settings. See
Plotting/python/utility/matplotlib_rc.py for the list of style options. Use e.g.
`--layout poster` to increase the font size for better plot readability in posters.

##### Python plot configs
- Python functions allow to construct loops of plots, but cannot be saved or read
as easily as json files. Execution of these functions with --python, a list of
the available functions can be displayed with --list-functions. The docstring of
the functions should contain a description.
- Plotting/plot-configs/configs/ contains some python plotting scripts

###### New Python plot config style
There is a new python plot config style which allows to create new configs based
on existing ones and override properties in the plot dictionary.

Example:
```
from Excalibur.Plotting.utility.toolsZJet import PlottingJob

def existing_config(args):
    plots = []
    for x_value in ['zpt', 'npv']:
        d = {
            'x_expression': x_value,
            'y_expression': 'jet1pt/matchedgenjet1pt',
            'y_lims': [0.8, 1.2],
            'tree_draw_options': 'prof'
        }
        plots.append(d)
    return [PlottingJob(plots=plots, args=args)]
    
def new_config(args):
    plotting_jobs = []
    
    existing_jobs = existing_config(args)
    for plot in existing_jobs[0].plots:
        plot['y_lims'] = [0.9, 1.4]
    plotting_jobs += existing_jobs
        
    return plotting_jobs
```

There's no need to call `harryinterface.harry_interface` because it is automatically
called if a list with `PlottingJob` is returned by the config function.


## Troubleshooting

Artus/Excalibur compilation/runtime errors:

- Make sure you have sourced CMSSW and  `ini_excalibur.sh`
- Check that you are up to date in all four repositories (Excalibur, Artus, Kappa, KappaTools)
- Use `make allclean` and `make all`
- If new files have been added to Artus, it might be necessary to recreate the Artus Makefile with `cmake .` in the Artus/ folder

Plotting errors:

- Merlin sometimes needs arguments including whitespaces enclosed in double and
single quotes, e.g. `--x-bins "'10 20 50'"`


## Tutorial
This tutorial (as well as the Artus, HarryPlotter and Excalibur documentation in
general) is incomplete. Please add any information that you think is missing or
talk to the main developers.

This tutorial will show you how to use Excalibur for (1) data analysis and (2) plotting.
Please make sure you have successfully installed and compiled Artus and sourced the
ini script according to the instructions above.
Have a look at this Readme and the documentation for [Artus](https://github.com/artus-analysis/Artus/blob/master/README.md "Artus Readme")
and [HarryPlotter](https://github.com/artus-analysis/Artus/blob/master/HarryPlotter/README.md "HarryPlotter Readme")
in case of questions.


### (1) Data Analysis with Artus
The `excalibur.py` script, located in the scripts/ folder, takes care of creating
a .json config file and running `artus` with it. `artus` will read in some skim
files and process the events: Several processors filter undesired events or
calculate additional quantities. The result is written into a ROOT output file.

- Execute `excalibur.py data -f 3` to run over three input files with data config.
The terminal output will tell you some general information, e.g. which files are used
or how many events per second are processed.
- Have a look at the used configuration file in `cfg/excalibur/data.py`. From these
few lines of code, the full json config is created according to
`cfg/python/defaultconfig.py`. Have a look at the `defaultconfig.py` and the
relevant sections in there (data, data_mm, ...). Where is e.g. the setting for
the MuonID defined?
- Have a look at the json file `cfg/excalibur/data.py.json`. This configuration
contains general settings and a list of pipelines. What is the difference between
the pipelines (look at the list of Quantities and Processors for each pipeline)?
- Use 'grep' or the search on github to find out at which positions a certain
config setting is used (This can be in the Artus or Excalibur repositories!).
Where e.g. is 'MuonID' used?
- Open the 'data.root' output file with a ROOT TBrowser. Have a look at the contents
of the different folders which correspond to the different Pipelines. What is the
difference between the pipelines/folders?
- Open the ntuple in one of the folders and examine the different variables. An
explanation of the quantities is given above. What does e.g. 'mupluspt' mean?
- Type `excalibur.py -h` and read the full list of command line arguments.
- Execute excalibur with the data config in batch mode: `excalibur.py data -b`.
(You will need [grid-control](http://www-ekp.physik.uni-karlsruhe.de/~berger/gc/install.html "grid-control installation instructions")
and have the go.py executable in your $PATH)


### (2) Plotting with HarryPlotter/Merlin
After the data processing with Artus, you need to use `merlin.py` to create plots
from the output ROOT files. Have a look at the documentation for [HarryPlotter](https://github.com/artus-analysis/Artus/blob/master/HarryPlotter/README.md "HarryPlotter Readme")
and merlin (above) for basic installation and usage help and also if you have
questions during the tutorial.

- The basic parameters you need are a root file, the path to an ntuple and a quantity name.
Type `merlin.py -i data.root -x zmass` to plot the Z boson mass.
- Read the merlin documentation above to understand how the folder name is put
together from the  --zjetfolder, --algorithms and --corrections arguments. Repeat
the plotting command for a different zjetfolder, e.g. 'nocuts'.
- Use the `--x-bins` argument to plot the zmass with a different equidistant (e.g.
`--x-bins "10,71,111"`) or custom (e.g. `--x-bins "71 81 86 91 96 101 111"`) binning.
Type `merlin.py -h` to get a list of the command line options to get further
information on how to use `--x-bins`.
- Create a 2D plot of the Z boson pT versus the leading jet pT by specifying zpt
and jet1pt for the -x and -y arguments.
- The `--weights/-w` argument can be used for weighting of events and thereby for
cutting out certain events, e.g. `-w "jet1pt>80&&zpt>100"`. Use this argument to
create the 2D plots only with events with zpt>100 and jet1pt>80.
- Create a profile plot by using `--tree-draw-options prof`.
- The --live or --www arguments are handy to directly open plots or upload them
to your webspace.
- Have a look at the full list of command line arguments: `merlin.py -h`

Congratulations! You have completed the Excalibur tutorial! :clap: :+1:
