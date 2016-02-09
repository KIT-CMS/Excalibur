#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface
from Excalibur.Plotting.utility.colors import histo_colors
from dicts_z_ee import color
from dicts_z_ee import latex
from dicts_z_ee import weighting_z
from dicts_z_ee import weighting_e
from dicts_z_ee import jmzexpress
from dicts_z_ee import jmzlabel
from dicts_z_ee import jmzbin
from dicts_z_ee import ejmexpress
from dicts_z_ee import ejmlabel
from dicts_z_ee import ejmbin

#Features ee_jet_muon_comparison functions in first half, then same functions with Z instead of ee

###########################
def ee_jet_muon_comparison(args=None, additional_dictionary=None, run=2):
	""" Quality of reconstruction of pt, eta, phi for (jet1, muminus, eminus) in one plot. 
	1D-plots of eminus/geneminus, muminus/genmuminus and jet1/genjet1 together in one diagram for pt, phi, eta each, with weights for pt>50, 50<pt<100, pt>100.
	"""
	
	#Plotting
	plots = []
	parameterlist = ['pt', 'phi', 'eta']
	weightinglist_pt = ["0_pt_noweight", "1_pt_lower50", "2_pt_50to100", "3_pt_higher100"]
	if run==2: 
		files=['work/mc15_25ns_ee.root','work/mc15_25ns.root', 'work/mc15_25ns.root'],
		algo =['ak4PFJetsCHS'],
	elif run==1:
		files =['work/mc_ee.root', 'work/mc.root', 'work/mc.root'],
		algo = ['ak5PFJetsCHS'],
	
	for parameter in parameterlist:
		for selection in weightinglist_pt:

			#1D-plots 
			d_1 = {
				#get data
				'files':files,
				'corrections': ['L1L2L3'],
				'algorithms': algo,
				#'zjetfolders':['zcuts'],

				#binning
				'x_expressions': [ejmexpress["e{}".format(parameter)],ejmexpress["jet{}".format(parameter)],ejmexpress["mu{}".format(parameter)]],
				'x_label': ejmlabel['{}'.format(parameter)],
				'x_bins': ejmbin['{}'.format(parameter)],
				'y_label':'Electron Events',

				#weights and normalization
				'weights': weighting_e[selection],
				'analysis_modules': ['NormalizeToFirstHisto','NormalizeToFirstHisto','NormalizeToFirstHisto'],

				
				#nicknames, text
				'nicks': ["eminus","jet1","mu"],
				'labels': [latex["eminus"],latex["jet1"],latex["muminus"]],
				'colors': [color['e'], color['jet'],color['mu']],
				'texts': '{}'.format(latex[selection]),
				'title':'Reconstruction\n of {}'.format(latex[parameter]),
		
				#formatting
				'filename': 'comparison_rel_recogen_{}_{}'.format(parameter, selection),
				'markers': ['_', '4', '3'],
				'marker_fill_styles': ['none', 'none', 'none'],
				'line_styles': ['-'],
				'step': True,
			}
			plots.append(d_1)

	for d in plots:
		d.update({
			# web gallery options
			'www_title': 'Reco-gen-comparisons: jet muon eminus',
			'www_text': 'Comparison of reco- and gen-level pT,eta,phi of muons, jets and electrons for different weightings of pt.',
		})
	harryinterface.harry_interface(plots, args)


