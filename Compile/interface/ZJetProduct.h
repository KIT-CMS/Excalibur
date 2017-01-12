#pragma once

#include "Artus/KappaAnalysis/interface/KappaProduct.h"
#include "Artus/Utility/interface/SafeMap.h"
#include <math.h>
#include <boost/ptr_container/ptr_map.hpp>

/**
   \brief Container class for everything that can be produced in pipeline.

   Defines any outcome that could be produced by a KappaProducer during a common analysis chain in a
   given KappaPipeline. Via the PipelineRunner the KappaProduct all extra products in the analysis
   chain will be passed on to subsequent Producers, Filters and Consumers.
*/

class ZJetProduct : public KappaProduct
{
  public:
    ZJetProduct() : KappaProduct() {}
    //Tags for debugging ZProducer
    bool m_validgenzfound = false;
    bool m_genzfound = false;

    // Added by ZJetCorrectionsProducer, shared pointers are necessary to keep the jets in the
    // product after creation
    std::map<std::string, std::vector<std::shared_ptr<KJet>>> m_correctedZJets;

    // Added by ZJetCorrectionsProducer, necessary to cross-check the applied JEC factors: pT of
    // jets has to be saved BEFORE sorting
    float jetpt_l1 = 0;
    float jetpt_rc = 0;
    float jetpt_l1l2l3 = 0;
    float jetpt_l1l2l3res = 0;

    // Added by TypeIMETProducer
    std::map<std::string, KMET> m_corrMET;

    // Added by RecoJetGenPartonMatchingProducer
    std::map<std::string, std::map<KJet*, KGenParticle*>> m_matchedGenPartons;

    // Added by RecoJetGenJetMatchingProducer
    boost::ptr_map<std::string, std::vector<int>> m_matchedGenJets;

    // Added by NPUProducer
    float npumean_data = -1.0;

    // Added by NeutrinoCounter
    long n_neutrinos = 0;

    /////////////////////////////
    // Functions for Consumers //
    /////////////////////////////

    // Access to valid/corrected jets
    unsigned long GetValidJetCount(ZJetSettings const& settings,
                                   ZJetEvent const& event,
                                   std::string corrLevel) const
    {
        // Gen jets are always valid
        if (corrLevel == "Gen") {
            return event.m_genJets->size();
        }
        // Uncorrected valid jet
        else if (corrLevel == "None") {
            return m_validJets.size();
        }
        // Corrected valid jet
        else {
            return SafeMap::Get(m_correctedZJets, corrLevel).size();
        }
    }

    unsigned long GetValidJetCount(ZJetSettings const& settings, ZJetEvent const& event) const
    {
        return GetValidJetCount(settings, event, settings.GetCorrectionLevel());
    }

    KLV* GetValidJet(ZJetSettings const& settings,
                     ZJetEvent const& event,
                     unsigned long index,
                     std::string corrLevel) const
    {
        assert(GetValidJetCount(settings, event, corrLevel) > index);

        // Gen jets
        if (corrLevel == "Gen") {
            return &(event.m_genJets->at(index));
        }
        // Uncorrected valid jet
        else if (corrLevel == "None") {
            return static_cast<KLV*>(m_validJets[index]);
        }
        // Corrected valid jet
        else {
            return (SafeMap::Get(m_correctedZJets, corrLevel)[index]).get();
        }
    }

    KLV* GetValidJet(ZJetSettings const& settings,
                     ZJetEvent const& event,
                     unsigned long index) const
    {
        return GetValidJet(settings, event, index, settings.GetCorrectionLevel());
    }

    KLV* GetValidPrimaryJet(ZJetSettings const& settings, ZJetEvent const& event) const
    {
        return GetValidJet(settings, event, 0, settings.GetCorrectionLevel());
    }

    // we cant use the KappaProduct function here since our jet collections are different
    unsigned int CountValidJetsAbovePt(ZJetSettings const& settings,
                                       ZJetEvent const& event,
                                       float ptthreshold) const
    {
        return CountValidJetsAbovePt(settings, event, ptthreshold, settings.GetCorrectionLevel());
    }

    unsigned int CountValidJetsAbovePt(ZJetSettings const& settings,
                                       ZJetEvent const& event,
                                       float ptthreshold,
                                       std::string corrLevel) const
    {
        unsigned int count = 0;
        for (unsigned int i = 0; i < GetValidJetCount(settings, event, corrLevel); ++i) {
            if (GetValidJet(settings, event, i, corrLevel)->p4.Pt() > ptthreshold) {
                count += 1;
            } else {
                return count;  // pT doesn't increase again, stop counting
            }
        }
        return count;
    }

    // Access to invalid jets
    unsigned long GetInvalidJetCount(ZJetSettings const& settings,
                                     ZJetEvent const& event,
                                     std::string corrLevel) const
    {
        // Gen jets are always valid
        if (corrLevel == "Gen") {
            return 0;
        }
        // Invalid jets, no need for different correction levels
        else {
            return m_invalidJets.size();
        }
    }

    unsigned long GetInvalidJetCount(ZJetSettings const& settings, ZJetEvent const& event) const
    {
        return GetInvalidJetCount(settings, event, settings.GetCorrectionLevel());
    }

