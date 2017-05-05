import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase


class GetConstant(analysisbase.AnalysisBase):
	"""Normalize all histograms by bin width."""
	def __init__(self):
		super(GetConstant, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(GetConstant, self).modify_argument_parser(parser, args)

		self.GetConstant_options = parser.add_argument_group("{} options".format(self.name()))
		self.GetConstant_options.add_argument("--nicks-for-binning", type=str, nargs="+",
				help="Nick which defines the binning")
		self.GetConstant_options.add_argument("--constant-nicks", type=str, nargs="+",
                                help="nick-name of the constant")
		self.GetConstant_options.add_argument("--constant", type=str, nargs="+",
                                help="value of the constant")


	def prepare_args(self, parser, plotData):
		super(GetConstant, self).prepare_args(parser, plotData)
		self.prepare_list_args(plotData, ['nicks_for_binning', 'constant_nicks', 'constant'])

	def run(self, plotData=None):
		super(GetConstant, self).run(plotData)
		for binning, constant_nick, constant in zip(plotData.plotdict['nicks_for_binning'],plotData.plotdict['constant_nicks'], plotData.plotdict['constant']):
			new_histo = plotData.plotdict["root_objects"][binning].Clone()
			for bin in xrange(1,new_histo.GetNbinsX()+1):
				new_histo.SetBinContent(bin, constant)
			plotData.plotdict["root_objects"][constant_nick] = new_histo
			plotData.plotdict["nicks"].append(constant_nick)	
