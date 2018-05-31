from copy import deepcopy

from ...core import (
    PlotHistograms1D,
    PlotHistograms1DFractions,
    PlotHistograms2D,
    CutSet
)


__all__ = ["plot_flavors", "plot_flavor_fractions"]

_flavor_fraction_cuts_parton_matching = dict(
    u={
        'cut': CutSet(name='u',
                      weights=["abs(matchedgenparton1flavour)==2"],
                      labels=[]),
        'label': r"u",
        'color': 'pink'
    },
    d={
        'cut': CutSet(name='d',
                      weights=["abs(matchedgenparton1flavour)==1"],
                      labels=[]),
        'label': r"d",
        'color': 'darkred'
    },
    ud={
        'cut': CutSet(name='ud',
                      weights=["(abs(matchedgenparton1flavour)==2||abs(matchedgenparton1flavour)==1)"],
                      labels=[]),
        'label': r"ud",
        'color': 'red'
    },
    s={
        'cut': CutSet(name='s',
                      weights=["abs(matchedgenparton1flavour)==3"],
                      labels=[]),
        'label': r"s",
        'color': 'green'
    },
    c={
        'cut': CutSet(name='c',
                      weights=["abs(matchedgenparton1flavour)==4"],
                      labels=[]),
        'label': r"c",
        'color': 'violet'
    },
    b={
        'cut': CutSet(name='b',
                      weights=["abs(matchedgenparton1flavour)==5"],
                      labels=[]),
        'label': r"b",
        'color': 'cornflowerblue'
    },
    g={
        'cut': CutSet(name='g',
                      weights=["abs(matchedgenparton1flavour)==21"],
                      labels=[]),
        'label': r"g",
        'color': 'orange'
    },
    undef={
        'cut': CutSet(name='undef',
                      weights=["abs(matchedgenparton1flavour)>900"],
                      labels=[]),
        'label': r"undef",
        'color': 'lightgray'
    },
)

_flavor_fraction_cuts_miniAOD = dict(
    u={
        'cut': CutSet(name='u',
                      weights=["abs(jet1flavor)==2"],
                      labels=[]),
        'label': r"u",
        'color': 'pink'
    },
    d={
        'cut': CutSet(name='d',
                      weights=["abs(jet1flavor)==1"],
                      labels=[]),
        'label': r"d",
        'color': 'darkred'
    },
    ud={
        'cut': CutSet(name='ud',
                      weights=["(abs(jet1flavor)==2||abs(jet1flavor)==1)"],
                      labels=[]),
        'label': r"ud",
        'color': 'red'
    },
    s={
        'cut': CutSet(name='s',
                      weights=["abs(jet1flavor)==3"],
                      labels=[]),
        'label': r"s",
        'color': 'green'
    },
    c={
        'cut': CutSet(name='c',
                      weights=["abs(jet1flavor)==4"],
                      labels=[]),
        'label': r"c",
        'color': 'violet'
    },
    b={
        'cut': CutSet(name='b',
                      weights=["abs(jet1flavor)==5"],
                      labels=[]),
        'label': r"b",
        'color': 'cornflowerblue'
    },
    g={
        'cut': CutSet(name='g',
                      weights=["abs(jet1flavor)==21"],
                      labels=[]),
        'label': r"g",
        'color': 'orange'
    },
    undef={
        'cut': CutSet(name='undef',
                      weights=["abs(jet1flavor)==0"],
                      labels=[]),
        'label': r"undef",
        'color': 'lightgray'
    },
)


def _get_flavor_cuts_colors_labels(flavors, flavor_definition="miniAOD"):
    """return flavor cuts for a particular flavor definition"""

    if flavor_definition == 'miniAOD':
        _flavor_fraction_cuts = _flavor_fraction_cuts_miniAOD
    elif flavor_definition == 'parton matching':
        _flavor_fraction_cuts = _flavor_fraction_cuts_parton_matching
    else:
        print ("ERROR: Unknown flavor definition '{}': "
               "expected one of {}".format(flavor_definition,
                                           set(['miniAOD', 'parton matching'])))

    _unknown_flavors = (set(flavors) - set(_flavor_fraction_cuts.keys()))
    if _unknown_flavors:
        raise ValueError(
            "Unknown flavors: {}! Available: {}".format(
                _unknown_flavors, set(_flavor_fraction_cuts.keys())
            )
        )

    _cuts = []
    _colors = []
    _labels = []
    for _flavor in flavors:
        _ac = _flavor_fraction_cuts[_flavor]
        _cuts.append(_ac['cut'])
        _colors.append(_ac['color'])
        _labels.append(_ac['label'])

    return _cuts, _colors, _labels


