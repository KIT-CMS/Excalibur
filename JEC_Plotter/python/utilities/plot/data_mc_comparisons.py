from ...core import PlotHistograms2D

from copy import deepcopy

__all__ = ['plot_data_mc_closure']


def plot_data_mc_closure(sample_data,
                         sample_mc,
                         selection_cuts,
                         subplot_cuts,
                         correction_levels,
                         quantity_pairs,
                         sample_label,
                         jec_campaign_label,
                         jec_version):
    _phs = []

    _add_cuts = [_ac['cut'] for _ac in subplot_cuts]
    _add_cuts.insert(0, None)

    _samples = []

    _samples.append(deepcopy(sample_mc))
    _samples[-1]['color'] = 'k'
    _samples[-1]['source_label'] = sample_mc['source_label']

    for _ac in subplot_cuts:
        _samples.append(deepcopy(sample_data))
        _samples[-1]['color'] = _ac['color']
        _samples[-1]['source_label'] = '{}'.format(_ac['label'])

    for _corr_level in correction_levels:
        _ph = PlotHistograms2D(
            basename="data_mc_closure_{}_JEC{}".format(sample_label, jec_version),
            # there is one subplot per sample and cut in each plot
            samples=_samples,
            corrections=_corr_level,
            additional_cuts=_add_cuts,
            # each quantity cut generates a different plot
            quantity_pairs=quantity_pairs,
            # each selection cut generates a new plot
            selection_cuts=selection_cuts,
            show_as_profile=True,
            show_ratio_to_first=True,
            show_cut_info_text=False,
            jec_version_label="{} JEC {}".format(jec_campaign_label, jec_version)
        )

        _phs.append(_ph)

        for _ph in _phs:
            _ph.make_plots()