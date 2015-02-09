#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Artus.HarryPlotter.harry as harry

if __name__ == '__main__':

	# some variables
	quantity = 'zpt'
	quantity = 'zmass'
	selection = '1'#'(abs(zy) < 0.4)'
	path = '/portal/ekpcms5/home/dhaitz/git/excalibur'
	data = '/work/data_ee_corr.root'
	mc = '/store/mc_ee_powheg_corr.root'
	#mc = '/work/mc_ee_corr.root'
	

	d = {
		'x_expressions': [
			quantity,
			
			quantity,
			"gen"+quantity,
			quantity,
			] +
			[quantity]*7,
		'y_expressions': [
			None, 
			
			None,
			quantity,
			None,
			] +
			[None]*7,

		'files': [
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
		],
		'scale_factors': [
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
		],
		'weights': [
			selection,
			]+[
			'(%s * 19.789 * weight)' % selection]*10
		,
		'nicks': [
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
		#'colors': [
		#	'black',
		#	'lightskyblue',
		#	'red',
		#	'green',
		#	#'orange',
		#],
		#'markers': ['o', '*', '.-', 'd'
		#	],
		'analysis_modules': [
			'Unfolding',
			'NormalizeToFirstHisto'
		],
		#module options
	
		'unfolding': 'data',
		'unfolding_responsematrix': 'responsematrix',
		'unfolding_mc_gen': 'gen',
		'unfolding_mc_reco': 'mc',
		'unfolding_new_nicks': ['unfolded','unfoldedup'],
		'unfolding_variation': [0, 1],
		'libRooUnfold': '~/home/RooUnfold-1.1.1/libRooUnfold.so',
				
		
		'nicks_blacklist': ['responsematrix',
		 'gen', 'unfolded'],

		'formats': ['png'],
		'lumi': 19.8,
		'energy': '8',
		#'live': 'evince',
		'userpc': True,
		'x_bins': "40,81,101",
		'x_bins': "40,81,101",
		#'x_bins': '10,30,230',
		#'y_bins': '10,30,230',
		#'x_ticks':[30, 50, 70, 100, 230],
		#'x_lims': [30, 230],
		'y_ratio_lims': [0.5, 1.5],
		'legloc': 'center left',
		'filename': quantity,#'zpt_unfolded_powheg',
		#'log_level': 'debug',
		'x_label': 'zpt',
		'y_log': True,
		#'x_log': True,
		'ratio': True,

	}

	harry_instance = harry.HarryPlotter(list_of_config_dicts=[d])

