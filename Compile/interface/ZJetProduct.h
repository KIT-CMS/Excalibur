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

    // Added by JetRecoilProducer
    std::map<std::string, KLV> m_correctedJetRecoils;

    // Added by RecoJetGenPartonMatchingProducer
    std::map<std::string, std::map<KJet*, KGenParticle*>> m_matchedGenPartons;
    std::vector<KGenParticle*> m_genPartons;

    // Added by RecoJetGenJetMatchingProducer
    boost::ptr_map<std::string, std::vector<int>> m_matchedGenJets;
    
    // Added by PartonProducer
    std::vector<KGenParticle*> m_partons;

    // Added by NPUProducer
    float npumean_data = -1.0;

    // Added by NeutrinoCounter
    long n_neutrinos = 0;
    
    // Added by ZJetDressedMuonsProducer
    std::vector<KGenParticle*> m_genPhotons;
    RMFLV m_truez;
    bool m_truezfound = false;

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
            //return ((KLVs*) event.m_genJets)->size();
            return m_simpleGenJets.size();
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
        //assert(GetValidJetCount(settings, event, corrLevel) > index);
        if (GetValidJetCount(settings, event, corrLevel) <= index) {
            return 0;
        }

        // Gen jets
        if (corrLevel == "Gen") {
            if (!settings.GetUseKLVGenJets()) {
               throw std::runtime_error("ZJets analysis must set 'UseKLVGenJets' flag to true!");
            }
            // need to cast from vector of KGenJet to vector of KLVs before getting index!
            //return &(((KLVs*) event.m_genJets)->at(index));
            return static_cast<KLV*>(m_simpleGenJets[index]);
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
    
    KLV* GetInvalidJet(ZJetSettings const& settings,
                     ZJetEvent const& event,
                     unsigned long index,
                     std::string corrLevel) const
    {
        assert(GetInvalidJetCount(settings, event, corrLevel) > index);

        // Invalid jets, no need for different correction levels
        return static_cast<KLV*>(m_invalidJets[index]);
    }

    KLV* GetInvalidJet(ZJetSettings const& settings,
                     ZJetEvent const& event,
                     unsigned long index) const
    {
        return GetInvalidJet(settings, event, index, settings.GetCorrectionLevel());
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

    // get the jet recoil for all correction levels
    const KLV* GetJetRecoil(ZJetSettings const& settings,
                            ZJetEvent const& event,
                            std::string corrLevel) const
    {
        std::map<std::string, KLV>::const_iterator it = m_correctedJetRecoils.find(corrLevel);
        if (it == m_correctedJetRecoils.end()) {
            // no jet recoil available
            return nullptr;
        }
        return &(it->second);
    }

    // get the jet recoil for the current correction level
    const KLV* GetJetRecoil(ZJetSettings const& settings,
                            ZJetEvent const& event) const
    {
        return GetJetRecoil(settings, event, settings.GetCorrectionLevel());
    }

    KMET* GetMet(ZJetSettings const& settings, ZJetEvent const& event) const
    {
        return GetMet(settings, event, settings.GetCorrectionLevel());
    }

	double GetGenHT(ZJetEvent const& event) const
	{
		double HT = 0;
		for (unsigned int idx = 0; idx<event.m_genParticles->size(); idx++)
		 { if(event.m_genParticles->at(idx).isHardProcess()==1 
				&& !( std::abs(event.m_genParticles->at(idx).pdgId ) == 23 ) 
				&& !( std::abs(event.m_genParticles->at(idx).pdgId ) == 13 ) 
				&& !( std::abs(event.m_genParticles->at(idx).pdgId ) == 11 ) )
	                 { HT += event.m_genParticles->at(idx).p4.Pt();}
		   }
	return HT;
	}

	double GetHT(ZJetSettings const& settings, ZJetEvent const& event) const
	
	{  	double HT = 0;
		for (unsigned int idx = 0; idx<GetValidJetCount(settings, event); idx++)
			{if (GetValidJet(settings, event, idx)->p4.Pt() > 30)  HT += GetValidJet(settings, event, idx)->p4.Pt(); }
		return HT;
	}

    //Calculate Phi* eta
    double GetPhiStarEta(ZJetEvent const& event) const {
        //KGenParticle* muplus;
        //KGenParticle* muminus;
        //if (m_zLeptons.first->charge()>0) {
        //    muplus = m_zLeptons.first;
        //    muminus = m_zLeptons.second;
        //}
        //else {
        //    muplus = m_zLeptons.second;
        //    muminus = m_zLeptons.first;
        //}
        //return(CalcPhiStarEta(muplus, muminus));
        KLepton* muone;
        KLepton* mutwo;
        muone = m_zLeptons.first;
        mutwo = m_zLeptons.second;
        return(CalcPhiStarEta(muone, mutwo));
    }

    double GetGenPhiStarEta(ZJetEvent const& event) const {
        //KGenParticle* muplus;
        //KGenParticle* muminus;
        //if (m_genLeptonsFromBosonDecay[0]->charge()>0) {
        //    muplus = m_genLeptonsFromBosonDecay[0];
        //    muminus = m_genLeptonsFromBosonDecay[1];
        //}
        //else {
        //    muplus = m_genLeptonsFromBosonDecay[1];
        //    muminus = m_genLeptonsFromBosonDecay[0];
        //}
        //return(CalcPhiStarEta(muplus, muminus));
        KGenParticle* muone;
        KGenParticle* mutwo;
        muone = m_genLeptonsFromBosonDecay[0];
        mutwo = m_genLeptonsFromBosonDecay[1];
        return(CalcPhiStarEta(muone, mutwo));
    }


    //template <class TParticle>
    //double CalcPhiStarEta(TParticle muplus, TParticle muminus) const
    //{
	//double pi = 3.1415926535;
	//double phiacop = pi - std::min<double>(fabs(muminus->p4.Phi()-muplus->p4.Phi()),2*pi-fabs(muminus->p4.Phi()-muplus->p4.Phi()));
	//double thetastar = acos(tanh((muminus->p4.Eta()-muplus->p4.Eta())/2));
	//return(tan(phiacop/2)*sin(thetastar));
    //}
    double CalcPhiStarEta(const KLV* muplus, const KLV* muminus) const
    {
        double pi = 3.1415926535;
        double phiacop = pi - std::min<double>(fabs(muminus->p4.Phi()-muplus->p4.Phi()),2*pi-fabs(muminus->p4.Phi()-muplus->p4.Phi()));
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

    // Calculate splitted MPFs
    // MPF_lead
    double GetMPFlead(ZJetSettings const& settings, ZJetEvent const& event, std::string corrLevel) const
    {
        if(GetValidJetCount(settings, event, corrLevel) < 1) {
            return 0;
        }
        else {
            KLV* leadingjet = GetValidJet(settings, event, 0, corrLevel);
            if(leadingjet->p4.Pt() < settings.GetMPFSplittingJetPtMin()) return 0;

            double scalPtEt = m_z.p4.Px() * leadingjet->p4.Px() + m_z.p4.Py() * leadingjet->p4.Py();
            double scalPtSq = m_z.p4.Px() * m_z.p4.Px() + m_z.p4.Py() * m_z.p4.Py();
            return - scalPtEt / scalPtSq;
        }
    }

    double GetMPFlead(ZJetSettings const& settings, ZJetEvent const& event) const
    {
        return GetMPFlead(settings, event, settings.GetCorrectionLevel());
    }

    // MPF_jets
    double GetMPFjets(ZJetSettings const& settings, ZJetEvent const& event, std::string corrLevel) const
    {
        if(GetValidJetCount(settings, event, corrLevel) < 2) {
            return 0;
        }
        else
        {
            double scalPtEt = 0;
            double scalPtSq = m_z.p4.Px() * m_z.p4.Px() + m_z.p4.Py() * m_z.p4.Py();
            for(uint index = 1; index < GetValidJetCount(settings, event, corrLevel); index++)
            {
                KLV* jet = GetValidJet(settings, event, index, corrLevel);
                if(jet->p4.Pt() < settings.GetMPFSplittingJetPtMin()) break;

                scalPtEt += m_z.p4.Px() * jet->p4.Px() + m_z.p4.Py() * jet->p4.Py();
            }
            return - scalPtEt / scalPtSq;
        }
    }

    double GetMPFjets(ZJetSettings const& settings, ZJetEvent const& event) const
    {
        return GetMPFjets(settings, event, settings.GetCorrectionLevel());
    }

    // MPF_unclustered
    double GetMPFunclustered(ZJetSettings const& settings, ZJetEvent const& event, std::string corrLevel) const
    {
        //TODO: #57 implement independent calculation of the unclustered energy contribution
        return GetMPF(GetMet(settings, event, corrLevel)) - GetMPFlead(settings, event, corrLevel) - GetMPFjets(settings, event, corrLevel);
    }

    double GetMPFunclustered(ZJetSettings const& settings, ZJetEvent const& event) const
    {
        return GetMPFunclustered(settings, event, settings.GetCorrectionLevel());
    }

    // Helper method for MPF
    double GetNegativeTransverseProjectionFraction(const KLV* klvProj, const KLV* klvRef) {
        double scalPtEt = klvRef->p4.Px() * klvProj->p4.Px() + klvRef->p4.Py() * klvProj->p4.Py();
        double scalPtSq = klvRef->p4.Px() * klvRef->p4.Px()  + klvRef->p4.Py() * klvRef->p4.Py();
        return -scalPtEt / scalPtSq;
    }

    // Calculate JNPF
    double GetJNPF(ZJetSettings const& settings, ZJetEvent const& event, std::string corrLevel) const
    {
        if(GetValidJetCount(settings, event, corrLevel) < 1) return DefaultValues::UndefinedDouble;
        else 
        {
            double scalPtEt = 0;
            double scalPtSqjet = 0;
            KLV* met = GetMet(settings, event, corrLevel);
            for(uint index = 1; index < GetValidJetCount(settings, event, corrLevel); index++)
            {    
                KLV* jet = GetValidJet(settings, event, index, corrLevel);
                scalPtEt += jet->p4.Px() * met->p4.Px() + jet->p4.Py() * met->p4.Py() + jet->p4.Pz() * met->p4.Pz();
                scalPtSqjet += jet->p4.Px() * jet->p4.Px()  + jet->p4.Py() * jet->p4.Py() + jet->p4.Pz() * jet->p4.Pz();
            }
            double scalPtSqmet = met->p4.Px() * met->p4.Px()  + met->p4.Py() * met->p4.Py() + met->p4.Pz() * met->p4.Pz();

            if(scalPtSqjet == 0 || scalPtSqmet == 0) return DefaultValues::UndefinedDouble;
            return scalPtEt / (sqrt(scalPtSqjet) * sqrt(scalPtSqmet));
        }
    }

    double GetJNPF(ZJetSettings const& settings, ZJetEvent const& event) const
    {
        return GetJNPF(settings, event, settings.GetCorrectionLevel());
    }

    // Calculate RPF
    double GetRPF(const KLV* jetRecoil) const
    {
        double scalPtEt = m_z.p4.Px() * jetRecoil->p4.Px() + m_z.p4.Py() * jetRecoil->p4.Py();
        double scalPtSq = m_z.p4.Px() * m_z.p4.Px() + m_z.p4.Py() * m_z.p4.Py();
        return -scalPtEt / scalPtSq;
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
    KGenParticle* GetTrueZ(ZJetEvent const& event) const {
        std::vector<KGenParticle*> trueZs =
            SafeMap::GetWithDefault(m_genParticlesMap, 23, (std::vector<KGenParticle*>)(0));
        if (trueZs.size() == 0)
            return nullptr;
        else {
            KGenParticle* trueZ = trueZs[0];
            while (trueZ->nDaughters() == 1) {
                trueZ = &event.m_genParticles->at(trueZ->daughterIndex(0));
            }
            return trueZ;
        }
    }

    double GetTruePhiStarEta(ZJetEvent const& event) const {
        KGenParticle* trueZ = GetTrueZ(event);
        KGenParticle* lepton1 = &event.m_genParticles->at(trueZ->daughterIndex(0));
        KGenParticle* lepton2 = &event.m_genParticles->at(trueZ->daughterIndex(1));
        return(CalcPhiStarEta(lepton1, lepton2));
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
