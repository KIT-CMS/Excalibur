from Excalibur.JEC_Plotter.core import PlotHistograms2DQuantitiesProfile, PlotHistograms2D, CutSet, Sample
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES,
    SELECTION_CUTS,
    ADDITIONAL_CUTS
)

from copy import deepcopy

_CORR_FOLDER = "L1L2L3"

_QUANTITIES = [
    'zpt_log',
    #'jet1pt', 'jet1eta', 'jet1phi',
]

_PF_ENERGY_FRACTIONS = [
    'jet1ef',
    'jet1mf',
    'jet1nhf',
    'jet1pf',
    'jet1chf',
]
_PF_ENERGY_FRACTION_COLORS = [
    'orange',
    'teal',
    'green',
    'royalblue',
    'red',
]
_PF_ENERGY_FRACTION_MARKERS = [
    '^',
    'v',
    'd',
    's',
    'o',
]

_SAMPLES_EE = [
    #SAMPLES['Data_Zmm_Summer16_BCDEFGH'],
    SAMPLES['Data_Zmm_BCD_Summer16_JECV5'],
    SAMPLES['Data_Zmm_EF_Summer16_JECV5'],
    SAMPLES['Data_Zmm_GH_Summer16_JECV5'],
]

_SAMPLES_MM = [
    #SAMPLES['Data_Zee_Summer16_BCDEFGH'],
    SAMPLES['Data_Zee_BCD_Summer16_JECV5'],
    SAMPLES['Data_Zee_EF_Summer16_JECV5'],
    SAMPLES['Data_Zee_GH_Summer16_JECV5'],
]


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

QUANTITY_X = 'jet1eta'  #'zpt_log'

if __name__ == "__main__":
    for _sample in _SAMPLES_MM:
        _ph = PlotHistograms2DQuantitiesProfile(
            basename="pf_energy_fractions_07Aug2017_JECV4_Run{}".format(_sample['source_label']),
            # there is one subplot per sample and cut in each plot
            sample_mc=SAMPLES['MC_Zmm_DYNJ_Summer16_JECV6'],
            sample_data=_sample,
            corrections="L1L2L3",
            # each quantity cut generates a different plot
            quantity_x=QUANTITY_X,
            quantities_y=_PF_ENERGY_FRACTIONS,
            colors_mc=_PF_ENERGY_FRACTION_COLORS,
            markers_data=_PF_ENERGY_FRACTION_MARKERS,
            y_label="PF Energy Fractions",
            y_range=(0, 1.15),
            # each selection cut generates a new plot
            selection_cuts=_SELECTION_CUTS,
            show_data_mc_comparison_as='difference percent',
            show_cut_info_text=False,
            show_as_profile=True,
            jec_version_label="Summer16 JEC V5 (Run{})".format(_sample['source_label'])
        )

        _ph.make_plots()


    for _sample in _SAMPLES_EE:
        break
        _ph = PlotHistograms2DQuantitiesProfile(
            basename="pf_energy_fractions_07Aug2017_JECV4_Run{}".format(_sample['source_label']),
            # there is one subplot per sample and cut in each plot
            sample_mc=SAMPLES['MC_Zee_DYNJ_Madgraph'],
            sample_data=_sample,
            corrections="L1L2L3",
            # each quantity cut generates a different plot
            quantity_x='zpt_log',
            quantities_y=_PF_ENERGY_FRACTIONS,
            colors_mc=_PF_ENERGY_FRACTION_COLORS,
            markers_data=_PF_ENERGY_FRACTION_MARKERS,
            y_label="PF Energy Fractions",
            y_range=(0, 1.15),
            # each selection cut generates a new plot
            selection_cuts=_SELECTION_CUTS,
            show_data_mc_comparison_as='difference percent',
            show_cut_info_text=False,
            show_as_profile=True,
            jec_version_label="Summer16 JEC V5 (Run{})".format(_sample['source_label'])
        )

        _ph.make_plots()
