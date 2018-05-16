from copy import deepcopy

from ...core import (
    PlotHistograms2D,
)

__all__ = ["plot_time_dependence"]

def plot_time_dependence(sample,
                         corrections_folder,
                         quantities,
                         selection_cuts,
                         additional_cuts,
                         www_folder_label,
                         dataset_label=None,
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
        show_as_profile=True,
        jec_version_label=dataset_label,
    )

    for _plot in _ph._plots:
        try:
            _plot._q
            if _plot._q in ('jet1pt_over_jet1ptraw', 'mpf', 'ptbalance'):
                _plot._basic_dict['lines'] = ['1.0']  # guide to the eye
        except AttributeError:
            if _plot._qy in ('jet1pt_over_jet1ptraw', 'mpf', 'ptbalance'):
                _plot._basic_dict['lines'] = ['1.0']  # guide to the eye

    _ph.make_plots()
