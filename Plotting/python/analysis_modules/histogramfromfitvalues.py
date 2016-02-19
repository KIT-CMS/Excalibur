# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT
from array import array
import Artus.HarryPlotter.analysisbase as analysisbase


class HistogramFromFitValues(analysisbase.AnalysisBase):
	"""Construct an histogram from root_objects mean values"""


	def modify_argument_parser(self, parser, args):
		super(HistogramFromFitValues, self).modify_argument_parser(parser, args)

		self.histogram_from_fitvalues_options = parser.add_argument_group("{} options".format(self.name()))
		self.histogram_from_fitvalues_options.add_argument("--histogram-from-fit-nicks", type=str, nargs="+", default=[],
				help="Nicks of the function fits to combine in histogram.")
		self.histogram_from_fitvalues_options.add_argument("--histogram-from-fit-newnick", type=str, nargs="+", default=[],
				help="Nickname of the new histogram.")
		self.histogram_from_fitvalues_options.add_argument("--histogram-from-fit-x-values", type=str, nargs="+", default=[],
				help="x-values of the new histogram.")

#	def run(self, plotData):
#
#		for hist_id in xrange(max(len(plotData.plotdict['histogram_from_fit_newnick']), len(plotData.plotdict['histogram_from_fit_nicks']))):
#
#			nicks=plotData.plotdict['histogram_from_fit_nicks'][hist_id].split()
#			x_values = plotData.plotdict['histogram_from_fit_x_values'][hist_id].split()
#
#			hist = ROOT.TGraph(int(len(nicks)))
#
#			for index, nick in enumerate(nicks):
#				fit_function = plotData.plotdict["root_objects"][nick]
#				hist.SetPoint(index+1,float(x_values[index]),float(fit_function.GetParameter(0))) #  float(fit_function.GetParError(0))
#				print 'Set point: '+str(x_values[index])+' '+str(fit_function.GetParameter(0))
#			nick = plotData.plotdict['histogram_from_fit_newnick'][hist_id]
#			plotData.plotdict['nicks'].append(nick)
#			plotData.plotdict['root_objects'][nick] = hist

	def run(self, plotData):
		for hist_id in xrange(max(len(plotData.plotdict['histogram_from_fit_newnick']), len(plotData.plotdict['histogram_from_fit_nicks']))):

			nicks=plotData.plotdict['histogram_from_fit_nicks'][hist_id].split()
			print nicks
			x_values = map(float,plotData.plotdict['histogram_from_fit_x_values'][hist_id].split())
			print x_values
			hist = ROOT.TH1D(self.__class__.__name__, self.__class__.__name__, len(nicks), array('d',x_values))

			for index, nick in enumerate(map(str,nicks)):
				print nick
				fit_function = plotData.plotdict["root_objects"][nick]
				hist.SetBinContent(index+1,  fit_function.GetParameter(0))
				hist.SetBinError(index+1,  fit_function.GetParError(0))
				print 'Set Bin: '+str(x_values[index])+' '+str(fit_function.GetParameter(0))+'+/-'+str(fit_function.GetParError(0))
			nick = plotData.plotdict['histogram_from_fit_newnick'][hist_id]
			plotData.plotdict['nicks'].append(nick)
			plotData.plotdict['root_objects'][nick] = hist
