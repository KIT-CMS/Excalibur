#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Artus.HarryPlotter.harry as harry
import plotscript

if __name__ == '__main__':
	""" data, signal and backgounds, over different x quantities"

	path = '/portal/ekpcms5/home/dhaitz/git/excalibur'
	plots = []
	
	for mc, mc_label in zip(['/work/mc_ee_corr.root', '/store/mc_ee_powheg_corr.root'],
		['Madgraph', 'Powheg']):
		for log, suffix in zip([False, True
						], ['', '_log']):
			for quantity, bins in zip(['zpt', 'zy', 'zmass'],
				[[20, 40, 60, 80, 100, 120, 140, 170, 200, 1000],
				"18,-3, 3",
				"20,81,101"]):
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
					'legend': None,
					"labels": [
						"data", 
						r"DY->ee ", 
						"ZZ", 
						"WZ", 
						"tt", 
						"tW", 
						"WW", 
						"W+jets", 
						"DY->tautau"
					],
					'title': mc_label,
					"markers": [
						"o", 
						"fill", 
						"fill", 
						"fill", 
						"fill", 
						"fill", 
						"fill", 
						"fill", 
						"fill"
					],
					'export_json': None,
					'stack': [
						'data',
						'mc']
						+ ['data']*7,
					'folders': ['zcuts_AK5PFJetsCHSL1L2L3'],

					'lumi': 19.8,
					'energy': '8',

					'x_bins': bins,
					'y_log': log,

					'ratio': True,
					'y_ratio_lims': [0.5, 1.5],

					'save_legend': "legend" + "_" + mc_label,

					'filename': quantity + suffix + "_" + mc_label,
				}
				if quantity == 'zpt':
					d['x_log'] = True
					d['x_lims'] = [20, 600]
				plots.append(d)
	plotscript.plotscript(plots)
