# -*- coding: utf-8 -*-

import logging
from collections import namedtuple
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

class PlottingJob(object):
	def __init__(self, plots, args):
		assert plots is not None and args is not None, "Both `plots` and `args` must be defined for plotting jobs"
		self.plots = plots
		self.args = args

	def __getitem__(self, item):
		if item in ("plots", "args"):
			return getattr(self, item)
		raise KeyError("No such element %r" % item)

	def __add__(self, other):
		if not isinstance(other, self.__class__):
			raise TypeError("cannot concatenate '%s' and '%s' objects" % (self.__class__.__name__, other.__class__.__name__))
		if self.args != other.args:
			raise ValueError("cannot concatenate '%s' objects with different 'args'" % self.__class__.__name__)
		return PlottingJob(plots=self.plots + other.plots, args=self.args)

def print_plotting_functions(plotting_path):
	""" print the comments / docstrings of the plotting configs"""

	log.info(tools.get_colored_string("plotting scripts: ({})".format(plotting_path), 'cyan'))
	# get docstrings
	module_list = get_module_list(plotting_path)
	for module in module_list:
		log.info(tools.get_colored_string(module.__name__ + ".py", "yellow"))
		functions = inspect.getmembers(module, inspect.isfunction)
		if len(functions) > 0:
			prefix = "\t\t"
			for func in functions:
				if func[0].startswith("_"):
					continue
				log.info("\t" + tools.get_colored_string(func[0], "green"))
				if inspect.getdoc(func[1]) != None:  # has docstring
					log.info(tools.get_indented_text(prefix, inspect.getdoc(func[1])))


def call_python_function(function_name, python_path, unknown_args=None):
	"""call a python if it is present in any module in the path."""
	module_list = []
	for path in python_path.split(':'):
		module_list += get_module_list(path)
	for module in module_list:
		functions = inspect.getmembers(module, inspect.isfunction)
		for func in functions:
			if func[0] == function_name:
				log.info("Executing function {} in module {}".format(func[0], module.__name__))
				plotting_jobs = func[1](unknown_args)
				if plotting_jobs is not None and isinstance(plotting_jobs, list):
					import Excalibur.Plotting.harryinterface as harryinterface
					# Aggregating plots with same arguments for parallel plotting
					all_plots = {}
					for plotting_job in plotting_jobs:
						all_plots.setdefault(tuple(plotting_job.args), []).extend(plotting_job.plots)
					for args in all_plots:
						harryinterface.harry_interface(all_plots[args], args)
				return
	log.warning("Could not execute function {}".format(function_name))


def get_input_files(args=None):
	"""
	Extract the list of input files from given CLI arguments

	:param args: command line arguments
	:type args: list[str]
	:returns: input files and remaining CLI arguments
	:rtype: list[str], list[str]
	"""
	if args is None:
		return [], []
	args_nofiles = []
	input_files = []
	input_file_args = False
	for elem in args:
		if not input_file_args and elem in ("-i", "--files"):
			input_file_args = True
			continue
		if input_file_args:
			if not elem.startswith("-"):
				input_files.append(elem)
				continue
			else:
				input_file_args = False
		args_nofiles.append(elem)
	return input_files, args_nofiles


def lims_from_binning(binning):
	"""
	Convert a binning string to plot limits
	"""
	if ',' in binning:
		return [float(border) for border in binning.split(',')[1:3]]
	return [float(binning.split(None, 1)[0]), float(binning.rsplit(None, 1)[-1])]


def get_module_list(path):
	"""get a list with all python modules in the path."""
	return [(module.find_module(name).load_module(name)) for module, name, is_pkg in pkgutil.walk_packages([path])]

def get_list_slice(lists, arg):
	if arg is False:
		return lists
	else:
		return [[l[arg]] for l in lists]

def get_special_parser(args):
	parser = argparse.ArgumentParser()
	# if these arguments are set true the function will not iterate over the respective quantities
	#	by default, argument ist False -> whole list is taken and iterated over
	#	if set without arguments: first item of list is taken, no iteration
	#	if set with arguments N: N-th item of list is taken, no iteration
	parser.add_argument('--no-quantities', type=int, nargs='?', default=False, const=0)
	parser.add_argument('--no-methods', type=int, nargs='?', default=False, const=0)
	if args is None:
		known_args, args = parser.parse_known_args()
	else:
		known_args, args = parser.parse_known_args(args)
	return known_args, args

