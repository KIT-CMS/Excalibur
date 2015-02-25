# -*- coding: utf-8 -*-

import argparse

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Excalibur.Plotting.harryZJet as harryZJet


def plotscript(dicts, unknown_args=None):
	""" main """	
	# get max processes name from command line
	parser = argparse.ArgumentParser()
	parser.add_argument('--max-processes', type=int, default=8)
	if unknown_args is None:
		known_args, unknown_args = parser.parse_known_args()
	else:
		known_args, unknown_args = parser.parse_known_args(unknown_args)

	logger.initLogger()

	harry_instance = harryZJet.HarryPlotterZJet(
		list_of_config_dicts=dicts,
		list_of_args_strings=" ".join(unknown_args),
		n_processes=min(known_args.max_processes, len(dicts))
	)

