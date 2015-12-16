# -*- coding: utf-8 -*-

"""
	This module contains a function template for the tutorial
"""

from Excalibur.Plotting.utility.toolsZJet import PlottingJob


def tutorial(args=None, additional_dictionary=None):
	"""Tutorial plotting function"""
	plots = []

	# 1. Define the plot dictionary, containing a list of Merlin key value pairs
	d = {
		'y_expressions': ['mpf'],
		# ...
	}

	# 2. Append to the list of plots
	plots.append(d)

	# 3. Update with 'additional_dictionary' and return:
	for plot in plots:
		if additional_dictionary != None:
			plot.update(additional_dictionary)
	return [PlottingJob(plots=plots, args=args)]
