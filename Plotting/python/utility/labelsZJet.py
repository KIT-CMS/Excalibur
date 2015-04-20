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
			'abs(zy)': '|$y^Z$|',
			'abs(jet1eta)': '|$\eta^\mathrm{Leading \ Jet}$|',
			'algoflavour': 'Flavour (Algorithmic Definition)',
			'constituents': 'Number of Jet Constituents',
			'eabseta': "|$\eta^\mathrm{electron}$|",
			'eminuspt': '$p_\mathrm{T}^\mathrm{e^{-}}$',
			'epluspt': '$p_\mathrm{T}^\mathrm{e^{+}}$',
			'ept': "$p_\mathrm{T}^\mathrm{Electron}$",
			'eventsperbin': 'Events per Bin',
			'genjet1pt': '$p_\mathrm{T}^\mathrm{Leading Gen Jet}$',
			'genjet2pt': '$p_\mathrm{T}^\mathrm{GenJet2}$',
			'genzpt': '$\mathrm{Z}^\mathrm{GEN} \ p_\mathrm{T}$ / GeV',
			'jet1area': 'Leading Jet Area',
			'jet1eta': '$\eta^\mathrm{Leading \ Jet}$',
			'jet1phi': r"$\phi^\mathrm{Leading \ Jet}$",
			'jet1pt': '$p_\mathrm{T}^\mathrm{Leading Jet}$',
			'jet2pt': '$p_\mathrm{T}^\mathrm{Jet2}$',
			'jetsvalid': 'Number of Valid Jets $n$',
			'matchedgenjet1pt': '$p_\mathrm{T}^\mathrm{Matched Gen Jet}$',
			'mu1pt': '$p_\mathrm{T}^\mathrm{\mu1}$',
			'mu2pt': '$p_\mathrm{T}^\mathrm{\mu2}$',
			'muminuspt': '$p_\mathrm{T}^\mathrm{\mu-}$',
			'mupluspt': '$p_\mathrm{T}^\mathrm{\mu+}$',
			'njets30': '$\mathrm{n}_{\mathrm{Jets}, p_T>30GeV}$',
			'npv': '$n_\mathrm{PV}$',
			'physflavour': 'Flavour (Physics Definition)',
			'rho': '$\rho$',
			'run': 'Run',
			'sumEt': '$\sum E^\mathrm{T}$',
			'zphi': r"$\phi^\mathrm{Z}$",
			'zpt': '$p_\mathrm{T}^\mathrm{Z}$ / GeV',
			'zy': '$y^Z$',

			# ZJet specific
			'METeta': '$\eta^\mathrm{MET}$',
			'METpt': '$E_\mathrm{T}^\mathrm{Miss}$',
			'alpha': '$p_\mathrm{T}^\mathrm{Jet 2}/p_\mathrm{T}^\mathrm{Z}$',
			'extrapol': 'Response',
			'genalpha': '$p_\mathrm{T}^\mathrm{GenJet 2}/p_\mathrm{T}^\mathrm{GenZ}$',
			'genmpf': '$MPF$ Response (Gen level)',
			'(jet1pt/zpt)': r"$p_\mathrm{T}$ balance",
			'mpf': '$MPF$ Response',
			'ptbalance': r"$p_\mathrm{T}$ Balance",
			'recogen': 'Jet Response $p_\mathrm{T}^\mathrm{RecoJet}/p_\mathrm{T}^\mathrm{GenJet}$',
			'sys': 'Relative Uncertainty [$\%$]',
			'tagflavour': 'Flavour (from Tagging)',
			'unc': 'Leading Jet Uncertainty',
		})
		if additional_labels != None:
			self.labels_dict.update(additional_labels)
