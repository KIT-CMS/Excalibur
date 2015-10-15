#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import Excalibur.Plotting.harryinterface as harryinterface
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, lims_from_binning
import Excalibur.Plotting.utility.binningsZJet as binningsZJet


def _expand_to_files(raw_list, file_count, add_number=False):
	"""
	Expand a list of individual arguments to match expansion for multiple input files
	"""
	out_list = []
	for item in raw_list:
		for _ in xrange(file_count):
			if add_number:
				out_list.append(item + _)
			else:
				out_list.append(item)
	return out_list


def cuts_2015(args=None, additional_dictionary=None):
	"""
	Plot cuts for 2015 analysis - cut_n_muons, cut_muon_kinematics and cut_jet_kinematics
	"""
	d = {
		"algorithms": ["ak4PFJetsCHS",],
		"corrections": ["L1L2L3"],
	}
	if additional_dictionary:
		d.update(additional_dictionary)
	# overwrite harryinterface to get plots in parallel
	all_plots = {}
	_hi = harryinterface.harry_interface
	harryinterface.harry_interface = lambda plots, args: all_plots.setdefault(tuple(args), []).extend(plots)
	# collect plots
	cut_n_muons(args=args, additional_dictionary=d)
	cut_muon_kinematics(args=args, additional_dictionary=d)
	cut_jet_kinematics(args=args, additional_dictionary=d)
	# create plots
	for args in all_plots:
		_hi(all_plots[args], args)
	# reset harrinterface for future function calls
	harryinterface.harry_interface = _hi


def muon_isolation(args=None, additional_dictionary=None):
	"""Show criteria for muon isolation based selection"""
	arg_plots = {}
	input_files, args_nofiles = get_input_files(args)
	# variables == mu1pt, muinv2sumnhet, ...
	# ISO == sumchpt + sumnhet + sumpet - 0.5 * sumpupt
	for muid in (1, 2):
		for validity in ("inv",""):
			muon_id = "mu%s%d"%(validity, muid)
			for obs in ("sumchpt", "sumnhet", "sumpet", "sumpupt"):
				# 1D plots
				d = {
					'x_expressions': ['%s%s/%spt' % (muon_id, obs, muon_id)],
					'analysis_modules': ['NormalizeToFirstHisto', 'Ratio'],
					"filename": "cuts_iso_%s_%s" % (muon_id, obs),
					'x_bins': "25,0,1",
					'weights':['%spt>0'%muon_id],
				}
				if additional_dictionary is not None:
					d.update(additional_dictionary)
				arg_plots.setdefault(tuple(args), []).append(d)
				# 2D plots
				for in_file in input_files:
					d_args = args_nofiles[:]
					d_args.extend(("-i", in_file))
					d = {
						'x_expressions': ['%siso/%spt' % (muon_id, muon_id)],
						'y_expressions': ['%s%s/%spt' % (muon_id, obs, muon_id)],
						'x_bins': "25,0,1",
						'y_bins': "25,0,1",
						'z_log': True,
						"filename": "cuts_iso_%s_%s_%s" % (muon_id, obs, os.path.basename(in_file).split(".",1)[0]),
						'weights':['%spt>0'%muon_id],
					}
					if additional_dictionary is not None:
						d.update(additional_dictionary)
					arg_plots.setdefault(tuple(d_args), []).append(d)
	for d_args in arg_plots:
		harryinterface.harry_interface(arg_plots[d_args], d_args)


def cut_n_muons(args=None, additional_dictionary=None):
	"""Plot min/max N muon cut"""
	plots = []
	d_base = {
		'x_bins': ["6,-0.5,5.5"],
		'plot_modules': ["PlotMplZJet", "PlotMplRectangle"],
		"rectangle_x": [-1,1.5,3.5,6],
		"rectangle_alpha": [0.2],
		"rectangle_color": ["red","red"],
		"y_log": True,
		'y_subplot_lims': [0.15, 1.95],
	}
	d1 = {
		"x_expressions": ["nmuons", "nmuons"],
		"markers": ["o", "fill"]*1 + ["o"]*1,
		"nicks": ["data", "mc"],
		"labels": [r"$\\mu_\\mathrm{Data}$", r"$\\mu_\\mathrm{MC}$"],
		'analysis_modules': ['Ratio'],
		"filename": "cuts_nmuons",
		"title": "Number of valid Muons",
	}
	d2 = {
		"x_expressions": ["nmuonsinv+nmuons", "nmuonsinv+nmuons"],
		"markers": ["o", "fill"]*2 + ["o"]*2,
		"nicks": ["data Mu Val", "mc Mu Val", "data Mu Tot", "mc Mu Tot"],
		"labels": [r"$\\mu_\\mathrm{Data}$", r"$\\mu_\\mathrm{MC}$", r"$\\mu_\\mathrm{Data}^\\mathrm{tot}$", r"$\\mu_\\mathrm{MC}^\\mathrm{tot}$"],
		"filename": "cuts_totmuons",
		"title": "Number of total Muons",
	}
	d1.update(d_base)
	d2.update(d_base)
	if additional_dictionary is not None:
		d1.update(additional_dictionary)
		d2.update(additional_dictionary)
	plots.append(d1)
	plots.append(d2)
	harryinterface.harry_interface(plots, args)


