#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface
from Excalibur.Plotting.utility.colors import histo_colors
from Excalibur.Plotting.utility.binnings import binnings


colors = {
	"uds": histo_colors['blue'],
	"c": histo_colors['yellow'],
	"b": histo_colors['red'],
	"g": histo_colors['green'],
	"undef": histo_colors['grey'],
}
flavour_selections = {
	'g': '(abs(matchedgenparton1flavour)==21)',
	'b': '(abs(matchedgenparton1flavour)==5)',
	'c': '(abs(matchedgenparton1flavour)==4)',
	'uds': '(abs(matchedgenparton1flavour)>0 && abs(matchedgenparton1flavour)<4)',
	'undef': '(matchedgenparton1flavour==0||matchedgenparton1flavour<-100)',
}

zone_selections = {
	'uds': '(jet1qgtag>0.9 && jet1btag<0.3 && jet1btag>-1)',
	'g': '(jet1qgtag<0.1 && jet1qgtag>-1 && jet1btag<0.3 && jet1btag>-1)',
	'c': '(jet1btag>0.3 && jet1btag<0.7 && jet1qgtag>=0)',
	'b': '(jet1btag>0.9 && jet1btag<1 && jet1qgtag>=0)',
}


def response_zones(args=None, additional_dictionary=None):
	""" MPF response in the tagging zones."""
	zone_labels = ['uds', 'c', 'b', 'g']
	d = {
		'x_expressions': [str(i) for i in range(1, len(zone_labels)+1)],
		'y_expressions': 'mpf',
		'weights': [zone_selections[zone] for zone in zone_labels],
		'x_ticks': range(1, len(zone_labels)+1),
		'x_tick_labels': zone_labels,
		'tree_draw_options': 'prof',
		'x_label': 'Tagging Zone',
		'legend': None,
		'markers': 'o',
		'x_bins': " ".join([str(x+0.5) for x in range(len(zone_labels)+1)]),
		'y_lims': [0.95, 1.05],
		'colors': 'black',
		'lines': [1.0],
		'filename': 'mpf_zones',
	}
	if additional_dictionary != None:
		d.update(additional_dictionary)
	harryinterface.harry_interface([d], args)


