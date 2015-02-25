# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import sys
import inspect
import argparse
import pkgutil

import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.tools as tools

def print_jsons_and_functions(json_path, python_path):
	""" print the comments / docstrings of the json/python plot configs"""

	# get jsons infos
	jsonTools.print_comments_from_json_files(json_path, "_comment")
	log.info(tools.get_colored_string("\npython scripts:", 'cyan'))

	# get docstrings from python functions
	module_list = get_module_list(python_path)
	for module in module_list:
		log.info("\t"+ tools.get_colored_string(module.__name__ + ".py", "yellow"))
		functions = inspect.getmembers(module, inspect.isfunction)
		if len(functions) > 0:
			prefix = "\t\t\t"
			for func in functions:
				log.info("\t\t" + tools.get_colored_string(func[0], "green"))
				log.info(tools.get_indented_text(prefix, inspect.getdoc(func[1])))
	sys.exit(0)

def call_python_function(function_name, python_path):
	"""call a python if it is present in any module in the path."""
	module_list = get_module_list(python_path)
	for module in module_list:
		functions = inspect.getmembers(module, inspect.isfunction)
		for func in functions:
			if func[0] == function_name:
				log.info("Executing function {} in module {}".format(func[0], module.__name__))
				func[1]()
				return


def get_module_list(path):
	"""get a list with all python modules in the path."""
	return [(module.find_module(name).load_module(name)) for module, name, is_pkg in pkgutil.walk_packages([path])]
