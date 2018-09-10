#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, lims_from_binning
import Excalibur.Plotting.utility.binningsZJet as binningsZJet

import argparse
import copy
import jec_factors
import jec_files


def generate_dict(args=None, additional_dictionary=None, channel_dict="m"):
    x_dict = {
        'alpha': ['40,0,1'],
        'jet1area': ['40,0.3,0.9'],
        'jet1eta': ['20,-1.5,1.5'],
        'jet1phi': ['20,-3.1415,3.1415', ],
        'jet1pt': ['40,0,250'],
        'jet2eta': ['20,-5,5'],
        'jet2phi': ['20,-3.1415,3.1415', ],
        'jet2pt': ['30,0,75'],
        'met': ['40,0,100'],
        'metphi': ['20,-3.1415,3.1415', ],
        'mpf': ['40,0,2'],
        'npu': ['31,-0.5,30.5'],
        'npumean': ['40,0,40'],
        'npv': ['30,0,30'],
        # 'npv': ['31,-0.5,30.5'],
        'ptbalance': ['40,0,2'],
        'rawmet': ['40,0,100'],
        'zmass': ['40,71,111'],
        'zphi': ['20,-3.1415,3.1415', ],
        'zpt': ['40,0,400'],
        'zy': ['25,-2.5,2.5'],
        'genzmass': ['40,71,111'],
        # 'genzpt/zpt': ['40,-30,0'],
        'genzpt/zpt': ['40,0.9,1.1'],
        'genjet1pt/jet1pt': ['40,0,2'],
        'jet1pt/genjet1pt': ['40,0,2'],
        'genjet1pt/genzpt': ['40,0,2'],
        'genjet1pt/zpt': ['40,0,2'],
        'jet1pt/zpt': ['40,0,2'],
        'jet1pt/zpt-genjet1pt/zpt': ['40,-1,1'],
        'generatorWeight': ['100,-2,2'],
        'puWeight': ['100,0,10'],
        'hlt': ['100,-0.5,1.5'],
        'weight': ['100,-1,1'],
    }
    x_dict_ee = {
        'e1phi': ['20,-3.1415,3.1415', ],
        'e1pt': ['20,0,150'],
        'e2pt': ['20,0,150'],
        'eminuspt': ['20,0,150'],
        'epluspt': ['20,0,150'],
    }
    x_dict_mm = {
        'mu1phi': ['20,-3.1415,3.1415', ],
        'mu1pt': ['20,0,150'],
        'mu2pt': ['20,0,150'],
        'muminuspt': ['20,0,150'],
        'mupluspt': ['20,0,150'],
        'muminuseta': ['20,-2.4,2.4'],
        'mupluseta': ['20,-2.4,2.4'],
    }
    if channel_dict == "m":
        x_dict.update(x_dict_mm)
    elif channel_dict == "e":
        x_dict.update(x_dict_ee)

    for q in x_dict:
        if len(x_dict[q]) == 1:
            x_dict[q] += ['best']
    return x_dict


