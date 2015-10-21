#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface
from Excalibur.Plotting.utility.colors import histo_colors
from dicts_z_ee import color


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


###########################
def npv_distribution(args=None, additional_dictionary=None):
	"""
	npv Distribution, 1D histogram: number of events for jet1pt, eminuspt, muminuspt
	"""

	plots = []

	d_1 = {
		#get data
		'files':[ 'work/mc.root', 'work/mc_ee.root', 'work/mc.root'],
		'corrections': ['L1L2L3'],

		#binning
		'x_expressions': ["npv","npv", 'npv'],
		'x_bins': ['35,-0.5,34.5'],
		'x_label':'npv',

		#formatting
		'nicks': ["jet1","e", 'mu'],
		'labels': [r"$Jet1$","$e^{-}$", r"$\\mu^{-}$"],
		'colors': [color['jet'],color['e'], color['mu']],
		'filename': 'npv_distribution',
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






if __name__ == '__main__':
	muoniso_aod()
