# -*- coding: utf-8 -*-

import os
import time
import subprocess
import itertools

import Excalibur.Plotting.harryinterface as harryinterface
import Artus.Utility.logger as logger
from Excalibur.Plotting.utility.toolsZJet import get_input_files
import warnings


def apply_double_profile(plotDict, args=None):
	"""
	Plot <y> vs <x>, i.e. use mean/err for X&Y per X bin

	:param plotDict: the HarryPlotter job information
	:param args: the command line arguments

	:note: This modifies `plotDict` inplace.
	"""
	if not 'prof' in plotDict['tree_draw_options'] or 'profs' in plotDict['tree_draw_options']:
		if isinstance(plotDict['tree_draw_options'], basestring):
			plotDict['tree_draw_options'] = [plotDict['tree_draw_options']]
		plotDict['tree_draw_options'].append('prof')
	# Parameter List Expansion
	#   the x vs x profile must be an exakt match of y vs x
	#   we thus must replicate all settings for their position to match
	# settings we need to replicate in a controlled fashion
	input_root_opts = ['nicks', 'x_expressions', 'y_expressions', 'z_expressions', 'x_bins', 'y_bins', 'z_bins', 'scale_factors', 'files', 'directories', 'folders', 'weights', 'friend_trees', 'tree_draw_options']
	if not plotDict.get('files'):
		plotDict['files'] = get_input_files(args)[0]
	# make sure all n-length (non-0,1) objects have the same size
	opt_n_length_max = max(len(plotDict.get(opt_name, ())) for opt_name in input_root_opts if not isinstance(plotDict.get(opt_name), str))
	assert opt_n_length_max > 0, 'Cannot expand empty plot definition'
	for opt_name in input_root_opts:
		if opt_name not in plotDict or isinstance(plotDict[opt_name], str):
			continue
		assert len(plotDict[opt_name]) <= 1 or len(plotDict[opt_name]) == opt_n_length_max, "Replication requires all input_root options to be either of 0, 1 or same max length ('%s' is %d/%d)" % (opt_name, len(plotDict[opt_name]), opt_n_length_max)
		# TODO: dunno if checking for None is required, saw this in HP - MF@20151130
		if not plotDict[opt_name] or plotDict[opt_name][0] is None:
			continue
		if len(plotDict[opt_name]) == 1:
			plotDict[opt_name] = plotDict[opt_name] * opt_n_length_max
		# never modify inplace - input may be mutable and used elsewhere/recursively
		plotDict[opt_name] = plotDict[opt_name][:] * 2
	if not plotDict.get('nicks') or plotDict['nicks'][0] is None:
		plotDict['nicks'] = ["nick%d" % nick for nick in xrange(len(plotDict['y_expressions']))]
	# X-Y Profile matching
	# explicitly create new x profiles
	plotDict['y_expressions'] = plotDict['y_expressions'][:opt_n_length_max] + plotDict['x_expressions'][opt_n_length_max:]
	plotDict['nicks'] = plotDict['nicks'][opt_n_length_max:] + ['%s_x_prof' % nick for nick in plotDict['nicks'][:opt_n_length_max]]
	# create new y vs <x> graphs
	plotDict['analysis_modules'] = plotDict.get('analysis_modules', [])[:]
	plotDict['analysis_modules'].insert(0, 'TGraphFromHistograms')
	plotDict['tgraph_strip_empty'] = 'any'
	plotDict['tgraph_y_nicks'] = plotDict['nicks'][:opt_n_length_max]
	plotDict['tgraph_x_nicks'] = plotDict['nicks'][opt_n_length_max:]
	plotDict['tgraph_result_nicks'] = ['%s_vs_x_prof' % nick for nick in plotDict['nicks'][:opt_n_length_max]]
	# disable source plots
	plotDict['nicks_blacklist'] = [r'^%s$' % nick for nick in plotDict['nicks']]
	return plotDict


