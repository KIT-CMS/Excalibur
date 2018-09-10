# -*- coding: utf-8 -*-

import logging
import ROOT
from array import array
import Artus.HarryPlotter.analysisbase as analysisbase
# import Artus.Utility.logger as logger
log = logging.getLogger(__name__)


class HistogramFromRMSValues(analysisbase.AnalysisBase):
    """Construct an histogram from root_objects RMS values"""

    def modify_argument_parser(self, parser, args):
        super(HistogramFromRMSValues, self).modify_argument_parser(parser, args)

        self.histogram_from_rmsvalues_options = parser.add_argument_group("{} options".format(self.name()))
        self.histogram_from_rmsvalues_options.add_argument("--histogram-from-rms-nicks", type=str, nargs="+",
                                                           default=[],
                                                           help="Nicks of the function fits to combine in histogram.")
        self.histogram_from_rmsvalues_options.add_argument("--histogram-from-rms-newnicks", type=str, nargs="+",
                                                           default=[], help="Nickname of the new histogram.")
        self.histogram_from_rmsvalues_options.add_argument("--histogram-from-rms-x-values", type=str, nargs="+",
                                                           default=[], help="x-values of the new histogram.")
        self.histogram_from_rmsvalues_options.add_argument("--histogram-from-rms-truncations", type=str, nargs="+",
                                                           default=[], help="Remaining percentage of truncated RMS for each nick, e.g. 98.5%.")

    def run(self, plot_data=None):
        for hist_id in xrange(max(len(plot_data.plotdict['histogram_from_rms_newnicks']),
                                  len(plot_data.plotdict['histogram_from_rms_nicks']))):
            nicks = plot_data.plotdict['histogram_from_rms_nicks'][hist_id].split()

            if 'histogram_from_rms_truncations' in plot_data.plotdict.keys():
                truncation = plot_data.plotdict['histogram_from_rms_truncations'][hist_id]
            else:
                truncation = None

            x_values = map(float, plot_data.plotdict['histogram_from_rms_x_values'][hist_id].split())
            hist = ROOT.TH1D(self.__class__.__name__, self.__class__.__name__, len(nicks), array('d', x_values))

            for index, nick in enumerate(map(str, nicks)):
                root_hist = plot_data.plotdict["root_objects"][nick]
                if truncation is not None:
                    mean = root_hist.GetMean()
                    # mean_error = root_hist.GetMeanError()
                    # rms = root_hist.GetRMS()
                    # rms_error = root_hist.GetRMSError()
                    integral_total = root_hist.Integral()
                    mean_bin = root_hist.GetXaxis().FindBin(mean)
                    width_bins = 0
                    deviation = 100.0
                    while deviation > (100.0 - float(truncation)) and width_bins <= mean_bin:
                        width_bins += 1
                        integral_new = root_hist.Integral(mean_bin - width_bins, mean_bin + width_bins)
                        deviation = (integral_total - integral_new) / integral_total * 100
                    print 'Reached ' + str(100.0-deviation) + '% RMS truncation of specified ' + str(truncation) + '%:'
                    print '    -> Using bins [' + str(mean_bin - width_bins) + ',' + str(mean_bin + width_bins) + ']'
                    root_hist.SetAxisRange(root_hist.GetBinCenter(mean_bin - width_bins), root_hist.GetBinCenter(
                        mean_bin + width_bins))
                hist.SetBinContent(index+1, root_hist.GetRMS())
                hist.SetBinError(index+1, root_hist.GetRMSError())
                # hist.GetXaxis().SetBinLabel(index+1, nick)
                print nick+' -> set Bin: ' + str(index) + ' -> ' + str(root_hist.GetRMS()) + '+/-' + str(
                    root_hist.GetRMSError())

            nick = plot_data.plotdict['histogram_from_rms_newnicks'][hist_id]
            plot_data.plotdict['nicks'].append(nick)
            plot_data.plotdict['root_objects'][nick] = hist