############################################
def ee_jet_muon_comparison_tree(args=None, additional_dictionary=None, run=2):
	"""Comparison of jet, muon, e reconstruction depending on pt: Tree-plots of eminus/geneminus, muminus/genmuminus and jet1/genjet1 together in one diagram for pt, phi, eta each. Additionally, plots of  statistical errors of said Tree-plots depending on pt.
	"""

	run=2
	
	plots = []
	parameterlist_jet1 = ['pt', 'phi', 'eta']

	bins = {
		"pt" : ['20 30 40 50 60 70 95 150 275 400 700'],
		"phi" : ['10 20 30 40 50 60 70 80 90 100 150 200 250 300 400 500 700'],
		"eta" : ['10 20 30 40 50 60 70 80 90 100 150 200 250 300 400 500 700'],
	}
	if run==2: 
		files=['work/mc15_25ns_ee.root','work/mc15_25ns.root', 'work/mc15_25ns.root'],
		algo =['ak4PFJetsCHS'],
	elif run==1:
		files =['work/mc_ee.root', 'work/mc.root', 'work/mc.root'],
		algo = ['ak5PFJetsCHS'],

	for parameter in parameterlist_jet1:

		#Tree-plots 
		d_1 = {
			#get data
			'files':files,
			'corrections': ['L1L2L3'],
			'algorithms': algo,
			#'zjetfolders':['zcuts'],

			#binning
			'x_expressions':["geneminuspt","genjet1pt","genmuminuspt"],
			'y_expressions':[ejmexpress["e{}".format(parameter)],ejmexpress["jet{}".format(parameter)],ejmexpress["mu{}".format(parameter)]],
			'tree_draw_options': 'profs',
			"x_ticks": [20,30,50,70,100,200,400,700], 
			'x_bins': bins[parameter],
			'x_log': True,

			#formatting
			'nicks': ["eminus","jet1","mu"],
			'labels': [latex["eminus"],latex["jet1"],latex["muminus"]],
			'colors': [color['e'],color['jet'], color['mu']],
			'texts': '{} - $error$ $bars$ $show$ $standard$ $deviation$'.format(latex[parameter]),
			'x_label': "{}$/GeV$".format(latex["pt"]),
			'y_label': ejmlabel['{}'.format(parameter)],
			'title':'Reconstruction of {} \n depending on {}'.format(latex[parameter], latex['pt']),
			'markers': ['_', '4', '3'],
			'marker_fill_styles': ['none', 'none', 'none'],
			'line_styles': ['-'],
			'step':'True',
			'filename': 'comparison_rel_recogen_{}_tree'.format(parameter),
		}
		plots.append(d_1)

		# shows errors in bin contents
		d_2 = {
			#get data
			'files':files,
			'corrections': ['L1L2L3'],
			'algorithms': algo,
			#'zjetfolders':['zcuts'],

			#binning
			'x_expressions':["geneminuspt","genjet1pt","genmuminuspt"],
			'y_expressions':[ejmexpress["e{}".format(parameter)], ejmexpress["jet{}".format(parameter)],ejmexpress["mu{}".format(parameter)]],
			'tree_draw_options':  'profs',
			"x_ticks": [20,30,50,70,100,200,400,700],
			'x_bins': bins[parameter],
			'x_log': True,
			'analysis_modules': ['ConvertToHistogram', 'StatisticalErrors',],
			'stat_error_nicks': ["e","jet1","mu"],
			'convert_nicks': ["e","jet1","mu"],
			
			#formatting
			'nicks': ["e","jet1","mu"],
			'labels': [latex["eminus"],latex["jet1"],latex["muminus"]],
			'colors': [color['e'], color['jet'],color['mu']],
			'x_label': "{}$/GeV$".format(latex["pt"]),
			'y_label': "{} $resolution$".format(latex[parameter]),
			'texts': '{} - $statistical$ $errors$'.format(latex[parameter]),
			'title':'Resolution of {} \n depending on {}'.format(latex[parameter], latex['pt']),
			'y_errors': 'none',
			'markers': ['.', '.', '.'],
			'marker_fill_styles': ['full', 'full', 'full'],
			'line_styles': ['-'],
			'step':'True',
			'filename': 'comparison_rel_recogen_{}_staterrors'.format(parameter),
		}
		plots.append(d_2)

	for d in plots:
		d.update({
			# web gallery options
			'www_title': 'Reco-gen-comparisons (tree): jet muon eminus',
			'www_text': 'Comparison of reco- and gen-level pT,eta,phi of muons, jets and electrons for different weightings of pt. High resolution-value indicates worse resolution than low res-value.',
		})

	harryinterface.harry_interface(plots, args)


