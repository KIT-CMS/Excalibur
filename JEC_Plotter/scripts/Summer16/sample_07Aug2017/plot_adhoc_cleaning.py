from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, QUANTITIES
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
    RUN_PERIOD_CUT_DICTS,
)


from copy import deepcopy

QUANTITIES['jet1eta_zoom'] = deepcopy(QUANTITIES['jet1eta'])
QUANTITIES['jet1eta_zoom'].name = "jet1eta_zoom"
QUANTITIES['jet1eta_zoom'].bin_spec = ("50", "-4.0", "-1.5")

QUANTITIES['jet1phi_zoom'] = deepcopy(QUANTITIES['jet1phi'])
QUANTITIES['jet1phi_zoom'].name = "jet1phi_zoom"
QUANTITIES['jet1phi_zoom'].bin_spec = ("50",  "2.0",  "2.7")

QUANTITIES['jet1phi_zoom'] = deepcopy(QUANTITIES['jet1phi'])
QUANTITIES['jet1phi_zoom'].name = "jet1phi_zoom"
QUANTITIES['jet1phi_zoom'].bin_spec = ("50",  "2.0",  "2.7")

QUANTITIES['jet2eta_zoom'] = deepcopy(QUANTITIES['jet2eta'])
QUANTITIES['jet2eta_zoom'].name = "jet2eta_zoom"
QUANTITIES['jet2eta_zoom'].bin_spec = ("50", "-4.0", "-1.5")

QUANTITIES['jet2phi_zoom'] = deepcopy(QUANTITIES['jet2phi'])
QUANTITIES['jet2phi_zoom'].name = "jet2phi_zoom"
QUANTITIES['jet2phi_zoom'].bin_spec = ("50",  "2.0",  "2.7")

QUANTITIES['jet3eta_zoom'] = deepcopy(QUANTITIES['jet3eta'])
QUANTITIES['jet3eta_zoom'].name = "jet3eta_zoom"
QUANTITIES['jet3eta_zoom'].bin_spec = ("50", "-4.0", "-1.5")

QUANTITIES['jet3phi_zoom'] = deepcopy(QUANTITIES['jet3phi'])
QUANTITIES['jet3phi_zoom'].name = "jet3phi_zoom"
QUANTITIES['jet3phi_zoom'].bin_spec = ("50",  "2.0",  "2.7")

_CORR_FOLDER = "L1L2L3"

_QUANTITIES = [
    'jet1phi', 'jet2phi', 'jet3phi',
    'jet1eta', 'jet2eta', 'jet3eta',
    #'jet1phi_zoom', 'jet2phi_zoom', 'jet3phi_zoom',
    #'jet1eta_zoom', 'jet2eta_zoom', 'jet3eta_zoom',
    #'jet1pt', 'jet2pt', 'jet3pt'
    'mpf', 'ptbalance', #'alpha'
    #'met', 'metphi',
    'zpt', #'zeta', 'zphi',
]

_QUANTITY_PAIRS = [
    #('jet1phi', 'jet1eta'),
    #('jet2phi', 'jet2eta'),
    #('jet3phi', 'jet3eta'),
    ('jet1phi_zoom', 'jet1eta_zoom'),
    ('jet2phi_zoom', 'jet2eta_zoom'),
    ('jet3phi_zoom', 'jet3eta_zoom'),
]

_QUANTITY_PAIRS_PROFILE = [
    ('zpt', 'ptbalance'),
    ('zpt', 'mpf'),
]

_SELECTION_CUTS = [
    SELECTION_CUTS['finalcuts'],
    #SELECTION_CUTS['basiccuts']
]

_ADDITIONAL_CUTS = [
    {
        'cut': None,
        'label': r"no $\\eta$-$\\phi$ veto",
        'color': 'k'
    },
    {
        'cut': ADDITIONAL_CUTS['user']['adhocEtaPhiBCD_pt0'],
        'label': r"$\\eta$-$\\phi$ veto, any jet $p_T$",
        'color': 'cornflowerblue'
    },
    # {
    #     'cut': ADDITIONAL_CUTS['user']['adhocEtaPhiBCD_pt5'],
    #     'label': "eta-phi veto if jet $p_T>5$ GeV",
    #     'color': 'orange'
    # },
    {
        'cut': ADDITIONAL_CUTS['user']['adhocEtaPhiBCD_pt15'],
        'label': r"$\\eta$-$\\phi$ veto if jet $p_T>15$ GeV",
        'color': 'red'
    },
]

_run_period_cuts = dict(
    runBCD=None,
    runB=ADDITIONAL_CUTS['run_periods']['runB'],
    runC=ADDITIONAL_CUTS['run_periods']['runC'],
    runD=ADDITIONAL_CUTS['run_periods']['runD']
)

_hcal_hot_eta_ranges = dict(
    runB=(-2.172, -1.930),
    runC=(-3.489, -3.139),
    runD=(-3.489, -3.139),
)

_hcal_hot_phi_ranges = dict(
    runB=(2.200, 2.500),
    runC=(2.237, 2.475),
    runD=(2.237, 2.475),
)

