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


def jec_combination(args=None, additional_dictionary=None, algo = 'CHS'):
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
#	alpha_limits = [0.4]
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
					'ratio_denominator_no_errors': False,
				}
				# histograms - raw event counts
				labelsuffix = '_'.join(['RawNEvents', algo, alphastring, etastring, correction])
				d_mpl = {
					'x_expressions': ['zpt'],
					'x_bins': 'zpt',
					'labels': ['_'.join([item, labelsuffix]) for item in ['Data', 'MC', 'Ratio']],
					'filename': labelsuffix + file_label,
					'no_weight': True, #Remove reweights in MC
				}
				d_mpl.update(base_plot)
				if additional_dictionary is not None:
					d_mpl.update(additional_dictionary)
				del d_mpl['tree_draw_options']
				d_root = mpl_to_root(d_mpl)
				# make plots comparable to jec_comparison
				d_mpl['x_log'] = True
				d_mpl['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]
				mpl_plots.append(d_mpl)
				root_plots.append(d_root)
				# profiles - responses
				for method in ['mpf', 'ptbalance', 'rawmpf', 'zmass']:
					labelsuffix = '_'.join([label_dict[method], algo, alphastring, etastring, correction])
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
					labelsuffix = "_".join((y_expression, "vs", x_expression, algo, alphastring, etastring, correction))
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


def jec_pu_combination(args=None, additional_dictionary=None, algo='CHS'):
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
			labelsuffix = "_".join((x_expression, "vs", y_expression, algo, correction))
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

FOLDER='/storage/jbod/tberger/zjets/excalibur_results_datamc_Summer16_03Feb2017_V7/'

def jec_combination_CHS_Zmm_BCD(args=None):
	d = {
		'files': [
			FOLDER+'data16_BCD_mm_remini.root',
			FOLDER+'mc16_BCDEFGH_mm_madgraph_NJ.root',
		],
		#"algorithms": ["ak4PFJetsCHS"],
		"output_dir": 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/combination_Zmm_BCD_remini_madgraph_NJ',
		'file_label' : 'Zmm_BCD_',
#	 	"www": 'jec_combination_CHS_Zmm_fullalpha',
	}
	jec_combination(args, d, 'CHS')

def jec_combination_CHS_Zmm_EF(args=None):
	d = {
		'files': [
			FOLDER+'data16_EF_mm_remini.root',
			FOLDER+'mc16_BCDEFGH_mm_madgraph_NJ.root',
		],
		#"algorithms": ["ak4PFJetsCHS"],
		'file_label' : 'Zmm_EF_',
		"output_dir": 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/combination_Zmm_EF_remini_madgraph_NJ',
#		"www": 'jec_combination_CHS_Zmm_fullalpha',
	}
	jec_combination(args, d, 'CHS')

def jec_combination_CHS_Zmm_G(args=None):
	d = {
		'files': [
			FOLDER+'data16_G_mm_remini.root',
			FOLDER+'mc16_BCDEFGH_mm_madgraph_NJ.root',
		],
		#"algorithms": ["ak4PFJetsCHS"],
		'file_label' : 'Zmm_G_',
		"output_dir": 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/combination_Zmm_G_remini_madgraph_NJ',
#		"www": 'jec_combination_CHS_Zmm_fullalpha',
	}
	jec_combination(args, d, 'CHS')

def jec_combination_CHS_Zmm_H(args=None):
	d = {
		'files': [
			FOLDER+'data16_H_mm_remini.root',
			FOLDER+'mc16_BCDEFGH_mm_madgraph_NJ.root',
		],
		#"algorithms": ["ak4PFJetsCHS"],
		'file_label' : 'Zmm_H_',
		"output_dir": 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/combination_Zmm_H_remini_madgraph_NJ',
#		"www": 'jec_combination_CHS_Zmm_fullalpha',
	}
	jec_combination(args, d, 'CHS')

def jec_combination_CHS_Zmm_BCDEFGH(args=None):
	d = {
		'files': [
			FOLDER+'data16_BCDEFGH_mm_remini.root',
			FOLDER+'mc16_BCDEFGH_mm_madgraph_NJ.root',
		],
		#"algorithms": ["ak4PFJetsCHS"],
		'file_label' : 'Zmm_BCDEFGH_',
		"output_dir": 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/combination_Zmm_BCDEFGH_remini_madgraph_NJ',
#		"www": 'jec_combination_CHS_Zmm_fullalpha',
	}
	jec_combination(args, d, 'CHS')
		
def jec_combination_CHS_Zee_BCD(args=None):
	d = {
		'files': [
			FOLDER+'data16_BCD_ee_remini.root',
			FOLDER+'mc16_BCDEFGH_ee_madgraph_NJ.root',
		],
		#"algorithms": ["ak4PFJetsCHS"],
		'file_label' : 'Zee_BCD_',
		"output_dir": 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/combination_Zee_BCD_remini_madgraph_NJ',
#		"www": 'jec_combination_CHS_Zee_fullalpha',
	}
	jec_combination(args, d, 'CHS')
	
def jec_combination_CHS_Zee_EF(args=None):
	d = {
		'files': [
			FOLDER+'data16_EF_ee_remini.root',
			FOLDER+'mc16_BCDEFGH_ee_madgraph_NJ.root',
		],
		#"algorithms": ["ak4PFJetsCHS"],
		'file_label' : 'Zee_EF_',
		"output_dir": 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/combination_Zee_EF_remini_madgraph_NJ',
#		"www": 'jec_combination_CHS_Zee_fullalpha',
	}
	jec_combination(args, d, 'CHS')

def jec_combination_CHS_Zee_G(args=None):
	d = {
		'files': [
			FOLDER+'data16_G_ee_remini.root',
			FOLDER+'mc16_BCDEFGH_ee_madgraph_NJ.root',
		],
		#"algorithms": ["ak4PFJetsCHS"],
		'file_label' : 'Zee_G_',
		"output_dir": 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/combination_Zee_G_remini_madgraph_NJ',
#		"www": 'jec_combination_CHS_Zee_fullalpha',
	}
	jec_combination(args, d, 'CHS')
	
def jec_combination_CHS_Zee_H(args=None):
	d = {
		'files': [
			FOLDER+'data16_H_ee_remini.root',
			FOLDER+'mc16_BCDEFGH_ee_madgraph_NJ.root',
		],
		#"algorithms": ["ak4PFJetsCHS"],
		'file_label' : 'Zee_H_',
		"output_dir": 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/combination_Zee_H_remini_madgraph_NJ',
#		"www": 'jec_combination_CHS_Zee_fullalpha',
	}
	jec_combination(args, d, 'CHS')
	
def jec_combination_CHS_Zee_BCDEFGH(args=None):
	d = {
		'files': [
			FOLDER+'data16_BCDEFGH_ee_remini.root',
			FOLDER+'mc16_BCDEFGH_ee_madgraph_NJ.root',
		],
		#"algorithms": ["ak4PFJetsCHS"],
		'file_label' : 'Zee_BCDEFGH_',
		"output_dir": 'plots_'+time.strftime("%Y_%m_%d", time.localtime())+'/combination_Zee_BCDEFGH_remini_madgraph_NJ',
#		"www": 'jec_combination_CHS_Zee_fullalpha',
	}
	jec_combination(args, d, 'CHS')
	
