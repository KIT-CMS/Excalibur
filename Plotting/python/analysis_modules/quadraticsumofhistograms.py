# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.analysisbase as analysisbase
import Artus.HarryPlotter.utility.roottools as roottools
import numpy as np

class QuadraticSumOfHistograms(analysisbase.AnalysisBase):
    """Creates the square root of the quadratic sum of histograms."""

    def __init__(self):
        super(QuadraticSumOfHistograms, self).__init__()
    
    def modify_argument_parser(self, parser, args):
        super(QuadraticSumOfHistograms, self).modify_argument_parser(parser, args)
    
        self.quad_sum_histograms_options = parser.add_argument_group("{} options".format(self.name()))
        self.quad_sum_histograms_options.add_argument(
                "--quad-sum-nicks", nargs="+",
                help="Nick names (whitespace separated) for the histograms to be quadratically added"
        )
        self.quad_sum_histograms_options.add_argument(
                "--quad-sum-scale-factors", nargs="+",
                help="Scale factor (whitespace separated) for the histograms to be quadratically added [Default: 1]."
        )
        self.quad_sum_histograms_options.add_argument(
                "--quad-sum-result-nicks", nargs="+",
                help="Nick names for the resulting histograms."
        )
    
    def prepare_args(self, parser, plotData):
        super(QuadraticSumOfHistograms, self).prepare_args(parser, plotData)
        self.prepare_list_args(plotData, ["quad_sum_nicks", "quad_sum_result_nicks", "quad_sum_scale_factors"])
        
        for index, (quad_sum_nicks, quad_sum_result_nick, quad_sum_scale_factors) in enumerate(zip(
                *[plotData.plotdict[k] for k in ["quad_sum_nicks", "quad_sum_result_nicks", "quad_sum_scale_factors"]]
        )):
            plotData.plotdict["quad_sum_nicks"][index] = quad_sum_nicks.split()
            if quad_sum_scale_factors is None:
                plotData.plotdict["quad_sum_scale_factors"][index] = [1] * len(quad_sum_nicks.split())
            else:
                plotData.plotdict["quad_sum_scale_factors"][index] = [float(quad_sum_scale_factor) for quad_sum_scale_factor in quad_sum_scale_factors.split()]
            if quad_sum_result_nick is None:
                plotData.plotdict["quad_sum_result_nicks"][index] = "quad_sum_{}".format(
                        "_".join(plotData.plotdict["quad_sum_nicks"][index]),
                )
    
    def run(self, plotData=None):
        super(QuadraticSumOfHistograms, self).run(plotData)
        for quad_sum_nicks, quad_sum_scale_factors, quad_sum_result_nick in zip(
                *[plotData.plotdict[k] for k in ["quad_sum_nicks", "quad_sum_scale_factors", "quad_sum_result_nicks"]]
            ):
            root_object_result = plotData.plotdict["root_objects"][quad_sum_nicks[0]].Clone(quad_sum_result_nick)
            for x_bin in xrange(1, root_object_result.GetNbinsX()+1):
                quad_sum = 0
                for j in xrange(len(quad_sum_nicks)):
                    root_object = plotData.plotdict["root_objects"][quad_sum_nicks[j]]
                    quad_sum += quad_sum_scale_factors[j]*(root_object.GetBinContent(x_bin))**2
                root_object_result.SetBinContent(x_bin,np.sqrt(quad_sum))
                #root_object_result.SetBinError(x_bin,0)
            plotData.plotdict['nicks'].append(quad_sum_result_nick)
            plotData.plotdict['root_objects'][quad_sum_result_nick] = root_object_result
        
