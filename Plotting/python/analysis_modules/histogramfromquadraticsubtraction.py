# -*- coding: utf-8 -*-

import logging
import ROOT
from array import array
import Artus.HarryPlotter.analysisbase as analysisbase
# import Artus.Utility.logger as logger
log = logging.getLogger(__name__)


class HistogramFromQuadraticSubtraction(analysisbase.AnalysisBase):
    """Construct an histogram from root_objects RMS values"""

    def modify_argument_parser(self, parser, args):
        super(HistogramFromQuadraticSubtraction, self).modify_argument_parser(parser, args)

        self.histogram_from_quadratic_subtraction_options = parser.add_argument_group("{} options".format(self.name()))
        self.histogram_from_quadratic_subtraction_options.add_argument("--histogram-from-quadratic-subtraction-minuend-nicks",
                                                           type=str, nargs="+", default=[],
                                                           help="Nick of the minuend of the quadratic subtraction.")
        self.histogram_from_quadratic_subtraction_options.add_argument("--histogram-from-quadratic-subtraction-subtrahend-nicks",
                                                           type=str, nargs="+", default=[],
                                                           help="Nicks of the subtrahends of the quadratic subtraction.")
        self.histogram_from_quadratic_subtraction_options.add_argument("--histogram-from-quadratic-subtraction-result-nicks",
                                                           type=str, nargs="+", default=[],
                                                           help="Nick of the resulting histogram.")

    def run(self, plot_data=None):
        for hist_id in xrange(max(len(plot_data.plotdict['histogram_from_quadratic_subtraction_minuend_nicks']),
                                  len(plot_data.plotdict['histogram_from_quadratic_subtraction_result_nicks']))):
            print 'HIST_ID: ' + str(hist_id)
            minuend_nick = plot_data.plotdict['histogram_from_quadratic_subtraction_minuend_nicks'][hist_id]
            print 'MINUEND NICK: ' + str(minuend_nick)

            subtrahend_nicks = plot_data.plotdict['histogram_from_quadratic_subtraction_subtrahend_nicks'][hist_id].split()
            print 'SUBTRAHEND NICKS: ' + str(subtrahend_nicks)

            result_nick = plot_data.plotdict['histogram_from_quadratic_subtraction_result_nicks'][hist_id]
            print 'RESULT NICK: ' + str(result_nick)

            # Explicitly copy
            minuend_hist = plot_data.plotdict["root_objects"][minuend_nick]
            nbins = minuend_hist.GetNbinsX()
            xlow = minuend_hist.GetBinLowEdge(1)
            xup = minuend_hist.GetBinLowEdge(nbins + 1)
            hist = ROOT.TH1D(self.__class__.__name__, self.__class__.__name__, nbins, xlow, xup)

            for bin in range(nbins + 1):
                if bin == 0:
                    continue
                # Determine result of quadratic subtraction for BinContent
                bin_value = pow(minuend_hist.GetBinContent(bin), 2)
                for subtrahend in subtrahend_nicks:
                    bin_value -= pow(plot_data.plotdict["root_objects"][subtrahend].GetBinContent(bin), 2)
                if bin_value < 0.:
                    continue
                bin_value = pow(bin_value, 0.5)

                # Calculate uncertainty for BinError
                if bin_value == 0.:
                    continue
                bin_error = pow(minuend_hist.GetBinContent(bin) * minuend_hist.GetBinError(bin) / bin_value, 2)

                for subtrahend in subtrahend_nicks:
                    bin_error += pow(plot_data.plotdict["root_objects"][subtrahend].GetBinContent(bin) *
                                     plot_data.plotdict["root_objects"][subtrahend].GetBinError(bin) / bin_value, 2)
                if bin_error < 0.:
                    continue
                bin_error = pow(bin_error, 0.5)

                hist.SetBinContent(bin, bin_value)
                hist.SetBinError(bin, bin_error)

                print 'Bin' + str(bin) + ' content was set to ' + str(bin_value) + '+/-' + str(bin_error)

            plot_data.plotdict['nicks'].append(result_nick)
            plot_data.plotdict['root_objects'][result_nick] = hist
