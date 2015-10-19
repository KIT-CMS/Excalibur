#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface
from Excalibur.Plotting.utility.colors import histo_colors

color = {
	"mu": 'blue',
	"e": 'red',
	"jet": 'black',
	"z": histo_colors['green'],
	"undef": histo_colors['yellow'],
	"undef2": histo_colors['grey'],
}
#Latex
latex = {
	"jet1" : ['$Jet1$'],
	"muminus" : r'$\\mu^-$',
	"eminus" : "$e^-$",
	"pt" : "$p_{{T}}$",
	"phi" : r"$\\phi$",
	"eta" : r"$\\eta$",
	"z" : "$Z$",
	"y" : "$y$",
	"mass" : "$mass$",
	#weightinglabels
	"0_pt_noweight" : '$gen p_{{T}}$',
	"1_pt_lower50" : '$gen p_{{T}}$ $<$ $50$ $GeV$',
	"2_pt_50to100" : '$50$ $GeV$ $<$ $gen p_{{T}}$ $<$ $100$ $GeV$',
	"3_pt_higher100" : '$gen p_{{T}}$ $>$ $100$ $GeV$',
}

#weightings for pt, used in jet_muon_z_comparison and jet_muon_ee_comparison
weighting_z = {
		"0_pt_noweight" : ["1", "1", "1"],
		"1_pt_lower50" : ["(genjet1pt<50)", "(genmuminuspt<50)", "(genzpt<50)"],
		"2_pt_50to100" : ["(genjet1pt>50&&genjet1pt<100)", "(genmuminuspt>50&&genmuminuspt<100)", "(genzpt>50&&genzpt<100)"],
		"3_pt_higher100" : ["(genjet1pt>100)", "(genmuminuspt>100)", "(genzpt>100)"],
}
weighting_e = {
		"0_pt_noweight" : ["1", "1", "1"],
		"1_pt_lower50" : ["(genjet1pt<50)", "(genmuminuspt<50)", "(geneminuspt<50)"],
		"2_pt_50to100" : ["(genjet1pt>50&&genjet1pt<100)", "(genmuminuspt>50&&genmuminuspt<100)", "(geneminuspt>50&&geneminuspt<100)"],
		"3_pt_higher100" : ["(genjet1pt>100)", "(genmuminuspt>100)", "(geneminuspt>100)"],
}




#########################
def reco_gen_comparison(args=None, additional_dictionary=None):
	"""Plots 2D plots of reco and gen for Z, jet1, muminus, as well as 1D-plots of Z/genZ and jet1/genjet1 for various parameters
	"""
	#binning overall number, start, stop
	startstop = {

		'pt' : ['30', '0', '250'],
		'phi' : ['30', '-2', '2'],
		'eta' : ['30', '-3.14', '3.14'],
		'y' : ['30', '-2.5', '2.5'],
		'mass': ['30', '85', '100'],
	}

	plots = []
	parameterlist_z =['pt', 'phi', 'y', 'mass']
	parameterlist_jet1 =['pt', 'phi', 'eta']

	#2D-plots of Z vs genZ and jet1 vs genjet1 for various parameters
	for objct, parameterlist in zip(['z', 'jet1', 'muminus',], [parameterlist_z, parameterlist_jet1, parameterlist_jet1]):

		#Plots
		for parameter  in parameterlist:

			#2D-plots of Z vs genZ and jet1 vs genjet1 for various parameters
			d_2 = {
				#get data
				'files':[ 'work/mc.root'],
				'corrections': ['L1L2L3'],

				#binning
				'x_expressions': ["gen{}{}".format(objct, parameter),],
				'y_expressions': ["{}{}".format(objct, parameter),],
				'x_bins': ','.join(startstop[parameter]),
				'y_bins': ','.join(startstop[parameter]),

				#formatting
				'y_lims': [float(startstop[parameter][1]), float(startstop[parameter][2])],
				'x_lims': [float(startstop[parameter][1]), float(startstop[parameter][2])],
				'filename': '{}{}_VS_gen{}{}'.format(objct, parameter, objct, parameter),
				'title':'{}{} vs gen{}{}'.format(objct, parameter, objct, parameter),
			}
			plots.append(d_2)

			#1D-plots of Z/genZ and jet1/genjet1 for various parameters
			d_1 = {
				#get data
				'files':[ 'work/mc.root'],
				'corrections': ['L1L2L3'],

				#binning
				'x_expressions': ["{}{}/gen{}{}".format(objct, parameter, objct, parameter),],
				'x_bins': '50,0.5,1.5',

				#formatting
				'x_lims': [0.5, 1.5],
				'filename': '{}{}overgen{}{}'.format(objct, parameter, objct, parameter),
				'title':'{}{}/gen{}{}'.format(objct, parameter, objct, parameter),
			}
			plots.append(d_1)

	for d in plots:
		d.update({
			# web gallery options
			'www_title': 'Reco-gen-comparisons',
			'www_text': 'Comparison of reco- and gen-level pT,eta,y,phi of muons, jets and Z bosons.',
		})

	harryinterface.harry_interface(plots, args)

