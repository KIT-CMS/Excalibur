#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, lims_from_binning
import Excalibur.Plotting.utility.binningsZJet as binningsZJet


def general_comparison(args=None, additional_dictionary=None, only_normalized=False, channel='m', quantity_list=[]):
    """Comparison of: various quantities, both absolute and normalized"""
    plots = []
    # x_dict = generate_dict(channel_dict=channel)

    for quantity in quantity_list:
        # normal comparison
        d = {
            'x_expressions': [quantity],
            'cutlabel': True,
            'y_subplot_lims': [0.75, 1.25],
            'y_log': quantity in ['zpt'],
            'x_log': quantity in ['zpt'],
            'plot_modules': ['PlotMplZJet'],
            'filename': 'Z' + channel + channel + '_' + quantity.replace('/', '%'),
        }

        if additional_dictionary:
            d.update(additional_dictionary)

        if len(d['files']) > 1:
            d['analysis_modules'] = ['Ratio']

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
        # elif quantity in x_dict:
        #     d['x_bins'] = [x_dict[quantity][0]]
        #     d['x_lims'] = lims_from_binning(x_dict[quantity][0])

        if quantity in ['zeta', 'mupluseta', 'muminuseta', 'epluseta', 'eminuseta']:
            d['plot_modules'] = d['plot_modules'] + ['PlotMplRectangle']
            if channel == 'm':
                d['rectangle_x'] = [-6, -1.3, 1.3, 6]
            elif channel == 'e':
                d['rectangle_x'] = [-6, -1.479, 1.479, 6]
            d['rectangle_alpha'] = [0.2]
            d['rectangle_color'] = ['red']

        # if quantity in ['genjet1pt', 'genzpt', 'genzmass']:
        #     d['files'] = [d['files'][1]]
        if only_normalized:
            # shape comparison
            d.update({
                'analysis_modules': d['analysis_modules'] + ['NormalizeToFirstHisto'],
                'filename': 'Z' + channel + channel + '_' + quantity.replace('/', '%') + '_shapeComparison',
            })
        plots.append(d)

    return [PlottingJob(plots=plots, args=args)]


def general_comparison_genreco(args=None, additional_dictionary=None, only_normalized=False, channel='m',
                               quantity_list=[]):
    """Comparison of: various quantities, both absolute and normalized"""
    plots = []
    # x_dict = generate_dict(channel_dict=channel)

    for quantity in quantity_list:
        # normal comparison
        d = {
            'x_expressions': [quantity, 'gen'+quantity],
            'cutlabel': True,
            'y_subplot_lims': [0.75, 1.25],
            'y_log': quantity in ['zpt', 'genzpt'],
            'x_log': quantity in ['zpt', 'genzpt'],
            'plot_modules': ['PlotMplZJet'],
            'filename': 'Z' + channel + channel + '_' + quantity.replace('/', '%') + '_genreco',
        }

        if additional_dictionary:
            d.update(additional_dictionary)

        d['analysis_modules'] = ['Ratio']

        if quantity == 'alpha' and (additional_dictionary is None or 'zjetfolders' not in additional_dictionary):
            d['zjetfolders'] = ['nocuts']

        if quantity == 'zpt':
            d['zjetfolders'] = ['nocuts']

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
        # elif quantity in x_dict:
        #     d['x_bins'] = [x_dict[quantity][0]]
        #     d['x_lims'] = lims_from_binning(x_dict[quantity][0])

        if quantity in ['zeta', 'mupluseta', 'muminuseta', 'epluseta', 'eminuseta']:
            d['plot_modules'] = d['plot_modules'] + ['PlotMplRectangle']
            if channel == 'm':
                d['rectangle_x'] = [-6, -1.3, 1.3, 6]
            elif channel == 'e':
                d['rectangle_x'] = [-6, -1.479, 1.479, 6]
            d['rectangle_alpha'] = [0.2]
            d['rectangle_color'] = ['red']

        # if quantity in ['genjet1pt', 'genzpt', 'genzmass']:
        #     d['files'] = [d['files'][1]]
        if only_normalized:
            # shape comparison
            d.update({
                'analysis_modules': d['analysis_modules'] + ['NormalizeToFirstHisto'],
                'filename': 'Z' + channel + channel + '_' + quantity.replace('/', '%') + '_shapeComparison',
            })
        plots.append(d)

    return [PlottingJob(plots=plots, args=args)]