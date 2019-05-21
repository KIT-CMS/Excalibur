#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, lims_from_binning
import Excalibur.Plotting.utility.binningsZJet as binningsZJet
import datetime

from jer_comparisons import general_comparison, general_comparison_genreco
from jer_functionfits import fit_function
from jer_profplots import rms_profplot_datamc
from jer_truncationscan import jer_truncation_scan_without_jer, jer_truncation_scan_jer_only
#from jer_extrapolation3 import jer_extrapolation3 as jer_extrapolation
from jer_extrapolation import jer_extrapolation

# 'jet1pt': '40,0,400',  # '5 10 20 30 50 75 125 175 225 300 400',
# 'jet2pt': '40,0,250',  # '5 10 20 30 40 50 75 125 175 250',
# 'jet3pt': '40,0,250',  # '5 10 20 30 40 50 75 125 175 250',


def jer_determination_data_mc_zll(args=None):
    channels = ['e', 'm']
    year = 2018
    plot_types = []
    # DataMC plots:
    # plot_types += ['rms_prof_plot']
    plot_types += ['jer_extrapolation']
    # plot_types += ['jer_truncation_scan']
    # plot_types += ['general_comparisons']
    # plot_types += ['fit_functions']
    # # MC only plots:
    # plot_types += ['general_comparisons_mc']
    # plot_types += ['fit_functions_mc']
    # plot_types += ['gen_reco_comparisons_mc']

    additional_weights = False

    zjetfolder = 'finalcuts'
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
            # 'lumis': [35.7],
            'lumis': [41.96],
            'ratio_denominator_no_errors': False,
            'markers': ['_', '_'],
            'colors': ['black', 'blue', 'black', 'blue', 'black'],
            # 'weights': ['1', '( sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5 )'],
            'weights': ['1', '1']

        }
        if channel == 'm':
            d['title'] = r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{\\mu \\mu}$"
            if year == 2018:
                d['files'] = ['/ceph/dsavoiu/JEC/Autumn18/17Sep2018_V8_2019-03-18/data18_mm_ABCD_17Sep2018.root',
                              '/ceph/dsavoiu/JEC/Autumn18/17Sep2018_V8_2019-03-18/mc18_mm_DYNJ_Madgraph.root']
            elif year == 2017:
                d['files'] = ['/ceph/cheidecker/zjets/excalibur/Fall17_17Nov2017_V24/data17_mm_BCDEF_17Nov2017.root',
                              '/ceph/cheidecker/zjets/excalibur/Fall17_17Nov2017_V24/mc17_mm_DYNJ_Madgraph.root']
                # d['files'] = ['/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/'
                #               'data17_mm_BCDEF_17Nov2017.root',
                #               '/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/'
                #               'mc17_mm_DYNJ_Madgraph.root']
            elif year == 2016:
                d['files'] = ['/ceph/cheidecker/zjets/excalibur/07Aug2017_V12_noEGMss_2018-07-15/'
                              'data16_mm_BCDEFGH_07Aug2017.root',
                              '/ceph/cheidecker/zjets/excalibur/07Aug2017_V12_noEGMss_2018-07-15/'
                              'mc16_mm_BCDEFGH_DYNJ_Madgraph.root']
                # d['files'] = ['/ceph/storage/c/dsavoiu/excalibur_results_calibration/Summer16/'
                #               '07Aug2017_V12_noEGMss_2018-07-15/data16_mm_BCDEFGH_07Aug2017.root',
                #               '/ceph/storage/c/dsavoiu/excalibur_results_calibration/Summer16/'
                #               '07Aug2017_V12_noEGMss_2018-07-15/mc16_mm_BCDEFGH_DYNJ_Madgraph.root']
        elif channel == 'e':
            d['title'] = r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{e e}$"
            if year == 2018:
                d['files'] = ['/ceph/dsavoiu/JEC/Autumn18/17Sep2018_V8_2019-03-18/data18_ee_ABCD_17Sep2018.root',
                              '/ceph/dsavoiu/JEC/Autumn18/17Sep2018_V8_2019-03-18/mc18_ee_DYNJ_Madgraph.root']
            elif year == 2017:
                d['files'] = ['/ceph/cheidecker/zjets/excalibur/Fall17_17Nov2017_V24/data17_ee_BCDEF_17Nov2017.root',
                              '/ceph/cheidecker/zjets/excalibur/Fall17_17Nov2017_V24/mc17_ee_DYNJ_Madgraph_egsm.root']
                # d['files'] = ['/ceph/cheidecker/zjets/excalibur/Fall17_17Nov2017_V24/data17_ee_BCDEF_17Nov2017.root',
                #               '/ceph/cheidecker/zjets/excalibur/Fall17_17Nov2017_V24/mc17_ee_DYNJ_Madgraph.root']
                # d['files'] = ['/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/'
                #               'data17_ee_BCDEF_17Nov2017.root',
                #               '/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/'
                #               'mc17_ee_DYNJ_Madgraph.root']
            elif year == 2016:
                d['files'] = ['/ceph/cheidecker/zjets/excalibur/07Aug2017_V12_backportEGMss_npvGood_2018-08-04/'
                              'data16_ee_BCDEFGH_07Aug2017.root',
                              '/ceph/cheidecker/zjets/excalibur/07Aug2017_V12_backportEGMss_npvGood_2018-08-04/'
                              'mc16_ee_BCDEFGH_DYNJ_Madgraph.root']
                # d['files'] = ['/ceph/storage/c/dsavoiu/excalibur_results_calibration/Summer16/'
                #               '07Aug2017_V12_backportEGMss_npvGood_2018-08-04/data16_ee_BCDEFGH_07Aug2017.root',
                #               '/ceph/storage/c/dsavoiu/excalibur_results_calibration/Summer16/'
                #               '07Aug2017_V12_backportEGMss_npvGood_2018-08-04/mc16_ee_BCDEFGH_DYNJ_Madgraph.root']

        # Adopting weights for Data and MC plots:
        if additional_weights:
            if channel == 'm':
                d['weights'] = [
                    # '( abs(mu1eta)<1.3 ) * ( abs(mu2eta)<1.3 )',
                    # '( sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5 ) * '
                    # '( abs(mu1eta)<1.3 ) * '
                    # '( abs(mu2eta)<1.3 )'
                    # '1', 'sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5'
                    # '1', 'matchedgenjet1pt>0'
                    '1', '(alpha<0.3)*(alpha>=0.25)'
                ]
            elif channel == 'e':
                d['weights'] = [
                    # '( abs(e1eta)<1.3 ) * ( abs(e2eta)<1.3 )',
                    # '( sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5 ) * '
                    # '( abs(e1eta)<1.3 ) * '
                    # '( abs(e2eta)<1.3 )'
                    # '1', 'sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5'
                    # '1', 'matchedgenjet1pt>0'
                    '1', '(alpha<0.3)*(alpha>=0.25)'
                ]

        # Plotting Data and MC without corrections label
        if 'rms_prof_plot' in plot_types:
            # Plotting cross check plots for RMS determination
            plotting_jobs += rms_profplot_datamc(args, d, channel=channel)
        if 'jer_extrapolation' in plot_types:
            # Plotting RMS extrapolations
            plotting_jobs += jer_extrapolation(args, d, channel=channel)
        if 'jer_truncation_scan' in plot_types:
            # Plotting RMS truncation scans
            plotting_jobs += jer_truncation_scan_jer_only(args, d, channel=channel)
            plotting_jobs += jer_truncation_scan_without_jer(args, d, channel=channel)

        text_size = 15
        text_factor = 0.022
        d.update({
            'texts': [d['corrections'][0]],
            'texts_y': [0.8],
            'texts_x': [0.98 - (len(d['corrections'][0])*text_factor)],
            'texts_size': [text_size],
        })

        # Plotting various quantities for cross checks with data and MC
        if 'general_comparisons' in plot_types:
            quantity_list0 = ['zpt', 'zeta', 'zphi', 'zy', 'metphi', 'met', 'npv', 'jet1pt', 'jet1eta', 'jet2pt',
                              'jet2eta', 'ptbalance', 'mpf', 'zmass']
            quantity_list_ee = ['epluseta', 'eminuseta', 'eminuspt', 'epluspt', 'eminusphi', 'eplusphi']
            quantity_list_mm = ['mupluseta', 'muminuseta', 'muminuspt', 'mupluspt', 'muminusphi', 'muplusphi']
            if channel == 'm':
                quantity_list0.extend(quantity_list_mm)
            elif channel == 'e':
                quantity_list0.extend(quantity_list_ee)

            plotting_jobs += general_comparison(args, d, channel=channel, only_normalized=False,
                                                quantity_list=quantity_list0)
        if 'fit_functions' in plot_types:
            quantity_list1 = ['ptbalance', 'mpf']
            plotting_jobs += fit_function(args, d, channel=channel, only_normalized=False,
                                          quantity_list=quantity_list1)

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
        if 'general_comparisons_mc' in plot_types:
            quantity_list2 = ['genzpt', 'genzeta', 'genjet1pt', 'genjet1eta', 'genjet2pt', 'genjet2eta', 'genzmass'] # ,
                              # 'deltarjet1genjet1']
            quantity_list_ee = []  # ['genepluseta', 'geneminuseta', 'geneminuspt', 'genepluspt']
            quantity_list_mm = []  # ['genmupluseta', 'genmuminuseta', 'genmuminuspt', 'genmupluspt']
            if channel == 'm':
                quantity_list2.extend(quantity_list_mm)
            elif channel == 'e':
                quantity_list2.extend(quantity_list_ee)

            plotting_jobs += general_comparison(args, d, channel=channel, only_normalized=False,
                                                quantity_list=quantity_list2)
        if 'fit_functions_mc' in plot_types:
            quantity_list3 = ['genjet1pt/genzpt', 'genzpt/zpt', 'jet1pt/genjet1pt']
            plotting_jobs += fit_function(args, d, channel=channel, only_normalized=False,
                                          quantity_list=quantity_list3)
        if 'gen_reco_comparisons_mc' in plot_types:
            quantity_list4 = ['zpt']
            plotting_jobs += general_comparison_genreco(args, d, channel=channel, only_normalized=False,
                                                quantity_list=quantity_list4)
    return plotting_jobs
