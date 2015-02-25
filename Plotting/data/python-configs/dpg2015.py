#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zee_bkgrs
import zee_unfolded

import Excalibur.Plotting.harryZJet as harryZJet

def dpg_dominik(unknown_args=None):
	"""Function to create all plots for Dominiks DPG presentation."""

	zee_bkgrs.zee_bkgrs(unknown_args)
	zee_unfolded.zee_unfolded(unknown_args)
	dpg_mad_pow(unknown_args)


def dpg_mad_pow(unknown_args=None):
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
		list_of_args_strings=" ".join(unknown_args),
		list_of_config_dicts=[d]
	)


if __name__ == '__main__':
	dpg_dominik()
