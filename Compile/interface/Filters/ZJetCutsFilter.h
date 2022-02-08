#pragma once


#include "Artus/Core/interface/FilterBase.h"
#include "Artus/KappaAnalysis/interface/Producers/ValidJetsProducer.h"

/**
 * Filter class with cuts for ZJet analysis.
 *
 * min nleptons (el + mu) 
 * max nleptons (el + mu)
 * leadinglep pt 
 * min nmuons    ***Not needed anymore [stefan wayand]
 * max nmuons    ***Not needed anymore [stefan wayand]
 * muon pt       ***Not needed anymore [stefan wayand]
 * muon eta      ***Not needed anymore [stefan wayand]
 * electron pt   ***Not needed anymore [stefan wayand]
 * electron eta  ***Not needed anymore [stefan wayand]
 * leading jet pt
 * leading jet eta
 * z pt
 * back to back
 * alpha (second jet pt to z pt)
 */
//////////////////
// Min nLeptons //
//////////////////
class MinNLeptonsCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "MinNLeptonsCut"; }

    MinNLeptonsCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        nLeptonsMin = settings.GetCutNLeptonsMin();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return ( (product.m_validMuons.size() + product.m_validElectrons.size()) >= nLeptonsMin);
    }

  private:
    unsigned long nLeptonsMin = 0;
};

//////////////////
// Max nLeptons //
//////////////////
class MaxNLeptonsCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "MaxNLeptonsCut"; }

    MaxNLeptonsCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        nLeptonsMax = settings.GetCutNLeptonsMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return ( (product.m_validMuons.size() + product.m_validElectrons.size()) <= nLeptonsMax);
    }

  private:
    unsigned long nLeptonsMax = 0;
};


///////////////////////
// leading lepton Pt //
///////////////////////
class LeadingLeptonPtCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "LeadingLeptonPtCut"; }

    LeadingLeptonPtCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
       leadingLeptonPtMin = settings.GetCutLeadingLeptonPtMin();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        // Only the first two muons need to pass this cut
	if (product.m_validMuons.size() > 0 && product.m_validMuons[0]->p4.Pt() > leadingLeptonPtMin) return true;
        if (product.m_validElectrons.size() > 0 && product.m_validElectrons[0]->p4.Pt() > leadingLeptonPtMin) return true;  
        return false;
    }

  private:
    float leadingLeptonPtMin = 0;
};

////////////////
// Min nMuons //
////////////////
class MinNMuonsCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "MinNMuonsCut"; }

    MinNMuonsCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        nMuonsMin = settings.GetCutNMuonsMin();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.m_validMuons.size() >= nMuonsMin);
    }

  private:
    unsigned long nMuonsMin = 0;
};

////////////////
// Max nMuons //
////////////////
class MaxNMuonsCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "MaxNMuonsCut"; }

    MaxNMuonsCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        nMuonsMax = settings.GetCutNMuonsMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.m_validMuons.size() <= nMuonsMax);
    }

  private:
    unsigned long nMuonsMax = 0;
};

/////////////
// Muon Pt //
/////////////
class MuonPtCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "MuonPtCut"; }

    MuonPtCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        muonPtMin = settings.GetCutMuonPtMin();
        if (settings.GetCutMuonSubPtMin() != -1.0) {
          muonSubPtMin = settings.GetCutMuonSubPtMin();
        } else {
          muonSubPtMin = muonPtMin;
        }
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        // Only the first two muons need to pass this cut
        bool allPassed = true;
        allPassed = allPassed && product.m_validMuons[0]->p4.Pt() > muonPtMin;
        allPassed = product.m_validMuons.size() >= 2
                        ? (allPassed && product.m_validMuons[1]->p4.Pt() > muonSubPtMin)
                        : allPassed;
        return allPassed;
    }

  private:
    float muonPtMin = 0;
    float muonSubPtMin = 0;
};

//////////////
// Muon Eta //
//////////////
class MuonEtaCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "MuonEtaCut"; }

    MuonEtaCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        muonEtaMax = settings.GetCutMuonEtaMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        // Only the first two muons need to pass this cut
        bool allPassed = true;
        allPassed = allPassed && std::abs(product.m_validMuons[0]->p4.Eta()) < muonEtaMax;
        allPassed = product.m_validMuons.size() >= 2
                        ? (allPassed && std::abs(product.m_validMuons[1]->p4.Eta()) < muonEtaMax)
                        : allPassed;
        return allPassed;
    }

  private:
    float muonEtaMax = 0;
};

