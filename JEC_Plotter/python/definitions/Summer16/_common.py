import numpy as np

from Excalibur.JEC_Plotter.core import CutSet, btb_cut_factory

_Z_BOSON_MASS_GEV = 91.1876

# -- Selection cuts: systems of cuts to apply to a Sample

SELECTION_CUTS = dict(
    nocuts=CutSet('ZJetnocuts',
                  weights=["jet1idloose==1", "jet2idloose==1"],
                  labels=[r"${\\bf ZJet}$ no sel.",
                          #r"$\\mathrm{jet1,2ID}=\\mathrm{loose}$"
                         ],
                  zjet_folder='nocuts'),
    basiccuts=CutSet('ZJetbasic',
                     weights=["jet1idloose==1", "jet2idloose==1"],
                     labels=[r"${\\bf ZJet}$ basic sel.",
                             #r"$\\mathrm{jet1,2ID}=\\mathrm{loose}$"
                             ],
                     zjet_folder='basiccuts'),
    noalphanoetacuts=CutSet('ZJetnoalphanoetacuts',
                     weights=["zpt>30"],
                     labels=[r"${\\bf ZJet}$ basic sel.",
                             r"$p_\\mathrm{T}^\\mathrm{Z}>30~GeV$",
                             ],
                     zjet_folder='basiccuts'),
    noetacut=CutSet('ZJetnoalphanoetacuts',
                     weights=["zpt>30", "alpha<0.3"],
                     labels=[r"${\\bf ZJet}$ basic sel.",
                             r"$\\alpha<0.3$",
                             r"$p_\\mathrm{T}^\\mathrm{Z}>30~GeV$",
                             ],
                     zjet_folder='basiccuts'),
    noalphacut=CutSet('ZJetnoalphacut',
                     weights=["zpt>30", "abs(jet1eta)<1.3"],
                     labels=[r"${\\bf ZJet}$ basic sel.",
                             r"$p_\\mathrm{T}^\\mathrm{Z}>30~GeV$",
                             r"$|\\eta^\\mathrm{Jet1}|<1.3$",
                             ],
                     zjet_folder='basiccuts'),
    finalcuts=CutSet('ZJetfinal',
                     weights=["jet1idloose==1", "jet2idloose==1"],
                     labels=[r"${\\bf ZJet}$ final sel.",
                             #r"$\\mathrm{jet1,2ID}=\\mathrm{loose}$",
                             r"$\\alpha<0.3$",
                             r"$|\\eta^\\mathrm{Jet1}|<1.3$",
                             r"$p_\\mathrm{T}^\\mathrm{Z}>30~GeV$",
                             ],
                     zjet_folder='finalcuts'),
    extendedeta=CutSet("ZJetextendedeta",
                       weights=[
                           "jet1idloose==1", "jet2idloose==1",
                           "alpha<0.3",
                           "zpt>30",
                       ],
                       labels=[
                           r"${\\bf ZJet}~(extended~\\eta)$",
                           #r"$\\mathrm{jet1,2ID}=\\mathrm{loose}$",
                           r"$\\alpha<0.3$",
                           r"$p_\\mathrm{T}^\\mathrm{Z}>30~GeV$",
                       ],
                       zjet_folder='basiccuts'),
)

# -- Additional cuts: systems of cuts to apply to a Sample after selection

