#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Excalibur.Plotting.utility.toolsZJet import PlottingJob, get_input_files, lims_from_binning
import Excalibur.Plotting.utility.binningsZJet as binningsZJet
import datetime


def fit_function_datamc_gauss(dictionary):
    """fits a distribution to the plot"""
    if 'FunctionPlot' not in dictionary['analysis_modules']:
        dictionary['analysis_modules'] = dictionary['analysis_modules'] + ['FunctionPlot']
    if 'PlotFitText' not in dictionary['plot_modules']:
        dictionary['plot_modules'] = dictionary['plot_modules'] + ['PlotFitText']
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
    if 'FunctionPlot' not in dictionary['analysis_modules']:
        dictionary['analysis_modules'] = dictionary['analysis_modules'] + ['FunctionPlot']
    if 'PlotFitText' not in dictionary['plot_modules']:
        dictionary['plot_modules'] = dictionary['plot_modules'] + ['PlotFitText']
    dictionary.update({
        'function_fit': ['nick0'],
        'function_nicknames': ['nick0_fit'],
        'functions': '[2]*TMath::Exp(-0.5*((x-[1])/[0])*((x-[1])/[0]))',
        # suits well for all tests
        # 'function_parameters': '0.5, 0, 1000',
        'function_parameters': '0.05, 1., 10000',
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
    if 'FunctionPlot' not in dictionary['analysis_modules']:
        dictionary['analysis_modules'] = dictionary['analysis_modules'] + ['FunctionPlot']
    if 'PlotFitText' not in dictionary['plot_modules']:
        dictionary['plot_modules'] = dictionary['plot_modules'] + ['PlotFitText']
    dictionary.update({
        'function_fit': ['nick0'],
        'function_nicknames': ['nick0_fit'],
        'functions':
            '[3]*TMath::Exp(-0.5*((x-[2])/[0])*((x-[2])/[0]))+[4]*TMath::Exp(-0.5*((x-[2])/[1])*((x-[2])/[1]))',
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
    if 'FunctionPlot' not in dictionary['analysis_modules']:
        dictionary['analysis_modules'] = dictionary['analysis_modules'] + ['FunctionPlot']
    if 'PlotFitText' not in dictionary['plot_modules']:
        dictionary['plot_modules'] = dictionary['plot_modules'] + ['PlotFitText']
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


def fit_function(args=None, additional_dictionary=None, only_normalized=False, channel='m', quantity_list=None):
    if quantity_list is None:
        quantity_list = []
    plots = []
    for quantity in quantity_list:
        d = {
            'x_expressions': [quantity],
            'cutlabel': True,
            'analysis_modules': [],
            'plot_modules': ['PlotMplZJet'],
            'filename': 'Z' + channel + channel + '_' + quantity.replace('/', '%') + '_fit',
            'legend': 'center left',
            'y_subplot_lims': [0.75, 1.25],
            'alphas': '0.5',
            'markers': ['_', '_', 'fill', 'fill'],
            'colors': ['black', 'blue', 'black'],
            'ratio_denominator_nicks': ['nick1'],
            'ratio_numerator_nicks': ['nick0'],
            'output_dir': "plots/%s/" % datetime.date.today().strftime('%Y_%m_%d')
        }
        if quantity in binningsZJet.BinningsDictZJet().binnings_dict:
            x_bins = binningsZJet.BinningsDictZJet().binnings_dict[quantity].replace('000', '0')
            x_lims = lims_from_binning(x_bins)
            d['x_bins'] = [x_bins]
            # d['x_bins'] = '400,0,2'
            # d['x_lims'] = x_lims

        if additional_dictionary:
            d.update(additional_dictionary)

        if len(d['files']) == 2:
            fit_function_datamc_gauss(d)
            d['analysis_modules'] = d['analysis_modules'] + ['Ratio']
        elif len(d['files']) == 1:
            # pass
            fit_function_mc_gauss(d)
            # fit_function_mc_doublegauss(d)
            # fit_function_mc_crystalball(d)
        if False:
            if channel == 'e':
                d['function_ranges'] = '0.87225,1.15225'  # for jet1pt/genjet1pt with 0.25<=alpha<0.3, 94.0% truncation
            if channel == 'm':
                d['function_ranges'] = '0.77925,1.22825'  # for jet1pt/genjet1pt with 0.25<=alpha<0.3, 98.5% truncation

        if only_normalized:
            # shape comparison
            d['analysis_modules'] = d['analysis_modules'] + ['NormalizeToFirstHisto']
            d['filename'] = 'Z' + channel + channel + '_' + quantity.replace('/', '%') + '_shapeComparison'

        plots.append(d)

    return [PlottingJob(plots=plots, args=args)]