def _workflow(sample, which='hist1D'):
    _phs = []
    for _run_period_cut_name, _run_period_cut in _run_period_cuts.iteritems():

        if _run_period_cut is None:
            _add_cuts = [_ac['cut'] for _ac in RUN_PERIOD_CUT_DICTS]
        else:
            _add_cuts = [(_ac['cut'] + _run_period_cut) if _ac['cut'] is not None else _run_period_cut for _ac in RUN_PERIOD_CUT_DICTS]

        _source_label = "{}".format(_run_period_cut_name)

        _SAMPLES = []
        for _ac in _ADDITIONAL_CUTS:
            _SAMPLES.append(deepcopy(sample))
            _SAMPLES[-1]['color'] = _ac['color']
            _SAMPLES[-1]['source_label'] = '{}, {}'.format(_source_label, _ac['label'])

        if which == 'hist1D':
            _ph = PlotHistograms1D(
                basename="adhoc_etaphiveto_1D_07Aug2017_{}".format(_source_label),
                # there is one subplot per sample and cut in each plot
                samples=_SAMPLES,
                jec_correction_string=_CORR_FOLDER,
                additional_cuts=_add_cuts,
                # each quantity cut generates a different plot
                quantities=_QUANTITIES,
                # each selection cut generates a new plot
                selection_cuts=_SELECTION_CUTS,
                show_ratio_to_first=True,
                show_cut_info_text=False
            )
            _eta_range = _hcal_hot_eta_ranges.get(_run_period_cut_name)
            _phi_range = _hcal_hot_phi_ranges.get(_run_period_cut_name)
            for _plot in _ph._plots:
                if _plot._q.name.endswith('eta') and _eta_range is not None:
                    _plot._basic_dict['vertical_lines'] = list(_eta_range)
                if _plot._q.name.endswith('phi') and _phi_range is not None:
                    _plot._basic_dict['vertical_lines'] = list(_phi_range)
                if _plot._q.name == 'zpt':
                    del _plot._basic_dict['x_lims']
                    _plot._basic_dict['x_bins'] = 'zpt'
                    _plot._basic_dict['x_log'] = True
            _phs.append(_ph)
        elif which == 'hist2D':
            for _ac in _add_cuts:
                _cutname = "all" if _ac is None else _ac.name
                _ph = PlotHistograms2D(
                    basename="adhoc_etaphiveto_2D_07Aug2017_{}_{}".format(_cutname, _source_label),
                    # there is one subplot per sample and cut in each plot
                    samples=_SAMPLES,
                    jec_correction_string=_CORR_FOLDER,
                    additional_cuts=[_ac],
                    # each quantity cut generates a different plot
                    quantity_pairs=_QUANTITY_PAIRS,
                    # each selection cut generates a new plot
                    selection_cuts=_SELECTION_CUTS,
                    # show_ratio_to_first=True
                )
                _eta_range = _hcal_hot_eta_ranges.get(_run_period_cut_name)
                _phi_range = _hcal_hot_phi_ranges.get(_run_period_cut_name)
                for _plot in _ph._plots:
                    if (_plot._qy.name.endswith('eta') or _plot._qy.name.endswith('eta_zoom')) and _eta_range is not None:
                        _plot._basic_dict['lines'] = list(_eta_range)
                    if (_plot._qx.name.endswith('phi') or _plot._qx.name.endswith('phi_zoom')) and _phi_range is not None:
                        _plot._basic_dict['vertical_lines'] = list(_phi_range)
                _phs.append(_ph)
        elif which == 'profile':
            _ph = PlotHistograms2D(
                basename="adhoc_etaphiveto_profile_07Aug2017_{}".format(_source_label),
                # there is one subplot per sample and cut in each plot
                samples=_SAMPLES,
                jec_correction_string=_CORR_FOLDER,
                additional_cuts=_add_cuts,
                # each quantity cut generates a different plot
                quantity_pairs=_QUANTITY_PAIRS_PROFILE,
                # each selection cut generates a new plot
                selection_cuts=_SELECTION_CUTS,
                #show_ratio_to_first=True,
                show_as_profile=True,
            )

            for _plot in _ph._plots:
                del _plot._basic_dict['y_bins']
                if _plot._qy.name == 'mpf' or _plot._qy.name == 'ptbalance':
                    _plot._basic_dict['y_lims'] = [0.8, 1.2]
                if _plot._qx.name == 'zpt':
                    del _plot._basic_dict['x_lims']
                    _plot._basic_dict['x_bins'] = 'zpt'
                    _plot._basic_dict['x_log'] = True

            _phs.append(_ph)
        else:
             raise ValueError("UNKNOWN 'which' = '{}'".format(which))

    for _ph in _phs:
        # for _plot in _ph._plots:
        #     print _plot.get_dict()
        #     import json
        #     with open('test.json', 'w') as f:
        #         json.dump(_plot.get_dict(), f)
        #     exit(44)
        _ph.make_plots()

        if which == 'hist1D':
            for _plot in _ph._plots:
                _plot.count_events(write_to_file=True)

if __name__ == "__main__":
    for _which in ['hist1D', 'hist2D', 'profile']:
        _workflow(SAMPLES['Data_Zmm_BCD_noetaphiclean'], which=_which)
        _workflow(SAMPLES['Data_Zee_BCD_noetaphiclean'], which=_which)
