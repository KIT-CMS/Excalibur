#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Artus.HarryPlotter.harry as harry
import Excalibur.Plotting.harryinterface as harryinterface

import numpy as np
import argparse


def zee_unfolded(args=None):
	"""Unfolded Z(->ee) distributions. All combinations of n jet categories, rapidity bins, MC samples and quantities (y, mass, pT) are plotted."""

	parser = argparse.ArgumentParser()
	# if these arguments are set true the function will not iterate over the respective quantities
	#    by default, argument ist False -> whole list is taken and iterated over
	#    if set without arguments: first item of list is taken, no iteration
	#    if set with arguments N: N-th item of list is taken, no iteration
	parser.add_argument('--no-njets', type=int, nargs='?', default=False, const=0)
	parser.add_argument('--no-ybins', type=int, nargs='?', default=False, const=0)
	parser.add_argument('--no-quantities', type=int, nargs='?', default=False, const=0)
	parser.add_argument('--no-mcs', type=int, nargs='?', default=False, const=0)
	if args is None:
		known_args, args = parser.parse_known_args()
	else:
		known_args, args = parser.parse_known_args(args)

	# some variables
	path = '/portal/ekpcms5/home/dhaitz/git/excalibur'
	data = '/work/data_ee_corr.root'
	ybins = np.arange(0, 2.8, 0.4)
	zcuts = "zmass>81 && zmass<101 && eminuspt>25 && epluspt>25 && abs(epluseta)<2.4 && abs(eminuseta)<2.4"

	# TODO if this proves, useful, move to tools or so
	def get_list_slice(lists, arg):
		if arg is False:
			return lists
		else:
			return [[l[arg]] for l in lists]

	plots = []
	for njetweight, njetlabel, njetsuffix in zip(*get_list_slice([
		["1", "njets30<2", "njets30>1"],
		["", "$ n_{jets(p_T>30GeV)}<=1$", "$ n_{jets(p_T>30GeV)}>1$"],
		["", "_njets0-1", "_njets2"]
	], known_args.no_njets)):
		for ybin, ybinlabel, ybinsuffix in zip(*get_list_slice([
					["1"] + ["abs(zy)<{1} && abs(zy)>{0}".format(low, up) for low, up in zip(ybins[:-1], ybins[1:])],
					["", "|y|<0.4"] + ["{0}<|y|<{1}".format(low, up) for low, up in zip(ybins[:-1], ybins[1:])][1:],
					["_inclusive"] + ["_{0:02d}y{1:02d}".format(int(10*low), int(10*up)) for low, up in zip(ybins[:-1], ybins[1:])]
		], known_args.no_ybins)):
			for mc_label, mc in zip(*get_list_slice([
				['Madgraph', 'Powheg'],
				['/store/mc_ee_corr.root', '/store/mc_ee_powheg_corr.root']
			], known_args.no_mcs)):
				for quantity, bins in zip(*get_list_slice([
					['zpt', 'zmass', 'zy'],
					[[15, 30, 40, 60, 80, 100, 140, 200, 1000], "10,81,101", "10,-3,3"]
				], known_args.no_quantities)):
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
							'data_reco',

							'mc_reco',
							'responsematrix',
							'mc_gen',

							'data_reco',
							'data_reco',
							'data_reco',
							'data_reco',
							'data_reco',
							'data_reco',
							'data_reco',
						],
						'folders': ['all_AK5PFJetsCHSL1L2L3'],
						'weights': "(({}) && ({}) && ({}))".format(zcuts, ybin, njetweight),
						'analysis_modules': [
							'Unfolding',
						],
						#module options
						'unfolding': ['data_reco', 'mc_reco'],
						'unfolding_responsematrix': 'responsematrix',
						'unfolding_mc_gen': 'mc_gen',
						'unfolding_mc_reco': 'mc_reco',
						'unfolding_new_nicks': ['data_unfolded', 'mc_unfolded'],
						'libRooUnfold': '~/home/RooUnfold-1.1.1/libRooUnfold.so',
				
		
						'nicks_blacklist': [
							'responsematrix',
							'gen',
							'reco',
						],

						'lumi': 19.8,
						'energy': '8',
						'y_ratio_lims': [0.5, 1.5],

						'texts': [ybinlabel, njetlabel],
						'texts_x':[0.03],
						'texts_y': [0.97, 0.87],
		
						'labels': ['Data', 'MC'],
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
	harryinterface.harry_interface(plots, args)


if __name__ == '__main__':
	zee_unfolded()