jmzexpress = {
	#relative reco gen for pT
		'jetpt':'jet1pt/genjet1pt',
		'mupt':'muminuspt/genmuminuspt',
		'zpt':'zpt/genzpt',
	#Delta reco gen for eta
		'jeteta':'(abs(jet1eta-genjet1eta))',
		'mueta':'(abs(muminuseta-genmuminuseta))',
		'zeta':'(abs(zeta-genzeta))',
	#Delta reco gen for phi, different formulas because of -pi < phi < pi
		'jetphi':'(abs(abs(abs(jet1phi-genjet1phi)-TMath::Pi())-TMath::Pi()))',
		'muphi':'(abs(abs(abs(muminusphi-genmuminusphi)-TMath::Pi())-TMath::Pi()))',
		'zphi':'(abs(abs(abs(zphi-genzphi)-TMath::Pi())-TMath::Pi()))',
}
jmzlabel = {
	#relative reco gen for pT
		'pt':'{}$_{{reco}}/${}$_{{gen}}$'.format(latex['pt'],latex['pt'],),
		'eta':r'|$ \\eta_{{reco}} - \\eta_{{gen}}$|',
		'phi':r'|$ \\phi_{{reco}} - \\phi_{{gen}}$|',
}
jmzbin = {
	'pt':'50,0.8,1.2',
	'eta':'50,0,0.06',
	'phi':'50,0,0.06',
}

