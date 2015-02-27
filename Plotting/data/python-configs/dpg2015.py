#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zee_bkgrs
import zee_unfolded
import zee_uncertainties

import Excalibur.Plotting.harryZJet as harryZJet

def dpg_dominik(args=None):
	"""Function to create all plots for Dominiks DPG presentation."""

	args += ['--title', '"own work"']

	zee_bkgrs.zee_bkgrs(args)
	zee_unfolded.zee_unfolded(args)
	dpg_mad_pow(args)
	zee_uncertainties.zee_unc(args)


def dpg_mad_pow(args=None):
	"""Mad pow comparison vs Njets"""
	d = {
		'json_defaults': 'Plotting/data/json-configs/zpt_mad_pow.json',
		'x': 'njets30',
		'x_expressions': 'njets30',
		'x_bins': "7,-0.5, 6.5",
		'x_lims': [-0.5, 6.5],
		'x_ticks': None,
		'x_log': False,
	}
	
	harry_instance = harryZJet.HarryPlotterZJet(
		list_of_args_strings=" ".join(args),
		list_of_config_dicts=[d]
	)


if __name__ == '__main__':
	dpg_dominik()