def jec_combination(args=None, additional_dictionary=None):
	"""function to create the root combination file for the jec group."""
	mpl_plots = []
	root_plots = []
	label_dict = {
		'ptbalance': 'PtBal',
		'mpf': 'MPF',
		'rawmpf': 'MPF-notypeI',
		'zmass': 'ZMass',
		'npumean': 'Mu',
		'rho': 'Rho',
		'npv': 'NPV',
	}
	alpha_limits = [0.1, 0.15, 0.2, 0.3, 0.4]
	alpha_cuts = ['(alpha<{})'.format(limit) for limit in alpha_limits]
	alpha_strings = ['a'+str(int(100*limit)) for limit in alpha_limits]

	eta_borders = [0, 0.783, 1.305, 1.93, 2.5, 2.964, 3.2, 5.191]
	eta_cuts = ["({0}<=abs(jet1eta)&&abs(jet1eta)<{1})".format(*b) for b in zip(eta_borders[:-1], eta_borders[1:])]
	eta_cuts = ["(0<=abs(jet1eta)&&abs(jet1eta)<1.3)"] + eta_cuts  # also include standard barrel jet selection
	eta_strings = ["eta_{0:0>2d}_{1:0>2d}".format(int(round(10*up)), int(round(10*low))) for up, low in zip(eta_borders[:-1], eta_borders[1:])]
	eta_strings = ["eta_00_13"] + eta_strings
	try:
		npv_weights = additional_dictionary.pop("_npv_weights")
		warnings.warn("Usage of '_npv_weights' is deprecated. Use PUWeights in Excalibur instead.")
	except (AttributeError, KeyError):
		npv_weights = ["1"]
	try:
		file_label = additional_dictionary.pop("file_label")
	except (AttributeError, KeyError):
		file_label = ""

	now = time.localtime()
	def mpl_to_root(mpl_plot_dict):
		"""Create root plot dict from mpl plot dict"""
		root_plot_dict = mpl_plot_dict.copy()
		root_plot_dict.update({
			'plot_modules': ['ExportRoot'],
			'filename': 'combination_ZJet_' + file_label + time.strftime("%Y-%m-%d", now),
			'file_mode': ('RECREATE' if mpl_to_root.first else 'UPDATE'),
		})
		mpl_to_root.first = False
		return root_plot_dict
	mpl_to_root.first = False

	for alphacut, alphastring in zip(alpha_cuts, alpha_strings):
		for etacut, etastring in zip(eta_cuts, eta_strings):
			for correction in ['L1L2L3']: # no L1L2L3Res available atm
				eta_alpha_cut = '&&'.join((alphacut, etacut))
				base_plot = {
					'nicks': ['data', 'mc'],
					'corrections': [correction],
					'zjetfolders': ['noalphanoetacuts'],
					'weights': ["(%s)*(%s)" % (eta_alpha_cut, npv_weight) for npv_weight in npv_weights],
					'tree_draw_options' : ['prof'],
					# ratio
					'analysis_modules': ['Ratio'],
					'ratio_numerator_nicks':['data'],
					'ratio_denominator_nicks':['mc'],
				}
				# histograms - event counts
				labelsuffix = '_'.join(['NEvents', 'CHS', alphastring, etastring, correction])
				d_mpl = {
					'x_expressions': ['zpt'],
					'x_bins': 'zpt',
					'labels': ['_'.join([item, labelsuffix]) for item in ['Data', 'MC', 'Ratio']],
					'filename': labelsuffix + file_label,
					'no_weight': True,
				}
				d_mpl.update(base_plot)
				del d_mpl['tree_draw_options']
				d_root = mpl_to_root(d_mpl)
				# make plots comparable to jec_comparison
				d_mpl['x_log'] = True
				d_mpl['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
				mpl_plots.append(d_mpl)
				root_plots.append(d_root)
				# profiles - responses
				for method in ['mpf', 'ptbalance', 'rawmpf', 'zmass']:
					labelsuffix = '_'.join([label_dict[method], 'CHS', alphastring, etastring, correction])
					d_mpl = {
						'x_expressions': ['zpt'],
						'y_expressions': [method],
						'x_bins': 'zpt',
						'y_label': method,
						'labels': ['_'.join([item, labelsuffix]) for item in ['Data', 'MC', 'Ratio']],
						'filename': labelsuffix + file_label,
					}
					d_mpl.update(base_plot)
					if additional_dictionary is not None:
						d_mpl.update(additional_dictionary)
					apply_double_profile(d_mpl, args)
					d_root = mpl_to_root(d_mpl)
					# make plots comparable to jec_comparison
					d_mpl['x_log'] = True
					d_mpl['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
					mpl_plots.append(d_mpl)
					root_plots.append(d_root)
				# pileup info
				for x_expression, y_expression in [("npumean", "rho"), ("npumean", "npv")]:
					labelsuffix = "_".join((y_expression, "vs", x_expression, 'CHS', alphastring, etastring, correction))
					d_mpl = {
						'x_expressions': [x_expression],
						'y_expressions': [y_expression],
						'y_label': y_expression,
						'cutlabel': True,
						'x_bins': "25,0.5,25.5",
						'legend': 'upper left',
						'labels': ['_'.join([item, labelsuffix]) for item in ['Data', 'MC', 'Ratio']],
						'filename': labelsuffix + file_label,
					}
					d_mpl.update(base_plot)
					if additional_dictionary is not None:
						d_mpl.update(additional_dictionary)
					apply_double_profile(d_mpl, args)
					d_root = mpl_to_root(d_mpl)
					mpl_plots.append(d_mpl)
					root_plots.append(d_root)
	harryinterface.harry_interface(mpl_plots, args)
	harryinterface.harry_interface(root_plots, args + ['--max-processes', '1'])


def jec_combination_zee(args=None, additional_dictionary=None):
	"""Use Z->ee defaults for :py:func:`~.jec_combination`"""
	additional_dictionary = additional_dictionary if additional_dictionary is not None else {}
	additional_dictionary["algorithms"] = ["ak4PFJetsCHS"]
	additional_dictionary["file_label"] = "Zee" + time.strftime("%Y%m%d")
	return jec_combination(args=args, additional_dictionary=additional_dictionary)


def jec_combination_zmm(args=None, additional_dictionary=None):
	"""Use Z->mm defaults for :py:func:`~.jec_combination`"""
	additional_dictionary = additional_dictionary if additional_dictionary is not None else {}
	additional_dictionary["algorithms"] = ["ak4PFJetsCHS"]
	additional_dictionary["file_label"] = "Zmm" + time.strftime("%Y%m%d")
	return jec_combination(args=args, additional_dictionary=additional_dictionary)


def jec_pu_combination(args=None, additional_dictionary=None):
	"""Create combination info on pileup"""
	mpl_plots = []
	root_plots = []
	try:
		file_label = additional_dictionary.pop("file_label")
	except (AttributeError, KeyError):
		file_label = ""
	now = time.localtime()
	create_file = True
	for x_expression, y_expression in [("npumean", "rho"), ("npv", "rho"), ("npumean", "npv")]:
		for correction in ['L1L2L3']: # no L1L2L3Res available atm
			labelsuffix = "_".join((x_expression, "vs", y_expression, 'CHS', correction))
			d_mpl = {
				'x_expressions': [x_expression],
				'y_expressions': [y_expression],
				'tree_draw_options': 'prof',
				'corrections': ['L1L2L3'],
				'cutlabel': True,
				'markers': ['o', 'd'],
				'x_bins': "50,0.5,50.5",
				'legend': 'lower right',
				'analysis_modules': ['Ratio', 'ConvertToTGraphErrors'],
				'labels': ['_'.join([item, labelsuffix]) for item in ['Data', 'MC', 'Ratio']],
			}
			if additional_dictionary is not None:
				d_mpl.update(additional_dictionary)
			d_root = d_mpl.copy()
			d_root.update({
				'plot_modules': ['ExportRoot'],
				'filename': 'combination_ZJet_PU_' + file_label + time.strftime("%Y-%m-%d", now),
				'file_mode': ('RECREATE' if create_file else 'UPDATE'),
			})
			create_file = False
			mpl_plots.append(d_mpl)
			root_plots.append(d_root)
	harryinterface.harry_interface(mpl_plots, args)
	harryinterface.harry_interface(root_plots, args + ['--max-processes', '1'])





def jec_combination_20150722(args=None):
	d = {
		'files': [
			'ntuples/Data_13TeV_74X_E2_50ns_2015-07-22.root',
			'ntuples/MC_13TeV_74X_E2_50ns_algo_2015-07-22.root',
		],
		"algorithms": ["ak4PFJetsCHS",],
		# NPV hardcoded from Dominik's ``get_weights`` script output @ 20150722
		"_npv_weights" : ["1", "(npv==1)*60.7406+(npv==2)*4.00814+(npv==3)*5.16789+(npv==4)*4.87128+(npv==5)*4.18218+(npv==6)*3.43252+(npv==7)*3.26353+(npv==8)*2.78556+(npv==9)*2.65932+(npv==10)*2.02964+(npv==11)*1.64236+(npv==12)*1.30764+(npv==13)*1.17253+(npv==14)*0.901506+(npv==15)*0.687614+(npv==16)*0.636555+(npv==17)*0.366818+(npv==18)*0.318782+(npv==19)*0.21218+(npv==20)*0.148066+(npv==21)*0.104698+(npv==22)*0.0391752+(npv==23)*0.0121797+(npv==24)*0.0611739+(npv==25)*0.0192279+(npv==26)*0+(npv==27)*0+(npv==28)*0+(npv==29)*0+(npv==30)*0"],
	}
	jec_combination(args, d)


def jec_combination_20150804(args=None):
	d = {
		'files': [
			'ntuples/Data_13TeV_74X_E2_50ns_2015-07-31.root',
			'ntuples/MC_13TeV_74X_E2_50ns_algo_2015-07-31.root',
		],
		"algorithms": ["ak4PFJetsCHS"],
		# NPV hardcoded from Dominik's ``get_weights`` script output @ 20150804
		"_npv_weights" : ["1", "(npv==1)*38.9021+(npv==2)*2.3337+(npv==3)*2.44477+(npv==4)*1.70175+(npv==5)*1.52866+(npv==6)*1.31595+(npv==7)*1.35314+(npv==8)*1.34328+(npv==9)*1.38119+(npv==10)*1.28674+(npv==11)*1.22246+(npv==12)*1.188+(npv==13)*1.14079+(npv==14)*1.13437+(npv==15)*1.10264+(npv==16)*1.0896+(npv==17)*0.953372+(npv==18)*0.917887+(npv==19)*0.739569+(npv==20)*0.707311+(npv==21)*0.637729+(npv==22)*0.570234+(npv==23)*0.471585+(npv==24)*0.391797+(npv==25)*0.279881+(npv==26)*0.247282+(npv==27)*0.171765+(npv==28)*0.146706+(npv==29)*0.150545+(npv==30)*0.0927622"],
	}
	jec_combination(args, d)


def jec_combination_20150814(args=None):
	d = {
		'files': [
			'ntuples/Data_13TeV_74X_E2_50ns_JECSummerV4_2015-08-14.root',
			'ntuples/MC_13TeV_74X_E2_50ns_JECSummerV4_2015-08-14.root',
		],
		"algorithms": ["ak4PFJetsCHS"],
		# NPV hardcoded from Dominik's ``get_weights`` script output @ 20150814
		"_npv_weights" : ["1", "(npv==1)*14.8846+(npv==2)*3.58332+(npv==3)*1.84285+(npv==4)*2.45195+(npv==5)*1.50428+(npv==6)*0.996686+(npv==7)*1.34553+(npv==8)*1.26528+(npv==9)*1.21698+(npv==10)*1.20916+(npv==11)*1.14444+(npv==12)*1.09916+(npv==13)*1.1722+(npv==14)*1.11612+(npv==15)*1.202+(npv==16)*1.12021+(npv==17)*1.00273+(npv==18)*1.00425+(npv==19)*0.768872+(npv==20)*0.785899+(npv==21)*0.649426+(npv==22)*0.714884+(npv==23)*0.534425+(npv==24)*0.278714+(npv==25)*0.333719+(npv==26)*0.28414+(npv==27)*0.0830113+(npv==28)*0.171738+(npv==29)*0.145598+(npv==30)*0.13861"],
	}
	jec_combination(args, d)


def jec_combination_25ns_20151001(args=None):
	d = {
		'files': [
			'ntuples/Data_13TeV_74X_E2_25ns_JECV3_2015D_2015-10-01.root',
			'ntuples/MC_13TeV_74X_E2_25ns_JECV3_2015-10-01.root',
		],
		"algorithms": ["ak4PFJetsCHS"],
		# NPV hardcoded from Dominik's ``get_weights`` script output @ 20151001
		"_npv_weights" : ["(weight)", "(weight)*((npv==1)*6.9295+(npv==2)*4.58177+(npv==3)*3.68256+(npv==4)*3.39719+(npv==5)*3.06555+(npv==6)*2.74328+(npv==7)*2.418+(npv==8)*2.02356+(npv==9)*1.71068+(npv==10)*1.37638+(npv==11)*1.07853+(npv==12)*0.814396+(npv==13)*0.60545+(npv==14)*0.443644+(npv==15)*0.322044+(npv==16)*0.215438+(npv==17)*0.145175+(npv==18)*0.104847+(npv==19)*0.0769262+(npv==20)*0.0508476+(npv==21)*0.0331774+(npv==22)*0.0311605+(npv==23)*0.0153405+(npv==24)*0.0131355+(npv==25)*0.00283383+(npv==26)*0.0132552+(npv==27)*0+(npv==28)*0+(npv==29)*0+(npv==30)*0)"],
	}
	jec_combination(args, d)


def jec_combination_25ns_20151016(args=None):
	plots = []
	mc_file = 'ntuples/MC_13TeV_74X_E2_25ns_2015-10-18.root'
	for label in [
		'', '_DCSOnly',
		'_2015C', '_2015D',
		'_DCSOnly_2015C', '_DCSOnly_2015D'
	]:
		data_file = 'ntuples/Data_13TEV_74X_E2_25ns%s_2015-10-16.root' % label
		file_label = label[1:]+'_' if label.startswith('_') and not label.endswith('_') else label
		d = {
			'files' : [data_file, mc_file],
			"algorithms": ["ak4PFJetsCHS"],
			"_npv_weights" : ["1", subprocess.check_output(["get_weights.sh", data_file, mc_file]).strip()],
			"file_label" : file_label,
		}
		print "Prepared: '%s'" % label
		plots.append(d)
	for d in plots:
		jec_combination(args, d)

def jec_combination_20151204_Zee(args=None):
	d = {
		'files': [
			'ntuples/Data_Zee_13TeV_74X_E2_25ns_2015-12-04.root',
			'ntuples/MC_Zee_13TeV_74X_E2_25ns_2015-12-04.root',
		],
		"algorithms": ["ak4PFJetsCHS",],
	}
	jec_combination(args, d)
