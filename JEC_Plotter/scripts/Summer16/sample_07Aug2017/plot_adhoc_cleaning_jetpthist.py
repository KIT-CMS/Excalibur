from Excalibur.JEC_Plotter.core import PlotHistograms1D, PlotHistograms2D
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
    RUN_PERIOD_CUT_DICTS,
)

from copy import deepcopy

_CORR_FOLDER = "L1L2L3"

_QUANTITIES = [
    'jet1pt', 'jet2pt', 'jet3pt'
]

_SELECTION_CUTS = [SELECTION_CUTS['finalcuts']]

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
    #runB_jet2=ADDITIONAL_CUTS['hcal_hot_towers']['runB_jet2'],
    #runC_jet2=ADDITIONAL_CUTS['hcal_hot_towers']['runC_jet2'],
    #runD_jet2=ADDITIONAL_CUTS['hcal_hot_towers']['runD_jet2'],
    #runB_jet3=ADDITIONAL_CUTS['hcal_hot_towers']['runB_jet3'],
    #runC_jet3=ADDITIONAL_CUTS['hcal_hot_towers']['runC_jet3'],
    #runD_jet3=ADDITIONAL_CUTS['hcal_hot_towers']['runD_jet3'],
    runB=ADDITIONAL_CUTS['run_periods']['runB'],
    runC=ADDITIONAL_CUTS['run_periods']['runC'],
    runD=ADDITIONAL_CUTS['run_periods']['runD'],
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

def _workflow(sample):
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

        _ph = PlotHistograms1D(
            basename="adhoc_etaphiveto_jetpthist_07Aug2017_{}".format(_source_label),
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
        _eta_range = _eta_ranges.get(_run_period_cut_name)
        _phi_range = _phi_ranges.get(_run_period_cut_name)
        for _plot in _ph._plots:
            if _plot._q.name.endswith('eta') and _eta_range is not None:
                _plot._basic_dict['vertical_lines'] = list(_eta_range)
            if _plot._q.name.endswith('phi') and _phi_range is not None:
                _plot._basic_dict['vertical_lines'] = list(_phi_range)

        _phs.append(_ph)

    for _ph in _phs:
        _ph.make_plots()

if __name__ == "__main__":
    #_SELECTION_CUTS[0].name += "_noetaphiclean"
    _workflow(SAMPLES['Data_Zmm_BCD_noetaphiclean'])
    _workflow(SAMPLES['Data_Zee_BCD_noetaphiclean'])
