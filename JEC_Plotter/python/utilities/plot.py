from copy import deepcopy

from Excalibur.JEC_Plotter.core import (PlotHistograms1D,
                              PlotHistograms2D)

def plot_time_dependence(sample, 
                         corrections_folder,
                         quantities,
                         selection_cuts,
                         additional_cuts,
                         www_folder_label,
                         time_quantity='run'):
    _samples = []
    _cuts = []
    for _ac in additional_cuts:
        _samples.append(deepcopy(sample))
        _cuts.append(_ac['cut'])
        _samples[-1]['color'] = _ac['color']
        _samples[-1]['source_label'] = '{}'.format(_ac['label'])

    _q_pairs = [(time_quantity, _q) for _q in quantities]

    _ph = PlotHistograms2D(
        basename="time_dependence_{}".format(www_folder_label),
        # there is one subplot per sample and cut in each plot
        samples=_samples,
        corrections=corrections_folder,
        additional_cuts=_cuts,
        # each quantity cut generates a different plot
        quantity_pairs=_q_pairs,
        # each selection cut generates a new plot
        selection_cuts=selection_cuts,
        # show_ratio_to_first=True,
        show_as_profile=True
    )

    for _plot in _ph._plots:
        _plot._basic_dict['lines'] = ['1.0']

    _ph.make_plots()

# def plot_quantities_hist1D(sample):
#     _phs = []
#     for _run_period_cut_name, _run_period_cut in _run_period_cuts.iteritems():
# 
#         if _run_period_cut is None:
#             _add_cuts = [_ac['cut'] for _ac in _ADDITIONAL_CUTS]
#         else:
#             _add_cuts = [(_ac['cut'] + _run_period_cut) if _ac['cut'] is not None else _run_period_cut for _ac in _ADDITIONAL_CUTS]
# 
#         _source_label = "run{}".format(_run_period_cut_name)
# 
#         _SAMPLES = []
#         for _ac in _ADDITIONAL_CUTS:
#             _SAMPLES.append(deepcopy(sample))
#             _SAMPLES[-1]['color'] = _ac['color']
#             _SAMPLES[-1]['source_label'] = '{}, {}'.format(_source_label, _ac['label'])
# 
#         if which == 'hist1D':
#             _ph = PlotHistograms1D(
#                 basename="adHocEtaPhiVeto_1D_Legacy_{}".format(_source_label),
#                 # there is one subplot per sample and cut in each plot
#                 samples=_SAMPLES,
#                 additional_cuts=_add_cuts,
#                 # each quantity cut generates a different plot
#                 quantities=_QUANTITIES,
#                 # each selection cut generates a new plot
#                 selection_cuts=_SELECTION_CUTS,
#                 show_ratio_to_first=True,
#                 show_cut_info_text=False
#             )
#             _eta_range = _eta_ranges.get(_run_period_cut_name)
#             _phi_range = _phi_ranges.get(_run_period_cut_name)
#             for _plot in _ph._plots:
#                 if _plot._q.name.endswith('eta') and _eta_range is not None:
#                     _plot._basic_dict['vertical_lines'] = list(_eta_range)
#                 if _plot._q.name.endswith('phi') and _phi_range is not None:
#                     _plot._basic_dict['vertical_lines'] = list(_phi_range)
# 
#         elif which == 'hist2D':
#             _ph = PlotHistograms2D(
#                 basename="adHocEtaPhiVeto_2D_Legacy_{}".format(_source_label),
#                 # there is one subplot per sample and cut in each plot
#                 samples=_SAMPLES,
#                 additional_cuts=_add_cuts,
#                 # each quantity cut generates a different plot
#                 quantity_pairs=_QUANTITY_PAIRS,
#                 # each selection cut generates a new plot
#                 selection_cuts=_SELECTION_CUTS,
#                 # show_ratio_to_first=True
#             )
#             _eta_range = _eta_ranges.get(_run_period_cut_name)
#             _phi_range = _phi_ranges.get(_run_period_cut_name)
#             for _plot in _ph._plots:
#                 if _plot._qy.name.endswith('eta') and _eta_range is not None:
#                     _plot._basic_dict['lines'] = list(_eta_range)
#                 if _plot._qx.name.endswith('phi') and _phi_range is not None:
#                     _plot._basic_dict['vertical_lines'] = list(_phi_range)
#         else:
#              raise ValueError("UNKNOWN 'which' = '{}'".format(which))
# 
#         _phs.append(_ph)
# 
#     for _ph in _phs:
#         _ph.make_plots()
