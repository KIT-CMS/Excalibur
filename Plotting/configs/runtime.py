#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from Artus.HarryPlotter.utility.tfilecontextmanager import TFileContextManager
import Excalibur.Plotting.harryinterface as harryinterface


def runtime(args=None, additional_dictionary=None):
	"""Make performance plots (processor runtime).

	To create the 'runTime'-ntuple in the excalibur output, add 'RunTimeConsumer'
	to the list of consumers in the config.
	"""

	only_producers = True  # dont plot filters

	plots = []
	for label, corr in zip(
		['Data', 'MC'],
		['Res', ''],
	):
		filename = '{}_runtime.root'.format(label.lower())
		folder = 'finalcuts_AK5PFJetsCHSL1L2L3{}/runTime'.format(corr)
		processors = []
		# get list of processors
		with TFileContextManager(filename, "READ") as rootfile:
			ntuple = rootfile.Get(folder)
			try:
				for leaf in ntuple.GetListOfLeaves():
					if ('Producer' in leaf.GetName()) or not only_producers:
						processors.append(leaf.GetName())
			except AttributeError:
				print "Could not find {}! Did you let the RunTimeConsumer run?".format(folder)
				exit(1)
		d = {
			# input
			'files': [filename],
			'folders': [folder],
			'x_expressions': processors,
			'nicks': processors,
			'x_bins': ['100,0,500'],
			'no_weight': True,
			# analysis
			'analysis_modules': ['NormalizeToUnity', 'HistogramFromMeanValues'],
			# formatting
			'nicks_whitelist': ['mean'],
			'markers': ['fill'],
			'legend': None,
			'x_label': ' ',
			'y_label': 'runtime',
			'energies': None,
			'title': label,
			'no_energy_label': True,
			# output
			'filename':  label.lower() + '_runtime',
		}
		plots.append(d)
	harryinterface.harry_interface(plots, args)

if __name__ == '__main__':
	runtime()
