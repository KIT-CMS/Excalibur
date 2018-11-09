#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, lims_from_binning
import Excalibur.Plotting.utility.binningsZJet as binningsZJet
import datetime

from jer_comparisons import general_comparison
from jer_functionfits import fit_function
from jer_profplots import rms_profplot_datamc
from jer_truncationscan import jer_truncation_scan_without_JER, jer_truncation_scan_JER
# from jer_subtraction import rms_subtraction_datamc
# from jer_truncations import rms_profplot_datamc_truncationscan
from jer_extrapolation import jer_extrapolation

# 'jet1pt': '40,0,400',  # '5 10 20 30 50 75 125 175 225 300 400',
# 'jet2pt': '40,0,250',  # '5 10 20 30 40 50 75 125 175 250',
# 'jet3pt': '40,0,250',  # '5 10 20 30 40 50 75 125 175 250',


def jer_determination_data_mc_zll(args=None):
    zjetfolder = 'finalcuts'
    channels = ['e', 'm']
    plotting_jobs = []
    for channel in channels:
        d = {
            # default format of labels ['DATA', 'MC', 'Ratio', 'DATA_fit', 'MC_fit']
            'labels': ['Data', 'MC', 'Ratio', '', ''],
            'corrections': ['L1L2L3Res', 'L1L2L3'],
            # 'www': zjetfolder+'_jer_comparison_datamc_Zee',
            # 'www_title': 'JER data-mc comparisons for Zee'+zjetfolder,
            # 'www_text':'JER data-mc comparisons for Zee'+zjetfolder,
            'zjetfolders': [zjetfolder],
            'formats': ['png'],
            # 'formats': ['pdf'],
            'lumis': [35.7],  # [41.86],
            'ratio_denominator_no_errors': False,
            'markers': ['_', '_'],
            'colors': ['black', 'blue', 'black', 'blue', 'black'],
            # 'weights': ['1', '( sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5 )'],
            'weights': ['1', '1']

        }
        if channel == 'm':
            d['title'] = r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{\\mu \\mu}$"
            d['files'] = ['/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/'
                          'data17_mm_BCDEF_17Nov2017.root',
                          '/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/'
                          'mc17_mm_DYNJ_Madgraph.root']
        elif channel == 'e':
            d['title'] = r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{e e}$"
            d['files'] = ['/portal/ekpbms3/home/cheidecker/CMSSW_9_2_14/src/Excalibur/work/'
                          'data17_ee_BCDEF_17Nov2017.root',
                          '/portal/ekpbms3/home/cheidecker/CMSSW_9_2_14/src/Excalibur/work/'
                          'mc17_ee_DYNJ_Madgraph.root']
            # d['files'] = ['/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/'
            #               'data17_ee_BCDEF_17Nov2017.root',
            #               '/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/'
            #               'mc17_ee_DYNJ_Madgraph.root']

        # Adopting weights for Data and MC plots:
        if False:
            if channel == 'm':
                d['weights'] = [
                    # '( abs(mu1eta)<1.3 ) * ( abs(mu2eta)<1.3 )',
                    # '( sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5 ) * '
                    # '( abs(mu1eta)<1.3 ) * '
                    # '( abs(mu2eta)<1.3 )'
                    '1', 'sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5'
                ]
            elif channel == 'e':
                d['weights'] = [
                    # '( abs(e1eta)<1.3 ) * ( abs(e2eta)<1.3 )',
                    # '( sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5 ) * '
                    # '( abs(e1eta)<1.3 ) * '
                    # '( abs(e2eta)<1.3 )'
                    '1', 'sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5'
                ]

        # Plotting Data and MC without corrections label
        if False:
            # Plotting cross check plots for RMS determination
            plotting_jobs += rms_profplot_datamc(args, d, channel=channel)
        if True:
            # Plotting RMS extrapolations
            plotting_jobs += jer_extrapolation(args, d, channel=channel)
        if True:
            # Plotting RMS truncation scans
            plotting_jobs += jer_truncation_scan_JER(args, d, channel=channel)
            plotting_jobs += jer_truncation_scan_without_JER(args, d, channel=channel)

        text_size = 15
        text_factor = 0.022
        d.update({
            'texts': [d['corrections'][0]],
            'texts_y': [0.8],
            'texts_x': [0.98 - (len(d['corrections'][0])*text_factor)],
            'texts_size': [text_size],
        })

        # Plotting various quantities for cross checks with data and MC
        if True:
            quantity_list0 = ['zpt', 'zeta', 'zphi', 'zy', 'metphi', 'met', 'npv', 'jet1pt', 'jet1eta', 'jet2pt',
                              'jet2eta', 'ptbalance', 'mpf', 'zmass']
            quantity_list_ee = ['epluseta', 'eminuseta', 'eminuspt', 'epluspt', 'eminusphi', 'eplusphi']
            quantity_list_mm = ['mupluseta', 'muminuseta', 'muminuspt', 'mupluspt', 'muminusphi', 'muplusphi']
            if channel == 'm':
                quantity_list0.extend(quantity_list_mm)
            elif channel == 'e':
                quantity_list0.extend(quantity_list_ee)

            # plotting_jobs += general_comparison(args, d, channel=channel, only_normalized=False,
            #                                     quantity_list=quantity_list0)

            quantity_list1 = ['ptbalance', 'mpf']
            # plotting_jobs += fit_function(args, d, channel=channel, only_normalized=False, quantity_list=quantity_list1)

        d.update({
            'texts_y': [0.975],
            'texts_size': [text_size],
        })

        # MC plots
        d.update({
            'files': [d['files'][1]],
            'corrections': [d['corrections'][1]],
            'labels': ['MC', ''],
            'colors': ['blue', 'blue', 'black'],
            'weights': [d['weights'][1]],
        })

        d.update({
          'texts': [d['corrections'][0]],
          'texts_y': [0.82],
          # 'texts_x': [0.92 - (len(d['corrections'][0])*text_factor)],
          'texts_size': [text_size],
        })

        # Plotting various quantities for cross checks with MC only
        if True:
            quantity_list2 = ['genzpt', 'genzeta', 'genjet1pt', 'genjet1eta', 'genjet2pt', 'genjet2eta', 'genzmass',
                              'deltarjet1genjet1']
            quantity_list_ee = []  # ['genepluseta', 'geneminuseta', 'geneminuspt', 'genepluspt']
            quantity_list_mm = []  # ['genmupluseta', 'genmuminuseta', 'genmuminuspt', 'genmupluspt']
            if channel == 'm':
                quantity_list2.extend(quantity_list_mm)
            elif channel == 'e':
                quantity_list2.extend(quantity_list_ee)

            # plotting_jobs += general_comparison(args, d, channel=channel, only_normalized=False,
            #                                     quantity_list=quantity_list2)

            quantity_list3 = ['genjet1pt/genzpt', 'genjet1pt/jet1pt', 'genzpt/zpt', 'genzpt', 'jet1pt/genjet1pt']
            # plotting_jobs += fit_function(args, d, channel=channel, only_normalized=False, quantity_list=quantity_list3)

    return plotting_jobs
