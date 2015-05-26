#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface
from Excalibur.Plotting.utility.colors import histo_colors
from Excalibur.Plotting.utility.binnings import binnings


colors = {
	"uds": histo_colors['blue'],
	"c": histo_colors['green'],
	"b": histo_colors['red'],
	"g": histo_colors['yellow'],
	"undef": histo_colors['grey'],
}

def flavour_fractions(args=None, additional_dictionary=None):
	""" Plots Flavour fraction (Physics definition) vs zpt, abs(jet1eta)"""
	plots = []

	for x_quantity, x_bins in zip(
			['zpt', 'abs(jet1eta)'],
			[binnings['zpt'], binnings['abseta']]):

		d = {
			"filename": "flavourFractions_vs_" + x_quantity,
			"legend": "lower left",
			"labels": ["undef", "g", "b", "c", "uds"],
			"colors": [colors['undef'],colors['g'],colors['b'],colors['c'],colors['uds']],
			"markers": ["fill" ],
			"stacks": ["a", "a", "a", "a", "a"],
			"tree_draw_options": ["prof"],
			"x_expressions": [x_quantity],
			"x_bins": x_bins,
			"y_label": "Flavour fraction (Physics definition)",
			"y_expressions": [
				"(matchedgenparton1flavour==-999)",
				"(abs(matchedgenparton1flavour)==21)",
				"(abs(matchedgenparton1flavour)==5)",
				"(abs(matchedgenparton1flavour)==4)",
				"(abs(matchedgenparton1flavour)>0 && abs(matchedgenparton1flavour)<4)"
			],
			"y_lims": [0.0, 1.0],
			"cutlabel": True,
		}
		if x_quantity == 'zpt':
			d['x_ticks'] = [30, 50, 100, 200, 400, 1000]
			d['x_log'] = True
		elif x_quantity == 'abs(jet1eta)':
			d["zjetfolders"] = ["noetacuts"]

		if additional_dictionary != None:
			d.update(additional_dictionary)
		plots.append(d)

	harryinterface.harry_interface(plots, args)


def flavour_jet1btag_vs_jet1qgtag(args=None, additional_dictionary=None):
	"""Plots jet1btag vs. jet1qgtag in 2D, inclusive and for different tagger zones"""
	plots = []

	for weights, filename, title in zip([
				None,
				'(abs(matchedgenparton1flavour)==4)',
				'(abs(matchedgenparton1flavour)==5)',
				'(abs(matchedgenparton1flavour)>0 && abs(matchedgenparton1flavour)<4)',
				'(abs(matchedgenparton1flavour)==21)'
			],
			['flavorTaggingZones', 'flavorTaggingZones_c', 'flavorTaggingZones_b', 'flavorTaggingZones_uds', 'flavorTaggingZones_g'],
			[
				'Tagger distribution',
				'c quark jets',
				'b quark jets',
				'light quark jets',
				'gluon jets'
			]):
		d = {
			"filename": filename,
			"legend": "None",
			"x_expressions": "jet1btag",
			"x_bins": "100,0,1",
			"x_lims": [0.0, 1.0],
			"y_expressions": "jet1qgtag",
			"y_bins": "100,0,1",
			"y_lims": [0.0, 1.0],
			"colormap": "Blues",
			"z_log": True
		}

		if title is not None:
			d['title'] = title

		if weights is not None:
			d['weights'] = weights
			d['x_bins'] = "20,0,1"
			d['y_bins'] = "20,0,1"
			d['z_log'] = False

		d.update(additional_dictionary)
		plots.append(d)

	harryinterface.harry_interface(plots, args)


def flavour_jet_response(args=None, additional_dictionary=None):
	"""Flavor response for simulated jets """
	d = {
		"filename": "flavorJetResponse",
		"legend": "lower center",
		"x_expressions": ["sortedabsflavour"],
		"x_label": "Flavour (Physics Definition)",
		"x_ticks": [0,1,2,3,4,5,6],
		"x_lims": [-0.5,6.5],
		"x_tick_labels": ['undef.','d','u','s','c','b','g'],
		"y_expressions": ["ptbalance", "mpf", "genjet1pt/zpt", "jet1pt/genjet1pt"],
		"labels": ["PtBalance", "MPF", "GenJet/RecoZ", "RecoJet/GenJet"],
		"y_lims": [0.8, 1.1],
		'tree_draw_options': 'prof',
		'markers': ['.', '*', 'o', 'd'],
		"cutlabel": True,
		"lines": [1.],
	}
	if additional_dictionary != None:
		d.update(additional_dictionary)
	harryinterface.harry_interface([d], args)


def flavours(args=None, additional_dictionary=None):
	"""Histogram of jet flavour (4 plots: q qbar g undef) """
	d = {
		'filename': 'flavours',
		'cutlabel': True,
		'x_label': 'Flavour',
		'x_lims': [0.8, 7.2],
		'x_expressions': [
		  'matchedgenparton1flavour * (matchedgenparton1flavour > 0 && matchedgenparton1flavour < 20)',
		  '0.4 + abs(matchedgenparton1flavour) * (matchedgenparton1flavour < 0 && matchedgenparton1flavour > -20)',
		  '6 * (matchedgenparton1flavour == 21)',
		  '6.8 * (matchedgenparton1flavour == -999)',
		],
		'x_bins': [' '.join(['{0} {0}.4 {0}.8 '.format(i) for i in range(1, 6)]) + '6 6.4 6.6 7 7.2'],
		'x_ticks': [i+1.4 for i in range(0, 5)] + [6.2, 6.8],
		'x_tick_labels': ['d', 'u', 's', 'c', 'b', 'g', 'undef'],
		'markers': ['fill'],
		'labels': ['quark', 'anti-quark', None, None],
		'colors': [histo_colors['blue'], histo_colors['yellow'], histo_colors['green'], histo_colors['grey']],
		'legend': 'upper center',
	}
	if additional_dictionary != None:
		d.update(additional_dictionary)
	harryinterface.harry_interface([d], args)