def general_comparison(args=None, additional_dictionary=None, only_normalized=False, channel='m', quantity_list=[]):
    """Comparison of: various quantities, both absolute and normalized"""
    plots = []
    x_dict = generate_dict(channel_dict=channel)
  
    for quantity in quantity_list:
        # normal comparison
        d = {
            'x_expressions': [quantity],
            'cutlabel': True,
            'analysis_modules': ['Ratio'],
            'y_subplot_lims': [0.75, 1.25],
            'y_log': quantity in ['zpt'],
            'x_log': quantity in ['zpt'],
            'plot_modules': ['PlotMplZJet'],
            'filename': 'Z'+channel+channel+'_'+quantity.replace('/', '%'),
        }
        if quantity in x_dict:
            d['x_bins'] = [x_dict[quantity][0]]
            # d['legend'] = x_dict[quantity][1]

        if additional_dictionary:
            d.update(additional_dictionary)
        if quantity == 'alpha' and (additional_dictionary is None or 'zjetfolders' not in additional_dictionary):
            d['zjetfolders'] = ['noalphacuts']

        if quantity == 'zphi':
            d['y_rel_lims'] = [1, 1.3]
        elif quantity == 'zpt':
            d['y_rel_lims'] = [1, 400]
        elif quantity in ['ptbalance', 'mpf']:
            d['plot_modules'] = d['plot_modules'] + ['PlotMplMean']
            d['mean_nicks'] = ['nick0', 'nick1']

        if quantity in binningsZJet.BinningsDictZJet().binnings_dict:
            x_bins = binningsZJet.BinningsDictZJet().binnings_dict[quantity]
            x_lims = lims_from_binning(x_bins)
            d['x_bins'] = [x_bins]
            d['x_lims'] = x_lims
        elif quantity in x_dict:
            d['x_bins'] = [x_dict[quantity][0]]
            d['x_lims'] = lims_from_binning(x_dict[quantity][0])

        if quantity in ['zeta', 'mupluseta', 'muminuseta', 'epluseta', 'eminuseta']:
            d['plot_modules'] = d['plot_modules'] + ['PlotMplRectangle']
            if channel == 'm':
                d['rectangle_x'] = [-6, -1.3, 1.3, 6]
            elif channel == 'e':
                d['rectangle_x'] = [-6, -1.479, 1.479, 6]
            d['rectangle_alpha'] = [0.2]
            d['rectangle_color'] = ['red']

        if quantity in ['genjet1pt', 'genzpt', 'genzmass']:
            d['files'] = [d['files'][1]]
        if only_normalized:
            # shape comparison
            d.update({
                'analysis_modules': d['analysis_modules'] + ['NormalizeToFirstHisto'],
                'filename': 'Z' + channel + channel + '_' + quantity.replace('/', '%') + '_shapeComparison',
            })
        plots.append(d)

    return [PlottingJob(plots=plots, args=args)]


def fit_profplot_datamc(args=None, additional_dictionary=None, only_normalized=False, channel='m'):
    """Profile Plot of fitted quantity in bins of any quantity"""
    plots = []
    x_dict = generate_dict(channel_dict=channel)
    cut_quantities = ['alpha']  # x_quantity on the plot
    cut_binnings = ['0.0 0.05 0.1 0.15 0.2 0.25 0.3']  # x_bins in plot
    # cut_binnings = ['0.025 0.05 0.075 0.1 0.125 0.15 0.175 0.2 0.225 0.25 0.275 0.3']  # x_bins in plot
    for cut_index, cut_quantity in enumerate(cut_quantities):
        cut_binning = cut_binnings[cut_index].split()
        fit_quantity = 'ptbalance'
        d = {
            'x_expressions': fit_quantity,  # y_expression in the plot
            'analysis_modules': ['FunctionPlot', 'HistogramFromFitValues', 'Ratio'],
            'filename': 'Z' + channel + channel + '_' + fit_quantity.replace('/', '%') + '_vs_' + cut_quantity.replace(
              '/', '%') + '_fit_profplot',
            'legend': 'upper left',
            'ratio_denominator_no_errors': False,
        }
        if additional_dictionary:
            d.update(additional_dictionary)
        copyfiles = d['files']
        weights = []
        nicks = []
        files = []
        labels = []
        fit_hist_nicks = []
        fit_function_nicks = []
        x_bins = []

        for dataset in ['MC', 'Data']:
            fit_nicks = []
            for index in range(len(cut_binning)-1):
                # cut out one bin in each loop
                weights += [str(cut_binning[index]) + '<' + cut_quantity + '&&' + cut_quantity + '<' +
                            str(cut_binning[index+1])]
                # Get nicks for each bin and each file
                nicks += ['nick_' + str(cut_quantity) + '_'+str(dataset) + '_' + str(index)]
                fit_nicks += ['nick_' + str(cut_quantity) + '_' + str(dataset) + '_' + str(index) + '_fit']
                if dataset == 'Data':
                    files += [copyfiles[0]]
                    labels += ['MC']
                elif dataset == 'Data':
                    files += [copyfiles[1]]
                    labels += ['Data']
                # corrections += ['L1L2L3']
            fit_function_nicks += fit_nicks
            fit_hist_nicks += [" ".join(fit_nicks)]
            x_bins += [" ".join(map(str, cut_binning))]
        d.update({
            'nicks': nicks,
            'files': files,
            "function_fit": nicks,
            "function_nicknames": fit_function_nicks,
            "functions": ['[2]*TMath::Exp(-0.5*((x-[1])/[0])*((x-[1])/[0]))'],
            "function_parameters": ["1., 1., 1."],
            'weights': weights,
            'nicks_whitelist': ['fit_data_values', 'fit_mc_values'],
            'histogram_from_fit_nicks': fit_hist_nicks,
            'histogram_from_fit_newnick': ['fit_data_values', 'fit_mc_values'],
            'histogram_from_fit_x_values': x_bins,
            'y_lims': [0.0, 0.35],
            'y_label': 'resolution',
            # 'x_lims': [min(cut_binning),max(cut_binning)],
            'x_log':  cut_quantity in ['jet1pt', 'zpt'],
            'x_label': cut_quantity,
            # 'markers': ['d','o', 'd'],
            "colors": ['blue', 'black', 'black'],
            'labels': ['Data', 'Ratio', 'MC'],
            # 'lines': [1.0],
            'ratio_numerator_nicks': 'fit_data_values',
            'ratio_denominator_nicks': 'fit_mc_values',
            # 'y_subplot_lims': [0.99, 1.01],
        })

        plots.append(d)

    return [PlottingJob(plots=plots, args=args)]