/////////////////
// Electron Pt //
/////////////////
class ElectronPtCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "ElectronPtCut"; }

    ElectronPtCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        electronPtMin = settings.GetCutElectronPtMin();
        if (settings.GetCutElectronSubPtMin() != -1.0) {
          electronSubPtMin = settings.GetCutElectronSubPtMin();
        } else {
          electronSubPtMin = electronPtMin;
        }
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        // Only the first two Electrons need to pass this cut
        bool allPassed = true;
        allPassed = allPassed && product.m_validElectrons[0]->p4.Pt() > electronPtMin;
        allPassed = product.m_validElectrons.size() >= 2
                        ? (allPassed && product.m_validElectrons[1]->p4.Pt() > electronSubPtMin)
                        : allPassed;
        return allPassed;
    }

  private:
    float electronPtMin = 0;
    float electronSubPtMin = 0;
};

//////////////////
// Electron Eta //
//////////////////
class ElectronEtaCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "ElectronEtaCut"; }

    ElectronEtaCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        electronEtaMax = settings.GetCutElectronEtaMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        // Only the first two electrons need to pass this cut
        bool allPassed = true;
        allPassed = allPassed && std::abs(product.m_validElectrons[0]->p4.Eta()) < electronEtaMax;
        allPassed =
            product.m_validElectrons.size() >= 2
                ? (allPassed && std::abs(product.m_validElectrons[1]->p4.Eta()) < electronEtaMax)
                : allPassed;
        return allPassed;
    }

  private:
    float electronEtaMax = 0;
};

////////////////////
// Leading Jet Pt //
////////////////////
class LeadingJetPtCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "LeadingJetPtCut"; }

    LeadingJetPtCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        leadingJetPtMin = settings.GetCutLeadingJetPtMin();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.GetValidJetCount(settings, event) > 0)
                ? (product.GetValidPrimaryJet(settings, event)->p4.Pt() > leadingJetPtMin)
                : false;
    }

  private:
    float leadingJetPtMin = 0;
};

/////////////////////
// Leading Jet Eta //
/////////////////////
class LeadingJetEtaCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "LeadingJetEtaCut"; }

    LeadingJetEtaCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        leadingJetEtaMax = settings.GetCutLeadingJetEtaMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.GetValidJetCount(settings, event) > 0)
                ? (std::abs(product.GetValidPrimaryJet(settings, event)->p4.Eta()) < leadingJetEtaMax)
                : false;
    }

  private:
    float leadingJetEtaMax = 0;
};

//////////////////////////
// Leading Jet Rapidity //
//////////////////////////
class LeadingJetYCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "LeadingJetYCut"; }

    LeadingJetYCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        leadingJetYMax = settings.GetCutLeadingJetYMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.GetValidJetCount(settings, event) > 0)
                ? (std::abs(product.GetValidPrimaryJet(settings, event)->p4.Rapidity()) < leadingJetYMax)
                : false;
    }

  private:
    float leadingJetYMax = 0;
};

////////////////
// Phistareta //
////////////////
class PhistaretaCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "PhistaretaCut"; }

    PhistaretaCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        phistaretaMin = settings.GetCutPhistaretaMin();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.m_zValid) 
                    ? (product.GetPhiStarEta(event) > phistaretaMin)
                    : false;
    }

  private:
    float phistaretaMin = 0;
};

//////////
// Z Pt //
//////////
class ZPtCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "ZPtCut"; }

    ZPtCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        zPtMin = settings.GetCutZPtMin();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.m_z.p4.Pt() > zPtMin);
    }

  private:
    float zPtMin = 0;
};

////////////
// ValidZ //
////////////

//For Pipelining ZFilter is not usable
class ValidZCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "ValidZCut"; }

    ValidZCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        ZMassRange = settings.GetZMassRange();
        ZMass = settings.GetZMass();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.m_zValid && std::abs(product.m_z.p4.M()-ZMass)<ZMassRange);
    }
  private:
    float ZMassRange = 0;
    float ZMass = 90;
};

//////////////////
// Back to Back //
//////////////////
class BackToBackCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "BackToBackCut"; }

    BackToBackCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        backToBack = settings.GetCutBackToBack();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        // ||Delta phi(Z, jet1)| - pi| < 0.34
        double deltaPhi = ROOT::Math::VectorUtil::DeltaPhi(
            product.m_z.p4, product.GetValidPrimaryJet(settings, event)->p4);
        return M_PI - std::abs(deltaPhi) < backToBack;
    }

  private:
    double backToBack = 0;
};

///////////
// Alpha //
///////////
class AlphaCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "AlphaCut"; }

    AlphaCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        alphaMax = settings.GetCutAlphaMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        // Always true if there is only one jet in the event
        return (product.GetValidJetCount(settings, event) > 1)
                   ? (product.GetValidJet(settings, event, 1)->p4.Pt() <
                      alphaMax * product.m_z.p4.Pt())
                   : true;
    }

  private:
    float alphaMax = 0;
};

