#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Artus.HarryPlotter.harry as harry

if __name__ == '__main__':

	# some variables
	quantity = 'zpt'
	selection = 'abs(zy)<0.4'
	path = '/portal/ekpcms5/home/dhaitz/git/excalibur'

	d = {
		'x_expressions': 
			[quantity]*3 +
			[quantity, 'gen'+quantity]

			+ [quantity]*7
			+ [quantity]*8
			+ [quantity]*2,

		'y_expressions': [
			None, None,
			None, 'gen'+quantity, None,]
			+ [None]*7
			+ [None]*8
			+ [None]*2,
		'files': [
			path + '/work/data.root',
			path + '/work/data.root',

			path + '/work/mc.root',
			path + '/work/mc.root',
			path + '/work/mc.root',

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
			path + '/work/data.root',

			path + '/work/data.root',
			path + '/work/data.root',
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
			'staterrors',
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

			'background',
			'background',
			'background',
			'background',
			'background',
			'background',
			'background',
			'background',
			
			'lumi_num',
			'lumi_denum',
		],
		'labels':[
			#'staterrors',
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
		'markers': ['o', '*', '.-', 'd'
			],
		'analysis_modules': [
			'StatisticalErrors',
			'Unfolding',
			'Divide',
			'ShiftBinContents',
			'AbsoluteBinContents',
			'ScaleBinContents',
		],
		#module options
		'stat_error': ['staterrors'],
		
		'unfolding': 'data',
		'unfolding_responsematrix': 'responsematrix',
		'unfolding_mc_gen': 'gen',
		'unfolding_mc_reco': 'mc',
		'unfolding_new_nicks': ['unfolded','unfoldedup'],
		'unfolding_variation': [0, 1],
		'libRooUnfold': '~/home/RooUnfold-1.1.1/libRooUnfold.so',
		
		'relative_error': True,
		
		'divide_numerator_nicks': ['lumi_num', 'data', 'unfolded'],
		'divide_denominator_nicks': ['lumi_denum', 'background', 'unfoldedup'],
		'divide_result_nicks' : ['lumi', 'bkgrunc', 'uunc'],
		
		'shift_bin_contents': ['bkgrunc', 'uunc'],
		'shift': -1,
		
		'scale_bin_contents': ['bkgrunc', 'uunc'],
		'scale': 100,

		'absolute_bin_contents': ['bkgrunc', 'uunc'],


		
		'nicks_blacklist': ['responsematrix', 'background',
		 'gen', 'data', 'mc', 'lumi_', 'unf'],

		'formats': ['png'],
		'lumi': 19.8,
		'energy': '8',
		#'live': 'evince',
		'userpc': True,
		'x_bins': '5,30,230',
		'y_bins': '5,30,230',
		'x_label': 'zpt',
		'y_label': 'error',
		'legloc': 'center left',
		'www': "test",
		'log_level': 'debug',
		#'y_lims': [0, 10],

	}

	harry_instance = harry.HarryPlotter(list_of_config_dicts=[d])

