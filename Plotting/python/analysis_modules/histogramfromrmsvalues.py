# -*- coding: utf-8 -*-

import logging
import ROOT
from array import array
import Artus.HarryPlotter.analysisbase as analysisbase
import numpy as np
# from scipy.special import erfinv

log = logging.getLogger(__name__)


class HistogramFromRMSValues(analysisbase.AnalysisBase):
    """Construct an histogram from root_objects RMS values"""

    def __init__(self):
        self.histogram_from_rmsvalues_options = None

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
                                                           default=[], help="Remaining percentage of truncated RMS for \
                                                           each nick, e.g. 98.5%.")

    @staticmethod
    def get_truncation_correction_version1(truncation):
        """Determines the correction for the RMS value required for the corresponding truncation by calculating the
        change of RMS compared to the original sigma using the inverse error-function within determination of variance.

        Have a look at http://nbviewer.jupyter.org/gist/wiso/bbb0f470668e3ae30859 for more details"""
        inv_erf = ROOT.TMath.ErfInverse(truncation)
        correction = 1. / np.sqrt(truncation - 2 / np.sqrt(np.pi) * inv_erf * np.exp(-pow(inv_erf, 2)))
        print('Truncated RMS correction factor: ' + str(correction))
        return correction

    @staticmethod
    def get_truncation_correction_version2(truncation):
        """Determines the correction for the RMS value required for the corresponding truncation by calculating the
        correction factor for a normalized Gaussian function with sigma=1 and mu=0.

        Have a look at https://en.wikipedia.org/wiki/Truncated_normal_distribution for more details"""
        print(truncation)
        alpha = -np.sqrt(2) * ROOT.TMath.ErfInverse(truncation)
        beta = -alpha
        z = ROOT.Math.gaussian_cdf(beta) - ROOT.Math.gaussian_cdf(alpha)
        phi_alpha = ROOT.Math.gaussian_pdf(alpha)
        phi_beta = ROOT.Math.gaussian_pdf(beta)
        print(alpha, beta, z, phi_alpha, phi_beta)
        correction = 1. / np.sqrt(1. + (alpha * phi_alpha - beta * phi_beta) / z - pow((phi_alpha - phi_beta) / z, 2))
        print('Truncated RMS correction factor: ' + str(correction))
        return correction

    @staticmethod
    def get_truncation_correction_version3(root_hist, a, b):
        """Determines the correction for the RMS value required for the corresponding truncation by calculating the
        correction factor for a fitted Gaussian function."""
        # a = root_hist.GetBinCenter(1)
        # b = root_hist.GetBinCenter(root_hist.GetNbinsX()+1)
        rms = root_hist.GetRMS()
        mean = root_hist.GetMean()
        fit = ROOT.TF1('gauss_fit', "[2]/([0]*(2*pi)**(0.5))*TMath::Exp(-0.5*((x-[1])/[0])*((x-[1])/[0]))", a, b)
        # fit = ROOT.TF1('gauss_fit', "[2]*TMath::Gaus(x,[1],[0],kFalse)", a, b)
        fit.SetParameters(rms, mean, 10)
        fit.SetParNames("sigma", "mean", "n")
        fit.SetParLimits(0, rms-0.01*rms, rms+0.01*rms)
        fit.SetParLimits(1, mean-0.01*mean, mean+0.01*mean)
        fit.SetParLimits(2, 0., 1000000000000.)
        root_hist.Fit(fit, '', '', a, b)
        parameters = fit.GetParameters()
        # parameter_errors = fit.GetParError()
        fit.SetParameters(parameters[0], parameters[1],  1.)
        print('Fitted sigma ' + str(parameters[0]) + ' <-> Truncated RMS ' + str(root_hist.GetRMS()))
        theoretical_truncation = fit.Integral(a, b)
        print('Theoretical Gaussian truncation: ' + str(theoretical_truncation * 100))
        if theoretical_truncation >= 1. or theoretical_truncation <= 0.:
            correction = 1.0
            print('Truncated RMS correction factor: ' + str(correction) + 'DANGER: Calculation might be out of limits!')
        else:
            alpha = -np.sqrt(2) * ROOT.TMath.ErfInverse(theoretical_truncation)
            beta = -alpha
            z = ROOT.Math.gaussian_cdf(beta) - ROOT.Math.gaussian_cdf(alpha)
            phi_alpha = ROOT.Math.gaussian_pdf(alpha)
            phi_beta = ROOT.Math.gaussian_pdf(beta)
            # print(alpha, beta, z, phi_alpha, phi_beta)
            correction = 1. / np.sqrt(1. + (alpha * phi_alpha - beta * phi_beta) / z -
                                      pow((phi_alpha - phi_beta) / z, 2))
            print('Truncated RMS correction factor: ' + str(correction))
        return correction

    def truncate_hist(self, root_hist, truncation):
        """Truncates the ROOT histogramm in preparation for the RMS determination"""
        mean = root_hist.GetMean()
        # mean_error = root_hist.GetMeanError()
        # rms = root_hist.GetRMS()
        # rms_error = root_hist.GetRMSError()
        integral_total = root_hist.Integral()
        if integral_total != 0.:
            mean_bin = root_hist.GetXaxis().FindBin(mean)
            bin_distance_from_mean = 0  # Start value for scanning width
            first_bin = 0
            last_bin = root_hist.GetNbinsX() - 1
            deviation = 100.0

            while deviation > (100.0 - float(truncation)) and (mean_bin - bin_distance_from_mean) > first_bin \
                    and (mean_bin + bin_distance_from_mean) < last_bin:
                bin_distance_from_mean += 1
                integral_new = root_hist.Integral(mean_bin - bin_distance_from_mean, mean_bin +
                                                  bin_distance_from_mean)
                deviation = (integral_total - integral_new) / integral_total * 100.

            x_bin_min = mean_bin - bin_distance_from_mean
            x_bin_max = mean_bin + bin_distance_from_mean
            x_value_min = root_hist.GetBinCenter(x_bin_min)
            x_value_max = root_hist.GetBinCenter(x_bin_max)
            real_truncation_value = 100.0-deviation

            print('Reached ' + str(real_truncation_value) + '% RMS truncation of specified ' + str(truncation) + '%:')
            print('    -> Using bins [' + str(x_bin_min) + ',' + str(x_bin_max) + '] with values [' + str(
                x_value_min) + ',' + str(x_value_max) + ']')

            # root_hist.SetAxisRange(x_value_min, x_value_max)  # same effect as GetXaxis().SetRange()
            root_hist.GetXaxis().SetRange(x_bin_min, x_bin_max)

            # Determine the correction factor required due to truncation of histogram
            # correction_factor = self.get_truncation_correction_version1(real_truncation_value / 100.)
            # correction_factor = self.get_truncation_correction_version2(real_truncation_value / 100.)
            correction_factor = self.get_truncation_correction_version3(root_hist, x_value_min, x_value_max)
            # correction_factor = 1.0
        else:
            correction_factor = 1.
        return root_hist, correction_factor

    def run(self, plot_data=None):
        """main function"""
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
                if truncation is not None and truncation != 100.0:
                    root_hist, correction_factor = self.truncate_hist(root_hist, truncation)

                else:
                    print('Skipping truncation of histogram')
                    correction_factor = 1.0

                hist.SetBinContent(index+1, root_hist.GetRMS()*correction_factor)
                hist.SetBinError(index+1, root_hist.GetRMSError()*correction_factor)
                # hist.GetXaxis().SetBinLabel(index+1, nick)
                print(nick+' -> set Bin: ' + str(index) + ' -> ' + str(root_hist.GetRMS()) + '+/-' + str(
                    root_hist.GetRMSError()))

            nick = plot_data.plotdict['histogram_from_rms_newnicks'][hist_id]
            plot_data.plotdict['nicks'].append(nick)
            plot_data.plotdict['root_objects'][nick] = hist
