#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Excalibur.Plotting.utility.colors as colors
from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, lims_from_binning
import Excalibur.Plotting.utility.binningsZJet as binningsZJet

import argparse
import copy
import jec_factors
import jec_files
import matplotlib as mp


def generate_dict(args=None, additional_dictionary=None, channel_dict="m"):
    # TODO move this to more general location
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
        'ptbalance': ['100,0,2'],
        'rawmet': ['40,0,100'],
        'zmass': ['40,71,111'],
        'zphi': ['20,-3.1415,3.1415'],
        'zpt': ['40,0,400'],
        'zy': ['25,-2.5,2.5'],
        'genzmass': ['40,71,111'],
        # 'genzpt/zpt': ['40,-30,0'],
        'genzpt/zpt': ['100,0.85,1.15'],
        'genjet1pt/jet1pt': ['100,0.,2.'],
        'jet1pt/genjet1pt': ['100,0.,2.'],
        'genjet1pt/genzpt': ['100,0.,2.'],
        'genjet1pt/zpt': ['100,0.,2.'],
        'jet1pt/zpt': ['100,0.,2.'],
        'jet1pt/zpt-genjet1pt/zpt': ['100,-1,1'],
        'generatorWeight': ['100,-2,2'],
        'puWeight': ['100,0,10'],
        'hlt': ['100,-0.5,1.5'],
        'weight': ['100,-1,1'],
    }
    x_dict_ee = {
        'e1phi': ['20,-3.1415,3.1415'],
        'e1pt': ['20,0,150'],
        'e2pt': ['20,0,150'],
        'eminuspt': ['20,0,150'],
        'epluspt': ['20,0,150'],
    }
    x_dict_mm = {
        'mu1phi': ['20,-3.1415,3.1415'],
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


def profplot_datamc(args=None, additional_dictionary=None, channel='m'):
    """Profile Plot of RMS quantity in bins of alpha"""
    plots = []
    x_dict = generate_dict(channel_dict=channel)

    cut_quantity = 'alpha'  # x_quantity on the plot
    x_range = [0.0, 2.0]  # range of resolutions
    # cut_binnings=['0.025 0.05 0.075 0.1 0.125 0.15 0.175 0.2 0.225 0.25 0.275 0.3'] # x_bins in plot
    cut_binning = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]  # x_bins in plot

    # plots_list = ['all', 'JER', 'PLI', 'ZRes', 'PTBal']
    plots_list = ['PLI', 'JER', 'ZRes', 'PTBal']
    rms_quantities = []
    rms_quantities_labels = []
    rms_quantities_colors = []

    for plot_type in plots_list:
        if plot_type == 'JER':
            rms_quantities = ['jet1pt/genjet1pt']
            rms_quantities_labels = ['JER(MC)']
            rms_quantities_colors = ['red']
            x_range = [0.0, 2.0]
        elif plot_type == 'PLI':
            rms_quantities = ['genjet1pt/genzpt']
            rms_quantities_labels = ['PLI(MC)']
            rms_quantities_colors = ['blue']
            x_range = [0.0, 2.0]
        elif plot_type == 'ZRes':
            rms_quantities = ['genzpt/zpt']
            rms_quantities_labels = ['ZRes(MC)']
            rms_quantities_colors = ['green']
            x_range = [0.85, 1.15]
        elif plot_type == 'PTBal':
            rms_quantities = ['ptbalance', 'jet1pt/zpt']
            rms_quantities_labels = ['PTB(Data)', 'PTB(MC)']
            rms_quantities_colors = ['black', 'yellow']
            x_range = [0.0, 2.0]

        d = {
            'analysis_modules': [],
            'legend': 'upper left',
            'filename': 'Z' + channel + channel + '_JER_RMS_cross_check_' + plot_type,
        }

        if additional_dictionary:
            d.update(additional_dictionary)

        # saving old entries for new order usage
        old_files = d['files']  # contains ['MC_file', 'Data_file']
        old_corrections = d['corrections']  # analogous to files
        old_weights = d['weights']

        # deleting old entries for new order
        d.update({
            'files': [],
            'nicks': [],
            'corrections': [],
            'x_expressions': [],
            'x_label': [],
            # 'nicks_whitelist': [],
            'colors': [],
            # 'alphas': [],
            'labels': [],
            'markers': ['d', 'v', 'o', '^', '<', '>', '*', '8', 's', 'p', 'h', 'D'],
            'weights': [],
            'line_styles': ['--'],
            'line_widths': ['1.'],
            'lines': [1.],
            'x_lims': x_range,
            'texts_size': 6,
            'legend_cols': 2,
        })
        label_list = []

        for (index2, rms_quantity) in enumerate(rms_quantities):
            nick_list = []
            label_list += [str(rms_quantities_labels[index2])]
            for index in range(len(cut_binning)-1):
                nick = 'nick_' + str(rms_quantity) + '_' + str(index)
                weight = cut_quantity + '>' + str(cut_binning[index]) + '&&' + cut_quantity + '<' + str(
                    cut_binning[index + 1])
                d.update({
                    'x_expressions': d['x_expressions'] + [rms_quantity],  # y_expression in the plot
                    'nicks': d['nicks'] + [nick],
                    'labels': d['labels'] + [str(rms_quantities_labels[index2])
                                             # + r'$ \\mathit{\\rightarrow} \\mathrm{\\alpha}$'
                                             + '[' + str(cut_binning[index])
                                             + ',' + str(cut_binning[index + 1]) + ']'],
                    'colors': d['colors'] + [str(rms_quantities_colors[index2])],
                })
                if rms_quantity in x_dict:
                    d['x_bins'] = [x_dict[rms_quantity][0]]
                if rms_quantity not in ['ptbalance']:
                    d.update({
                        'files': d['files'] + [old_files[1]],
                        'corrections': d['corrections'] + [old_corrections[1]],
                        'weights': d['weights'] + [weight + '&&' + old_weights[1]],
                    })
                else:
                    d.update({
                        'files': d['files'] + [old_files[0]],
                        'corrections': d['corrections'] + [old_corrections[0]],
                        'weights': d['weights'] + [weight + '&&' + old_weights[0]],
                    })
                nick_list.append(nick)
        d['x_label'] = ','.join(label_list)
        plots.append(d)
    return [PlottingJob(plots=plots, args=args)]