///////////
// JetID //
///////////
class JetIDCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "JetIDCut"; }

    JetIDCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);

        // store the CutJetID and CutJetIDVersion as enum types for fast evaluation
        m_jetIDEnumType = KappaEnumTypes::ToJetID(settings.GetCutJetID());
        m_jetIDVersionEnumType = KappaEnumTypes::ToJetIDVersion(settings.GetCutJetIDVersion());
        m_numJets = settings.GetCutJetIDFirstNJets();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
	    LOG(DEBUG) << "\n[JetIDCut]";
	    LOG(DEBUG) << "CutJetID: " << settings.GetCutJetID() << ", CutJetIDVersion: " << settings.GetCutJetIDVersion();
	    if (m_jetIDEnumType == KappaEnumTypes::JetID::NONE) {
	        LOG(WARNING) << "JetID Cut selected but no CutJetID given!";
	        LOG(DEBUG) << "JetID Cut skipped!\n";
	        return true;
	    } else {
    	    LOG(DEBUG) << "Apply event-based jetID cut.";
            for (unsigned int iJet = 0; iJet < m_numJets; ++iJet) {
                bool _jetPassesID = (product.GetValidJetCount(settings, event) > iJet)
                                        ? ValidJetsProducer::passesJetID(
                                              dynamic_cast<KBasicJet*>(product.GetValidJet(settings, event, iJet)),
                                              m_jetIDVersionEnumType,
                                              m_jetIDEnumType,
                                              settings)
                                        : false;
                // return immediately on non-passing jet
                if (!_jetPassesID) {
                    LOG(DEBUG) << "JetID cut not passed!\n";
                    return false;
                }
            }
       	}

       	LOG(DEBUG) << "First " << m_numJets << " jets passed the JetID cut!\n";
        return true;  // first 'm_numJets' Jets passed ID
    }

    private:
      unsigned int m_numJets;
      KappaEnumTypes::JetID m_jetIDEnumType;
      KappaEnumTypes::JetIDVersion m_jetIDVersionEnumType;
};

//GenLevelCuts
///////////////////
// Min nGenMuons //
///////////////////
class MinNGenMuonsCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "MinNGenMuonsCut"; }

    MinNGenMuonsCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        nMuonsMin = settings.GetCutNMuonsMin();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
	/*unsigned int nMuons = 0;
	for(unsigned int i = 0; i < product.m_genLeptonsFromBosonDecay.size();i++){
		if(std::abs(product.m_genLeptonsFromBosonDecay.at(i)->pdgId) == 13)
			nMuons++;
	}*/
	
	//return(nMuons>=nMuonsMin);
	return(product.m_genMuons.size()>=nMuonsMin);
    }

  private:
    unsigned long nMuonsMin = 0;
};

///////////////////
// Max nGenMuons //
///////////////////
class MaxNGenMuonsCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "MaxNGenMuonsCut"; }

    MaxNGenMuonsCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        nMuonsMax = settings.GetCutNMuonsMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        //return (product.m_genLeptonsFromBosonDecay.size() <= nMuonsMax);
	return (product.m_genMuons.size() <= nMuonsMax);
    }

  private:
    unsigned long nMuonsMax = 0;
};

////////////////
// GenMuon Pt //
////////////////
class GenMuonPtCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "GenMuonPtCut"; }

    GenMuonPtCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        muonPtMin = settings.GetCutMuonPtMin();
        if (settings.GetCutMuonSubPtMin() != -1.0) {
          muonSubPtMin = settings.GetCutMuonSubPtMin();
        } else {
          muonSubPtMin = muonPtMin;
        }
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        // Only the first two muons need to pass this cut
        bool allPassed = true;
        /*allPassed = allPassed && product.m_genLeptonsFromBosonDecay.at(0)->p4.Pt() > muonPtMin;
        allPassed = product.m_genLeptonsFromBosonDecay.size() >= 2
                        ? (allPassed &&product.m_genLeptonsFromBosonDecay.at(1)->p4.Pt() > muonPtMin)
                        : allPassed; product.m_genMuons[0]->p4.Phi()*/
        allPassed = allPassed && product.m_genMuons[0]->p4.Pt() > muonPtMin;
        allPassed = product.m_genMuons.size() >= 2
                        ? (allPassed && product.m_genMuons[1]->p4.Pt() > muonSubPtMin)
                        : allPassed;
        return allPassed;
    }

  private:
    float muonPtMin = 0;
    float muonSubPtMin = 0;
};

