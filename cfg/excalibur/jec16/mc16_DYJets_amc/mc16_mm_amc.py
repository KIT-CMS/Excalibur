import configtools
import os
import sys

# -- import common information
sys.path.append(os.path.dirname(__file__))
from common import JEC_BASE, JEC_VERSION, JER, SE_PATH_PREFIXES

RUN = 'BCDEFGH'
CH = 'mm'
JEC = '{}_{}'.format(JEC_BASE, JEC_VERSION)


def config():
	cfg = configtools.getConfig('mc', 2016, CH, JEC=JEC, JER=JER, bunchcrossing='25ns')
	cfg["InputFiles"].set_input(
		path="{}/tberger/Skimming_94X/DYJetsToLL_amcatnloFXFX-pythia8_RunIISummer16/*.root".format(
			SE_PATH_PREFIXES['xrootd_gridka_nrg']),

	)

	# cfg = configtools.expand(cfg, ['nocuts','noalphanoetacuts','basiccuts','finalcuts'], ['None', 'L1', 'L1L2L3'])
	cfg = configtools.expand(cfg, ['basiccuts', 'finalcuts'], ['None', 'L1L2L3'])

	cfg['PileupWeightFile'] = os.path.join(configtools.getPath(), 'data/pileup/PUWeights_' + RUN + '_13TeV_23Sep2016ReReco_DYJetsToLL_M-50_amcatnloFXFX-pythia8_RunIISummer16.root')

	cfg['NumberGeneratedEvents'] = 11043183 #28968252 # for: amc@nlo
	cfg['GeneratorWeight'] = 0.670123731536
	cfg['CrossSection'] = 1921.8*3

	return cfg
