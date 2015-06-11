#  -*- coding: utf-8 -*-

"""
	Derived from base in HarryPlotter
"""

import Artus.HarryPlotter.utility.labels as labels

class LabelsDictZJet(labels.LabelsDict):
	def __init__(self, additional_labels=None):
		super(LabelsDictZJet, self).__init__(additional_labels)
		
		self.labels_dict.update({
			#more general stuff. maybe move to Artus?
			'abs(zy)': '|$\mathit{y}^Z$|',
			'abs(jet1eta)': '|$\mathit{\eta}^{Leading \ Jet}$|',
			'algoflavour': 'Flavour (Algorithmic Definition)',
			'constituents': 'Number of Jet Constituents',
			'eabseta': "|$\mathit{\eta}^{Electron}$|",
			'eminuspt': '$\mathit{p}_{T}^{e^{-}}$',
			'epluspt': '$\mathit{p}_{T}^{e^{+}}$',
			'ept': "$\mathit{p}_{T}^{Electron}$",
			'eventsperbin': 'Events per Bin',
			'genjet1pt': '$\mathit{p}_{T}^{Leading Gen Jet}$',
			'genjet2pt': '$\mathit{p}_{T}^{GenJet2}$',
			'genzpt': '${Z}^{GEN} \ \mathit{p}_{T}$ / GeV',
			'jet1area': 'Leading Jet Area',
			'jet1eta': '$\mathit{\eta}^{Leading \ Jet}$',
			'jet1phi': r"$\mathit{\phi}^{Leading \ Jet}$",
			'jet1pt': '$\mathit{p}_{T}^{Leading Jet}$',
			'jet1btag': 'CSV b-Tag',
			'jet1qgtag': 'QG Likelihood',
			'(jet1nhf*jet1pt)': "Jet Neutral Hadron Energy / GeV",
			'(jet1chf*jet1pt)': "Jet Charged Hadron Energy / GeV",
			'(jet1mf*jet1pt)': "Jet Muon Energy / GeV",
			'(jet1pf*jet1pt)': "Jet Photon Energy / GeV",
			'jet2eta': '$\mathit{\eta}^{Jet2}$',
			'jet2pt': '$\mathit{p}_{T}^{Jet2}$',
			'jet2phi': r"$\mathit{\phi}^{Second \ Jet}$",
			'jetsvalid': 'Number of Valid Jets $n$',
			'matchedgenjet1pt': '$\mathit{p}_T^{Matched Gen Jet}$',
			'meteta': '$\mathit{\eta}^{MET}$',
			'metphi': r"$\mathit{\phi}^{MET}$",
			'metpt': '$E_{T}^{Miss}$ / GeV',
			'mu1pt': '$\mathit{p}_{T}^{\mu1}$',
			'mu1eta': '$\mathit{\eta}^{\mu1}$',
			'mu1phi': '$\mathit{\phi}^{\mu1}$',
			'mu2pt': '$\mathit{p}_{T}^{\mu2}$',
			'mu2eta': '$\mathit{\eta}^{\mu2}$',
			'mu2phi': '$\mathit{\phi}^{\mu2}$',
			'muminuseta': '$\mathit{\eta}^{\mu-}$',
			'muminusphi': '$\mathit{\phi}^{\mu-}$',
			'muminuspt': '$\mathit{p}_{T}^{\mu-}$',
			'mupluseta': '$\mathit{\eta}^{\mu+}$',
			'muplusphi': '$\mathit{\phi}^{\mu+}$',
			'mupluspt': '$\mathit{p}_{T}^{\mu+}$',
			'njets30': '$\mathit{n}_{Jets, \mathit{p}_T>30 GeV}$',
			'npu': '$\mathit{n}_{PU}$',
			'npumean': r'$\langle\mathit{n}_{PU}\rangle$',
			'npv': '$\mathit{n}_{PV}$',
			'physflavour': 'Flavour (Physics Definition)',
			'rawmetphi': r"raw $\mathit{\phi}^{MET}$",
			'rawmetpt': '$raw E_{T}^{Miss}$ / GeV',
			'rho': r'$\rho$',
			'run': 'Run',
			'sumet': '$\sum E^{T}$',
			'zmass': '$\mathit{m}_{Z}$ / GeV',
			'zphi': r"$\mathit{\phi}^{Z}$",
			'zpt': '$\mathit{p}_{T}^{Z}$ / GeV',
			'zy': '$\mathit{y}_Z$',

			# ZJet specific
			'alpha': '$\mathit{p}_{T}^{Jet 2}/\mathit{p}_{T}^{Z}$',
			'extrapol': 'Response',
			'genalpha': '$\mathit{p}_{T}^{GenJet 2}/\mathit{p}_{T}^{GenZ}$',
			'genmpf': '$MPF$ Response (Gen level)',
			'(jet1pt/zpt)': r"$\mathit{p}_T$ balance",
			'mpf': '$MPF$ Response',
			'ptbalance': r"$\mathit{p}_T$ Balance",
			'recogen': 'Jet Response $\mathit{p}_T^{RecoJet}/\mathit{p}_T^{GenJet}$',
			'sys': 'Relative Uncertainty [$\%$]',
			'sortedflavour': "Leading Jet Flavour",
			'sortedabsflavour': "Leading Jet Flavour",
			'tagflavour': 'Flavour (from Tagging)',
			'unc': 'Leading Jet Uncertainty',
			'deltaetajet1jet2': "$\Delta\eta_{Jet1}^{Jet2}$"
		})
		if additional_labels != None:
			self.labels_dict.update(additional_labels)
