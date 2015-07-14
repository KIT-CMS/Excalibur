#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface


def jec_factors(args=None, additional_dictionary=None):
	""" Plot JEC factors from artus output ntuples.

		Creates 4 plots for L1, RC, L2L3 and Res
		Usage e.g.:  merlin.py --py jec_factors -i work/data.root
	"""
	plots = []

	for level, title, basept in zip(
		['l1', 'rc', 'l2', 'res'],
		['L1', 'L1RC', 'L2', 'Res'],
		['raw', 'raw', 'l1', 'l1l2l3']
	):
		d = {
			'x_expressions': ['jet1eta'],
			'y_expressions': ['jet1pt'+basept],
			'x_bins': ['100,-5,5'],
			'y_bins': ['100,0,100'],
			'zjetfolders': ['nocuts'],
			'z_expressions': ['jet1'+level],
			'colormap': 'seismic',
			'z_lims': [0, 2],
			'tree_draw_options': 'prof',
			'title': title,
			'filename': title.lower(),
			'x_label': 'jet1eta',
			'y_label': 'jet1pt',
			'z_label': 'JEC Correction Factor',
		}
		if additional_dictionary is not None:
			d.update(additional_dictionary)
		plots.append(d)
	harryinterface.harry_interface(plots, args)


if __name__ == '__main__':
	jec_factors()
