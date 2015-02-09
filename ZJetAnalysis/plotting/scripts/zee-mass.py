#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ZJet.Plotting.harryZJet as harryZJet

if __name__ == '__main__':
	# some variables
	quantity = 'zmass'
	selection = '1'
	path = '/portal/ekpcms5/home/dhaitz/git/excalibur'
	data = '/work/data_ee_corr.root'
	mc = '/store/mc_ee_powheg_corr.root'
	#mc = '/work/mc_ee_corr.root'

	d = {
		'x_expressions': quantity,
		'files': [
			path + data,

			path + mc,

			path + '/store/background_ee_zz.root',
			path + '/store/background_ee_wz.root',
			path + '/store/background_ee_tt.root',
			path + '/store/background_ee_tw.root',
			path + '/store/background_ee_ww.root',
			path + '/store/background_ee_wjets.root',
			path + '/store/background_ee_dytautau.root',
		],
		'weights': selection,
		'nicks': [
			'data',
			'mc',
			'ZZ', 'WZ', 'tt', 'tW', 'WW', 'Wjets', 'DYtautau'
		],

		'folders': ['zcuts_AK5PFJetsCHSL1L2L3'],
		'analysis_modules': [
		#	'NormalizeToFirstHisto'
		],
		
		#'y_lims': [1, 400],
		'x_lims': [81, 101],
		'x_bins': "40,81,101",
		'x_label': 'zmass',
		'y_log': True,

		#'ratio': True,
		'y_ratio_lims': [0.5, 1.5],
		#'legloc': None,

		'formats': ['pdf'],
		#'userpc': True,
		'filename': quantity,
		#'log_level': 'debug',
		'stack': ['data']+['x']*8,

	}
	harry_instance = harryZJet.HarryPlotterZJet(list_of_config_dicts=[d])

