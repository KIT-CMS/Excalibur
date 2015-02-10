#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Artus.HarryPlotter.harry as harry
import plotscript

if __name__ == '__main__':
	""" test unfolding from one mc with another."""

	# some variables
	path = '/portal/ekpcms5/home/dhaitz/git/excalibur'
	data = '/work/data_ee_corr.root'

	plots = []
	for mc_label, mc, data in zip( ['Madgraph', 'Powheg'],
				['/work/mc_ee_corr.root', '/store/mc_ee_powheg_corr.root'],
				['/store/mc_ee_powheg_corr.root', '/work/mc_ee_corr.root']):
		for quantity, bins in zip(['zpt', 'zmass', 'zy'], ["10,30,430", "10,81,101","10,-3,3"]):
			d = {
				'x_expressions': [
					quantity,
					quantity,
					"gen"+quantity,
					"gen"+quantity,
					],
				'y_expressions': [
					None,
					None,
					quantity,
					None,
					],
				'files': [
					path + data,

					path + mc,
					path + mc,
					path + mc,

				],
				'scale_factors': [
					1,

					1,
					1,
					1,

				],
				'nicks': [
					'data',

					'mc',
					'responsematrix',
					'gen',

				],
				'folders': ['zcuts_AK5PFJetsCHSL1L2L3'],
				'analysis_modules': [
					'Unfolding',
				],
				#module options
	
				'unfolding': 'data',
				'unfolding_responsematrix': 'responsematrix',
				'unfolding_mc_gen': 'gen',
				'unfolding_mc_reco': 'mc',
				'unfolding_new_nicks': 'Data',
				'libRooUnfold': '~/home/RooUnfold-1.1.1/libRooUnfold.so',
				
		
				'nicks_blacklist': ['responsematrix',
				 'mc', 'data'],

				'lumi': 19.8,
				'energy': '8',
				'y_ratio_lims': [0.5, 1.5],
		
				'x_bins': bins,
				'y_bins': bins,
				'x_label': quantity,
				'y_label': 'Events',

				'ratio': True,
				'filename': quantity + "_" + mc_label,

			}
			if quantity == 'zpt':
				d['x_log'] = True
				d['y_log'] = True
				d['x_ticks'] = [30, 50, 70, 100, 230]

			plots.append(d)
	plotscript.plotscript(plots)
