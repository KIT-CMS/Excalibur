#!/usr/bin/env python
# -*- coding: utf-8 -*-


import Excalibur.Plotting.coreZJet as coreZJet
import Artus.HarryPlotter.harry as harry

class HarryPlotterZJet(harry.HarryPlotter):

	def plot(self, plot_index):
		harry_args = self.harry_args[plot_index]
		harry_core_zjet = coreZJet.HarryCoreZJet(args_from_script=harry_args)
		return harry_core_zjet.run()
