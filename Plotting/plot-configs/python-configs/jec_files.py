#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface
import Artus.Utility.logger as logger
import argparse
import glob
import copy

def jec_files(args=None, additional_dictionary=None):
	"""make plots for L1,RC,L1L2L3,Res files in a directory.

	Usage: merlin.py --py jec_files --jec-dir data/jec/Winter14_V8"""
	plots = []

	parser = argparse.ArgumentParser()
	parser.add_argument('--jec-dir', type=str, default="data/jec/Winter14_V6",
		help="path to jec directory, e.g. data/jec/Winter14_V8")
	parser.add_argument('--jec-algo', type=str, default="AK5PFchs", help="algo")
	
	if args is None:
		known_args, args = parser.parse_known_args()
	else:
		known_args, args = parser.parse_known_args(args)

	# get the list of files from the path
	files = glob.glob(known_args.jec_dir+"/*.txt")
	files = [file for file in files if known_args.jec_algo in file]

	leveldict = {
		"L2Relative": "L2",
		"RC": "L1RC",
	}

	basedict = {
		"input_modules": ["InputJEC"],
		"x_expressions": ["jeteta"],
		"y_bins": ["100,0,100"],
		"y_expressions": ["jetpt"],
		"z_label": "JEC Correction Factor",
		"colormap": "seismic",
		"z_lims": [0.0, 2.0]
	}
	for typ in ['DATA', 'MC']:
		for level in ["L1FastJet", "RC", "L2Relative", "L2L3Residual"]:
			matching_files = [item for item in files if ("_"+typ in item and "_"+level+"_" in item)]
			if len(matching_files) > 0:
				d = copy.deepcopy(basedict)
				d.update({
					"title": typ + " " + leveldict.get(level, level),
					"filename": typ.lower() + "_" + leveldict.get(level, level).lower(),
					"files": matching_files[0]
				})
				plots.append(d)
			else:
				print typ, level, "NOT FOUND:", len(matching_files)

	harryinterface.harry_interface(plots, args)