def fit_function_datamc_gauss(dictionary):
    """fits a distribution to the plot"""
    dictionary.update({
        'function_fit': ['nick0', 'nick1'],
        'function_nicknames': ['nick0_fit', 'nick1_fit'],
        'functions': '[2]*TMath::Exp(-0.5*((x-[1])/[0])*((x-[1])/[0]))',
        'function_parameters': '0.5, 1, 1000',
        'fit_text_npar': 1,
        'fit_text_parameter_names': ['sigma', 'mu', 'A'],
        'legend_cols': 1,
        'fit_text_nicks': ['nick0_fit', 'nick1_fit'],
        'fit_text_colors': ['black', 'blue'],
        # 'fit_text_position_x': [0.6,0.6],
        # 'fit_text_position_y': [0.9,0.85],
        'fit_text_size': '12',
        # 'y_subplot_lims': [0.0, 2.0],
        # 'subplot_fraction': 40,
        # 'mean_nicks': ['nick0', 'nick1'],
    })


def fit_function_mc_gauss(dictionary):
    """fits a distribution to the plot"""
    dictionary.update({
        'function_fit': ['nick0'],
        'function_nicknames': ['nick0_fit'],
        'functions': '[2]*TMath::Exp(-0.5*((x-[1])/[0])*((x-[1])/[0]))',
        # suits well for all tests
        # 'function_parameters': '0.5, 0, 1000',
        'function_parameters': '0.5, 1, 1000',
        'fit_text_npar': 1,
        'fit_text_parameter_names': ['sigma', 'mu', 'A'],
        # 'legend_cols': 1,
        'fit_text_nicks': ['nick0_fit'],
        'fit_text_colors': ['blue'],
        # 'fit_text_position_x': 0.6,
        # 'fit_text_position_y': 0.9,
        'fit_text_size': '12',
        # 'y_subplot_lims': [0.0, 2.0],
        # 'subplot_fraction': 40,
        # 'mean_nicks': ['nick0'],
    })


def fit_function_mc_doublegauss(dictionary):
    """fits a distribution to the plot"""
    dictionary.update({
        'function_fit': ['nick0'],
        'function_nicknames': ['nick0_fit'],
        'functions': '[3]*TMath::Exp(-0.5*((x-[2])/[0])*((x-[2])/[0]))+[4]*TMath::Exp(-0.5*((x-[2])/[1])*((x-[2])/[1]))',
        # suits well for genjet1pt/zpt:
        'function_parameters': '0.5, 0.05, 1, 1000, 10000',
        # suits well for genzpt/zpt, genjet1pt/genzpt, jet1pt/genjet1pt:
        # 'function_parameters': '1., 0.05, 1, 100, 1000',
        'fit_text_npar': 2,
        'fit_text_parameter_names': ['sigma1', 'sigma2', 'mu', 'A1', 'A2'],
        # 'legend_cols': 1,
        'fit_text_nicks': ['nick0_fit'],
        'fit_text_colors': ['blue'],
        # 'fit_text_position_x': 0.6,
        # 'fit_text_position_y': 0.9,
        'fit_text_size': '12',
        # 'y_subplot_lims': [0.0, 2.0],
        # 'subplot_fraction': 40,
        # 'mean_nicks': ['nick0'],
    })


