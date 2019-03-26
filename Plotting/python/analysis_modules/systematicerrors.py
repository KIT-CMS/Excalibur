# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import array

import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase
import Artus.HarryPlotter.utility.roottools as roottools


class SystematicErrors(analysisbase.AnalysisBase):
    """Creates histograms that contain the maximal deviation of given histograms (variated) from a central histogram
        mainly used to derive systematic errors"""
    
    def __init__(self):
        super(SystematicErrors, self).__init__()
    
    def modify_argument_parser(self, parser, args):
        super(SystematicErrors, self).modify_argument_parser(parser, args)
    
        self.SystematicErrors_options = parser.add_argument_group("SystematicErrors options")
        self.SystematicErrors_options.add_argument("--syst-error-central-nicks", type=str, nargs="+",
                help="Nick names of the central histograms/graphs.")
        self.SystematicErrors_options.add_argument("--syst-error-variated-nicks", type=str, nargs="+",
                help="Nick names of the systematically modified histograms/graphs.")
        self.SystematicErrors_options.add_argument("--syst-error-result-nicks", type=str, nargs="+",
                help="Nick names of the systematic uncertainty histogram/graph.")
        self.SystematicErrors_options.add_argument("--syst-error-relative", nargs="?", type="bool", default=True, const=True,
                help="Do not plot absolute errors, but relative to bin content. [Default: %(default)s]")
        self.SystematicErrors_options.add_argument("--syst-error-relative-percent", nargs="?", type="bool", default=False, const=True,
                help="Output relative errors as percentage. [Default: %(default)s]")
        self.SystematicErrors_options.add_argument("--syst-error-offsets", nargs="+", type=str,
                help="Set an offset to the systematics. [Default: %(default)s]")
        
    def prepare_args(self, parser, plotData):
        super(SystematicErrors, self).prepare_args(parser, plotData)
        self.prepare_list_args(plotData, ["syst_error_central_nicks", "syst_error_variated_nicks", "syst_error_result_nicks", "syst_error_offsets"])
        for index, (syst_error_central_nick, syst_error_result_nick, syst_error_variated_nick, syst_error_offset) in enumerate(zip(
            *[plotData.plotdict[k] for k in ["syst_error_central_nicks","syst_error_result_nicks","syst_error_variated_nicks","syst_error_offsets"]]
            )):
            plotData.plotdict["syst_error_variated_nicks"][index] = syst_error_variated_nick.split()
            if syst_error_offset is None:
                plotData.plotdict["syst_error_offsets"][index] = 0
            else:
                plotData.plotdict["syst_error_offsets"][index] = float(syst_error_offset)
            if syst_error_result_nick is None:
                plotData.plotdict["syst_error_result_nicks"][index] = "syst_error_{}".format(
                        "_".join(plotData.plotdict["syst_error_variated_nicks"][index]),
                )
                
    def run(self, plotData=None):
        super(SystematicErrors, self).run(plotData)
        for nicks, varnicks, resultnicks, offset in zip(
            *[plotData.plotdict[k] for k in ["syst_error_central_nicks", "syst_error_variated_nicks", "syst_error_result_nicks", "syst_error_offsets"]]
        ):
            root_object_central = plotData.plotdict["root_objects"][nicks]
            root_object_result = root_object_central.Clone(resultnicks)
            for x_bin in xrange(1, root_object_central.GetNbinsX()+1):
                varlist = []
                for j in xrange(len(varnicks)):
                    root_object_variated = plotData.plotdict["root_objects"][varnicks[j]]
                    varlist.append(abs(root_object_variated.GetBinContent(x_bin)-root_object_central.GetBinContent(x_bin)))
                root_object_result.SetBinContent(x_bin, offset + max(varlist)/root_object_central.GetBinContent(x_bin))
                root_object_result.SetBinError(x_bin,0)
            plotData.plotdict['nicks'].append(resultnicks)
            plotData.plotdict['root_objects'][resultnicks] = root_object_result
        
