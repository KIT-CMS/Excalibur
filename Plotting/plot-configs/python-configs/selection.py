#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.harryinterface as harryinterface

def muon_isolation(args=None, additional_dictionary=None):
	"""Show criteria for muon isolation based selection"""
	def make_title(param):
		title = r"Mu"
		if "inv" in param:
			title = "Inv " + title
		for mid in range(10):
			if str(mid) in param:
				title += "%d" % mid
				break
		for key, name in (("sumchpt","Ch Had $p_T$"),("sumpet","Phot $E_T$"),("sumnhet","Nt Had $p_T$"),("sumpupt","PileUp $p_T$"),("iso","Iso")):
			if key in param:
				title += " %s" % name
				break
		if "/mu" in param:
			title += r" / Mu%d $p_T$" % mid
		return title
	plots = []
	for x_param in [
				"mu%s%d%s/mu%s%dpt"%(mu_type, mu_idx, param, mu_type, mu_idx)
					for mu_idx in range(1,3)
					for param in ("iso","sumchpt","sumnhet","sumpet","sumpupt")
					for mu_type in ("","inv")
					]:
		d = {
			'x_expressions': [x_param],
			'x_bins':["20,0,0.5"],
			#'y_log' : True,
			'filename' : "muiso_%s"%x_param.replace("/","_"),
			'analysis_modules': ['NormalizeToFirstHisto', 'Ratio'],
			"algorithms": ["ak4PFJetsCHS",],
			"corrections": ["L1L2L3"],
			'title': make_title(x_param),
			'y_subplot_lims': [0, 2],
			}
		if additional_dictionary is not None:
			d.update(additional_dictionary)
		plots.append(d)
	for x_param in [
				"mu%s%d%s"%(mu_type, mu_idx, param)
					for mu_idx in range(1,3)
					for param in ("iso","sumchpt","sumnhet","sumpet","sumpupt")
					for mu_type in ("","inv")
					]:
		d = {
			'x_expressions': [x_param],
			'x_bins':["20,0,20"],
			#'y_log' : True,
			'filename' : "muiso_%s"%x_param.replace("/","_"),
			'analysis_modules': ['NormalizeToFirstHisto', 'Ratio'],
			"algorithms": ["ak4PFJetsCHS",],
			"corrections": ["L1L2L3"],
			'title': make_title(x_param),
			'y_subplot_lims': [0, 2],
			}
		if additional_dictionary is not None:
			d.update(additional_dictionary)
		plots.append(d)
	harryinterface.harry_interface(plots, args)