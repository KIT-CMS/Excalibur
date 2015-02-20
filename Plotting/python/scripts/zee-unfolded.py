#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Artus.HarryPlotter.harry as harry
import plotscript

if __name__ == '__main__':

	# some variables
	path = '/portal/ekpcms5/home/dhaitz/git/excalibur'
	data = '/work/data_ee_corr.root'

	plots = []
	for ybin, ybinlabel, ybinsuffix in zip(
				["abs(zy)<0.4", "abs(zy)<2.4 && abs(zy)>2"],
				["|y|<0.4", "2.0<|y|<2.4"],
				["_y04", "_20y24"]
	):
		for mc_label, mc in zip( ['Madgraph', 'Powheg'], ['/store/mc_ee_corr.root', '/store/mc_ee_powheg_corr.root']):
			for quantity, bins in zip(['zpt', 'zmass', 'zy'], ["10,30,430", "10,81,101","10,-3,3"]):
				d = {
					'x_expressions': [
						quantity,
						quantity,
						"gen"+quantity,
						"gen"+quantity,
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
					'folders': ['zcuts_AK5PFJetsCHSL1L2L3'],
					'weights': ybin,
					'analysis_modules': [
						'Unfolding',
					],
					#module options
	
					'unfolding': ['data', 'mc'],
					'unfolding_responsematrix': 'responsematrix',
					'unfolding_mc_gen': 'gen',
					'unfolding_mc_reco': 'mc',
					'unfolding_new_nicks': ['Data', mc_label],
					'libRooUnfold': '~/home/RooUnfold-1.1.1/libRooUnfold.so',
				
		
					'nicks_blacklist': ['responsematrix',
					 'gen', 'mc', 'data'],

					'lumi': 19.8,
					'energy': '8',
					'y_ratio_lims': [0.5, 1.5],
					'text': "{},0.03,0.97".format(ybinlabel),
		
					'x_bins': bins,
					'y_bins': bins,
					'x_label': quantity,
					'y_label': 'Events',

					'ratio': True,
					'filename': quantity + "_" + mc_label + ybinsuffix,

				}
				if quantity == 'zpt':
					d['x_log'] = True
					d['y_log'] = True
					d['x_ticks'] = [30, 50, 70, 100, 230]

				plots.append(d)
	plotscript.plotscript(plots)
