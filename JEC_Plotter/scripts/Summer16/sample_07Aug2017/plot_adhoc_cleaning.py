from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D, QUANTITIES
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
)

from copy import deepcopy


QUANTITIES['jet2eta'].bin_spec = ("50", "-4.0", "-1.5")
QUANTITIES['jet2phi'].bin_spec = ("50",  "2.0",  "2.7")
QUANTITIES['jet3eta'].bin_spec = ("50", "-4.0", "-1.5")
QUANTITIES['jet3phi'].bin_spec = ("50",  "2.0",  "2.7")

_CORR_FOLDER = "L1L2L3"

_QUANTITIES = [
    'jet1phi', 'jet2phi', 'jet3phi',
    'jet1eta', 'jet2eta', 'jet3eta',
    'jet1pt', 'jet2pt', 'jet3pt'
    'mpf', 'ptbalance', 'alpha'
    'met', 'metphi',
    'zpt', 'zeta', 'zphi',
]

_QUANTITY_PAIRS = [
    ('jet1phi', 'jet1eta'),
    ('jet2phi', 'jet2eta'),
    ('jet3phi', 'jet3eta')
]

_SELECTION_CUTS = [SELECTION_CUTS['finalcuts'],
                   SELECTION_CUTS['basiccuts']]

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
    BCD=None,
    B=ADDITIONAL_CUTS['run_periods']['runB'],
    C=ADDITIONAL_CUTS['run_periods']['runC'],
    D=ADDITIONAL_CUTS['run_periods']['runD']
)

_eta_ranges = dict(
    B=(-2.172, -2.043),
    C=(-3.314, -3.139),
    D=(-3.489, -3.139),
)

_phi_ranges = dict(
    B=(2.290, 2.422),
    C=(2.237, 2.475),
    D=(2.237, 2.475),
)

def _workflow(sample, which='hist1D'):
    _phs = []
    for _run_period_cut_name, _run_period_cut in _run_period_cuts.iteritems():

        if _run_period_cut is None:
            _add_cuts = [_ac['cut'] for _ac in _ADDITIONAL_CUTS]
        else:
            _add_cuts = [(_ac['cut'] + _run_period_cut) if _ac['cut'] is not None else _run_period_cut for _ac in _ADDITIONAL_CUTS]

        _source_label = "run{}".format(_run_period_cut_name)

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
                corrections=_CORR_FOLDER,
                additional_cuts=_add_cuts,
                # each quantity cut generates a different plot
                quantities=_QUANTITIES,
                # each selection cut generates a new plot
                selection_cuts=_SELECTION_CUTS,
                show_ratio_to_first=True,
                show_cut_info_text=False
            )
            _eta_range = _eta_ranges.get(_run_period_cut_name)
            _phi_range = _phi_ranges.get(_run_period_cut_name)
            for _plot in _ph._plots:
                if _plot._q.name.endswith('eta') and _eta_range is not None:
                    _plot._basic_dict['vertical_lines'] = list(_eta_range)
                if _plot._q.name.endswith('phi') and _phi_range is not None:
                    _plot._basic_dict['vertical_lines'] = list(_phi_range)
            _phs.append(_ph)
        elif which == 'hist2D':
            for _ac in _add_cuts:
                _cutname = "all" if _ac is None else _ac.name
                _ph = PlotHistograms2D(
                    basename="adhoc_etaphiveto_2D_07Aug2017_{}_{}".format(_cutname, _source_label),
                    # there is one subplot per sample and cut in each plot
                    samples=_SAMPLES,
                    corrections=_CORR_FOLDER,
                    additional_cuts=[_ac],
                    # each quantity cut generates a different plot
                    quantity_pairs=_QUANTITY_PAIRS,
                    # each selection cut generates a new plot
                    selection_cuts=_SELECTION_CUTS,
                    # show_ratio_to_first=True
                )
                _eta_range = _eta_ranges.get(_run_period_cut_name)
                _phi_range = _phi_ranges.get(_run_period_cut_name)
                for _plot in _ph._plots:
                    if _plot._qy.name.endswith('eta') and _eta_range is not None:
                        _plot._basic_dict['lines'] = list(_eta_range)
                    if _plot._qx.name.endswith('phi') and _phi_range is not None:
                        _plot._basic_dict['vertical_lines'] = list(_phi_range)
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

if __name__ == "__main__":
    #for _which in ['hist1D', 'hist2D']:
    for _which in ['hist1D']:
        #_SELECTION_CUTS[0].name += "_noetaphiclean"
        _workflow(SAMPLES['Data_Zmm_BCD_noetaphiclean'], which=_which)
        _workflow(SAMPLES['Data_Zee_BCD_noetaphiclean'], which=_which)
