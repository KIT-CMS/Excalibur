from ...core import PlotHistograms1D, PlotProfiles, PlotStackProfiles

from copy import deepcopy

__all__ = ['plot_data_mc_profiles', 'plot_data_mc_hist', 'plot_pf_energy_fractions']


def _prepare_samples_cuts(sample_mc, sample_data, subplot_cuts):
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

    return _samples, _add_cuts


def plot_data_mc_profiles(sample_data,
                          sample_mc,
                          selection_cuts,
                          subplot_cuts,
                          jec_correction_string,
                          quantity_pairs,
                          sample_label,
                          jec_campaign_label,
                          jec_version,
                          **plot_profile_kwargs):

    _default_kwargs=dict(
            basename="data_mc_profile_{}_JEC{}".format(sample_label, jec_version),
            show_ratio_to_first=True,
            show_cut_info_text=False,
            plot_label="{} JEC {}".format(jec_campaign_label, jec_version),
    )

    _default_kwargs.update(plot_profile_kwargs)

    _samples, _add_cuts = _prepare_samples_cuts(sample_mc, sample_data, subplot_cuts)

    _pc = PlotProfiles(
            # there is one subplot per sample and cut in each plot
            samples=_samples,
            selection_cuts=selection_cuts,
            jec_correction_string=jec_correction_string,
            additional_cuts=_add_cuts,
            # each quantity cut generates a different plot
            quantity_pairs=quantity_pairs,
            # each selection cut generates a new plot
            **_default_kwargs
    )

    return _pc


def plot_data_mc_hist(sample_data,
                      sample_mc,
                      selection_cuts,
                      subplot_cuts,
                      jec_correction_string,
                      quantities,
                      sample_label,
                      jec_campaign_label,
                      jec_version,
                      **plot_profile_kwargs):

    _default_kwargs=dict(
            basename="data_mc_hist_{}_JEC{}".format(sample_label, jec_version),
            show_ratio_to_first=True,
            show_cut_info_text=False,
            plot_label="{} JEC {}".format(jec_campaign_label, jec_version),
    )

    _default_kwargs.update(plot_profile_kwargs)

    _samples, _add_cuts = _prepare_samples_cuts(sample_mc, sample_data, subplot_cuts)

    _pc = PlotHistograms1D(
            # there is one subplot per sample and cut in each plot
            samples=_samples,
            selection_cuts=selection_cuts,
            jec_correction_string=jec_correction_string,
            additional_cuts=_add_cuts,
            # each quantity cut generates a different plot
            quantities=quantities,
            # each selection cut generates a new plot
            **_default_kwargs
    )

    return _pc

_PF_ENERGY_FRACTIONS_SPEC = [
    dict(
        quantity_name='jet1ef',
        marker='^',
        color='orange',
    ),
    dict(
        quantity_name='jet1mf',
        marker='v',
        color='teal',
    ),
    dict(
        quantity_name='jet1nhf',
        marker='d',
        color='green',
    ),
    dict(
        quantity_name='jet1pf',
        marker='s',
        color='royalblue',
    ),
    dict(
        quantity_name='jet1chf',
        marker='o',
        color='red',
    ),
]

def plot_pf_energy_fractions(sample_data,
                             sample_mc,
                             quantity_x,
                             selection_cuts,
                             selection_label,
                             jec_correction_string,
                             data_sample_label,
                             jec_campaign_label,
                             jec_version,
                             **plot_stackprofile_kwargs):

    _default_kwargs=dict(
        jec_corr_text_topleft_xy=(0.1, 0.98),
        show_data_mc_comparison_as='difference percent',
        show_cut_info_text=False,
        y_range=(0, 1.15),
        y_label="PF Energy Fractions",
        plot_label="{} JEC {} ({})".format(jec_campaign_label, jec_version, selection_label),
    )

    _default_kwargs.update(plot_stackprofile_kwargs)

    _ph = PlotStackProfiles(
        basename="pf_energy_fractions_{}_JEC{}_{}".format(data_sample_label, jec_version, selection_label),
        # there is one subplot per sample and cut in each plot
        sample_mc=sample_mc,
        sample_data=sample_data,
        selection_cuts=selection_cuts,
        jec_correction_string=jec_correction_string,
        quantity_x=quantity_x,
        quantities_y=[_spec['quantity_name'] for _spec in _PF_ENERGY_FRACTIONS_SPEC],
        colors_mc=[_spec['color'] for _spec in _PF_ENERGY_FRACTIONS_SPEC],
        markers_data=[_spec['marker'] for _spec in _PF_ENERGY_FRACTIONS_SPEC],
        # each selection cut generates a new plot
        **_default_kwargs
    )

    return _ph

