#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, lims_from_binning
import Excalibur.Plotting.utility.binningsZJet as binningsZJet


def rms_profplot_datamc(args=None, additional_dictionary=None, channel='m'):
    """Profile Plot of RMS quantity in bins of alpha"""
    plots = []

    cut_quantity = 'alpha'  # x_quantity on the plot
    x_range = [0.0, 2.0]  # range of resolutions
    # cut_binnings=['0.025 0.05 0.075 0.1 0.125 0.15 0.175 0.2 0.225 0.25 0.275 0.3'] # x_bins in plot
    # cut_binning = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]  # x_bins in plot
    cut_binning = [0.0, 0.05, 0.1]

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
            # x_range = [0.0, 2.0]
            x_range = [0.6, 1.4]
        elif plot_type == 'ZRes':
            rms_quantities = ['genzpt/zpt']
            rms_quantities_labels = ['ZRes(MC)']
            rms_quantities_colors = ['green']
            x_range = [0.9, 1.1]
        elif plot_type == 'PTBal':
            rms_quantities = ['ptbalance', 'jet1pt/zpt']
            rms_quantities_labels = ['PTB(Data)', 'PTB(MC)']
            rms_quantities_colors = ['black', 'orange']
            x_range = [0.0, 2.0]

        d = {
            'analysis_modules': ['NormalizeToFirstHisto'],
            'plot_modules': ['PlotMplZJet'],
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
            'x_bins': [],
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

                # update x range from predefined values:
                if rms_quantity in binningsZJet.BinningsDictZJet().binnings_dict:
                    x_bins = binningsZJet.BinningsDictZJet().binnings_dict[rms_quantity]
                    d['x_bins'] = d['x_bins'] + [x_bins]
                else:
                    d['x_bins'] = d['x_bins'] + ['40,0.,2.']

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