##############################
def jet_muon_z_comparison(args=None, additional_dictionary=None):
	"""9 plots: 1D-plots of Z/genZ, muminus/genmuminus and jet1/genjet1 together in one diagram for pt, phi, eta each, with weights for pt>50, 50<pt<100, pt>100 
	"""

	plots = []
	parameterlist_jet1 = ['pt', 'phi', 'eta']

	weightinglist_pt = ["0_pt_noweight", "1_pt_lower50", "2_pt_50to100", "3_pt_higher100"]
	
	for parameter in parameterlist_jet1:
		for selection in weightinglist_pt:

			#1D-plots 
			d_1 = {
				#get data
				'files':[ 'work/mc.root'],
				'corrections': ['L1L2L3'],

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
def jet_muon_z_comparison_tree(args=None, additional_dictionary=None):
	"""Comparison of jet, muon, z reconstruction quality depending on pT: Tree-plots of Z/genZ, muminus/genmuminus and jet1/genjet1 together in one diagram for pt, phi, eta each 
	"""
	
	plots = []
	parameterlist_jet1 = ['pt', 'phi', 'eta']

	bins = {
		"pt" : ['10 30 40 50 60 70 80 90 100 150 200 300 500 700'],
		"phi" : ['10 30 40 50 60 70 80 90 100 150 200 250 300 400 500 600'],
		"eta" : ['10 30 40 50 60 70 80 90 100 150 200 250 300 400 500 600'],
	}

	for parameter in parameterlist_jet1:

		#Tree-plots 
		d_1 = {
			#get data
			'files':[ 'work/mc.root'],
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
			'files':[ 'work/mc.root'],
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

jmeexpress = {
	#relative reco gen for pT
		'jetpt':'jet1pt/genjet1pt',
		'mupt':'muminuspt/genmuminuspt',
		'ept':'eminuspt/geneminuspt',
	#Delta reco gen for eta
		'jeteta':'(abs(jet1eta-genjet1eta))',
		'mueta':'(abs(muminuseta-genmuminuseta))',
		'eeta':'(abs(eminuseta-geneminuseta))',
	#Delta reco gen for phi, different formulas because of -pi < phi < pi (abs(abs(abs(jet1phi-jet2phi)-TMath::Pi())-TMath::Pi()))
		'jetphi':'(abs(abs(abs(jet1phi-genjet1phi)-TMath::Pi())-TMath::Pi()))',
		'muphi':'(abs(abs(abs(muminusphi-genmuminusphi)-TMath::Pi())-TMath::Pi()))',
		'ephi':'(abs(abs(abs(eminusphi-geneminusphi)-TMath::Pi())-TMath::Pi()))',
}
jmelabel = {
	#relative reco gen for pT
		'pt':'{}$_{{reco}}/${}$_{{gen}}$'.format(latex['pt'],latex['pt'],),
		'eta':r'|$ \\eta_{{reco}} - \\eta_{{gen}}$|',
		'phi':r'|$ \\phi_{{reco}} - \\phi_{{gen}}$|',
}
jmebin = {
	'pt':'50,0.8,1.2',
	'eta':'50,0,0.06',
	'phi':'50,0,0.06',
}

###########################
def jet_muon_ee_comparison(args=None, additional_dictionary=None):
	""" Quality of reconstruction of pt, eta, phi for (jet1, muminus, eminus) in one plot. 
	1D-plots of eminus/geneminus, muminus/genmuminus and jet1/genjet1 together in one diagram for pt, phi, eta each, with weights for pt>50, 50<pt<100, pt>100.
	"""
	
	#Plotting
	plots = []
	parameterlist = ['pt', 'phi', 'eta']
	weightinglist_pt = ["0_pt_noweight", "1_pt_lower50", "2_pt_50to100", "3_pt_higher100"]
	
	for parameter in parameterlist:
		for selection in weightinglist_pt:

			#1D-plots 
			d_1 = {
				#get data
				'files':['work/mc.root','work/mc.root', 'work/mc_ee.root'],
				'corrections': ['L1L2L3'],
				#'zjetfolders':['zcuts'],

				#binning
				'x_expressions': [jmeexpress["jet{}".format(parameter)],jmeexpress["mu{}".format(parameter)],jmeexpress["e{}".format(parameter)]],
				'x_label': jmelabel['{}'.format(parameter)],
				'x_bins': jmebin['{}'.format(parameter)],

				#weights and normalization
				'weights': weighting_e[selection],
				'analysis_modules': ['NormalizeToFirstHisto','NormalizeToFirstHisto',],

				
				#nicknames, text
				'nicks': ["jet1","mu","eminus"],
				'labels': [latex["jet1"],latex["muminus"],latex["eminus"]],
				'colors': [color['jet'],color['mu'], color['e']],
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
			'www_title': 'Reco-gen-comparisons: jet muon eminus',
			'www_text': 'Comparison of reco- and gen-level pT,eta,phi of muons, jets and electrons for different weightings of pt.',
		})
	harryinterface.harry_interface(plots, args)


############################################
def jet_muon_ee_comparison_tree(args=None, additional_dictionary=None):
	"""Comparison of jet, muon, e reconstruction depending on pt: Tree-plots of eminus/geneminus, muminus/genmuminus and jet1/genjet1 together in one diagram for pt, phi, eta each. Additionally, plots of  statistical errors of said Tree-plots depending on pt.
	"""
	
	plots = []
	parameterlist_jet1 = ['pt', 'phi', 'eta']

	bins = {
		"pt" : ['10 20 30 40 50 60 70 80 90 100 150 200 300 500 700'],
		#"pt" : ['0 50 100 150 200 300 700'],
		"phi" : ['10 20 30 40 50 60 70 80 90 100 150 200 250 300 400 500 700'],
		"eta" : ['10 20 30 40 50 60 70 80 90 100 150 200 250 300 400 500 700'],
	}

	for parameter in parameterlist_jet1:

		#Tree-plots 
		d_1 = {
			#get data
			'files':['work/mc.root','work/mc.root', 'work/mc_ee.root'],
			'corrections': ['L1L2L3'],
			#'zjetfolders':['zcuts'],

			#binning
			'x_expressions':["genjet1pt","genmuminuspt","geneminuspt"],
			'y_expressions':[jmeexpress["jet{}".format(parameter)],jmeexpress["mu{}".format(parameter)],jmeexpress["e{}".format(parameter)]],
			'tree_draw_options': 'profs',
			'x_bins': bins[parameter],
			'x_log': True,

			#formatting
			'nicks': ["jet1","mu","eminus"],
			'labels': [latex["jet1"],latex["muminus"],latex["eminus"]],
			'colors': [color['jet'],color['mu'], color['e']],
			'texts': '{} - $error$ $bars$ $show$ $standard$ $deviation$'.format(latex[parameter]),
			'x_label': "{}$/GeV$".format(latex["pt"]),
			'y_label': jmelabel['{}'.format(parameter)],
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
			'files':['work/mc.root','work/mc.root', 'work/mc_ee.root'],
			'corrections': ['L1L2L3'],
			#'zjetfolders':['zcuts'],

			#binning
			'x_expressions':["genjet1pt","genmuminuspt","geneminuspt"],
			'y_expressions':[jmeexpress["jet{}".format(parameter)],jmeexpress["mu{}".format(parameter)],jmeexpress["e{}".format(parameter)]],
			'tree_draw_options':  'profs',
			'x_bins': bins[parameter],
			'x_log': True,
			'analysis_modules': ['ConvertToHistogram', 'StatisticalErrors',],
			'stat_error_nicks': ["jet1","mu","e"],
			'convert_nicks': ["jet1","mu","e"],
			
			#formatting
			'nicks': ["jet1","mu","e"],
			'labels': [latex["jet1"],latex["muminus"],latex["eminus"]],
			'colors': [color['jet'],color['mu'], color['e']],
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




###########################
def pt_distribution(args=None, additional_dictionary=None):
	"""
	pT Distribution, 1D histogram: number of events for jet1pt, eminuspt, muminuspt
	"""

	plots = []

	d_1 = {
		#get data
		'files':[ 'work/mc.root', 'work/mc_ee.root', 'work/mc.root'],
		'corrections': ['L1L2L3'],

		#binning
		'x_expressions': ["jet1pt","eminuspt", 'muminuspt'],
		'x_bins': '100,0,700',
		'x_label':'$p_{{T}}$ / GeV',

		#formatting
		'nicks': ["jet1","e", 'mu'],
		'labels': [r"$Jet1$","$e^{-}$", r"$\\mu^{-}$"],
		'colors': [color['jet'],color['e'], color['mu']],
		'filename': 'pT_distribution',
		'analysis_modules': ['NormalizeToFirstHisto',],
		'markers': ['.', '.', '.'],
		'marker_fill_styles': ['full', 'full', 'full'],
		'line_styles': ['-'],
		'step':['True','True','True'],
		'title':'Number of events\n depending on pT',
	}
	plots.append(d_1)

	for d in plots:
		d.update({
			# web gallery options
			#'www_title': 'Comparison of Zmass',
			#'www_text': 'Comparison of Zmass calculated from ee and mm',
		})

	harryinterface.harry_interface(plots, args)
	
def zmass_ee_mm(args=None, additional_dictionary=None):
	"""1D histograms for Zmass calculated from ee and mm
	"""

	plots = []

	d_1 = {
		#get data
		'files':[ 'work/mc.root', 'work/mc_ee.root', 'work/mc.root'],
		'corrections': ['L1L2L3'],

		#binning
		'x_expressions': ["zmass","zmass", 'genzmass'],
		'x_bins': '20,81,102',
		'x_label':'$m_{{Z}}$ / GeV',

		#formatting
		'nicks': ["zmu","ze", 'genz'],
		'labels': [r"$Z_{{\\mu}}$","$Z_{e}$", "$Z_{gen}$"],
		'colors': [color['mu'],color['e'], color['undef']],
		'filename': 'zmass_ee_mm_comparison_2',
		'analysis_modules': ['NormalizeToFirstHisto',],
		'markers': ['_', '4', '3'],
		'marker_fill_styles': ['none', 'none', 'none'],
		'line_styles': ['-'],
		'step':['True','True','True'],
		'title':'Comparison of Zmass \n calculated from ee and mm',
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