############################################
def ee_jet_muon_comp_npv_tree(args=None, additional_dictionary=None, run=2):
	"""Comparison of jet, muon, e reconstruction depending on number of pileupevents (npv): Tree-plots of eminus/geneminus, muminus/genmuminus and jet1/genjet1 together in one diagram for pt, phi, eta each. Additionally, plots of  statistical errors of said Tree-plots depending on npv.
	"""

	plots = []
	parameterlist_jet1 = ['pt', 'phi', 'eta']
	bins = {
		"pt" : ['35,-0.5,34.5'],
		"phi" : ['35,-0.5,34.5'],
		"eta" : ['35,-0.5,34.5'],
	}
	weightlist ={
		"e" : "(eminuspt/geneminuspt>0&&eminuspt/geneminuspt<5)",
		"jet" : "(jet1pt/genjet1pt>0&&jet1pt/genjet1pt<5)",
		"mu" : "(muminuspt/genmuminuspt>0&&muminuspt/genmuminuspt<5)",
	}
	if run==2: 
		files=['work/mc15_25ns_ee.root','work/mc15_25ns.root', 'work/mc15_25ns.root'],
		algo =['ak4PFJetsCHS'],
	elif run==1:
		files =[ 'work/mc_ee.root', 'work/mc.root', 'work/mc.root'],
		algo = ['ak5PFJetsCHS'],

	for parameter in parameterlist_jet1:

		#Tree-plots 
		d_1 = {
			#get data
			'files':files,
			'algorithms': algo,
			'corrections': ['L1L2L3'],
			'zjetfolders':['zcuts'],
			'weights':[weightlist['e'], weightlist['jet'], weightlist['mu']],

			#binning
			'x_expressions':["npv","npv","npv"],
			'y_expressions':[ejmexpress["e{}".format(parameter)],ejmexpress["jet{}".format(parameter)],ejmexpress["mu{}".format(parameter)]],
			'tree_draw_options': 'profs',
			#'x_bins': bins[parameter],
			'x_log': True,

			#formatting
			'nicks': ["eminus","jet1","mu"],
			'labels': [latex["eminus"],latex["jet1"],latex["muminus"]],
			'colors': [ color['e'],color['jet'],color['mu']],
			'texts': '{} - $error$ $bars$ $show$ $standard$ $deviation$'.format(latex[parameter]),
			'x_label': "$pileup$ $activity$ $n_{{PV}}$",
			'y_label': ejmlabel['{}'.format(parameter)],
			'title':'Reconstruction of {} \n depending on npv'.format(latex[parameter], latex['pt']),
			'markers': ['_', '4', '3'],
			'marker_fill_styles': ['none', 'none', 'none'],
			'line_styles': ['-'],
			'step':'True',
			'filename': 'resolution_{}_pileup_tree'.format(parameter),
		}
		plots.append(d_1)

		# shows errors in bin contents
		d_2 = {
			#get data
			'files':files,
			'algorithms': algo,
			'corrections': ['L1L2L3'],
			'zjetfolders':['zcuts'],
			'weights':[weightlist['jet'], weightlist['mu'], weightlist['e']],

			#binning
			'x_expressions':["npv","npv","npv"],
			'y_expressions':[ejmexpress["e{}".format(parameter)],ejmexpress["jet{}".format(parameter)],ejmexpress["mu{}".format(parameter)]],
			'tree_draw_options': 'profs',
			'x_bins': bins[parameter],
			'x_log': True,
			'analysis_modules': ['ConvertToHistogram', 'StatisticalErrors',],
			'stat_error_nicks': ["e","jet1","mu"],
			'convert_nicks': ["e","jet1","mu"],
			
			#formatting
			'nicks': ["e","jet1","mu"],
			'labels': [latex["eminus"],latex["jet1"],latex["muminus"]],
			'colors': [ color['e'],color['jet'],color['mu']],
			'x_label': "$pileup$ $activity$ $npv$".format(latex["pt"]),
			'y_label': "{} $resolution$".format(latex[parameter]),
			'texts': '{} - $statistical$ $errors$'.format(latex[parameter]),
			'title':'Resolution of {} \n depending on $n_{{PV}}$'.format(latex[parameter]),
			'y_errors': 'none',
			'markers': ['.', '.', '.'],
			'marker_fill_styles': ['full', 'full', 'full'],
			'line_styles': ['-'],
			'step':'True',
			'filename': 'resolution_{}_pileup_staterrors'.format(parameter),
			
			'y_lims':[0,0.5],
		}
		plots.append(d_2)

	for d in plots:
		d.update({
			# web gallery options
			'www_title': 'Reco-gen-comparisons (tree): jet muon eminus',
			'www_text': 'Comparison of pT,eta,phi resolution of muons, jets and electrons as a function on pileup activity. High resolution-value indicates worse resolution than low res-value.',
		})

	harryinterface.harry_interface(plots, args)