    // Access to (un)corrected MET
    KMET* GetMet(ZJetSettings const& settings, ZJetEvent const& event, std::string corrLevel) const
    {
        // Only L3 is corrected in TypeIMETProducer
        if ((std::string::npos != corrLevel.find("L3")) ||
            (std::string::npos != corrLevel.find("Res"))) {
            return const_cast<KMET*>(&(m_corrMET.at(corrLevel)));
        } else {
            return event.m_met;
        }
    }

    KMET* GetMet(ZJetSettings const& settings, ZJetEvent const& event) const
    {
        return GetMet(settings, event, settings.GetCorrectionLevel());
    }

    //Calculate Phi* eta
    double GetPhiStarEta(ZJetEvent const& event) const
    {
	KLepton* muplus;
	KLepton* muminus;
	if (m_zLeptons.first->charge()>0)
	{
		muplus = m_zLeptons.first;
		muminus = m_zLeptons.second;
	}
	else 
	{
		muplus = m_zLeptons.second;
		muminus = m_zLeptons.first;
	}
	return(CalcPhiStarEta<KLepton*>(muplus, muminus));
    }
    double GetGenPhiStarEta(ZJetEvent const& event) const
    {
	KGenParticle* muplus;
	KGenParticle* muminus;
	if (m_genLeptonsFromBosonDecay[0]->charge()>0)
	{
		muplus = m_genLeptonsFromBosonDecay[0];
		muminus = m_genLeptonsFromBosonDecay[1];
	}
	else 
	{
		muplus = m_genLeptonsFromBosonDecay[1];
		muminus = m_genLeptonsFromBosonDecay[0];
	}
	return(CalcPhiStarEta<KGenParticle*>(muplus, muminus));
    }

    template <class TParticle>
    double CalcPhiStarEta(TParticle muplus, TParticle muminus) const
    {
	double pi = 3.1415926535;
	double phiacop = pi - std::min(fabs(muminus->p4.Phi()-muplus->p4.Phi()),2*pi-fabs(muminus->p4.Phi()-muplus->p4.Phi()));
	double thetastar = acos(tanh((muminus->p4.Eta()-muplus->p4.Eta())/2));
	return(tan(phiacop/2)*sin(thetastar));
    }

    // Calculate MPF
    double GetMPF(const KLV* met) const
    {
        double scalPtEt = m_z.p4.Px() * met->p4.Px() + m_z.p4.Py() * met->p4.Py();
        double scalPtSq = m_z.p4.Px() * m_z.p4.Px() + m_z.p4.Py() * m_z.p4.Py();
        return 1.0 + scalPtEt / scalPtSq;
    }

    // Reco jet - gen parton matching result
    KGenParticle* GetMatchedGenParton(ZJetEvent const& event,
                                      ZJetSettings const& settings,
                                      unsigned long index) const
    {
        if (GetValidJetCount(settings, event) > index)
            return SafeMap::GetWithDefault(
                SafeMap::GetWithDefault(m_matchedGenPartons, settings.GetCorrectionLevel(),
                                        std::map<KJet*, KGenParticle*>()),
                static_cast<KJet*>(GetValidJet(settings, event, index)),
                static_cast<KGenParticle*>(nullptr));
        else
            return nullptr;
    }

    // Reco jet - gen jet matching result
    KLV* GetMatchedGenJet(ZJetEvent const& event,
                          ZJetSettings const& settings,
                          unsigned long index) const
    {
        std::vector<int> defaultValue = std::vector<int>(0);
        std::vector<int> jetList = SafeMap::GetPtrMapWithDefault(
            m_matchedGenJets, settings.GetCorrectionLevel(), defaultValue);

        if (index >= jetList.size())
            return nullptr;

        unsigned long matchedJet = static_cast<unsigned long>(jetList.at(index));

        if (GetValidJetCount(settings, event, "Gen") >= matchedJet)
            return GetValidJet(settings, event, matchedJet, "Gen");
        else
            return nullptr;
    }

    // Access to gen Z
    KGenParticle* GetGenZ() const
    {
        std::vector<KGenParticle*> genZs =
            SafeMap::GetWithDefault(m_genParticlesMap, 23, (std::vector<KGenParticle*>)(0));
        return (genZs.size() > 0) ? genZs[0] : nullptr;
    }

    // Reco muon - gen muon matching result
    KGenParticle* GetMatchedGenMuon(ZJetEvent const& event,
                                    ZJetSettings const& settings,
                                    unsigned int index) const
    {
        if (m_validMuons.size() > index)
            return SafeMap::GetWithDefault(m_genParticleMatchedMuons, m_validMuons.at(index),
                                           static_cast<KGenParticle*>(nullptr));
        else
            return nullptr;
    }
    // Reco electron - gen electorn matching result
    KGenParticle* GetMatchedGenElectron(ZJetEvent const& event,
                                        ZJetSettings const& settings,
                                        unsigned int index) const
    {
        if (m_validElectrons.size() > index)
            return SafeMap::GetWithDefault(m_genParticleMatchedElectrons,
                                           m_validElectrons.at(index),
                                           static_cast<KGenParticle*>(nullptr));
        else
            return nullptr;
    }
};
