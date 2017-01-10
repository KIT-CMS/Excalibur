# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)
import collections
import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase


class PrintResults(analysisbase.AnalysisBase):

	def __init__(self):
		super(PrintResults, self).__init__()
	
	def modify_argument_parser(self, parser, args):
		super(PrintResults, self).modify_argument_parser(parser, args)
		self.printresults_options = parser.add_argument_group("{} options".format(self.name()))
		self.printresults_options.add_argument("--filename", type=str, nargs="+",
				help="Filename for the output")
	def prepare_args(self, parser, plotData):
		super(PrintResults, self).prepare_args(parser, plotData)
	
	def run(self, plotData=None):
		super(PrintResults, self).run(plotData)
		f = open(plotData.plotdict["filename"]+'.txt', 'w')
		nBins = plotData.plotdict["root_objects"].itervalues().next().GetNbinsX()
		for iBin in range(1,nBins+1):
			f.write(str(plotData.plotdict["root_objects"].itervalues().next().GetBinLowEdge(iBin))+"  "+str(plotData.plotdict["root_objects"].itervalues().next().GetBinLowEdge(iBin)+plotData.plotdict["root_objects"].itervalues().next().GetBinWidth(iBin)))
			od = collections.OrderedDict(sorted(plotData.plotdict["root_objects"].items(), key=lambda t: t[0]))
			for nick, root_object in od.iteritems():
				f.write (" %.6f" % root_object.GetBinContent(iBin))
			f.write(" "+str(2.70000)+'\n') 
		f.close()
		print "Results written in ", plotData.plotdict["filename"]+'.txt'

			