#From here on same functions as above, only with Z instead of e
##############################
def jet_muon_z_comparison(args=None, additional_dictionary=None, run=2):
	"""9 plots: 1D-plots of Z/genZ, muminus/genmuminus and jet1/genjet1 together in one diagram for pt, phi, eta each, with weights for pt>50, 50<pt<100, pt>100 
	"""

	plots = []
	parameterlist_jet1 = ['pt', 'phi', 'eta']
	weightinglist_pt = ["0_pt_noweight", "1_pt_lower50", "2_pt_50to100", "3_pt_higher100"]
	if run==2: 
		files=['work/mc15_25ns.root'],
		algo =['ak4PFJetsCHS'],
	elif run==1:
		files =[ 'work/mc.root'],
		algo = ['ak5PFJetsCHS'],

	for parameter in parameterlist_jet1:
		for selection in weightinglist_pt:

			#1D-plots 
			d_1 = {
				#get data
				'files':files,
				'corrections': ['L1L2L3'],
				'algorithms': algo,

				#binning
				'x_expressions': [jmzexpress["jet{}".format(parameter)],jmzexpress["mu{}".format(parameter)],jmzexpress["z{}".format(parameter)]],
				'x_label': jmzlabel['{}'.format(parameter)],
				'x_bins': jmzbin['{}'.format(parameter)],
				
				#weights and normalization
				'weights': weighting_z[selection],
				'analysis_modules': ['NormalizeToFirstHisto',],

				
				#nicknames, text
				'nicks': ["jet1","mu","z"],
				'labels': [latex["jet1"],latex["muminus"],latex["z"]],
				'colors': [color['jet'],color['mu'], color['z']],
				'texts': '{}'.format(latex[selection]),
				'title':'Reconstruction of {}'.format(latex[parameter]),
		
				#formatting
				'filename': 'comparison_rel_recogen_{}_{}'.format(parameter, selection),
				'markers': ['_', '4', '3'],
				'marker_fill_styles': ['none', 'none', 'none'],
				'line_styles': ['-'],
				'step': True,
			}
			plots.append(d_1)
			#print d_1

	for d in plots:
		d.update({
			# web gallery options
			'www_title': 'Reco-gen-comparisons',
			'www_text': 'Comparison of reco- and gen-level pT,eta,phi of muons, jets and Z bosons for different weightings of pt.',
		})
	harryinterface.harry_interface(plots, args)


