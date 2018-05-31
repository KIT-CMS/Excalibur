from copy import deepcopy

from ...core import (
    PlotProfiles,
)

__all__ = ["plot_time_dependence"]


def plot_time_dependence(sample,
                         jec_correction_string,
                         quantities,
                         selection_cuts,
                         additional_cuts,
                         www_folder_label,
                         time_quantity='run',
                         **plot_profile_kwargs):
    _samples = []
    _cuts = []
    for _ac in additional_cuts:
        _samples.append(deepcopy(sample))
        _cuts.append(_ac['cut'])
        _samples[-1]['color'] = _ac['color']
        _samples[-1]['source_label'] = '{}'.format(_ac['label'])

    _q_pairs = [(time_quantity, _q) for _q in quantities]

    _pc = PlotProfiles(
        basename="time_dependence_{}".format(www_folder_label),
        # there is one subplot per sample and cut in each plot
        samples=_samples,
        jec_correction_string=jec_correction_string,
        additional_cuts=_cuts,
        # each quantity cut generates a different plot
        quantity_pairs=_q_pairs,
        # each selection cut generates a new plot
        selection_cuts=selection_cuts,
        # show_ratio_to_first=True,
        **plot_profile_kwargs
    )

    for _plot in _pc._plots:
        if _plot._qs[1] in ('jet1pt_over_jet1ptraw', 'mpf', 'ptbalance'):
            _plot._basic_dict['lines'] = ['1.0']  # guide to the eye

    return _pc
