from Excalibur.JEC_Plotter.core import CutSet, Sample
from Excalibur.JEC_Plotter.definitions.Fall17.samples_17Nov2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS,
    RUN_PERIOD_CUT_DICTS,
)
from Excalibur.JEC_Plotter.utilities.plot import plot_pf_energy_fractions

from copy import deepcopy

_REGION_SPEC = {
    'eta_00_13' : dict(
        abseta=(0.0, 1.3),
    ),
    'eta_13_25' : dict(
        abseta=(1.3, 2.5),
    ),
    'eta_25_30' : dict(
        abseta=(2.5, 3.0),
    ),
    'eta_30_50' : dict(
        abseta=(3.0, 5.0),
    ),
    'pt_0_50' : dict(
        pt=(0.0, 50.0),
    ),
    'pt_50_150' : dict(
        pt=(50.0, 150.0),
    ),
    'pt_150_5000' : dict(
        pt=(150.0, 5000.0),
    ),
}

_REGION_CUTS = {
    _region_name : {
        'cut': CutSet(
            '{}'.format(_region_name),
            weights=[
                "{obj}{prop}>{lo}&&{obj}{prop}<={hi}".format(
                    obj='z',#"jet1",
                    prop=prop,
                    lo=_region_dict[prop][0],
                    hi=_region_dict[prop][1]) for prop in _region_dict],
            labels=[]
        ),
        'label': '{}'.format(_region_name)
    }
    for _region_name, _region_dict in _REGION_SPEC.iteritems()
}

_SELECTION_CUTS = [
    # SELECTION_CUTS['finalcuts'],
    # SELECTION_CUTS['extendedeta'],
    # SELECTION_CUTS['extendedeta']+_COLD_REGION_CUTS['cold']['cut'],
    # SELECTION_CUTS['extendedeta']+_COLD_REGION_CUTS['control']['cut'],
    #SELECTION_CUTS['nocuts'],
    #SELECTION_CUTS['nocuts']+_COLD_REGION_CUTS['cold']['cut'],
    #SELECTION_CUTS['nocuts']+_COLD_REGION_CUTS['control']['cut'],
    #SELECTION_CUTS['finalcuts'],
    #SELECTION_CUTS['nocuts'] + ADDITIONAL_CUTS['eta']['central']
    #SELECTION_CUTS['noetacut'] + _REGION_CUTS['eta_00_13']['cut'],
    #SELECTION_CUTS['noetacut'] + _REGION_CUTS['eta_13_25']['cut'],
    #SELECTION_CUTS['noetacut'] + _REGION_CUTS['eta_25_30']['cut'],
    #SELECTION_CUTS['noetacut'] + _REGION_CUTS['eta_30_50']['cut'],
    SELECTION_CUTS['noetacut'] + _REGION_CUTS['pt_0_50']['cut'],
    SELECTION_CUTS['noetacut'] + _REGION_CUTS['pt_50_150']['cut'],
    SELECTION_CUTS['noetacut'] + _REGION_CUTS['pt_150_5000']['cut'],
]

QUANTITY_X = 'jet1eta_narrow'  #'zpt_log'

SAMPLES_MC = dict(
    mm=SAMPLES['MC_Zmm_DYNJ_Fall17_JECV4'],
    ee=SAMPLES['MC_Zee_DYNJ_Fall17_JECV4'],
)
RUN_PERIODS = ["B", "C", "D", "E", "F"]


if __name__ == "__main__":
    for _jecv in ("V6",):
        for _channel in ("mm", "ee"):
            _samples_data = [SAMPLES['Data_Z{}_{}_Fall17_JEC{}'.format(_channel, _run_period, _jecv)] for _run_period in RUN_PERIODS]
            for _sample_data in _samples_data:
                _pc = plot_pf_energy_fractions(
                    sample_data=_sample_data,
                    sample_mc=SAMPLE_MC[_channel],
                    quantity_x=QUANTITY_X,
                    selection_cuts=_SELECTION_CUTS,
                    selection_label="Run{}".format(_sample_data['source_label']),
                    jec_correction_string="L1L2L3",
                    data_sample_label="17Nov2017",
                    jec_campaign_label="Fall17",
                    jec_version=_jecv,)

                _pc.make_plots()