def plot_flavors(sample,
                 jec_correction_string,
                 quantities_or_quantity_pairs,
                 selection_cuts,
                 www_folder_label,
                 flavors_to_include=('ud', 's', 'c', 'b', 'g', 'undef'),
                 flavor_definition='miniAOD',
                 force_n_bins=None,
                 stacked=False,
                 y_log=False):
    """Plot contributions from various jet flavors."""

    _cuts, _colors, _labels = _get_flavor_cuts_colors_labels(flavors_to_include, flavor_definition=flavor_definition)

    _qs = []
    _qpairs = []
    for _q_or_qp in quantities_or_quantity_pairs:
        if isinstance(_q_or_qp, tuple) or isinstance(_q_or_qp, tuple):
            assert len(_q_or_qp) == 2
            _qpairs.append(_q_or_qp)
        else:
            _qs.append(_q_or_qp)

    # color each histogram by flavor
    _samples = []
    for _color, _label in zip(_colors, _labels):
        _samples.append(deepcopy(sample))
        _samples[-1]['source_label'] = _label
        _samples[-1]['color'] = _color

    _ph = None
    if _qs:
        _ph = PlotHistograms1D(
            basename="flavors_{}".format(www_folder_label),
            # there is one subplot per sample and cut in each plot
            samples=_samples,
            jec_correction_string=jec_correction_string,
            additional_cuts=_cuts,
            # each quantity cut generates a different plot
            quantities=_qs,
            # each selection cut generates a new plot
            selection_cuts=selection_cuts,
            stacked=stacked,
        )

        if force_n_bins is not None:
            for _plot in _ph._plots:
                _plot._basic_dict['x_bins'] = ",".join([str(force_n_bins)] + _plot._basic_dict['x_bins'].split(",")[1:])

        _ph_log = deepcopy(_ph)

        if y_log:
            for _plot in _ph_log._plots:
                _plot._basic_dict['y_log'] = True

    _ph2 = None
    if _qpairs:
        _ph2 = PlotProfiles(
            basename="flavors_{}".format(www_folder_label),
            # there is one subplot per sample and cut in each plot
            samples=_samples,
            jec_correction_string=jec_correction_string,
            additional_cuts=_cuts,
            # each quantity cut generates a different plot
            quantity_pairs=_qpairs,
            # each selection cut generates a new plot
            selection_cuts=selection_cuts,
            # show_ratio_to_first=True,
        )

        for _plot2D in _ph2._plots:
            if _plot2D._qy in ('jet1pt_over_jet1ptraw',):
                _plot2D._basic_dict['lines'] = ['1.0']  # guide to the eye

    if _ph is not None:
        _ph.make_plots()

    if _ph2 is not None:
        _ph2.make_plots()


def plot_flavor_fractions(
        sample,
        jec_correction_string,
        quantities,
        selection_cuts,
        www_folder_label,
        flavors_to_include=('ud', 's', 'c', 'b', 'g', 'undef'),
        flavor_definition='miniAOD',
        force_n_bins=None):
    """Plot flavor composition as a fraction of total. Always stacked."""

    _cuts, _colors, _labels = _get_flavor_cuts_colors_labels(flavors_to_include, flavor_definition=flavor_definition)

    _ph = PlotHistograms1DFractions(
        basename="flavor_fractions_{}".format(www_folder_label),
        # there is one subplot per sample and cut in each plot
        jec_correction_string=jec_correction_string,
        reference_cut_set=None,
        sample=sample,
        fraction_cut_sets=_cuts,
        fraction_colors=_colors,
        fraction_labels=_labels,
        # each quantity cut generates a different plot
        quantities=quantities,
        # each selection cut generates a new plot
        selection_cuts=selection_cuts,
        y_label="Fraction of Total Events"
    )

    for _plot in _ph._plots:
        if force_n_bins is not None:
            _plot._basic_dict['x_bins'] = ",".join([str(force_n_bins)] + _plot._basic_dict['x_bins'].split(",")[1:])

    return _ph