def rms_profplot_datamc(args=None, additional_dictionary=None, channel='m'):
    """Profile Plot of RMS quantity in bins of alpha"""
    plots = []
    x_dict = generate_dict(channel_dict=channel)
    
    cut_quantity = 'alpha'  # x_quantity on the plot
    # cut_binnings=['0.025 0.05 0.075 0.1 0.125 0.15 0.175 0.2 0.225 0.25 0.275 0.3'] # x_bins in plot
    cut_binning = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]  # x_bins in plot

    plots_list = ['all', 'without_JER', 'JER', 'PLI', 'ZRes', 'PTBal']
    rms_quantities = []
    rms_quantities_labels = []
    rms_quantities_colors = []

    for plot_type in plots_list:
        if plot_type == 'JER':
            rms_quantities = ['jet1pt/genjet1pt']
            rms_quantities_labels = ['JER(MC)']
            rms_quantities_colors = ['red']
        elif plot_type == 'PLI':
            rms_quantities = ['genjet1pt/genzpt']
            rms_quantities_labels = ['PLI(MC)']
            rms_quantities_colors = ['blue']
        elif plot_type == 'ZRes':
            rms_quantities = ['genzpt/zpt']
            rms_quantities_labels = ['ZRes(MC)']
            rms_quantities_colors = ['green']
        elif plot_type == 'PTBal':
            rms_quantities = ['ptbalance', 'jet1pt/zpt']
            rms_quantities_labels = ['PTBal(Data)', 'PTBal(MC)']
            rms_quantities_colors = ['black', 'yellow']
        elif plot_type == 'without_JER':
            rms_quantities = ['genjet1pt/genzpt', 'genzpt/zpt', 'ptbalance', 'jet1pt/zpt']
            rms_quantities_labels = ['PLI(MC)', 'ZRes(MC)', 'PTBal(Data)', 'PTBal(MC)']
            rms_quantities_colors = ['blue', 'green', 'black', 'yellow']
        elif plot_type == 'all':
            rms_quantities = ['jet1pt/genjet1pt', 'genjet1pt/genzpt', 'genzpt/zpt', 'ptbalance', 'jet1pt/zpt']
            rms_quantities_labels = ['JER(MC)', 'PLI(MC)', 'ZRes(MC)', 'PTBal(Data)', 'PTBal(MC)']
            rms_quantities_colors = ['red', 'blue', 'green', 'black', 'yellow']

        d = {
            'analysis_modules': [],
            'legend': 'upper left',
            'filename': 'Z' + channel + channel + '_JER_alpha_extrapolation' + '_' + plot_type,
        }

        if additional_dictionary:
            d.update(additional_dictionary)

        # saving old entries for new order usage
        old_files = d['files']  # contains ['MC_file', 'Data_file']
        old_corrections = d['corrections']  # analogous to files
        old_weights = d['weights']

        # deleting old entries for new order
        d.update({
            'files': [],
            'nicks': [],
            'corrections': [],
            'x_expressions': [],
            'nicks_whitelist': [],
            'histogram_from_rms_nicks': [],
            'histogram_from_rms_newnicks': [],
            'histogram_from_rms_x_values': [],
            'histogram_from_rms_truncations': [],
            'colors': [],
            'alphas': [],
            'labels': [],
            'markers': ['d'],
            'weights': [],
            'function_fit': [],
            'function_nicknames': [],
            'functions': [],
            'function_parameters': [],
            'function_ranges': [],
            'line_styles': [],
            'x_bins': [],
        })

        for (index2, rms_quantity) in enumerate(rms_quantities):
            nick_list = []
            for index in range(len(cut_binning)-1):
                nick = 'nick_' + str(rms_quantity) + '_' + str(index)
                weight = cut_quantity + '>' + str(cut_binning[index]) + '&&' + cut_quantity + '<' + str(
                    cut_binning[index + 1])
                d.update({
                    'x_expressions': d['x_expressions'] + [rms_quantity],  # y_expression in the plot
                    'nicks': d['nicks'] + [nick],
                    # 'labels': d['labels'] + [nick],
                    # 'colors': d['colors'] + [str(rms_quantities_colors[index2])],
                })

                # update x range from predefined values:
                if rms_quantity in x_dict:
                    d['x_bins'] = d['x_bins'] + [x_dict[rms_quantity][0]]
                else:
                    d['x_bins'] = d['x_bins'] + ['40,0.,2.'],

                # update values for Data and MC entries separatelly:
                if rms_quantity not in ['ptbalance']:
                    d.update({
                        'files': d['files'] + [old_files[1]],
                        'corrections': d['corrections'] + [old_corrections[1]],
                        'weights': d['weights'] + [weight + '&&' + old_weights[1]],
                    })
                else:
                    d.update({
                        'files': d['files'] + [old_files[0]],
                        'corrections': d['corrections'] + [old_corrections[0]],
                        'weights': d['weights'] + [weight + '&&' + old_weights[0]],
                    })
                nick_list.append(nick)

            # Format plot:
            d.update({
                'x_label': cut_quantity,
                'lines': [1.],
                # 'line_styles': ['--'],
                'line_widths': ['1.'],
            })

            # Prepare new nicks for RMS and fit
            nick_string = ' '.join(nick_list)
            rms_nick_string = 'nick_' + str(rms_quantity) + '_rms'
            fit_nick_string = 'nick_' + str(rms_quantity) + '_fit'

            # Get RMS value of each alpha bin for all variables and write them in new nicks
            if True:
                if 'HistogramFromRMSValues' not in d['analysis_modules']:
                    d['analysis_modules'] = d['analysis_modules'] + ['HistogramFromRMSValues']
                d.update({
                    'histogram_from_rms_nicks': d['histogram_from_rms_nicks'] + [nick_string],
                    'histogram_from_rms_newnicks': d['histogram_from_rms_newnicks'] + [rms_nick_string],
                    'histogram_from_rms_x_values': d['histogram_from_rms_x_values'] + [' '.join(map(str, cut_binning))],
                    'histogram_from_rms_truncations': d['histogram_from_rms_truncations'] + [98.5],
                    'nicks_whitelist': d['nicks_whitelist'] + [rms_nick_string],
                    'y_label': 'resolution',
                    'y_lims': [0.0, 0.3],
                    'colors': d['colors'] + [rms_quantities_colors[index2]],
                    'alphas': d['alphas'] + [1.0],
                    'labels': d['labels'] + [rms_quantities_labels[index2]],
                    'line_styles': d['line_styles'] + [''],
                })
            # extrapolate to alpha equal zero
            if True:
                if 'FunctionPlot' not in d['analysis_modules']:
                    d['analysis_modules'] = d['analysis_modules'] + ['FunctionPlot']
                d.update({
                    'function_fit': d['function_fit'] + [rms_nick_string],
                    'function_nicknames': d['function_nicknames'] + [fit_nick_string],
                    'functions': d['functions'] + ['[0]*x*x*x+[1]*x*x+[2]*x+[3]'],
                    'function_parameters': d['function_parameters'] + ['1., 1., 1., 1.'],
                    'function_ranges': d['function_ranges'] + ['0.0, 0.3'],
                    'nicks_whitelist': d['nicks_whitelist'] + [fit_nick_string],
                    'colors': d['colors'] + [rms_quantities_colors[index2]],
                    'alphas': d['alphas'] + [0.4],
                    'labels': d['labels'] + [''],
                    'line_styles': d['line_styles'] + ['--'],
                })

        if len(filter(None, d['labels'])) == 1:
            d['labels'] = filter(None, d['labels']) + ['fit']
        plots.append(d)
    return [PlottingJob(plots=plots, args=args)]


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
            'lumis': [27],
            'ratio_denominator_no_errors': False,
            'markers': ['_', '_'],
            'colors': ['black', 'blue', 'black', 'blue', 'black'],
            'weights': ['1', '( sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5 )'],
            # 'weights': ['1', '1']

        }
        if channel == 'm':
            d['title'] = r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{\\mu \\mu}$"
            d['files'] = ['/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/data17_mm_BCDEF_17Nov2017.root',
                          '/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/mc17_mm_DYNJ_Madgraph.root']
        elif channel == 'e':
            d['title'] = r"$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{e e}$"
            d['files'] = ['/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/data17_ee_BCDEF_17Nov2017.root',
                          '/storage/c/dsavoiu/excalibur_results_calibration/Fall17/17Nov2017_V10_2018-06-13/mc17_ee_DYNJ_Madgraph.root']

        plotting_jobs += rms_profplot_datamc(args, d, channel=channel)
        plotting_jobs += profplot_datamc(args, d, channel=channel)

        text_size = 15
        text_factor = 0.022
        d.update({
            'texts': [d['corrections']],
            'texts_y': [0.85],
            'texts_x': [0.92 - (len(d['corrections'][0])*text_factor)],
            'texts_size': [text_size],
        })

        # quantity_list0 = ['zpt','zeta','zphi','zy','metphi','met','npv','jet1pt','jet1eta','jet2pt','jet2eta',
        #                   'ptbalance', 'mpf', 'zmass']
        # quantity_list_ee = ['epluseta','eminuseta','eminuspt','epluspt','eminusphi','eplusphi']
        # quantity_list_mm = ['mupluseta','muminuseta','muminuspt','mupluspt','muminusphi','muplusphi']
        # if channel == 'm': quantity_list0.extend(quantity_list_mm)
        # elif channel == 'e': quantity_list0.extend(quantity_list_ee)
        # quantity_list0 = ['ptbalance', 'mpf']

        # plotting_jobs += general_comparison(args, d, channel=channel, only_normalized=False,
        #                                     quantity_list=quantity_list0)
        # quantity_list1=['ptbalance','mpf'] #, 'jet1pt/zpt']
        # plotting_jobs += fit_gauss(args, d, channel=channel, only_normalized=False, quantity_list=quantity_list1)

        d.update({
            'texts_y': [0.975],
            'texts_size': [text_size],
        })

        # MC plots
        d.update({
            'files': [d['files'][1]],
            'corrections': ['L1L2L3'],
            'labels': ['MC', ''],
            'colors': ['blue', 'blue', 'black'],
            'weights': ['( sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5 )'],
        })

        # if channel == 'm':
        #     d['weights'] = ['( sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5 ) * ( abs(mu1eta)<1.3 ) * '
        #                     '( abs(mu2eta)<1.3 )']
        # elif channel == 'e':
        #     d['weights'] = ['( sqrt((jet1eta-genjet1eta)**2+(jet1phi-genjet1phi)**2)<0.5 ) * ( abs(e1eta)<1.3 ) * '
        #                     '( abs(e2eta)<1.3 )']

        d.update({
          # 'texts': [r'$\\mathrm{Z} \\mathit{\\rightarrow} \\mathrm{e e}$'],
          'texts': [d['corrections']],
          'texts_y': [0.82],
          # 'texts_x': [0.92 - (len(d['corrections'][0])*text_factor)],
          'texts_size': [text_size],
        })

        # quantity_list2=['genjet1pt/genzpt', 'genjet1pt/jet1pt', 'genzpt/zpt', 'genzpt', 'jet1pt/genjet1pt']
        # quantity_list2=['genjet1pt/jet1pt', 'genzpt/zpt', 'jet1pt/genjet1pt']
        # quantity_list2=['genzpt/zpt']
        # quantity_list2=['genjet1pt/genzpt']
        # quantity_list2=['genjet1pt/zpt']
        # quantity_list2=['jet1pt/zpt-genjet1pt/zpt']
        # plotting_jobs += fit_gauss(args, d, channel=channel, only_normalized=False, quantity_list=quantity_list2)

    return plotting_jobs
