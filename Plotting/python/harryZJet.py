#!/usr/bin/env python
# -*- coding: utf-8 -*-


import ZJet.Plotting.coreZJet as coreZJet
import Artus.HarryPlotter.harry as harry

class HarryPlotterZJet(harry.HarryPlotter):

	def plot(self, harry_args):
		harry_core_zjet = coreZJet.HarryCoreZJet(args_from_script=harry_args)
		harry_core_zjet.parser.set_defaults(plot_modules=["PlotMplZJet"])
		harry_core_zjet.run()
