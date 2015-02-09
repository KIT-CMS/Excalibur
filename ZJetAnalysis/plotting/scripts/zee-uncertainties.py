#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Artus.HarryPlotter.harry as harry
import harryZJet as harryZJet

if __name__ == '__main__':

	# some variables
	quantity = 'zpt'
	selection = "1"#'(abs(zy)<0.4)'
	path = '/portal/ekpcms5/home/dhaitz/git/excalibur'
	data = '/work/data_ee_corr.root'
	mc = '/store/mc_ee_powheg_corr.root'

	d = {
		'x_expressions': 
			[quantity]*3 +
			["gen"+quantity, 'gen'+quantity]

			+ [quantity]*7
			+ [quantity]*8
			+ [quantity]*2,

		'y_expressions': [
			None, None,
			None, #'gen'+
			quantity, None,]
			+ [None]*7
			+ [None]*8
			+ [None]*2,
		'files': [
			path + data,
			path + data,

			path + mc,
			path + mc,
			path + mc,

			path + '/store/background_ee_zz.root',
			path + '/store/background_ee_wz.root',
			path + '/store/background_ee_tt.root',
			path + '/store/background_ee_tw.root',
			path + '/store/background_ee_ww.root',
			path + '/store/background_ee_wjets.root',
			path + '/store/background_ee_dytautau.root',

			path + '/store/background_ee_zz.root',
			path + '/store/background_ee_wz.root',
			path + '/store/background_ee_tt.root',
			path + '/store/background_ee_tw.root',
			path + '/store/background_ee_ww.root',
			path + '/store/background_ee_wjets.root',
			path + '/store/background_ee_dytautau.root',
			path + data,

			path + data,
			path + data,
		],
		'scale_factors': [
			1,
			1,

			1,
			1,
			1,

			-1,
			-1,
			-1,
			-1,
			-1,
			-1,
			-1,


		]
		+[-1.5]*7
		+[1]
		
		+[2.6, 1]
		,
		'weights': [
			selection,
			selection,

			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',

			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',

			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',
			selection + ' * 19.789 * weight',
			selection,
			
			selection,
			selection,
		],
		'nicks': [
			'statistical',
			'data',

			'mc',
			'responsematrix',
			'gen',

			'data',
			'data',
			'data',
			'data',
			'data',
			'data',
			'data',

			'backgroundunc',
			'backgroundunc',
			'backgroundunc',
			'backgroundunc',
			'backgroundunc',
			'backgroundunc',
			'backgroundunc',
			'backgroundunc',
			
			'lumi_num',
			'lumi_denum',
		],
		'labels':[
			#'statistical',
			#'data',
			#'mc',
			#'background',
			#'unfolding',
			#'lumi'
		],
		'folders': ['zcuts_AK5PFJetsCHSL1L2L3'],
		'colors': [
			'black',
			'lightskyblue',
			'red',
			'green',
			#'orange',
		],
		'markers': ['o', '*', '.', 'd'
			],
		'linestyles': ['-', '-', '-', '-'],
		'analysis_modules': [
			'StatisticalErrors',
			'Unfolding',
			'Divide',
			'ShiftBinContents',
			'AbsoluteBinContents',
			'ScaleBinContents',
		],
		#module options
		'stat_error': ['statistical'],
		
		'unfolding': 'data',
		'unfolding_responsematrix': 'responsematrix',
		'unfolding_mc_gen': 'gen',
		'unfolding_mc_reco': 'mc',
		'unfolding_new_nicks': ['unfolded','unfoldedup'],
		'unfolding_variation': [0, 1],
		'libRooUnfold': '~/home/RooUnfold-1.1.1/libRooUnfold.so',
		
		'relative_error': True,
		
		'divide_numerator_nicks': ['lumi_num', 'data', 'unfolded'],
		'divide_denominator_nicks': ['lumi_denum', 'backgroundunc', 'unfoldedup'],
		'divide_result_nicks' : ['lumi', 'background', 'unfolding'],
		
		'shift_bin_contents': ['background', 'unfolding'],
		'shift': -1,
		
		'scale_bin_contents': ['background', 'unfolding'],
		'scale': 100,

		'absolute_bin_contents': ['background', 'unfolding'],


		'nicks_blacklist': ['responsematrix', 'backgroundunc',
		 'gen', 'data', 'mc', 'lumi_', 'unfolded'],
		 
		 
		#'nicks_whitelist': ['unfolding'],

		'formats': ['png'],
		'lumi': 19.8,
		'energy': '8',
		#'live': 'evince',
		#'userpc': True,
		'x_bins': '5,30,230',
		'y_bins': '5,30,230',
		'x_label': 'zpt',
		'y_label': 'relative error [%]',
		'legloc': 'upper left',
		'log_level': 'debug',
		#'y_lims': [0, 10],

		#'axes': [0, 1, 2, 3],
		'n_axes_x': 1,
		'n_axes_y': 1,
		'x_lims': [0, 250],
		'y_lims': [0, 5],

	}

	harry_instance = harryZJet.HarryPlotterZJet(list_of_config_dicts=[d])