def flavour_fractions(args=None, additional_dictionary=None):
	""" Plots flavour fraction (q,qbar,g,undef) vs zpt, abs(jet1eta)"""
	plots = []

	for x_quantity, x_bins in zip(
			['zpt', 'abs(jet1eta)'],
			[binnings['zpt'], binnings['abseta']]):

		d = {
			"filename": "flavourFractions_vs_" + x_quantity,
			"legend": "lower left",
			"labels": ["undef", "g", "anti-quark", "quark"],
			"colors": [colors['undef'], colors['g'], histo_colors['yellow'], histo_colors['blue']],
			"markers": ["fill" ],
			"stacks": ["a", "a", "a", "a"],
			"tree_draw_options": ["prof"],
			"x_expressions": [x_quantity],
			"x_bins": x_bins,
			"y_label": "Flavour Fraction",
			"y_expressions": [
				"(matchedgenparton1flavour==-999||matchedgenparton1flavour==0)",
				"(abs(matchedgenparton1flavour)==21)",
				"(matchedgenparton1flavour<0&&matchedgenparton1flavour>-6)",
				"(matchedgenparton1flavour>0&&matchedgenparton1flavour<6)",
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


def flavour_composition_zones(args=None, additional_dictionary=None):
	"""Flavour composition for the different tagging zones"""

	# The plot is put together according to these two lists:
	flavour_labels = [ 'undef', 'g', 'b', 'c', 'uds']
	zone_labels = ['uds', 'c', 'b', 'g']

	d = {
		'y_expressions': [flavour_selections[x] for x in flavour_labels]*len(zone_labels),
		'colors': [colors[i] for i in flavour_labels]*len(zone_labels),
		'weights': 	[zone_selections[x] for x in zone_labels for i in range(len(flavour_labels))],
		'stacks': [str(x) for x in range(1,len(zone_labels)+1) for i in range(len(flavour_labels))],
		'x_expressions': [str(x) for x in range(1,len(zone_labels)+1) for i in range(len(flavour_labels))],
		'labels': flavour_labels +[None]*len(flavour_labels)*(len(zone_labels)-1),
		'x_ticks': range(1,1+len(zone_labels)),
		'x_tick_labels': zone_labels,
		'x_bins':[" ".join(["0.4"] + ["{0}.6 {1}.4".format(i, i+1) for i in range(len(zone_labels))] + [str(len(zone_labels)+2.2)])],
		'x_label': 'Tagging Zone',
		'y_label': 'Flavour Fraction',
		'y_lims': [0, 1],
		'legend': 'center right',
		'tree_draw_options': 'prof',
		'markers': ['fill'],
		'filename': 'flavour_composition_zones',
	}

	if additional_dictionary != None:
		d.update(additional_dictionary)
	harryinterface.harry_interface([d], args)


def flavour_jet1btag_vs_jet1qgtag(args=None, additional_dictionary=None):
	"""Plots jet1btag vs. jet1qgtag in 2D, inclusive and for different tagger zones"""
	plots = []

	for weights, filename, title, colormap in zip([
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
			],
			['Greys', 'Oranges', 'Reds', 'Blues', 'Greens']):
		d = {
			"filename": filename,
			"legend": "None",
			"x_expressions": "jet1btag",
			"x_bins": "100,0,1",
			"x_lims": [0.0, 1.0],
			"y_expressions": "jet1qgtag",
			"y_bins": "100,0,1",
			"y_lims": [0.0, 1.0],
			"colormap": colormap,
			"z_log": True
		}

		if weights is None:
			d['plot_modules'] = ['PlotMplZJet', 'PlotTaggingZones']

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
		"x_label": "Jet Response",
		"x_ticks": [1,2,3,4,5,6, 7],
		"x_lims": [0.5,7.5],
		"x_tick_labels": ['d','u','s','c','b','g', 'undef.'],
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
			"x_bins": "25,0,1"
		}
		if x_quantity == "jet1btag":
			d['y_log'] = True

		d.update(additional_dictionary)
		plots.append(d)

	harryinterface.harry_interface(plots, args)

def flavour_mpf_individual(args=None, additional_dictionary=None):
	plots = []

	weights = []
	nicks = []
	zone_names = [
		'light_quark_zone_',
		'c_quark_zone_',
		'b_quark_zone_',
		'gluon_zone_',
	]

	for weight_param, zone in zip([
			zone_selections['uds'],
			zone_selections['c'],
			zone_selections['b'],
			zone_selections['g'],
		], zone_names):
		nicks.append(zone + "all")
		nicks.append(zone + "g")
		nicks.append(zone + "b")
		nicks.append(zone + "c")
		nicks.append(zone + "uds")
		weights.append(weight_param)
		weights.append(flavour_selections['g'] + "*" + weight_param)
		weights.append(flavour_selections['b'] + "*" + weight_param)
		weights.append(flavour_selections['c'] + "*" + weight_param)
		weights.append(flavour_selections['uds'] + "*" + weight_param)

	d = {
		"x_expressions": ["mpf"],
		"legend": "None",
		"x_lims": [0.5,4.5],
		"x_bins": ["24,0,2"],
		"x_ticks": [1,2,3,4],
		"x_tick_labels": ['uds', 'c', 'b', 'gluon'],
		"x_label": "Flavour (from tagging)",
		"y_lims": [0.80, 1.25],
		"y_label": "MPF Response",
		"nicks": nicks,
		"weights": weights,
		"markers": ["o"],
		"analysis_modules": ["FlavourTagging"],
		"flavour_tagging_zone_names": zone_names,
		"lines": [1.0]
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
			'(jet1btag>0.3&&jet1btag<0.7)',
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
			"title": title,
			"x_expressions": ["mpf"],
			"x_lims": [0.0,2.0],
			"x_bins": ["24,0,2"],
			"labels": ["g","b","c","uds"],
			"nicks": ["g", "b", "c", "uds"],
			"colors": [colors['g'],colors['b'],colors['c'],colors['uds']],
			"markers": ["fill" ],
			"stacks": ["a", "a", "a", "a"],
			"weights": [
				"(abs(matchedgenparton1flavour)==21)*" + weight_param,
				"(abs(matchedgenparton1flavour)==5)*" + weight_param,
				"(abs(matchedgenparton1flavour)==4)*" + weight_param,
				"(abs(matchedgenparton1flavour)>0 && abs(matchedgenparton1flavour)<4)*" + weight_param
			],
		}

		d.update(additional_dictionary)
		plots.append(d)

	harryinterface.harry_interface(plots, args)


def pf_fractions_vs_flavour(args=None, additional_dictionary=None):
	"""Jet composition of the leading jet for different flavours"""
	d = {
		"filename": "pf_fractions_vs_flavor",
		"x_expressions": ["sortedabsflavour"],
		"x_ticks": [1,2,3,4,5,6,7],
		"x_bins": ["13,0.5,7.5"],
		'x_bins':[" ".join(["0.4"] + ["{0}.6 {1}.4".format(i, i+1) for i in range(7)] + [str(7+3.4)])],
		"x_tick_labels": ['d','u','s','c','b','g', 'undef.'],
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
		"legend": "center right",
	}
	if additional_dictionary is not None:
		d.update(additional_dictionary)
	harryinterface.harry_interface([d], args)


def flavour(args=None):
	"""Plots all flavour plots"""
	d = {
		"files": [
			"ntuples/MC_RD1_8TeV_53X_E2_50ns_2015-05-20.root",
	#		"ntuples/MC_RD1_8TeV_53X_E2_50ns_2015-05-20.root",
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
	flavour_composition_zones(args, d)
	response_zones(args, d)
	flavour_mpf_individual(args, d)
