# -*- coding: utf-8 -*-

"""
"""

import os

import Artus.HarryPlotter.core as core
import ZJet.Plotting.harryparserZJet as harryparserZJet

class HarryCoreZJet(core.HarryCore):

	def __init__(self, additional_modules_dirs=None, args_from_script=None):

		#append the directories relative of this file
		zjet_plot_base_dir = os.path.dirname(os.path.realpath(__file__))
		relative_dirs = ['/input_modules', '/analysis_modules', '/plot_modules']
		zjet_plot_module_dirs = [zjet_plot_base_dir + rel_dir for rel_dir in relative_dirs]
		if additional_modules_dirs is not None:
			additional_modules_dirs += zjet_plot_module_dirs
		else:
			additional_modules_dirs = zjet_plot_module_dirs

		super(HarryCoreZJet, self).__init__(additional_modules_dirs, args_from_script,
			parser = harryparserZJet.HarryParserZJet())

