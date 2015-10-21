#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface
from Excalibur.Plotting.utility.colors import histo_colors



#########################
def reco_gen_comparison(args=None, additional_dictionary=None):
	"""Plots 2D plots of reco and gen for Z, jet1, muminus, as well as 1D-plots of Z/genZ and jet1/genjet1 for various parameters
	"""
	#binning overall number, start, stop
	startstop = {

		'pt' : ['30', '0', '250'],
		'phi' : ['30', '-2', '2'],
		'eta' : ['30', '-3.14', '3.14'],
		'y' : ['30', '-2.5', '2.5'],
		'mass': ['30', '85', '100'],
	}

	plots = []
	parameterlist_z =['pt', 'phi', 'y', 'mass']
	parameterlist_jet1 =['pt', 'phi', 'eta']

	#2D-plots of Z vs genZ and jet1 vs genjet1 for various parameters
	for objct, parameterlist in zip(['z', 'jet1', 'muminus',], [parameterlist_z, parameterlist_jet1, parameterlist_jet1]):

		#Plots
		for parameter  in parameterlist:

			#2D-plots of Z vs genZ and jet1 vs genjet1 for various parameters
			d_2 = {
				#get data
				'files':[ 'work/mc.root'],
				'corrections': ['L1L2L3'],

				#binning
				'x_expressions': ["gen{}{}".format(objct, parameter),],
				'y_expressions': ["{}{}".format(objct, parameter),],
				'x_bins': ','.join(startstop[parameter]),
				'y_bins': ','.join(startstop[parameter]),

				#formatting
				'y_lims': [float(startstop[parameter][1]), float(startstop[parameter][2])],
				'x_lims': [float(startstop[parameter][1]), float(startstop[parameter][2])],
				'filename': '{}{}_VS_gen{}{}'.format(objct, parameter, objct, parameter),
				'title':'{}{} vs gen{}{}'.format(objct, parameter, objct, parameter),
			}
			plots.append(d_2)

			#1D-plots of Z/genZ and jet1/genjet1 for various parameters
			d_1 = {
				#get data
				'files':[ 'work/mc.root'],
				'corrections': ['L1L2L3'],

				#binning
				'x_expressions': ["{}{}/gen{}{}".format(objct, parameter, objct, parameter),],
				'x_bins': '50,0.5,1.5',

				#formatting
				'x_lims': [0.5, 1.5],
				'filename': '{}{}overgen{}{}'.format(objct, parameter, objct, parameter),
				'title':'{}{}/gen{}{}'.format(objct, parameter, objct, parameter),
			}
			plots.append(d_1)

	for d in plots:
		d.update({
			# web gallery options
			'www_title': 'Reco-gen-comparisons',
			'www_text': 'Comparison of reco- and gen-level pT,eta,y,phi of muons, jets and Z bosons.',
		})
	harryinterface.harry_interface(plots, args)





if __name__ == '__main__':
	muoniso_aod()
