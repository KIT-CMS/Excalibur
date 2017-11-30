import numpy as np

from copy import deepcopy

from Excalibur.JEC_Plotter.core import Sample
from _common import *

# -- Samples: each sample is a ROOT file containing Excalibur output

_SAMPLE_DIR = "/storage/c/tberger/excalibur_results_calibration/Summer16_07Aug2017_V1_2017-11-13"

SAMPLES = {
    'Data_Zmm_BCDEFGH': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='data16_mm_BCDEFGH_DoMuLegacy.root'
    ),
    'Data_Zmm_BCD': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='data16_mm_BCD_DoMuLegacy.root'
    ),
    # 'MC_Zmm_DYJets_Madgraph': Sample.load_using_convention(
    #     sample_dir=_SAMPLE_DIR,
    #     sample_file='mc16_mm_BCDEFGH_DYJets_Madgraph.root'
    # ),
    'MC_Zmm_DYNJ_Madgraph': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='mc16_mm_BCDEFGH_DYNJ_Madgraph.root'
    ),
    'Data_Zee_BCDEFGH': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='data16_ee_BCDEFGH_DoElLegacy.root'
    ),
    'Data_Zee_BCD': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='data16_ee_BCD_DoElLegacy.root'
    ),
    # 'MC_Zee_DYJets_Madgraph': Sample.load_using_convention(
    #     sample_dir=_SAMPLE_DIR,
    #     sample_file='mc16_ee_BCDEFGH_DYJets_Madgraph.root'
    # ),
    'MC_Zee_DYNJ_Madgraph': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='mc16_ee_BCDEFGH_DYNJ_Madgraph.root'
    ),
    'Data_Zmm_BCD_noetaphiclean': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='data16_mm_BCD_DoMuLegacy_noetaphiclean.root'
    ),
    'Data_Zee_BCD_noetaphiclean': Sample.load_using_convention(
        sample_dir=_SAMPLE_DIR,
        sample_file='data16_ee_BCD_DoElLegacy_noetaphiclean.root'
    ),
}

# -- Additional Cuts

# -- HCAL hot towers eta ranges

_hcal_hot_eta_ranges = dict(
    runB=(-2.172, -2.043),
    runC=(-3.314, -3.139),
    runD=(-3.489, -3.139),
)

_hcal_hot_phi_ranges = dict(
    runB=(2.290, 2.422),
    runC=(2.237, 2.475),
    runD=(2.237, 2.475),
)

#ADDITIONAL_CUTS = deepcopy(ADDITIONAL_CUTS)
ADDITIONAL_CUTS['hcal_hot_towers'] = dict()
for _run_name, _run_range_cutset in ADDITIONAL_CUTS['run_periods'].iteritems():
    if _run_name not in _hcal_hot_eta_ranges:
        continue
    for _jet in ['jet1', 'jet2', 'jet3']:
        _cutname = _run_name + '_' + _jet
        ADDITIONAL_CUTS['hcal_hot_towers'].update({
            _cutname: CutSet(
                _cutname,
                weights=_run_range_cutset.weights_list + [
                    "({jet}eta>{0}&&{jet}eta<{1}&&{jet}phi>{2}&&{jet}phi<{3})".format(
                        _hcal_hot_eta_ranges[_run_name][0],
                        _hcal_hot_eta_ranges[_run_name][1],
                        _hcal_hot_phi_ranges[_run_name][0],
                        _hcal_hot_phi_ranges[_run_name][1],
                        jet=_jet
                    ),
                ],
                labels=["{} HCAL hot tower regions, {}".format(_run_name, _jet)]
            )
        })