def cut_muon_kinematics(args=None, additional_dictionary=None):
	"""Plot pt and eta muon cut"""
	arg_plots = {}
	input_files, args_nofiles = get_input_files(args)
	for in_file in input_files:
		args = args_nofiles[:]
		args.extend(("-i", in_file))
		for muid in range(1,3):
			d = {
				'x_expressions': ['mu%dpt' % muid],
				'y_expressions': ['mu%deta' % muid],
				'x_bins': "25,0,100",
				'y_bins': "25,0,2.5",
				'y_lims': [0,2.5],
				'x_lims': [0,100],
				#'z_log': True,
				'plot_modules': ["PlotMplZJet", "PlotMplRectangle"],
				# cfg['CutMuonPtMin'] = 20.0
				# cfg['CutMuonEtaMax'] = 2.3
				"rectangle_x": [-1,20],
				"rectangle_y": [0,2.3, 2.3,5],
				"rectangle_alpha": [0.2],
				"rectangle_color": ["red","red"],
				"filename": "cuts_muon%d_%s"%(muid,os.path.basename(in_file).split(".",1)[0]),
				"title": "Muon %d"%muid,
			}
			if additional_dictionary is not None:
				d.update(additional_dictionary)
			arg_plots.setdefault(tuple(args), []).append(d)
	for args in arg_plots:
		harryinterface.harry_interface(arg_plots[args], args)


def cut_jet_kinematics(args=None, additional_dictionary=None):
	"""Plot pt and eta jet1 cut"""
	arg_plots = {}
	input_files, args_nofiles = get_input_files(args)
	for in_file in input_files:
		args = args_nofiles[:]
		args.extend(("-i", in_file))
		for muid in range(1,2):
			d = {
				'x_expressions': ['jet%dpt' % muid],
				'y_expressions': ['jet%deta' % muid],
				'x_bins': "25,0,100",
				'y_bins': "25,0,2.5",
				'y_lims': [0,2.5],
				'x_lims': [0,100],
				#'z_log': True,
				'plot_modules': ["PlotMplZJet", "PlotMplRectangle"],
				# cfg['CutLeadingJetPtMin'] = 12.0
				# cfg['CutLeadingJetEtaMax'] = 1.3
				"rectangle_x": [-1,12],
				"rectangle_y": [0,1.3, 1.3,5],
				"rectangle_color": ["red","red"],
				"rectangle_alpha": [0.2],
				"filename": "cuts_jet%d_%s" % (muid, os.path.basename(in_file).split(".",1)[0]),
				"title": "Jet %d"%muid,
			}
			if additional_dictionary is not None:
				d.update(additional_dictionary)
			arg_plots.setdefault(tuple(args), []).append(d)
	for args in arg_plots:
		harryinterface.harry_interface(arg_plots[args], args)


def jetid_2015(args, additional_dictionary=None):
	"""All jetID plots for 2015 data"""
	d = {
		"algorithms": ["ak4PFJetsCHS"],
	}
	if additional_dictionary is not None:
		d.update(additional_dictionary)
	plotting_jobs = []
	plotting_jobs += jetid_efficiency(args=args, additional_dictionary=d)
	plotting_jobs += jetid_changes(args=args, additional_dictionary=d)
	return plotting_jobs


def jetid_efficiency(args, additional_dictionary=None):
	"""Plot efficiency of jetID veto for leading skim jet over pt, eta, phi"""
	plots = []
	input_files, args_nofiles = get_input_files(args)
	binnings = binningsZJet.BinningsDictZJet()
	for x_expr, x_binning in [
		("skimjet1pt", "20,0,200"),
		("skimjet1eta", binnings.binnings_dict["eta"]),
		("skimjet1phi", binnings.binnings_dict["phi"]),
		("zpt", "50,0,200"),
	]:
		d = {
			'labels': ['valid'] * len(input_files) + ["total"] * len(input_files),
			'x_expressions': [x_expr],
			'x_lims': lims_from_binning(x_binning),
			'weights': ['(weight*skimjet1validity)'] * len(input_files) + ["(weight*(skimjet1pt>=0))"] * len(input_files),
			'x_bins': x_binning,
			'filename': "jetid_efficiency_" + x_expr,
			'analysis_modules': ['Ratio'],
			'y_subplot_lims': [0.01, 0.99],
		}
		if additional_dictionary is not None:
			d.update(additional_dictionary)
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]


def jetid_changes(args, additional_dictionary=None):
	"""Plot changes from jetID veto for leading jet vs leading skim jet over pt, eta, phi"""
	plots = []
	input_files, args_nofiles = get_input_files(args)
	#binningsZJet.BinningsDictZJet().binnings_dict["abseta"]
	for x_expr, x_binning in [
		("jet1pt", "20,0,200"),
		("jet1eta", binningsZJet.BinningsDictZJet().binnings_dict["eta"]),
		("jet1phi", binningsZJet.BinningsDictZJet().binnings_dict["phi"])
	]:
		d = {
			'labels': ['valid'] * len(input_files) + ["total"] * len(input_files),
			'x_expressions': [x_expr],
			'y_expressions': ["skim%s" % x_expr],
			'x_lims': lims_from_binning(x_binning),
			'y_lims': lims_from_binning(x_binning),
			'x_bins': x_binning,
			'y_bins': x_binning,
			'filename': "jetid_changes_" + x_expr,
		}
		if additional_dictionary is not None:
			d.update(additional_dictionary)
		plots.append(d)
	return [PlottingJob(plots=plots, args=args)]
