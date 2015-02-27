#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Artus.HarryPlotter.harry as harry
import Excalibur.Plotting.plotscript as plotscript

import numpy as np


def zee_unfolded(args=None):
	"""Unfolded Z(->ee) distributions. All combinations of n jet categories, rapidity bins, MC samples and quantities (y, mass, pT) are plotted."""

	# some variables
	path = '/portal/ekpcms5/home/dhaitz/git/excalibur'
	data = '/work/data_ee_corr.root'
	ybins = np.arange(0, 2.8, 0.4)
	zcuts = "zmass>81 && zmass<101 && eminuspt>25 && epluspt>25 && abs(epluseta)<2.4 && abs(eminuseta)<2.4"

	plots = []
	for njetweight, njetlabel, njetsuffix in zip(
		["1", "njets30<2", "njets30>1"],
		["", "$ n_{jets(p_T>30GeV)}<=1$", "$ n_{jets(p_T>30GeV)}>1$"],
		["", "_njets0-1", "_njets2"]
	):
		for ybin, ybinlabel, ybinsuffix in zip(
					["1"] + ["abs(zy)<{1} && abs(zy)>{0}".format(low, up) for low, up in zip(ybins[:-1], ybins[1:])],
					["", "|y|<0.4"] + ["{0}<|y|<{1}".format(low, up) for low, up in zip(ybins[:-1], ybins[1:])][1:],
					["_inclusive"] + ["_{0:02d}y{1:02d}".format(int(10*low), int(10*up)) for low, up in zip(ybins[:-1], ybins[1:])]
		):
			for mc_label, mc in zip( ['Madgraph', 'Powheg'], ['/store/mc_ee_corr.root', '/store/mc_ee_powheg_corr.root']):
				for quantity, bins in zip(
					['zpt', 'zmass', 'zy'],
					[[15, 30, 40, 60, 80, 100, 140, 200, 1000], "10,81,101","10,-3,3"]
				):
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
						'folders': ['all_AK5PFJetsCHSL1L2L3'],
						'weights': "(({}) && ({}) && ({}))".format(zcuts, ybin, njetweight),
						'analysis_modules': [
							'Unfolding',
						],
						#module options
	
						'unfolding': ['data', 'mc'],
						'unfolding_responsematrix': 'responsematrix',
						'unfolding_mc_gen': 'gen',
						'unfolding_mc_reco': 'mc',
						'unfolding_new_nicks': ['Data', 'MC'],
						'libRooUnfold': '~/home/RooUnfold-1.1.1/libRooUnfold.so',
				
		
						'nicks_blacklist': ['responsematrix',
						 'gen', 'mc', 'data'],

						'lumi': 19.8,
						'energy': '8',
						'y_ratio_lims': [0.5, 1.5],

						'texts': [ybinlabel, njetlabel],
						'texts_x':[0.03],
						'texts_y': [0.97, 0.87],
		
						'x_bins': bins,
						'y_bins': bins,
						'x_label': quantity,
						'y_label': 'Events',

						'ratio': True,
						'filename': quantity + "_unfolded_" + mc_label + ybinsuffix + njetsuffix,

					}
					if quantity == 'zpt':
						d['x_log'] = True
						d['y_log'] = True
						d['x_lims'] = [30, 1000]
						d['x_ticks'] = [30, 50, 70, 100, 200, 400, 1000]

					plots.append(d)
	plotscript.plotscript(plots, args)


if __name__ == '__main__':
	zee_unfolded()
