from Excalibur.JEC_Plotter.core import Combination
from Excalibur.JEC_Plotter.definitions.Summer16.samples_07Aug2017 import (
    SAMPLES
)

if __name__ == "__main__":
    _c = Combination(
        sample_data=SAMPLES['Data_Zmm_BCDEFGH'],
        sample_mc=SAMPLES['MC_Zmm_DYJets_Madgraph'],
        global_selection=None,
        alpha_upper_bin_edges=[0.3],
        eta_bin_edges=[0, 0.65, 1.3],
    )
    _c.run()
