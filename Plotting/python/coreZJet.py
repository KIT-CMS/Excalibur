# -*- coding: utf-8 -*-

"""
"""

import os

import Artus.HarryPlotter.core as core
import ZJet.Plotting.harryparserZJet as harryparserZJet

class HarryCoreZJet(core.HarryCore):

	def __init__(self, additional_modules_dirs=None, args_from_script=None):
		#append the directory of this file
		plotdir = os.path.dirname(os.path.realpath(__file__))
		if additional_modules_dirs is not None:
			additional_modules_dirs += [plotdir]
		else:
			additional_modules_dirs = [plotdir]

		super(HarryCoreZJet, self).__init__(additional_modules_dirs, args_from_script)
		self.parser = harryparserZJet.HarryParserZJet()