def fit_function_mc_crystalball(dictionary):
    """fits a distribution to the plot"""
    dictionary.update({
        'function_fit': ['nick0'],
        'function_nicknames': ['nick0_fit'],
        'functions': 'crystalball',
        'function_parameters': '1, 1, 1, 1, 1',
        'fit_text_npar': 5,
        'fit_text_parameter_names': ['A', 'alpha', 'n', 'sigma', 'mu'],
        # 'legend_cols': 1,
        'fit_text_nicks': ['nick0_fit'],
        'fit_text_colors': ['blue'],
        # 'fit_text_position_x': 0.6,
        # 'fit_text_position_y': 0.9,
        'fit_text_size': '12',
        # 'y_subplot_lims': [0.0, 2.0],
        # 'subplot_fraction': 40,
        # 'mean_nicks': ['nick0'],
    })


def fit_gauss(args=None, additional_dictionary=None, only_normalized=False, channel='m', quantity_list=[]):
    plots = []
    x_dict = generate_dict(channel_dict=channel)
    for quantity in quantity_list:
        d = {
            'x_expressions': [quantity],
            'cutlabel': True,
            'analysis_modules': ['FunctionPlot'],
            'plot_modules': ['PlotMplZJet', 'PlotFitText'],  # 'PlotMplZJet','PlotMplMean'],
            'filename': 'Z'+channel+channel+'_'+quantity.replace('/', '%')+'_fit',
            # 'legend': 'upper right',
            'legend': 'center left',
            'y_subplot_lims': [0.75, 1.25],
            'alphas': '0.5',
            'markers': ['_', '_', 'fill', 'fill'],
            'colors': ['black', 'blue', 'black'],
            'ratio_denominator_nicks': ['nick1'],
            'ratio_numerator_nicks': ['nick0'],
        }
        if quantity in x_dict:
            d['x_bins'] = [x_dict[quantity][0]]
            # d['legend'] = x_dict[quantity][1]
        if quantity in binningsZJet.BinningsDictZJet().binnings_dict:
            x_bins = binningsZJet.BinningsDictZJet().binnings_dict[quantity]
            x_lims = lims_from_binning(x_bins)
            d['x_bins'] = [x_bins]
            d['x_lims'] = x_lims
        elif quantity in x_dict:
            d['x_bins'] = [x_dict[quantity][0]]
            d['x_lims'] = lims_from_binning(x_dict[quantity][0])
        if additional_dictionary:
            d.update(additional_dictionary)
        if len(d['files']) == 2:
            fit_function_datamc_gauss(d)
            d['analysis_modules'] = d['analysis_modules']+['Ratio']
        elif len(d['files']) == 1:
            # fit_function_mc_gauss(d)
            fit_function_mc_doublegauss(d)
            # fit_function_mc_crystalball(d)
        if only_normalized:
            # shape comparison
            d['analysis_modules'] = d['analysis_modules']+['NormalizeToFirstHisto']
            d['filename'] = 'Z'+channel+channel+'_'+quantity.replace('/', '%')+'_shapeComparison'
        plots.append(d)

    return [PlottingJob(plots=plots, args=args)]