############################
def jet_muon_z_comparison_tree(args=None, additional_dictionary=None, run=2):
	"""Comparison of jet, muon, z reconstruction quality depending on pT: Tree-plots of Z/genZ, muminus/genmuminus and jet1/genjet1 together in one diagram for pt, phi, eta each 
	"""
	
	plots = []
	parameterlist_jet1 = ['pt', 'phi', 'eta']

	bins = {
		"pt" : ['10 30 40 50 60 70 80 90 100 150 200 300 500 700'],
		"phi" : ['10 30 40 50 60 70 80 90 100 150 200 250 300 400 500 600'],
		"eta" : ['10 30 40 50 60 70 80 90 100 150 200 250 300 400 500 600'],
	}
	if run==2: 
		files=['work/mc15_25ns.root'],
		algo =['ak4PFJetsCHS'],
	elif run==1:
		files =[ 'work/mc.root'],
		algo = ['ak5PFJetsCHS'],

	for parameter in parameterlist_jet1:

		#Tree-plots 
		d_1 = {
			#get data
			'files':files,
			'algorithms': algo,
			'corrections': ['L1L2L3'],

			#binning
			'x_expressions':["genjet1pt","genmuminuspt","genzpt"],
			'y_expressions':[jmzexpress["jet{}".format(parameter)],jmzexpress["mu{}".format(parameter)],jmzexpress["z{}".format(parameter)]],
			'y_label': jmzlabel['{}'.format(parameter)],
			'tree_draw_options':  'profs',
			'x_bins': bins[parameter],

			#nicknames, text
			'nicks': ["jet1","mu","z"],
			'labels': [latex["jet1"],latex["muminus"],latex["z"]],
			'colors': [color['jet'],color['mu'], color['z']],
			'texts': '{} - $error$ $bars$ $show$ $standard$ $deviation$'.format(latex[parameter]),
			'x_label': "{}$/GeV$".format(latex["pt"]),
			'y_label': (r"{}$_{{reco}}/${}$_{{gen}}$".format(latex[parameter],latex[parameter])),
			'x_log': True,

			#formatting
			'filename': 'comparison_rel_recogen_{}_tree'.format(parameter),
			'markers': ['_', '4', '3'],
			'marker_fill_styles': ['none', 'none', 'none'],
			'line_styles': ['-'],
			'step':'True',
		}
		plots.append(d_1)

		# shows errors in bin contents
		d_2 = {
			#get data
			'files':files,
			'algorithms': algo,
			'corrections': ['L1L2L3'],

			#binning
			'x_expressions':["genjet1pt","genmuminuspt","genzpt"],
			'y_expressions':[jmzexpress["jet{}".format(parameter)],jmzexpress["mu{}".format(parameter)],jmzexpress["z{}".format(parameter)]],
			'tree_draw_options':  'profs',
			'x_bins': bins[parameter],

			'analysis_modules': ['ConvertToHistogram', 'StatisticalErrors',],
			'stat_error_nicks': ["jet1","mu","z"],
			'convert_nicks': ["jet1","mu","z"],
			
			#nicknames, text
			'nicks': ["jet1","mu","z"],
			'labels': [latex["jet1"],latex["muminus"],latex["z"]],
			'colors': [color['jet'],color['mu'], color['z']],
			'x_label': "{}$/GeV$".format(latex["pt"]),
			'y_label': "{} $resolution$".format(latex[parameter]),
			'texts': '{} - $statistical$ $errors$'.format(latex[parameter]),
			'x_log': True,

			#formatting
			'y_errors': 'none',
			'filename': 'comparison_rel_recogen_{}_staterrors'.format(parameter),
			'markers': ['_', '4', '3'],
			'marker_fill_styles': ['none', 'none', 'none'],
			'line_styles': ['-'],
			'step':'True',
		}
		plots.append(d_2)
		

	for d in plots:
		d.update({
			# web gallery options
			'www_title': 'Reco-gen-comparisons',
			'www_text': 'Comparison of reco- and gen-level pT,eta,phi of muons, jets and Z bosons for different weightings of pt. High resolution-value indicates worse resolution than low res-value.',
		})
	harryinterface.harry_interface(plots, args)


#############
def zmass_ee_mm(args=None, additional_dictionary=None, run=2):
	"""1D histograms for Zmass calculated from ee and mm
	"""

	plots = []
	if run==2: 
		files=['work/mc15_25ns_ee.root','work/mc15_25ns.root', 'work/mc15_25ns.root'],
		algo =['ak4PFJetsCHS'],
	elif run==1:
		files =[ 'work/mc_ee.root', 'work/mc.root', 'work/mc.root'],
		algo = ['ak5PFJetsCHS'],
	d_1 = {
		#get data
		'files':files,
		'algorithms': algo,
		'corrections': ['L1L2L3'],

		#binning
		'x_expressions': ["zmass","zmass", 'genzmass'],
		'x_bins': '20,81,102',
		'x_label':'$m_{{Z}}$ / GeV',

		#formatting
		'nicks': ["ze","zmu", 'genz'],
		'labels': ["$Z_{e}$",r"$Z_{{\\mu}}$","$Z_{gen}$"],
		'colors': [color['e'],color['mu'], color['undef']],
		'filename': 'zmass_ee_mm_comparison_run{}'.format(str(run)),
		'analysis_modules': ['NormalizeToFirstHisto',],
		'y_label':'Electron Events',
		'markers': ['_', '4', '3'],
		'marker_fill_styles': ['none', 'none', 'none'],
		'line_styles': ['-'],
		'step':['True','True','True'],
		'title':r'Zmass calculated \n from ee and $\\mu\\mu$',
	}
	plots.append(d_1)

	for d in plots:
		d.update({
			# web gallery options
			'www_title': 'Comparison of Zmass',
			'www_text': 'Comparison of Zmass calculated from ee and mm',
		})
	harryinterface.harry_interface(plots, args)



if __name__ == '__main__':
	muoniso_aod()
