#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface

colors = {
	"uds": "#7293cb",
	"c": "#68A55A",
	"b": "#D35658",
	"g": "#FAA75B",
	"undef": "grey"
}

def flavour_fractions(args=None, additional_dictionary=None):
	""" Plots Flavour fraction (Physics definition) vs zpt, abs(jet1eta)"""
	plots = []

	for x_quantity, x_bins in zip(
			['zpt', 'abs(jet1eta)'],
			["30 40 50 60 75 95 125 180 300 1000", "0 0.783 1.305 1.93 2.5 2.964 3.139 5.191"]):

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
	"""Plots Flavour jet1btag vs. jet1qgtag for different tagger zones"""
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
			d['x_bins'] = "10,0,1"
			d['y_bins'] = "10,0,1"
			d['z_log'] = False

		d.update(additional_dictionary)
		plots.append(d)

	harryinterface.harry_interface(plots, args)

def flavour_jet_response(args=None, additional_dictionary=None):
	"""Flavor response for simulated jets """
	plots = []

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
	}
	if additional_dictionary != None:
		d.update(additional_dictionary)
	plots.append(d)

	harryinterface.harry_interface(plots, args)

def sortedflavour_histo(args=None, additional_dictionary=None):
	"""Histogram of jet flavour (sorted) """
	d = {
		'filename': 'sortedflavourHisto',
		'x_expressions': ['sortedflavour'],
		'x_bins': '12,-5.5,6.5',
		'x_ticks': [i-5 for i in range(0, 12)],
		'x_tick_labels': ['-b', '-c', '-s', '-u', '-d', 'undef', 'd', 'u', 's', 'c', 'b', 'g'],
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
	plots = []
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
			"CHad",
			r"$\\gamma$",
			"NHad",
		],
		"markers": ["fill" ],
		"stacks": ["a", "a", "a", "a", "a"],
		"y_expressions": [
			"jet1mf",
			"jet1ef",
			"jet1chf",
			"jet1pf",
			"jet1nhf",
		],
		"y_label": "Leading Jet PF Energy Fraction",
		"y_lims": [0.0, 1.0],
		"tree_draw_options": ["prof"],
	}
	d.update(additional_dictionary)
	plots.append(d)
	harryinterface.harry_interface(plots, args)

def flavour(args=None):
	"""Plots all flavour plots"""
	d = {
		"files": [
			"ntuples/MC_RD1_8TeV_53X_E2_50ns_2015-05-20.root"
		],
		"algorithms": ["AK5PFJetsCHS",],
		"corrections": ["L1L2L3",]
	}

	flavour_fractions(args, d)
	flavour_jet1btag_vs_jet1qgtag(args, d)
	sortedflavour_histo(args, d)
	flavour_jet_response(args, d)
	flavour_comparison(args, d)
	flavour_mpf_response(args, d)
	pf_fractions_vs_flavour(args, d)