def jer_comparison_datamc_zll(args=None):
    zjetfolder = 'finalcuts'
    channels = ['e', 'm']
    plotting_jobs = []

    # Preparing Data and MC plots
    for channel in channels:
        d = {
            # default format of labels ['DATA', 'MC', 'Ratio', 'DATA_fit', 'MC_fit']:
            'labels': ['Data', 'MC', 'Ratio', '', ''],
            'corrections': ['L1L2L3Res', 'L1L2L3'],
            # 'www': zjetfolder+'_jer_comparison_datamc_Zee',
            # 'www_title': 'JER data-mc comparisons for Zee'+zjetfolder,
            # 'www_text':'JER data-mc comparisons for Zee'+zjetfolder,
            'zjetfolders': [zjetfolder],
            'formats': ['png'],
            # 'formats': ['pdf'],
            # 'weights': ['1', '32.5'],
            'lumis': [27],
            'ratio_denominator_no_errors': False,
            'markers': ['_', '_'],
            'colors': ['black', 'blue', 'black', 'blue', 'black'],
        }
        if channel == 'm':
            d['title'] = r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{\\mu \\mu}$",
            d['files'] = ['/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/data17_mm_BCDEF_17Nov2017.root',
                          '/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/mc17_mm_DYNJ_Madgraph.root']
        elif channel == 'e':
            d['title'] = r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{e e}$",
            d['files'] = ['/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/data17_ee_BCDEF_17Nov2017.root',
                          '/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/mc17_ee_DYNJ_Madgraph.root']
        text_size = 15
        text_factor = 0.022
        d.update({
            'texts': [d['corrections']],
            'texts_y': [0.85],
            'texts_x': [0.92 - (len(d['corrections'][0])*text_factor)],
            'texts_size': [text_size],
        })

        # Plotting all variables for first checks (Data and MC):
        if False:
            quantity_list0 = ['zpt', 'zeta', 'zphi', 'zy', 'met', 'npv', 'jet1pt', 'jet1eta', 'jet2pt', 'jet2eta',
                              'ptbalance', 'mpf', 'zmass']
            quantity_list_ee = ['epluseta', 'eminuseta', 'eminuspt', 'epluspt', 'eminusphi', 'eplusphi']
            quantity_list_mm = ['mupluseta', 'muminuseta', 'muminuspt', 'mupluspt', 'muminusphi', 'muplusphi']
            if channel == 'm':
                quantity_list0.extend(quantity_list_mm)
            elif channel == 'e':
                quantity_list0.extend(quantity_list_ee)
            # quantity_list0 = ['ptbalance', 'mpf']

            plotting_jobs += general_comparison(args, d, channel=channel, only_normalized=False,
                                                quantity_list=quantity_list0)

        # Plotting specific variables and fit Gaussian functions (Data and MC):
        if False:
            quantity_list1 = ['ptbalance', 'mpf']
            plotting_jobs += fit_gauss(args, d, channel=channel, only_normalized=False, quantity_list=quantity_list1)

        d.update({
            'texts_y': [0.975],
            'texts_size': [text_size],
        })

        # Plotting profile plots of various variables (Data and MC):
        if False:
            plotting_jobs += fit_profplot_datamc(args, d, only_normalized=False, channel=channel)

        # Preparing MC plots
        d.update({
            'files': [d['files'][1]],
            'corrections': ['L1L2L3'],
            'labels': ['MC', ''],
            'colors': ['blue', 'blue', 'black'],
            'weights': ['( sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5 )'],
        })

        # Applying cuts on MC jet kinematics:
        if False:
            if channel == 'm':
                d['weights'] = ['( sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5 ) * ( abs(mu1eta)<1.3 ) * \
                               ( abs(mu2eta)<1.3 )']
            elif channel == 'e':
                d['weights'] = ['( sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5 ) * ( abs(e1eta)<1.3 ) * \
                               ( abs(e2eta)<1.3 )']

        # Preparing
        d.update({
            # 'texts': [r'$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{e e}$'],
            'texts': [d['corrections']],
            'texts_y': [0.82],
            # 'texts_x': [0.92 - (len(d['corrections'][0])*text_factor)],
            'texts_size': [text_size],
        })

        # Plotting various resolutions and fit Gaussian function:
        if True:
            quantity_list2 = ['ptbalance', 'jet1pt/genjet1pt', 'genjet1pt/genzpt', 'genzpt/zpt']
            plotting_jobs += fit_gauss(args, d, channel=channel, only_normalized=False, quantity_list=quantity_list2)

    return plotting_jobs
