#pragma once

#include "Excalibur/Compile/interface/ZJetTypes.h"
#include "TFile.h"
#include "TF1.h"
#include "TH2.h"
#include <memory>

enum fluctuations { central = 0, up, down, upStat, downStat, upSyst, downSyst };


class PrefiringWeightProducer : public ZJetProducerBase {
    public:
        std::string GetProducerId() const override;
        PrefiringWeightProducer() : ZJetProducerBase() {};
        void Init(ZJetSettings const& settings);
        void Produce(ZJetEvent const& event,
                     ZJetProduct& product,
                     ZJetSettings const& settings) const override;

    private:
        double getPrefiringRateEcal(double eta, double pt, TH2F* h_prefmap, fluctuations fluctuation) const;
        double getPrefiringRateMuon(double eta, double phi, double pt, fluctuations fluctuation) const;

        std::unique_ptr<TFile> file_prefiringmaps_;
        std::unique_ptr<TFile> file_prefiringparams_;

        // Verwendung von unique_ptr für TF1-Objekte
        std::unique_ptr<TF1> parametrization0p0To0p2_;
        std::unique_ptr<TF1> parametrization0p2To0p3_;
        std::unique_ptr<TF1> parametrization0p3To0p55_;
        std::unique_ptr<TF1> parametrization0p55To0p83_;
        std::unique_ptr<TF1> parametrization0p83To1p24_;
        std::unique_ptr<TF1> parametrization1p24To1p4_;
        std::unique_ptr<TF1> parametrization1p4To1p6_;
        std::unique_ptr<TF1> parametrization1p6To1p8_;
        std::unique_ptr<TF1> parametrization1p8To2p1_;
        std::unique_ptr<TF1> parametrization2p1To2p25_;
        std::unique_ptr<TF1> parametrization2p25To2p4_;
        std::unique_ptr<TF1> parametrizationHotSpot_;

        TH2F* h_prefmap_photon_;
        TH2F* h_prefmap_jet_;
        std::string dataeraEcal_;
        std::string dataeraMuon_;
        bool useEMpt_;
        double prefiringRateSystUncEcal_;
        double prefiringRateSystUncMuon_;
        double jetMaxMuonFraction_;
        bool missingInputEcal_;
        bool missingInputMuon_;
        bool isData_;
};
