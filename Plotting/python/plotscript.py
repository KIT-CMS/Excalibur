#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import pkgutil
import sys

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.Utility.jsonTools as jsonTools
import Excalibur.Plotting.harryZJet as harryZJet
import Excalibur.Plotting.scripts



def main():
	""" main """
	# get function name from command line
	parser = argparse.ArgumentParser()
	parser.add_argument('function', type=str)
	parser.add_argument('--max-processes', type=int, default=2)
	opt, unknown_args = parser.parse_known_args()

	# get list of modules
	module_list = [(module.find_module(name).load_module(name)) for module, name, is_pkg in pkgutil.walk_packages(scripts.__path__)]

	# iterate over modules, try to find function and execute
	for module in module_list:
		if hasattr(module, opt.function):
			log.info("Using function '%s' in module '%s'" %(opt.function, module.__name__))
			dicts, json = getattr(module, opt.function)()
			makePlots(dicts, json, unknown_args, opt.max_processes)
			return
	log.critical("Function '%s'not found" % opt.function)



def makePlots(plots, json=None, args=sys.argv[1:], max_processes=2):
	"""doc """
	l_plots = []
	for dic in plots:
		# get json defaults, overwrite with dict entries
		if json is not None:
			json_dict = jsonTools.JsonDict([os.path.expandvars(json)]).doIncludes().doComments()
			json_dict.update(dic)
			dic = json_dict
		l_plots.append(dic)

	harry_instance = harryZJet.HarryPlotterZJet(
		list_of_config_dicts=l_plots,
		list_of_args_strings=" ".join(args),
		n_processes=min(max_processes, len(l_plots))
	)

if __name__ == '__main__':
	main()
