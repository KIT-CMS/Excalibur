#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface


def jec_factors(args=None, additional_dictionary=None, rc=True, res=False):
	""" Plot JEC factors from artus output ntuples.

		Creates plots for L1 and L2L3, optionally also RC and Res
		Usage e.g.:  merlin.py --py jec_factors -i work/data.root
	"""
	plots = []

	#level: (title, basept)
	jec_dict = {
		'l1': ('L1', 'raw'),
		'l2': ('L2', 'l1'),
		'rc': ('L1RC', 'raw'),
		'res': ('Res', 'l1l2l3')
	}

	corr_levels = ['l1', 'l2']
	if rc:
		corr_levels.append('rc')
	if res:
		corr_levels.append('res')

	for level, (title, basept) in zip(corr_levels, [jec_dict[level] for level in corr_levels]):
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
