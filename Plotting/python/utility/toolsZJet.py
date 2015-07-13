# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import os
import sys
import inspect
import argparse
import pkgutil
import math
import numpy as np
import ROOT

import Artus.Utility.jsonTools as jsonTools
import Artus.HarryPlotter.utility.roottools as roottools
import Artus.Utility.tools as tools

def print_jsons_and_functions(json_path, python_path):
	""" print the comments / docstrings of the json/python plot configs"""

	# get jsons infos
	jsonTools.print_comments_from_json_files(json_path, "_comment")
	for subdir in [x[0] for x in os.walk(json_path)][1:]:
		jsonTools.print_comments_from_json_files(subdir, "_comment")

	log.info(tools.get_colored_string("\npython scripts: ({})".format(python_path), 'cyan'))
	# get docstrings from python functions
	module_list = get_module_list(python_path)
	for module in module_list:
		log.info("\t"+ tools.get_colored_string(module.__name__ + ".py", "yellow"))
		functions = inspect.getmembers(module, inspect.isfunction)
		if len(functions) > 0:
			prefix = "\t\t\t"
			for func in functions:
				log.info("\t\t" + tools.get_colored_string(func[0], "green"))
				if inspect.getdoc(func[1]) != None:  # has docstring
					log.info(tools.get_indented_text(prefix, inspect.getdoc(func[1])))
	sys.exit(0)

def call_python_function(function_name, python_path, unknown_args=None):
	"""call a python if it is present in any module in the path."""
	module_list = get_module_list(python_path)
	for module in module_list:
		functions = inspect.getmembers(module, inspect.isfunction)
		for func in functions:
			if func[0] == function_name:
				log.info("Executing function {} in module {}".format(func[0], module.__name__))
				func[1](unknown_args)
				return
	log.warning("Could not execute function {}".format(function_name))


def get_module_list(path):
	"""get a list with all python modules in the path."""
	return [(module.find_module(name).load_module(name)) for module, name, is_pkg in pkgutil.walk_packages([path])]


class JECfile(object):
	"""Class to handle JEC files and create ROOT histograms with the correction factors"""
	def __init__(self, filename):
		self.lines = open(filename).read().splitlines() 
		self.lines_short = [[item for item in line[:-2].split(" ")if item != ""] for line in self.lines[1:]]

		self.quantitydict = {
			"JetA": "JetArea",
		}

		# get correction formula, number of parameters etc from first line
		firstline = self.lines[0].split("{")[1].split("}")[0]
		firstline_list = [item for item in firstline.split(" ") if item != ""]
		self.n_bins = len(self.lines)-1
		self.n_bin_vars = int(firstline_list[0])
		self.n_input_vars = int(firstline_list[self.n_bin_vars+1])
		self.bin_vars = self._format_variable_list(firstline_list[1:self.n_bin_vars+1])
		self.input_vars = self._format_variable_list(firstline_list[self.n_bin_vars+2:self.n_bin_vars+self.n_input_vars+2])
		log.info(str(self.n_bin_vars) + " Binning variable(s): " + ", ".join(self.bin_vars))
		log.info(str(self.n_input_vars) + " Input variable(s): "+ ", ".join(self.input_vars))

		n_parameters = int([item for item in self.lines[1][:-2].split(" ") if item != ""][self.n_bin_vars*2])  - 2 * self.n_input_vars
		log.info("N parameters: "+ str(n_parameters))

		#prepare formula
		self.formula = firstline_list[2+self.n_bin_vars + self.n_input_vars]
		for i in range(n_parameters):
			self.formula = self.formula.replace("[{}]".format(i), "l[{}+2*self.n_bin_vars + 2*self.n_input_vars+1]".format(i))
		# convert from tmath to python syntax
		formula_replace_dict = {
			"log(": "math.log(",
			"log10(": "math.log10(",
			"TMath::Log10": "ROOT.TMath.Log10",
			"TMath::LogNormal": "ROOT.TMath.LogNormal",
			"TMath::Log(": "ROOT.TMath.Log(",
			"^": "**",
			"exp(": "math.exp("
		}
		for key in formula_replace_dict:
			self.formula = self.formula.replace(key, formula_replace_dict[key])
		log.info("Correction formula: " + self.formula)

		#get binning for binned variable
		self.binning = []
		for line in self.lines_short:
			self.binning.append(float(line[0]))
		self.binning.append(float(self.lines_short[-1][1])) #last bin


	def get_corr_histo(self, input_var_binning, area=None, rho=None):
		"""Use this method to evaluate the JEC file with a certain binning (and some fixed parameters if needed)"""

		#create root histo
		self.jec_histo = ROOT.TProfile2D()

		binning = [str(item) for item in self.binning]
		self.jec_histo = roottools.RootTools.create_root_histogram(
			x_bins=roottools.RootTools.prepare_binning(binning)[1],
			y_bins=roottools.RootTools.prepare_binning(input_var_binning[0])[1],
			z_bins=None, profile_histogram=True, name="name"
		)

		input_values_dict = {
			#'jetpt': y, #set this in each iteration
			'jetarea': area,
			'rho': rho,
		}

		#iterate over bin and input variable, fill histo
		for x in range(len(self.lines_short)):
			for y in self._get_bin_centers(input_var_binning[0][0]):

				# prepare input values
				input_values_dict['jetpt'] = y
				input_values = []
				for quantity in self.input_vars:
					input_values.append(input_values_dict[quantity])

				corr_factor = self._get_corr_factor(x, (input_values)[:self.n_input_vars])
				if corr_factor is not None:
					self.jec_histo.Fill(self.binning[x], y, corr_factor)

		return self.jec_histo


	def _get_corr_factor(self, bin_nr, input_vars):
		"""Get correction factor for single bin"""
		l = [float(item) for item in self.lines[1+bin_nr].split(" ") if item != ""]
		bin_limits = [float(i) for i in l[:2]]
		for index, (input_value, var_name) in enumerate(zip(input_vars, ["x", "y", "z"])):
			vars()[var_name] = input_value

			input_limits = [float(i) for i in l[1+2*(self.n_bin_vars+index):3+2*(self.n_bin_vars+index)]]
			if (input_value < input_limits[0] or input_value > input_limits[1]):
				log.debug(str(var_name) + " " + str(input_value) + " not in limits "+ ",".join([str(item) for item in input_limits]))
				return None
		try:
			return eval(self.formula)
		except NameError as e:
			log.critical("Could not evaluate formula: " + e.message)
			log.critical("Is the formula correctly converted into python? (perhaps check the formula_replace_dict in the init method of the JECfile class)")
			sys,exit()

	def _get_bin_centers(self, input_var_binning):
		"""Get the bin centers for the input binning"""
		if len(input_var_binning.split(",")) == 3:
			n, low, high = [float(item) for item in input_var_binning.split(",")]
			bins =  list(np.arange(low,high,(high-low)/n))+[high]
		else:
			bins = [float(item) for item in input_var_binning.split(" ")]
		bin_centers = [(low+high)/2. for low, high in zip(bins[:-1], bins[1:])]
		return bin_centers

	def _format_variable_list(self, var_list):
		return [self.quantitydict.get(var, var).lower() for var in var_list]
