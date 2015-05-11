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
	parser.add_argument('--fast', type=int, default=None, help="Only do the n first plots.")
	known_args, unknown_args = parser.parse_known_args((unknown_args if unknown_args is not None else []))

	harry_instance = harryZJet.HarryPlotterZJet(
		list_of_config_dicts=(dicts if known_args.fast is None else dicts[:known_args.fast]),
		list_of_args_strings=" ".join(unknown_args),
		n_processes=min(known_args.max_processes, len(dicts))
	)