# TODO: compute automatically from 'hcal_hot_towers' cuts
ADDITIONAL_CUTS['user'].update(
    dict(
        adhocEtaPhiBCD_pt0=CutSet("adhocEtaPhiBCD_pt0",
                              weights=[
                                  # run B veto
                                  "(1.0-(run>=272007&&run<=275376&&("
                                    "(jet1eta>-2.172&&jet1eta<-2.073&&jet1phi>2.290&&jet1phi<2.422&&jet1pt>0)||"
                                    "(jet2eta>-2.172&&jet2eta<-2.073&&jet2phi>2.290&&jet2phi<2.422&&jet2pt>0)||"
                                    "(jet3eta>-2.172&&jet3eta<-2.073&&jet3phi>2.290&&jet3phi<2.422&&jet3pt>0)"
                                  ")))",
                                  # run C veto
                                  "(1.0-(run>=275657&&run<=276283&&("
                                    "(jet1eta>-3.314&&jet1eta<-3.139&&jet1phi>2.237&&jet1phi<2.475&&jet1pt>0)||"
                                    "(jet2eta>-3.314&&jet2eta<-3.139&&jet2phi>2.237&&jet2phi<2.475&&jet2pt>0)||"
                                    "(jet3eta>-3.314&&jet3eta<-3.139&&jet3phi>2.237&&jet3phi<2.475&&jet3pt>0)"
                                  ")))",
                                  # run D veto
                                  "(1.0-(run>=276315&&run<=276811&&("
                                    "(jet1eta>-3.489&&jet1eta<-3.139&&jet1phi>2.237&&jet1phi<2.475&&jet1pt>0)||"
                                    "(jet2eta>-3.489&&jet2eta<-3.139&&jet2phi>2.237&&jet2phi<2.475&&jet2pt>0)||"
                                    "(jet3eta>-3.489&&jet3eta<-3.139&&jet3phi>2.237&&jet3phi<2.475&&jet3pt>0)"
                                  ")))"
                              ],
                              labels=[
                                  r"ad-hoc BCD eta-phi cleaning",
                              ]
        ),
        adhocEtaPhiBCD_pt15=CutSet("adhocEtaPhiBCD_pt15",
                              weights=[
                                  # run B veto
                                  "(1.0-(run>=272007&&run<=275376&&("
                                    "(jet1eta>-2.172&&jet1eta<-2.073&&jet1phi>2.290&&jet1phi<2.422&&jet1pt>15)||"
                                    "(jet2eta>-2.172&&jet2eta<-2.073&&jet2phi>2.290&&jet2phi<2.422&&jet2pt>15)||"
                                    "(jet3eta>-2.172&&jet3eta<-2.073&&jet3phi>2.290&&jet3phi<2.422&&jet3pt>15)"
                                  ")))",
                                  # run C veto
                                  "(1.0-(run>=275657&&run<=276283&&("
                                    "(jet1eta>-3.314&&jet1eta<-3.139&&jet1phi>2.237&&jet1phi<2.475&&jet1pt>15)||"
                                    "(jet2eta>-3.314&&jet2eta<-3.139&&jet2phi>2.237&&jet2phi<2.475&&jet2pt>15)||"
                                    "(jet3eta>-3.314&&jet3eta<-3.139&&jet3phi>2.237&&jet3phi<2.475&&jet3pt>15)"
                                  ")))",
                                  # run D veto
                                  "(1.0-(run>=276315&&run<=276811&&("
                                    "(jet1eta>-3.489&&jet1eta<-3.139&&jet1phi>2.237&&jet1phi<2.475&&jet1pt>15)||"
                                    "(jet2eta>-3.489&&jet2eta<-3.139&&jet2phi>2.237&&jet2phi<2.475&&jet2pt>15)||"
                                    "(jet3eta>-3.489&&jet3eta<-3.139&&jet3phi>2.237&&jet3phi<2.475&&jet3pt>15)"
                                  ")))"
                              ],
                              labels=[
                                  r"ad-hoc BCD eta-phi cleaning",
                              ]
        ),
    )
)

if __name__ == "__main__":
    for _sn, _s in SAMPLES.iteritems():
        print "Sample '{}':".format(_sn)
        for k, v in _s._dict.iteritems():
            print "\t{}: {}".format(k, v)
