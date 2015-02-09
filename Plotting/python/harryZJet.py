#!/usr/bin/env python
# -*- coding: utf-8 -*-


import ZJet.Plotting.coreZJet as coreZJet
import Artus.HarryPlotter.harry as harry

class HarryPlotterZJet(harry.HarryPlotter):

	def plot(self, harry_args):
		harry_core_zjet = coreZJet.HarryCoreZJet(args_from_script=harry_args)
		return harry_core_zjet.run()