def generate_dict(args=None, additional_dictionary=None):
	x_dict = {
		'alpha': ['80,0,1'],
		'jet1area': ['80,0.3,0.9'],
		'jet1eta': ['60,-5,5'],
		'jet1phi': ['40,-3.1415,3.1415',],
		'jet1pt': ['160,0,800'],
		'jet1res': ['80,0.95,1.2'],
		'jet2eta': ['40,-5,5'],
		'jet2phi': ['40,-3.1415,3.1415',],
		'jet2pt': ['60,0,75'],
		'met': ['80,0,100'],
		'metphi': ['40,-3.1415,3.1415',],
		'mpf': ['40,0,2'],
		'npu': ['31,-0.5,60.5'],
		'npumean': ['100,1,50'],
		'npv': ['51,-0.5,50.5'],
		'ptbalance': ['40,0,2'],
		'A': ['40,-1,1'],
		'B': ['40,-1,1'],
		'rawmet': ['80,0,100'],
		'zmass': ['160,71,111'],
		'zphi': ['40,-3.1415,3.1415',],
		'zpt': ['80,0,400'],
		'zy': ['50,-2.5,2.5'],
		'genHT': ['3000,10.5,3000.5'],
		'jetHT': ['3000,10.5,3000.5']
	}
	return x_dict
	
def basiccutlabel(args, d,CH,ZPT,ALPHA,ETA,RES):
	etalabel=r"$%s<"%ETA[0]+r"|\\eta^\\mathrm{Jet1}|<%s$"%ETA[1]
	if ALPHA==[0.0]:
		alphalabel=r"$\\alpha=0$"
	else:
		alphalabel=r"$\\alpha<%s$"%ALPHA[0]
	if len(ZPT)==2:
		zptlabel=r"$%s<"%ZPT[0]+r"\\mathrm{p}^Z_T/GeV<%s$"%ZPT[1]
	elif len(ZPT)==1:
		zptlabel=r"$\\mathrm{p}^Z_T/GeV>%s$"%ZPT[0]
	if CH=='ee':
		channellabel=r"$\\mathrm{\\bf{Z \\rightarrow} e e}$"
	elif CH=='mm':
		channellabel=r"$\\mathrm{\\bf{Z \\rightarrow} \\mu \\mu}$"
		
	d.update({	'texts': [channellabel,r"$\\bf{"+RES+"}$",zptlabel,etalabel,alphalabel],
				'texts_x': [0.34,0.69,0.03,0.03,0.03] if RES == 'L1L2L3Res' else [0.34,0.76,0.03,0.03,0.03],
				'texts_y': [0.95,0.09,0.83,0.90,0.97],
				'texts_size': [20,25,15,15,15],
				'title': r"$\\bf{CMS} \\hspace{0.5} \\it{Preliminary \\hspace{3.2}}$",#'CMS Preliminary',
				#'title': r"$\\bf{CMS} \\hspace{0.5} \\it{work\\hspace{0.2}in\\hspace{0.2}progress \\hspace{3.2}}$"
				})
	return d

def get_lumis(args, d, RUN, YEAR):
    if YEAR==2016:
        if RUN=='BCD':
            d.update({  'lumis' : [12.6]})# ICHEP Dataset
        elif RUN=='EF':
            d.update({  'lumis' : [6.7]})
        elif RUN=='G':
            d.update({  'lumis' : [8.13]})
        elif RUN=='H':
            d.update({  'lumis' : [8.86]})
        elif RUN=='BCDEF':
            d.update({ 'lumis' : [19.7]})
        elif RUN=='BCDEFG':
            d.update({ 'lumis' : [27.2]})
        elif RUN=='BCDEFGH':
            d.update({ 'lumis' : [35.8]})
        elif RUN=='GH':
            d.update({ 'lumis' : [16.5]})
    elif YEAR==2017:
        if RUN=='BCD':
            d.update({  'lumis' : [17.8]})

def cutlabel(args,d,cut):
    d.update({  'texts': [r'$\\mathrm{p^\\mu_T}>25\\mathrm{GeV}$, |$\\mathrm{\\eta^\\mu}$|$<2.4$']})
    if cut == '_zpt30':
        d['texts'] += [ r'$\\mathrm{p^{Z}_T}>30\\mathrm{GeV}$, |$\\mathrm{m^Z}-\\mathrm{m^Z_{PDG}}$|$<20\\mathrm{GeV}$']
    elif cut == '_phistareta04':
        d['texts'] += [ r'$\\mathrm{\\Phi^*_\\eta}>0.4$,  |$\\mathrm{m^Z}-\\mathrm{m^Z_{PDG}}$|$<20\\mathrm{GeV}$']
    elif cut == '_jet1pt20':
        d['texts'] += [ r'|$\\mathrm{m^Z}-\\mathrm{m^Z_{PDG}}$|$<20\\mathrm{GeV}$',
                        r'$\\mathrm{p^{jet1}_T}>20\\mathrm{GeV}$, |$\\mathrm{y^{jet}}$|$<2.4$'],

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
			sys.exit()

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
	
