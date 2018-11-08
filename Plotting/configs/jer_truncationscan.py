#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, lims_from_binning
import Excalibur.Plotting.utility.binningsZJet as binningsZJet


def jer_extraction(args=None, additional_dictionary=None, channel='m', truncation=98.5, dict={}, plot_type='', plots=[]):
    """Profile Plot of RMS quantity in bins of alpha"""
    # x_dict = generate_dict(channel_dict=channel)

    cut_quantity = 'alpha'  # x_quantity on the plot
    # cut_binnings=['0.025 0.05 0.075 0.1 0.125 0.15 0.175 0.2 0.225 0.25 0.275 0.3'] # x_bins in plot
    cut_binning = [0., 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]  # x_bins in plot

    if plot_type == 'Data':
        rms_quantities = ['ptbalance', 'genjet1pt/genzpt', 'genzpt/zpt', 'jet1pt/genjet1pt']
        rms_quantities_labels = ['PTBal(Data)', 'PLI(MC)', 'ZRes(MC)', 'JER(MC-generated)']
        rms_quantities_colors = ['black', 'blue', 'green', 'red']
        minuend_quantity = 'PTBal(Data)'
        subtrahend_quantities = 'PLI(MC) ZRes(MC)'
        result_quantity = 'JER(Data-extracted)'
    elif plot_type == 'MC':
        rms_quantities = ['jet1pt/zpt', 'genjet1pt/genzpt', 'genzpt/zpt', 'jet1pt/genjet1pt']
        rms_quantities_labels = ['PTBal(MC)', 'PLI(MC)', 'ZRes(MC)', 'JER(MC-generated)']
        rms_quantities_colors = ['orange', 'blue', 'green', 'red']
        minuend_quantity = 'PTBal(MC)'
        subtrahend_quantities = 'PLI(MC) ZRes(MC)'
        result_quantity = 'JER(MC-extracted)'
    else:
        rms_quantities = []
        rms_quantities_labels = []
        rms_quantities_colors = []
        minuend_quantity = ''
        subtrahend_quantities = ''
        result_quantity = ''

    d = dict

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
    })

    # Saving nicks for quadratic subtraction
    minuend_nick = []
    subtrahend_nicks = []
    result_nick = []

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
                d['x_bins'] = d['x_bins'] + ['40,0.,2.']

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
                'histogram_from_rms_x_values': d['histogram_from_rms_x_values'] + [' '.join(map(str, cut_binning))],
                'histogram_from_rms_truncations': d['histogram_from_rms_truncations'] + [truncation],
                'nicks_whitelist': d['nicks_whitelist'] + [rms_nick_string],
                # 'nicks': d['nicks'] + [rms_nick_string],
                'y_label': 'resolution',
                'y_lims': [0.0, 0.3],
                'colors': d['colors'] + [rms_quantities_colors[index2]],
                'alphas': d['alphas'] + [1.0],
                'labels': d['labels'] + [rms_quantities_labels[index2]],
                'line_styles': d['line_styles'] + [''],
            })
    # Getting JER from quadratic subtraction
    if True:
        if 'HistogramFromQuadraticSubtraction' not in d['analysis_modules']:
            d['analysis_modules'] = d['analysis_modules'] + ['HistogramFromQuadraticSubtraction']
        d.update({
            'histogram_from_quadratic_subtraction_minuend_nicks': [minuend_nick],
            'histogram_from_quadratic_subtraction_subtrahend_nicks': [' '.join(subtrahend_nicks)],
            'histogram_from_quadratic_subtraction_result_nicks': [result_nick],
            'nicks_whitelist': d['nicks_whitelist'] + [result_nick],
            # 'nicks_whitelist': [result_nick],
            # 'nicks': d['nicks'] + [result_nick],
            'colors': d['colors'] + ['grey'],
            'alphas': d['alphas'] + [1.0],
            'labels': d['labels'] + [result_quantity],
            'line_styles': d['line_styles'] + [''],
        })
    # extrapolate to alpha equal zero by fitting a function
    if True:
        nick_whitelist = d['nicks_whitelist']
        nick_colors = d['colors']
        nick_labels = d['labels']
        nick_linestyles = d['line_styles']
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
                'functions': d['functions'] + ['[0]*x*x*x+[1]*x*x+[2]*x+[3]'],
                'function_parameters': d['function_parameters'] + ['1., 1., 1., 1.'],
                'function_ranges': d['function_ranges'] + ['0.001, 0.3'],
                'nicks_whitelist': d['nicks_whitelist'] + [fit_nick_white],
                'alphas': d['alphas'] + [1.0, 0.4],
                'colors': d['colors'] + [nick_colors[index], nick_colors[index]],
                'labels': d['labels'] + [nick_labels[index], ''],
                'line_styles': d['line_styles'] + [nick_linestyles[index], '--'],
            })
        plots.append(d)
    return [PlottingJob(plots=plots, args=args)]

def jer_extrapolation_truncation_scan(args=None, additional_dictionary=None, channel='m'):
    truncations_list = [85., 93., 95., 97., 98.5]
    plots_list = ['MC', 'Data']
    plots = []


    for plot_type in plots_list:
        d = {
            'analysis_modules': [],
            'plot_modules': ['PlotMplZJet'],
            'legend': 'upper left',
            'filename': 'Z' + channel + channel + '_JER_alpha_extrapolation' + '_' + plot_type,
        }
        if additional_dictionary:
            d.update(additional_dictionary)
        for truncation in truncations_list:
            if channel == 'm':
                jer_extraction(args, d, channel=channel, truncation=truncation, dict=d, plot_type=plot_type, plots=plots)
            elif channel == 'e':
                jer_extraction(args, d, channel=channel, truncation=truncation, dict=d, plot_type=plot_type, plots=plots)
            else:
                pass
        print d

    return [PlottingJob(plots=plots, args=args)]


def jer_extrapolation(args=None, additional_dictionary=None, channel='m'):
    # TODO: adjust trunctation values to optimal working point (gamma channel: 98.5%)
    plots_list = ['MC', 'Data']
    plots = []

    if channel == 'm':
        truncation=85.0
    elif channel == 'e':
        truncation=85.0
    else:
        truncation = 100.

    for plot_type in plots_list:
        d = {
            'analysis_modules': [],
            'plot_modules': ['PlotMplZJet'],
            'legend': 'upper left',
            'filename': 'Z' + channel + channel + '_JER_alpha_extrapolation' + '_' + plot_type,
        }
        if additional_dictionary:
            d.update(additional_dictionary)

        if 'texts' in d.keys():
            d.update({
                'texts': d['texts'] + ['truncation: ' + str(truncation)],
                'texts_y': d['texts_y'] + [0.95],
                'texts_x': d['texts_x'] + [0.7 ],
                'texts_size': d['texts_size'] + [13],
            })
        else:
            d.update({
                'texts': ['truncation: ' + str(truncation) + '%'],
                'texts_y': [0.95],
                'texts_x': [0.7],
                'texts_size': [13],
            })

        if additional_dictionary:
            d.update(additional_dictionary)

        jer_extraction(args, d, channel=channel, truncation=truncation, dict=d, plot_type=plot_type, plots=plots)

    return [PlottingJob(plots=plots, args=args)]