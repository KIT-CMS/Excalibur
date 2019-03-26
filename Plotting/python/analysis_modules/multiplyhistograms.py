# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.analysisbase as analysisbase
import Artus.HarryPlotter.utility.roottools as roottools
import numpy as np

class MultiplyHistograms(analysisbase.AnalysisBase):
    """Create sum of histograms. This module does exactly the same as AddHistograms, but is can enable different addition steps together with this module."""
    
    def __init__(self):
        super(MultiplyHistograms, self).__init__()

    def modify_argument_parser(self, parser, args):
        super(MultiplyHistograms, self).modify_argument_parser(parser, args)

        self.sum_histograms_options = parser.add_argument_group("{} options".format(self.name()))
        self.sum_histograms_options.add_argument(
                "--multiply-nicks", nargs="+",
                help="Nick names (whitespace separated) for the histograms to be multiplied"
        )
        self.sum_histograms_options.add_argument(
                "--multiply-result-nicks", nargs="+",
                help="Nick names for the resulting histograms."
        )

    def prepare_args(self, parser, plotData):
        super(MultiplyHistograms, self).prepare_args(parser, plotData)
        self.prepare_list_args(plotData, ["multiply_nicks", "multiply_result_nicks"])
        
        for index, (multiply_nicks, multiply_result_nick) in enumerate(zip(
                *[plotData.plotdict[k] for k in ["multiply_nicks", "multiply_result_nicks"]]
        )):
            plotData.plotdict["multiply_nicks"][index] = multiply_nicks.split()
            if multiply_result_nick is None:
                plotData.plotdict["multiply_result_nicks"][index] = "multiply_{}".format(
                        "_".join(plotData.plotdict["multiply_nicks"][index]),
                )

    def run(self, plotData=None):
        super(MultiplyHistograms, self).run(plotData)
        
        for multiply_nicks, multiply_result_nick in zip(
                *[plotData.plotdict[k] for k in ["multiply_nicks", "multiply_result_nicks"]]
        ):
            root_object_result = plotData.plotdict["root_objects"][multiply_nicks[0]].Clone(multiply_result_nick)
            for x_bin in xrange(1, root_object_result.GetNbinsX()+1):
                result = 1
                error = 0
                for j in xrange(len(multiply_nicks)):
                    root_object = plotData.plotdict["root_objects"][multiply_nicks[j]]
                    result *= root_object.GetBinContent(x_bin)
                    try:
                        error += (root_object.GetBinError(x_bin)/root_object.GetBinContent(x_bin))**2
                    except ZeroDivisionError:
                        error += 0
                root_object_result.SetBinContent(x_bin,result)
                root_object_result.SetBinError(x_bin,result*np.sqrt(error))
            
            plotData.plotdict['nicks'].append(multiply_result_nick)
            plotData.plotdict['root_objects'][multiply_result_nick] = root_object_result
            
