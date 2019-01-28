#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, lims_from_binning
import Excalibur.Plotting.utility.binningsZJet as binningsZJet


def jer_extrapolation(args=None, additional_dictionary=None, channel='m'):
    """Profile Plot of RMS quantity in bins of alpha"""
    cut_binning = []  # x_bins in plot
    cut_range = []
    plots = []
    ratio_plot = True

    cut_quantities = ['alpha', 'zeta', 'zpt']  # Quantities used as x-axis

    whitelist_quantities = []  # for whitelisting all quantities per default
    y_lims = [0.0, 1.0]  # for setting range of y axis per default

    for cut_quantity in cut_quantities:  # x_quantity on the plot

        if cut_quantity == 'alpha':
            # cut_binnings=['0.025 0.05 0.075 0.1 0.125 0.15 0.175 0.2 0.225 0.25 0.275 0.3']
            cut_binning = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
            cut_range = ['0.0, 0.3']
        elif cut_quantity == 'zeta':
            cut_binning = [-5.191, -3.139, -2.964, -2.5, -1.93, -1.305, -0.783, 0., 0.783, 1.305, 1.93, 2.5, 2.964,
                           3.139, 5.191]
            cut_range = ['-5.191, 5.191']
        elif cut_quantity == 'zpt':
            # cut_binning = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 130, 150, 170, 190, 220,
            #                250, 400, 1000]
            cut_binning = [30, 50, 75, 125, 175, 225, 300, 400, 1000]
            cut_range = ['30, 1000']

        # TODO: adjust truncation values to optimal working point (gamma channel: 98.5%)
        # plots_list = ['MC', 'Data']
        plots_list = ['MC-ZRes-study']

        if channel == 'm':
            truncation = 98.5
        elif channel == 'e':
            truncation = 94.
        else:
            truncation = 100.

        for plot_type in plots_list:
            d = {
                'analysis_modules': [],
                'plot_modules': ['PlotMplZJet'],
                'legend': 'upper left',
                'filename': 'Z' + channel + channel + '_JER_' + cut_quantity + '_extrapolation' + '_' + plot_type,
                'x_log': cut_quantity in ['zpt']
            }
            if additional_dictionary:
                d.update(additional_dictionary)

            if 'texts' in d.keys():
                d.update({
                    'texts': d['texts'] + ['truncation to ' + str(truncation)],
                    'texts_y': d['texts_y'] + [0.95],
                    'texts_x': d['texts_x'] + [0.65],
                    'texts_size': d['texts_size'] + [13],
                })
            else:
                d.update({
                    'texts': ['truncation to ' + str(truncation) + '%'],
                    'texts_y': [0.95],
                    'texts_x': [0.65],
                    'texts_size': [13],
                })

            if plot_type == 'Data':
                whitelist_quantities = ['jet1pt/genjet1pt']  # JER extracted is automatically added to whitelist
                rms_quantities = ['ptbalance', 'genjet1pt/genzpt', 'genzpt/zpt', 'jet1pt/genjet1pt']
                rms_quantities_labels = ['PTBal(Data)', 'PLI(MC)', 'ZRes(MC)', 'JER(MC-generated)']
                rms_quantities_colors = ['grey', 'springgreen', 'forestgreen', 'orange', 'blue', 'blue']
                minuend_quantity = 'PTBal(Data)'
                subtrahend_quantities = 'PLI(MC) ZRes(MC)'
                result_quantity = 'JER(Data-extracted)'
                y_lims = [0.0, 0.4]
            elif plot_type == 'MC':
                whitelist_quantities = ['jet1pt/genjet1pt']  # JER extracted is automatically added to whitelist
                rms_quantities = ['jet1pt/zpt', 'genjet1pt/genzpt', 'genzpt/zpt', 'jet1pt/genjet1pt']
                rms_quantities_labels = ['PTBal(MC)', 'PLI(MC)', 'ZRes(MC)', 'JER(MC-generated)']
                rms_quantities_colors = ['royalblue', 'springgreen', 'forestgreen', 'orange']
                minuend_quantity = 'PTBal(MC)'
                subtrahend_quantities = 'PLI(MC) ZRes(MC)'
                result_quantity = 'JER(MC-extracted)'
                y_lims = [0.0, 0.4]
            elif plot_type == 'MC-ZRes-study':
                whitelist_quantities = []  # all quantities are automatically added to whitelist
                rms_quantities = ['genzpt/zpt', 'genepluspt/epluspt', 'genmupluspt/mupluspt']
                rms_quantities_labels = ['ZRes(MC)', 'eRes(MC)', 'muRes(MC)']
                rms_quantities_colors = ['forestgreen', 'blue', 'blue']
                minuend_quantity = ''
                subtrahend_quantities = ''
                result_quantity = ''
                y_lims = [0.0, 0.05]
            else:
                rms_quantities = []
                rms_quantities_labels = []
                rms_quantities_colors = []
                minuend_quantity = ''
                subtrahend_quantities = ''
                result_quantity = ''

            if whitelist_quantities == []:
                whitelist_quantities = rms_quantities

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
                'markers': ['+'],
                'weights': [],
                'function_fit': [],
                'function_nicknames': [],
                'functions': [],
                'function_parameters': [],
                'function_ranges': [],
                'line_styles': [],
                'x_bins': [],
                # 'x_lims': [],
                'ratio_numerator_nicks': [],
                'ratio_denominator_nicks': [],
                'ratio_result_nicks': [],
                # 'ratio_denominator_no_errors': False,
            })

            # Saving nicks for quadratic subtraction
            minuend_nick = []
            subtrahend_nicks = []
            result_nick = []

            nick_colors = []
            nick_labels = []
            nick_linestyles = []

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
                    if rms_quantity in binningsZJet.BinningsDictZJet().binnings_dict:
                        x_bins = binningsZJet.BinningsDictZJet().binnings_dict[rms_quantity]
                        d['x_bins'] = d['x_bins'] + [x_bins]
                    else:
                        d['x_bins'] = d['x_bins'] + ['4000,0.,2.']

                    # update values for Data and MC entries separately:
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

                if rms_quantities_labels[index2] == minuend_quantity:
                    minuend_nick += [rms_nick_string]
                if rms_quantities_labels[index2] in subtrahend_quantities.split():
                    subtrahend_nicks += [rms_nick_string]
                result_nick = 'nick_' + str(result_quantity.replace('(', '').replace(')', '')) + '_subtracted'

                # Get RMS value of each alpha bin for all variables and write them in new nicks
                if True:
                    if 'HistogramFromRMSValues' not in d['analysis_modules']:
                        d['analysis_modules'] = d['analysis_modules'] + ['HistogramFromRMSValues']
                    d.update({
                        'histogram_from_rms_nicks': d['histogram_from_rms_nicks'] + [nick_string],
                        'histogram_from_rms_newnicks': d['histogram_from_rms_newnicks'] + [rms_nick_string],
                        'histogram_from_rms_x_values': d['histogram_from_rms_x_values'] + [' '.join(map(str,
                                                                                                        cut_binning))],
                        'histogram_from_rms_truncations': d['histogram_from_rms_truncations'] + [truncation],
                        # 'nicks': d['nicks'] + [rms_nick_string],
                        'y_label': 'resolution',
                        'y_lims': y_lims,
                    })
                    if rms_quantity in whitelist_quantities:
                        d.update({
                            'nicks_whitelist': d['nicks_whitelist'] + [rms_nick_string],
                            'colors': d['colors'] + [rms_quantities_colors[index2]],
                            'alphas': d['alphas'] + [1.0],
                            'labels': d['labels'] + [rms_quantities_labels[index2]],
                            'line_styles': d['line_styles'] + [''],
                        })
                        nick_colors += [rms_quantities_colors[index2]]
                        nick_labels += [rms_quantities_labels[index2]]
                        nick_linestyles += ['']
                        if ratio_plot:
                            d.update({
                                'ratio_numerator_nicks': d['ratio_numerator_nicks'] + [rms_nick_string],
                                # 'ratio_denominator_nicks': d['ratio_denominator_nicks'] + [rms_nick_string],
                                'ratio_result_nicks': d['ratio_result_nicks'] + [rms_nick_string + '_ratio'],
                                # 'nicks_whitelist': d['nicks_whitelist'] + [rms_nick_string + '_ratio'],
                                'colors': d['colors'] + [rms_quantities_colors[index2]],
                                'alphas': d['alphas'] + [1.0],
                                'labels': d['labels'] + [''],
                                'line_styles': d['line_styles'] + [''],
                            })

            # Getting JER from quadratic subtraction
            if minuend_quantity != '':
                if 'HistogramFromQuadraticSubtraction' not in d['analysis_modules']:
                    d['analysis_modules'] = d['analysis_modules'] + ['HistogramFromQuadraticSubtraction']
                d.update({
                    'histogram_from_quadratic_subtraction_minuend_nicks': [minuend_nick],
                    'histogram_from_quadratic_subtraction_subtrahend_nicks': [' '.join(subtrahend_nicks)],
                    'histogram_from_quadratic_subtraction_result_nicks': [result_nick],
                    'nicks_whitelist': d['nicks_whitelist'] + [result_nick],
                    # 'nicks': d['nicks'] + [result_nick],
                    'colors': d['colors'] + ['red'],
                    'alphas': d['alphas'] + [1.0],
                    'labels': d['labels'] + [result_quantity],
                    'line_styles': d['line_styles'] + [''],
                })
                nick_colors += ['red']
                nick_labels += [result_quantity]
                nick_linestyles += ['']
                if ratio_plot:
                    if 'Ratio' not in d['analysis_modules']:
                        d['analysis_modules'] = d['analysis_modules'] + ['Ratio']
                    d.update({
                        'ratio_denominator_nicks': d['ratio_denominator_nicks'] + [result_nick],
                        'y_subplot_lims': [0.75, 1.25],
                        'y_subplot_label': 'Ratio',
                        'subplot_fraction': 25,
                        'subplot_legend': 'upper right',
                    })
            # extrapolate to alpha equal zero by fitting a function
            if cut_quantity in ['alpha']:
                nick_whitelist = d['nicks_whitelist']
                # nick_colors = d['colors']
                # nick_labels = d['labels']
                # nick_linestyles = d['line_styles']
                d['alphas'] = []
                d['colors'] = []
                d['labels'] = []
                d['line_styles'] = []
                for index, nick_white in enumerate(nick_whitelist):
                    fit_nick_white = nick_white + '_fit'
                    if 'FunctionPlot' not in d['analysis_modules']:
                        d['analysis_modules'] = d['analysis_modules'] + ['FunctionPlot']
                    d.update({
                        'function_fit': d['function_fit'] + [nick_white],
                        'function_nicknames': d['function_nicknames'] + [fit_nick_white],
                        'functions': d['functions'] + ['[0]+[1]*x'],
                        'function_parameters': d['function_parameters'] + ['0., 0.'],
                        'function_ranges': d['function_ranges'] + cut_range,
                    })
                    if not ratio_plot or nick_white == result_nick:
                        d.update({
                            'alphas': d['alphas'] + [1.0, 0.4],
                            'colors': d['colors'] + [nick_colors[index], nick_colors[index]],
                            'labels': d['labels'] + [nick_labels[index], ''],
                            'line_styles': d['line_styles'] + [nick_linestyles[index], '--'],
                        })
                    else:
                        d.update({
                            'alphas': d['alphas'] + [1.0, 1.0, 0.4],
                            'colors': d['colors'] + [nick_colors[index], nick_colors[index], nick_colors[index]],
                            'labels': d['labels'] + [nick_labels[index], '', ''],
                            'line_styles': d['line_styles'] + [nick_linestyles[index], '', '--'],
                        })

            plots.append(d)

    return [PlottingJob(plots=plots, args=args)]