ADDITIONAL_CUTS = dict(
    eta=dict(
        central=CutSet('central',
                       weights=["abs(jet1eta)<1.3"],
                       labels=[r"$|\\eta^\\mathrm{Jet1}|<1.3$"]),
        medium=CutSet('mediumeta',
                      weights=["2.5<abs(jet1eta)", "abs(jet1eta)<3.2"],
                      labels=[r"$2.5<|\\eta^\\mathrm{Jet1}|<3.2$"]),
        high=CutSet('higheta',
                    weights=["3.2<abs(jet1eta)", "abs(jet1eta)<5.2"],
                    labels=[r"$3.2<|\\eta^\\mathrm{Jet1}|<5.2$"])
    ),
    alpha=dict(
        default=CutSet('default',
                       weights=["alpha<0.3"],
                       labels=[r"$\\alpha<0.3$"]
                       ),
    ),
    zpt=dict(
        zpt30=CutSet('zpt30',
                     weights=["zpt>30"],
                     labels=[r"$p_\\mathrm{T}^\\mathrm{Z}>30~GeV$"]),
        low=CutSet('lowzpt',
                   weights=["zpt<60"],
                   labels=[r"$p_\\mathrm{T}^\\mathrm{Z}<60~GeV$"]),
    ),
    btb=dict(
        btb054=btb_cut_factory(0.54),
        btb034=btb_cut_factory(0.34),
        btb010=btb_cut_factory(0.10),
        btb005=btb_cut_factory(0.05),
    ),
    user=dict(
        basicToFinal=CutSet("basicToFinal",
                            weights=[
                                "alpha<0.3",
                                "abs(jet1eta)<1.3",
                                "zpt>30",
                            ],
                            labels=[
                                r"$\\alpha<0.3$",
                                r"$|\\eta^\\mathrm{Jet1}|<1.3$",
                                r"$p_\\mathrm{T}^\\mathrm{Z}>30~GeV$",
                            ]
                            ),
        likeZJetfinal=CutSet("likeZJetfinal",
                             weights=[
                                 "abs(jet1eta)<1.3",
                                 "alpha<0.3",
                                 "mu1pt>20",
                                 "mu2pt>20",
                                 "jet1pt>12",
                                 "abs(mu1eta)<2.3",
                                 "abs(mu2eta)<2.3",
                                 "zmass>{:.4f}&&zmass<{:.4f}".format(_Z_BOSON_MASS_GEV - 20.,
                                                                     _Z_BOSON_MASS_GEV + 20.),
                                 "zpt>30",
                                 "abs(abs({a}phi-{b}phi)-{pi:7.6f})<0.34".format(a='jet1', b='z', pi=np.pi),
                             ],
                             labels=[
                                 # r"standard selection cuts, including:",
                                 r"$\\alpha<0.3$",
                                 r"$|\\eta^\\mathrm{Jet1}|<1.3$",
                                 r"$\\Delta\\phi(Jet1,Z)<2.8 \\approx\\pi+0.34$"
                             ]
                             ),
        higgsCrosscheck=CutSet('higgsCrosscheck',
                               weights=[
                                   "abs(jet1eta)<2.5",
                                   "alpha<0.3",
                                   "met<40",
                                   "mu1pt>25",
                                   "mu2pt>20",
                                   "abs(mu1eta)<2.1",
                                   "abs(mu2eta)<2.1",
                                   "zmass>80&&zmass<100",
                                   "zpt>100&&zpt<150",
                                   "abs(abs({a}phi-{b}phi)-{pi:7.6f})<0.3".format(a='jet1', b='z', pi=np.pi),
                               ],
                               labels=[
                                   r"Higgs group cuts",
                                   r"$\\alpha<0.3$",
                                   r"$|\\eta^\\mathrm{Jet1}|<2.5$",
                                   r"$\\Delta\\phi(Jet1,Z)<2.6 \\approx \\pi+0.54$"
                               ]),
    ),
    pileup=dict(
        jet1pt50=CutSet("jet1pt50", ["jet1pt>50"], [r"$\\mathrm{p}^{Jet1}_T > 50~GeV$"]),
        jet1pt40=CutSet("jet1pt40", ["jet1pt>40"], [r"$\\mathrm{p}^{Jet1}_T > 40~GeV$"]),
        jet1pt30=CutSet("jet1pt30", ["jet1pt>30"], [r"$\\mathrm{p}^{Jet1}_T > 30~GeV$"]),
        jet1pt20=CutSet("jet1pt20", ["jet1pt>20"], [r"$\\mathrm{p}^{Jet1}_T > 20~GeV$"]),
        asymmPt02=CutSet("asymmPt02", ["(jet1pt-jet2pt)/(jet1pt+jet2pt)>0.2"],
                         ["$A_{p,T}^{Jet1} > 0.2$"]),
        ratioPt2=CutSet("ratioPt2", ["jet1pt/jet2pt>2"],
                        [r"$\\mathrm{p}^{Jet1}_T/\\mathrm{p}^{Jet2}_T > 2$"]),

    ),
)

# -- 2016 Run Periods

_run_ranges = dict(
    runB=(272007, 275376),
    runC=(275657, 276283),
    runD=(276315, 276811),
    runE=(276831, 277420),
    runF=(277772, 278808),
    runG=(278820, 280385),
    runH=(280919, 284044),
)

ADDITIONAL_CUTS['run_periods'] = dict()
for _run_name, _run_range in _run_ranges.iteritems():
    ADDITIONAL_CUTS['run_periods'].update({
        _run_name: CutSet(
            _run_name,
            weights=[
                "((run>={}&&run<={})||run==1)".format(  # exclude MC from cut
                    _run_range[0],
                    _run_range[1],
                )
            ],
            labels=["{}".format(_run_name)]
        )
    })


# -- Summer16 JEC Intervals of Validity

_jec_iovs = dict(
    BCD=(272007, 276811),
    EFearly=(276831, 278801),
    #FlateG=(278802, 280385),
    #H=(280919, 284044),
    FlateGH=(278802, 284044),
)

ADDITIONAL_CUTS['jec_iovs'] = dict()
for _jec_iov, _jec_iov_range in _jec_iovs.iteritems():
    ADDITIONAL_CUTS['jec_iovs'].update({
        _jec_iov: CutSet(
            _jec_iov,
            weights=[
                "((run>={}&&run<={})||run==1)".format(  # exclude MC from cut
                    _jec_iov_range[0],
                    _jec_iov_range[1],
                )
            ],
            labels=["{}".format(_jec_iov)]
        )
    })

    # _alljet_cuts = []
    # for _jet in ['jet1', 'jet2', 'jet3']:
    #     "({jet}eta>{0}&&{jet}eta<{1}&&{jet}phi>{2}&&{jet}phi<{3})".format(
    #         _hcal_hot_eta_ranges[_run][0],
    #         _hcal_hot_eta_ranges[_run][1],
    #         _hcal_hot_phi_ranges[_run][0],
    #         _hcal_hot_phi_ranges[_run][1],
    #         jet=_jet
    #     ),
    # 
    # _cutname = _run
    # ADDITIONAL_CUTS['hcal_hot_towers'].update({
    #     _cutname: CutSet(
    #         _cutname,
    #         weights=[
    #             "run>=272007&&run<=275376".format(
    #                 _run_range[0],
    #                 _run_range[1],
    #             ),
    #             "({jet}eta>{0}&&{jet}eta<{1}&&{jet}phi>{2}&&{jet}phi<{3})".format(
    #                 _hcal_hot_eta_ranges[_run][0],
    #                 _hcal_hot_eta_ranges[_run][1],
    #                 _hcal_hot_phi_ranges[_run][0],
    #                 _hcal_hot_phi_ranges[_run][1],
    #                 jet=_jet
    #             ),
    #         ],
    #         labels=["{} HCAL hot tower regions, {}".format(_run, _jet)]
    #     )
    # })
