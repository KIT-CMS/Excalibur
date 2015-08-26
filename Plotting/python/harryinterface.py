# -*- coding: utf-8 -*-

import argparse

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Excalibur.Plotting.harryZJet as harryZJet

def harry_interface(dicts, unknown_args=None):
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

def return_harry_input(function, *args, **kwargs):
	"""
	Run a Merlin plot function, returning its input to :py:func:`harry_interface`

	This executes ``function(*args, **kwargs)``, capturing any calls to
	:py:func:`harry_interface` to extract the respective ``*args`` and
	``**kwargs`` and return them to the caller. The actual execution of
	:py:func:`harry_interface` is skipped.

	Since multiple calls to :py:func:`harry_interface` can happen in a plot
	function, a *list* of the captured ``(args, kwargs)`` is returned.

	:param function: function to execute; should contain at least one call to :py:func:`harry_interface`
	:type function: callable
	:param args: positional arguments to pass to ``function``
	:type args: list
	:param kwargs: keyword arguments to pass to ``function``
	:type kwargs: dict
	:returns: list of tuples of ``(args, kwargs)`` passed to :py:func:`harry_interface`
	:rtype: list[tuple[list, dict]]
	"""
	# overwrite harry_interface to intercept input
	global harry_interface
	harry_input = []
	_hi = harry_interface
	harry_interface = lambda *harry_args, **harry_kwargs: harry_input.append((harry_args, harry_kwargs))
	# execute and capture
	function(*args, **kwargs)
	# reset harrinterface for future function calls
	harry_interface = _hi
	return harry_input