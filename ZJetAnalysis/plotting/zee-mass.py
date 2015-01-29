#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Artus.HarryPlotter.harry as harry
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
		'scale_factors': [
			1,
			1,

			-1,
			-1,
			-1,
			-1,
			-1,
			-1,
			-1,
		],
		'weights': [selection] + ['(%s * 19.789 * weight)' % selection]*8,
		'nicks': [
			'data',
			'mc',

			'data',
			'data',
			'data',
			'data',
			'data',
			'data',
			'data',

		],
		'folders': ['zcuts_AK5PFJetsCHSL1L2L3'],
		'analysis_modules': [
			'NormalizeToFirstHisto'
		],
		
		'nicks_blacklist': ['responsematrix',
		 'gen', 'unfolded'],

		'formats': ['pdf'],
		'lumi': 19.8,
		'energy': '8',
		#'live': 'evince',
		#'userpc': True,
		'x_lims': [81, 101],
		'x_bins': "40,81,101",
		'x_bins': "40,81,101",
		'y_ratio_lims': [0.5, 1.5],
		'legloc': 'center left',
		'filename': quantity,
		'x_label': 'zpt',
		'ratio': True,
		'no_logo': True,
		'log_level': 'debug',

	}

	harry_instance = harryZJet.HarryPlotterZJet(list_of_config_dicts=[d])