//////////////////
// Gen Muon Eta //
//////////////////
class GenMuonEtaCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "GenMuonEtaCut"; }

    GenMuonEtaCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        muonEtaMax = settings.GetCutMuonEtaMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        // Only the first two muons need to pass this cut
        bool allPassed = true;
        /*allPassed = allPassed && std::fabs(product.m_genLeptonsFromBosonDecay.at(0)->p4.Eta()) < muonEtaMax;
        allPassed = product.m_genLeptonsFromBosonDecay.size() >= 2
                       ? (allPassed && std::fabs(product.m_genLeptonsFromBosonDecay.at(1)->p4.Eta()) < muonEtaMax)
                        : allPassed;*/
        allPassed = allPassed && std::fabs(product.m_genMuons[0]->p4.Eta()) < muonEtaMax;
        allPassed = product.m_genMuons.size() >= 2
                       ? (allPassed && std::fabs(product.m_genMuons[1]->p4.Eta()) < muonEtaMax)
                        : allPassed;
        return allPassed;
    }

  private:
    float muonEtaMax = 0;
};

///////////////////
// GenPhistareta //
///////////////////
class GenPhistaretaCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "GenPhistaretaCut"; }

    GenPhistaretaCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        phistaretaMin = settings.GetCutPhistaretaMin();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.m_genBosonLVFound)
                    ? (product.GetGenPhiStarEta(event) > phistaretaMin)
                    : false;
    }

  private:
    float phistaretaMin = 0;
};

//////////////
// Gen Z Pt //
//////////////
class GenZPtCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "GenZPtCut"; }

    GenZPtCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        zPtMin = settings.GetCutZPtMin();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.m_genBosonLV.Pt() > zPtMin);
    }

  private:
    float zPtMin = 0;
};

////////////////////
// Leading Jet Pt //
////////////////////
class LeadingGenJetPtCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "LeadingGenJetPtCut"; }

    LeadingGenJetPtCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        leadingJetPtMin = settings.GetCutLeadingJetPtMin();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.m_simpleGenJets.size()>0)
                ? (product.m_simpleGenJets.at(0)->p4.Pt() > leadingJetPtMin)
                : false;
    }

  private:
    float leadingJetPtMin = 0;
};

//////////////////////////////
// Leading Gen Jet Rapidity //
//////////////////////////////
class LeadingGenJetYCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "LeadingGenJetYCut"; }

    LeadingGenJetYCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        leadingJetYMax = settings.GetCutLeadingJetYMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.m_simpleGenJets.size()>0)
                ? (std::abs(product.m_simpleGenJets.at(0)->p4.Rapidity()) < leadingJetYMax)
                : false;
    }

  private:
    float leadingJetYMax = 0;
};

///////////
// GenHT //
///////////
class GenHTCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "GenHTCut"; }

    GenHTCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        genhtMax = settings.GetCutGenHTMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.GetGenHT(event) < genhtMax);
    }

  private:
    float genhtMax = 0;
};

///////////////
// ValidGenZ //
///////////////

class ValidGenZCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "ValidGenZCut"; }

    ValidGenZCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        ZMassRange = settings.GetZMassRange();
        ZMass = settings.GetZMass();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        return (product.m_genBosonLVFound && std::fabs(product.m_genBosonLV.mass() - ZMass) < ZMassRange);
    }
  private:
    float ZMassRange = 0;
    float ZMass = 90;
};

////////////////
// MET Filter //
////////////////

class METFiltersFilter : public ZJetFilterBase {

  public:
    std::string GetFilterId() const override { return "METFiltersFilter"; }

    METFiltersFilter() : ZJetFilterBase() {}

    void OnLumi(ZJetEvent const& event, ZJetSettings const& settings) override {
      if (metFilterBitIndices.empty()) {
        if (!event.m_triggerObjectMetadata) {
          LOG(FATAL) << "No trigger object metadata branch given. Please specify using setting \"TriggerInfos\".";
        }
        if (!event.m_triggerObjects) {
          LOG(FATAL) << "No trigger objects branch given. Please specify using setting \"TriggerObjects\".";
        }
        for (const auto& filterName : settings.GetMETFilterNames()) {
          size_t index = event.m_triggerObjectMetadata->metFilterPos(filterName);
          metFilterBitIndices.push_back(index);
        }
      }
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override {
      for (const size_t metFilterIndex : metFilterBitIndices) {
        if (!event.m_triggerObjects->passesMetFilter(metFilterIndex)) {
          // At least one required MetFilter is not passed. Reject Event.
          return false;
        }
      }
      return true;
    }

  private:
    std::vector<size_t> metFilterBitIndices;
};
