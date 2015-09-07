#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface


def muoniso_aod(args=None, additional_dictionary=None):
	"""Plot muons PF Iso/pT quantities directly out of AOD files.
	   WORKS ONLY AT NAF!
	"""

	# set a pT threshold for the muons:
	pt_threshold = 0
	weights = ['patMuons_slimmedMuons__{}.obj.m_state.p4Polar_.fCoordinates.fPt>{}'.format(item, pt_threshold) for item in ['RECO', 'PAT']]

	plots = []
	for fraction in ['ChargedHadronPt', 'ChargedParticlePt', 'PUPt', 'PhotonEt', 'NeutralHadronEt']:
		for cone_size in ['3', '4']:
			d = {
				'files':[  # MINIAOD data and mc
					'/pnfs/desy.de/cms/tier2/store/data/Run2015B/DoubleMuon/MINIAOD/PromptReco-v1/000/251/883/00000/44864117-232D-E511-8C15-02163E01463E.root',
					'/pnfs/desy.de/cms/tier2/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt50ns_MCRUN2_74_V9A-v2/60000/2A5F281F-F007-E511-87F2-00074305CD93.root',
				],
				'folders': 'Events',
				'x_expressions': [
					"patMuons_slimmedMuons__RECO.obj.pfIsolationR0{}_.sum{}/patMuons_slimmedMuons__RECO.obj.m_state.p4Polar_.fCoordinates.fPt".format(cone_size, fraction),
					"patMuons_slimmedMuons__PAT.obj.pfIsolationR0{}_.sum{}/patMuons_slimmedMuons__PAT.obj.m_state.p4Polar_.fCoordinates.fPt".format(cone_size, fraction),
					# for AOD: 'recoMuons_muons__RECO.obj.pfIsolationR04_.sumChargedHadronPt/recoMuons_muons__RECO.obj.m_state.p4Polar_.fCoordinates.fPt'
				],
				'x_bins': '25,0,50',
				'weights': [weights],
				#analysis
				'analysis_modules': ['NormalizeToFirstHisto', 'Ratio'],
				#formatting
				'labels': ['Data', 'MC'],
				'energies': [13],
				'y_subplot_lims': [0, 2.99],  # not exactly three so the tick labels of upper and lower plot dont clash
				'x_label': r'Muon {}R0{}'.format(fraction, cone_size) + r'$/\\mathit{p}_T^{\\mu}$',
				'title': 'Shape comparison',
				'y_log': True,
				# output
				'filename': 'muons_{}_R0{}'.format(fraction, cone_size),
			}
			plots.append(d)
	harryinterface.harry_interface(plots, args)

if __name__ == '__main__':
	muoniso_aod()
