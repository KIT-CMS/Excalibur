# -*- coding: utf-8 -*-

import time

import Excalibur.Plotting.harryinterface as harryinterface
import Artus.Utility.logger as logger

def jec_combination(args=None, additional_dictionary=None):
	"""function to create the root combination file for the jec group."""
	mpl_plots = []
	root_plots = []

	methoddict = {
		'ptbalance': 'PtBal',
		'mpf': 'MPF',
		'rawmpf': 'MPF-notypeI',
	}

	alpha_limits = [0.1, 0.15, 0.2, 0.3, 0.4]
	alpha_cuts = ['(alpha<{})'.format(limit) for limit in alpha_limits]
	alpha_strings = ['a'+str(int(100*limit)) for limit in alpha_limits]

	eta_borders = [0, 0.783, 1.305, 1.93, 2.5, 2.964, 3.2, 5.191]
	eta_cuts = ["({0}<=abs(jet1eta)&&abs(jet1eta)<{1})".format(*b) for b in zip(eta_borders[:-1], eta_borders[1:])]
	eta_cuts = ["(0<=abs(jet1eta)&&abs(jet1eta)<1.3)"] + eta_cuts # also include standard barrel jet selection
	eta_strings = ["eta_{0:0>2d}_{1:0>2d}".format(int(round(10*up)), int(round(10*low))) for up, low in zip(eta_borders[:-1], eta_borders[1:])]
	eta_strings = ["eta_00_13"] + eta_strings
	try:
		npv_weights = additional_dictionary.pop("_npv_weights")
	except (AttributeError, KeyError):
		npv_weights = ["1"]

	now = time.localtime()
	first = True
	for method in ['mpf', 'ptbalance', 'rawmpf']:
		for alphacut, alphastring in zip(alpha_cuts, alpha_strings):
			for etacut, etastring in zip(eta_cuts, eta_strings):
				for correction in ['L1L2L3']: # no L1L2L3Res available atm
					labelsuffix = '_'.join([methoddict[method], 'CHS', alphastring, etastring, correction])
					eta_alpha_cut = '&&'.join((alphacut, etacut))
					d = {
						# input
						'x_expressions': ['zpt'],
						'y_expressions': [method],
						'x_bins': 'zpt',
						'corrections': [correction],
						'zjetfolders': ['noalphanoetacuts'],
						'weights': ["(%s)*(%s)" % (eta_alpha_cut, npv_weight) for npv_weight in npv_weights],
						'tree_draw_options' : 'prof',
						# ratio, labels
						'analysis_modules': ['Ratio', 'ConvertToTGraphErrors'],
						'labels': ['_'.join([item, labelsuffix]) for item in ['Data', 'MC', 'Ratio']],
						# output
						'filename': labelsuffix,
					}
					if additional_dictionary is not None:
						d.update(additional_dictionary)
					d_root = d.copy()
					d_root.update({
						'plot_modules': ['ExportRoot'],
						'filename': 'combination_ZJet_' + time.strftime("%Y-%m-%d", now),
						'file_mode': ('RECREATE' if first else 'UPDATE'),
					})
					first = False
					mpl_plots.append(d)
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