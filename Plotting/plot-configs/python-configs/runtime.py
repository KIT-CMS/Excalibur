#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
		filename = 'work/{}.root'.format(label.lower())
		folder = 'finalcuts_AK5PFJetsCHSL1L2L3{}/runTime'.format(corr)
		processors = []
		# get list of processors
		with TFileContextManager(filename, "READ") as rootfile:
			ntuple = rootfile.Get(folder)
			for leaf in ntuple.GetListOfLeaves():
				if (only_producers and 'Producer' in leaf.GetName()) or not only_producers:
					processors.append(leaf.GetName())

		d = {
			# input
			'files': [filename],
			'folders': [folder],
			'x_expressions': processors,
			'x_bins': ['100,0,500'],
			'no_weight': True,
			# analysis
			'analysis_modules': ['NormalizeToUnity'],
			# formatting
			'plot_modules': ['PlotMplZJet', 'PlotMplMean'],
			'markers': ['.'],
			'legend': None,
			'line_styles': ['-'],
			'labels': processors,
			'x_label': 'runtime',
			'y_label': 'au',
			'y_lims': [0, 1],
			'energies': None,
			'title': label,
			'no_energy_label': True,
			'texts': ["Vertical lines indicate\naverage processor runtime"],
			'texts_x': [0.4],
			# output
			'filename':  label.lower() + '_runtime',
			'save_legend': label.lower() + '_legend',
		}
		plots.append(d)
	harryinterface.harry_interface(plots, args)

if __name__ == '__main__':
	runtime()