def flavour_comparison(args=None, additional_dictionary=None):
	"""Flavour comparsion with jet1btag and jet1qgtag """
	plots = []
	for x_quantity in ['jet1btag', 'jet1qgtag']:
		d = {
			"filename": "flavorComparison_vs_" + x_quantity,
			"legend": "upper center",
			"labels": ["uds", "c", "b", "g"],
			"colors": [colors['uds'],colors['c'],colors['b'],colors['g']],
			"markers": ["fill" ],
			"stacks": ["a", "a", "a", "a"],
			"x_expressions": [x_quantity],
			"weights": [
				"(abs(matchedgenparton1flavour)>0 && abs(matchedgenparton1flavour)<4)",
				"(abs(matchedgenparton1flavour)==4)",
				"(abs(matchedgenparton1flavour)==5)",
				"(abs(matchedgenparton1flavour)==21)"
			],
			"x_lims": [0.0, 1.0],
			"x_bins": "25,0,1",
			"y_log": True
		}
		d.update(additional_dictionary)
		plots.append(d)

	harryinterface.harry_interface(plots, args)


def flavour_mpf_response(args=None, additional_dictionary=None):
	"""MPF Response for different Flavour Zones """
	plots = []

	for weight_param, filename, title in zip([
			'(jet1qgtag>0.9&&jet1btag<0.3)',
			'(jet1qgtag<0.1&&jet1btag<0.3)',
			'(jet1btag>0.3&&jet1btag<0.9)',
			'(jet1btag>0.9)',
		],[
			'flavorMpfResponse_light_quark_zone',
			'flavorMpfResponse_gluon_zone',
			'flavorMpfResponse_c_quark_zone',
			'flavorMpfResponse_b_quark_zone',
		], [
			'Light Quark Zone',
			'Gluon Zone',
			'c Quark Zone',
			'b Quark Zone',
		]):
		d = {
			"filename": filename,
			"x_expressions": ["mpf"],
			"x_lims": [0.0,2.0],
			"x_bins": ["24,0,2"],
			"labels": ["g","b","c","uds"],
			"colors": [colors['g'],colors['b'],colors['c'],colors['uds']],
			"markers": ["fill" ],
			"stacks": ["a", "a", "a", "a"],
			"weights": [
				"(abs(matchedgenparton1flavour)==21)*" + weight_param,
				"(abs(matchedgenparton1flavour)==5)*" + weight_param,
				"(abs(matchedgenparton1flavour)==4)*" + weight_param,
				"(abs(matchedgenparton1flavour)>0 && abs(matchedgenparton1flavour)<4)*" + weight_param
			]
		}

		if title is not None:
			d['title'] = title
		d.update(additional_dictionary)
		plots.append(d)
	harryinterface.harry_interface(plots, args)


def pf_fractions_vs_flavour(args=None, additional_dictionary=None):
	"""Jet composition of the leading jet for different flavours"""
	d = {
		"filename": "pf_fractions_vs_flavor",
		"x_expressions": ["sortedabsflavour"],
		"x_label": "Flavour (Physics Definition)",
		"x_ticks": [0,1,2,3,4,5,6],
		"x_bins": ["7,-0.5,6.5"],
		"x_tick_labels": ['undef.','d','u','s','c','b','g'],
		"labels": [
			r"$\\mu$",
			r"$e$",
			r"$\\gamma$",
			"CHad",
			"NHad",
		],
		"markers": ["fill" ],
		"stacks": ["a", "a", "a", "a", "a"],
		"y_expressions": [
			"jet1mf",
			"jet1ef",
			"jet1pf",
			"jet1chf",
			"jet1nhf",
		],
		"colors": [histo_colors[c] for c in ['violet', 'brown', 'green', 'yellow', 'blue']],
		"y_label": "Leading Jet PF Energy Fraction",
		"y_lims": [0.0, 1.0],
		"tree_draw_options": ["prof"],
		"legend": "center left",
	}
	if additional_dictionary is not None:
		d.update(additional_dictionary)
	harryinterface.harry_interface([d], args)


def flavour(args=None):
	"""Plots all flavour plots"""
	d = {
		"files": [
			"ntuples/MC_RD1_8TeV_53X_E2_50ns_2015-05-20.root"
		],
		"algorithms": ["AK5PFJetsCHS",],
		"corrections": ["L1L2L3",]
	}

	flavours(args, d)
	flavour_fractions(args, d)
	flavour_jet1btag_vs_jet1qgtag(args, d)
	flavour_jet_response(args, d)
	flavour_comparison(args, d)
	flavour_mpf_response(args, d)
	pf_fractions_vs_flavour(args, d)
