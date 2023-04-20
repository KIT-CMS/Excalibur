#pragma once


#include "Artus/Core/interface/FilterBase.h"
#include "Artus/KappaAnalysis/interface/Producers/ValidJetsProducer.h"

/**
 * Filter class with cuts for ZJet analysis.
 *
 * min nleptons (el + mu)
 * max nleptons (el + mu)
 * leadinglep pt
 * min nmuons
 * max nmuons
 * muon pt
 * muon eta
 * min nelectrons
 * max nelectrons
 * electron pt
 * electron eta
 * leading jet pt
 * leading jet eta
 * z pt
 * back to back
 * alpha (second jet pt to z pt)
 */
//////////////////
// Min nLeptons // +++CURRENTLY NOT USED+++
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "Number of m_validLaptons: " << product.m_validLeptons.size() << ", Cut: " << nLeptonsMin ;
        if (product.m_validLeptons.size() >= nLeptonsMin) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
    }

  private:
    unsigned long nLeptonsMin = 0;
};

//////////////////
// Max nLeptons // +++CURRENTLY NOT USED+++
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "Number of m_validLaptons: " << product.m_validLeptons.size() << ", Cut: " << nLeptonsMax ;
        if (product.m_validLeptons.size() <= nLeptonsMax) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
    }

  private:
    unsigned long nLeptonsMax = 0;
};


///////////////////////
// leading lepton Pt // +++CURRENTLY NOT USED+++
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "leadingLeptonPtMin: " << leadingLeptonPtMin;
        LOG(WARNING) << "THIS CUT IS OUTDATED AND HAS TO BE REVIEWED!";
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "Number of m_validMuons: " << product.m_validMuons.size() << " >= " << nMuonsMin;
        if (product.m_validMuons.size() >= nMuonsMin) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "Number of m_validMuons: " << product.m_validMuons.size() << " <= " << nMuonsMax;
        if (product.m_validMuons.size() <= nMuonsMax) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
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
        if (settings.GetCutMuonSubPtMin() != -1.0) { // -1.0 is the default value
          muonSubPtMin = settings.GetCutMuonSubPtMin();
          LOG(DEBUG) << "Asymmetric muon pt cut used with: " << muonSubPtMin;
        } else {
          muonSubPtMin = muonPtMin;  // if not set, use symmetric lepton cut
          LOG(DEBUG) << "Use symmetric muon pt cut with: " << muonSubPtMin;
        }
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutMuonPtMin: " << muonPtMin << ", CutMuonSubPtMin: " << muonSubPtMin;
        // Only the two muons of the Z lepton need to pass this cut
        if (product.m_zValid == false) {
            LOG(FATAL) << "No valid Z! Please check if the ValidZ cut was already applied.";
        }
        if (settings.GetDebugVerbosity() > 0) {
            LOG(DEBUG) << "leading: " << product.m_zLeptons.first->p4;
            LOG(DEBUG) << "sub-leading: " << product.m_zLeptons.second->p4;
        }
        if (product.m_zLeptons.first->p4.Pt() > muonPtMin && product.m_zLeptons.second->p4.Pt() > muonSubPtMin) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutMuonEtaMax: " << muonEtaMax;
        // Only the two muons of the Z lepton need to pass this cut
        if (product.m_zValid == false) {
            LOG(FATAL) << "No valid Z! Please check if the ValidZ cut was already applied.";
        }
        if (settings.GetDebugVerbosity() > 0) {
            LOG(DEBUG) << "leading: " << product.m_zLeptons.first->p4;
            LOG(DEBUG) << "sub-leading: " << product.m_zLeptons.second->p4;
        }
        if (std::abs(product.m_zLeptons.first->p4.Eta()) < muonEtaMax && std::abs(product.m_zLeptons.second->p4.Eta()) < muonEtaMax) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
    }

  private:
    float muonEtaMax = 0;
};

////////////////////
// Min nElectrons //
////////////////////
class MinNElectronsCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "MinNElectronsCut"; }

    MinNElectronsCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        nElectronsMin = settings.GetCutNElectronsMin();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "Number of m_validElectrons: " << product.m_validElectrons.size() << " >= " << nElectronsMin;
        if (product.m_validElectrons.size() >= nElectronsMin) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
    }

  private:
    unsigned long nElectronsMin = 0;
};

////////////////////
// Max nElectrons //
////////////////////
class MaxNElectronsCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "MaxNElectronsCut"; }

    MaxNElectronsCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        nElectronsMax = settings.GetCutNElectronsMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "Number of m_validElectrons: " << product.m_validElectrons.size() << " <= " << nElectronsMax;
        if (product.m_validElectrons.size() <= nElectronsMax) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
    }

  private:
    unsigned long nElectronsMax = 0;
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
          LOG(DEBUG) << "Asymmetric electron pt cut used with: " << electronSubPtMin;
        } else {
          electronSubPtMin = electronPtMin;
          LOG(DEBUG) << "Use symmetric electron pt cut with: " << electronSubPtMin;
        }
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutElectronPtMin: " << electronPtMin << ", CutElectronSubPtMin: " << electronSubPtMin;
        // Only the two electrons of the Z lepton need to pass this cut
        if (product.m_zValid == false) {
            LOG(FATAL) << "No valid Z! Please check if the ValidZ cut was already applied.";
        }
        if (settings.GetDebugVerbosity() > 0) {
            LOG(DEBUG) << "leading: " << product.m_zLeptons.first->p4;
            LOG(DEBUG) << "sub-leading: " << product.m_zLeptons.second->p4;
        }
        if (product.m_zLeptons.first->p4.Pt() > electronPtMin && product.m_zLeptons.second->p4.Pt() > electronSubPtMin) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutElectronEtaMax: " << electronEtaMax;
        // Only the two electrons of the Z lepton need to pass this cut
        if (product.m_zValid == false) {
            LOG(FATAL) << "No valid Z! Please check if the ValidZ cut was already applied.";
        }
        if (settings.GetDebugVerbosity() > 0) {
            LOG(DEBUG) << "leading: " << product.m_zLeptons.first->p4;
            LOG(DEBUG) << "sub-leading: " << product.m_zLeptons.second->p4;
        }
        if (std::abs(product.m_zLeptons.first->p4.Eta()) < electronEtaMax &&
            std::abs(product.m_zLeptons.second->p4.Eta()) < electronEtaMax) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "LeadingJetPtMin: " << leadingJetPtMin;
        LOG(DEBUG) << "LEVEL: " << settings.GetCorrectionLevel();
        int valids = product.m_validJets.size();
        int jetcount = product.GetValidJetCount(settings, event, settings.GetCorrectionLevel());
        LOG(DEBUG) << "Number of m_validJets= " << valids << ", Number of corrected jets: " << jetcount <<"\n";
        if (jetcount > 0) {
            if (settings.GetDebugVerbosity() > 2) {
                LOG(DEBUG) << "m_validJets:";
                for (auto jet = product.m_validJets.begin(); jet != product.m_validJets.end();
                     ++jet) {
                    std::cout << (*jet)->p4 << std::endl;
                }
                LOG(DEBUG) << "\ncorrected jets: ";
                for (int index = 0; index < jetcount; index++) {
                    auto myjet =
                        product.GetValidJet(settings, event, index, settings.GetCorrectionLevel());
                    LOG(DEBUG) << "Index: " << index << ", " << myjet->p4;
                }
            }
            LOG(DEBUG) << "Corrected leading Jet: " << product.GetValidPrimaryJet(settings, event)->p4;
        } else {
            LOG(DEBUG) << "+++++++ No valid jet left! ++++++++";
            return false;
        }
        if (product.GetValidPrimaryJet(settings, event)->p4.Pt() > leadingJetPtMin){
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutLeadingJetEtaMax: " << leadingJetEtaMax;

        if (!(product.GetValidJetCount(settings, event) > 0)) {
            LOG(DEBUG) << "+++++++ No valid jet left! ++++++++";
            return false;
        }

        LOG(DEBUG) << "abs(Eta): " << std::abs(product.GetValidPrimaryJet(settings, event)->p4.Eta());
        if (std::abs(product.GetValidPrimaryJet(settings, event)->p4.Eta()) < leadingJetEtaMax) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutLeadingJetYMax: " << leadingJetYMax;

        if (!(product.GetValidJetCount(settings, event) > 0)) {
            LOG(DEBUG) << "+++++++ No valid jet left! ++++++++";
            return false;
        }

        LOG(DEBUG) << "abs(Rapidity): " << std::abs(product.GetValidPrimaryJet(settings, event)->p4.Rapidity());
        if (std::abs(product.GetValidPrimaryJet(settings, event)->p4.Rapidity()) < leadingJetYMax) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
    }

  private:
    float leadingJetYMax = 0;
};

//////////////////////
// JetEtaPhiCleaner //
//////////////////////
class JetEtaPhiCleanerCut : public ZJetFilterBase {
    public:
        std::string GetFilterId() const override { return "JetEtaPhiCleanerCut"; }
        JetEtaPhiCleanerCut() : ZJetFilterBase() {}

        void Init(ZJetSettings const& settings) override {
            ZJetFilterBase::Init(settings);
            vetoCleanedEvents = settings.GetCutVetoCleanedEvents();
        }

        bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override {
            LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
            LOG(DEBUG) << "CutVetoCleanedEvents: (0:no veto|1:veto events if cleaned) " << vetoCleanedEvents;
            if (vetoCleanedEvents) {
                if (product.m_etaPhiCleaned == true) {
                    LOG(DEBUG) << "Event vetoed due to " << this->GetFilterId();
                    return false;
                } else {
                    LOG(DEBUG) << "No (relevant) Jet cleaned. " <<  this->GetFilterId() << " passed!";
                    return true;
                }
            } else {
                LOG(DEBUG) << "Object-based JetEtaPhiCleaner selected. Skipping the filter.";
                return true;
            }
        }
    private:
        bool vetoCleanedEvents = false;
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutPhistaretaMin: " << phistaretaMin;

        if (product.m_zValid == false) {
            LOG(FATAL) << "No valid Z! Please check if the ValidZ cut was already applied.";
        }

        LOG(DEBUG) << "PhiStarEta: " << product.GetPhiStarEta(event);
        if (product.GetPhiStarEta(event) > phistaretaMin) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutZPtMin: " << zPtMin;
        if (product.m_zValid == false) {
            LOG(FATAL) << "No valid Z! Please check if the ValidZ cut was already applied.";
        }

        LOG(DEBUG) << "Z Pt: " << product.m_z.p4.Pt();
        if (product.m_z.p4.Pt() > zPtMin) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "Accepted Z mass: " << ZMass << " (pdg) +- " << settings.GetZMassRange()
                   << " (mass window)";
        LOG(DEBUG) << "Valid Z available? (0:No|1:Yes) " << product.m_zValid << ", reconstructed Z mass: "
                   << product.m_z.p4.M();

        if (product.m_zValid == false) {
            LOG(DEBUG) << "No Z available! Cut not passed!";
            return false;
        }

        if (std::abs(product.m_z.p4.M()-ZMass) < ZMassRange) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutBackToBack: " << backToBack;
        int jetcount = product.GetValidJetCount(settings, event, settings.GetCorrectionLevel());
        if (jetcount > 0) {
            // ||Delta phi(Z, jet1)| - pi| < 0.34
            double deltaPhi = ROOT::Math::VectorUtil::DeltaPhi(
                product.m_z.p4, product.GetValidPrimaryJet(settings, event)->p4);
            LOG(DEBUG) << "Delta Phi: " << deltaPhi << " => pi - dPhi = " << M_PI - std::abs(deltaPhi);

            if (M_PI - std::abs(deltaPhi) < backToBack) {
                LOG(DEBUG) << this->GetFilterId() << " passed!";
                return true;
            } else {
                LOG(DEBUG) << this->GetFilterId() << " not passed!";
                return false;
            }
        } else {
            LOG(DEBUG) << "No valid jet left. Event is vetoed.";
            return false;
        }

    }

  private:
    double backToBack = 0;
};

///////////
// Alpha // +++CURRENTLY NOT USED+++
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutAlphaMax: " << alphaMax;

        // Always true if there is only one jet in the event
        if (!(product.GetValidJetCount(settings, event) > 1)) {
            LOG(DEBUG) << "Not enough jets for alpha calculation!";
            LOG(WARNING) << "Alpha Cut skipped!";
            return true;
        }

        if (product.GetValidJet(settings, event, 1)->p4.Pt() < alphaMax * product.m_z.p4.Pt()) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
	    LOG(DEBUG) << "CutJetID: " << settings.GetCutJetID() << ", CutJetIDVersion: " << settings.GetCutJetIDVersion();
        LOG(DEBUG) << "Apply JetID on the first " << m_numJets << " jets.";

	    if (m_jetIDEnumType == KappaEnumTypes::JetID::NONE) {
	        LOG(DEBUG) << "JetID Cut in pipeline but no CutJetID given!";
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

       	LOG(DEBUG) << "First (" << m_numJets << ") jets passed the JetID cut!\n";
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "Number of m_genMuons: " << product.m_genMuons.size() << " >= " << nMuonsMin;

	/*unsigned int nMuons = 0;
	for(unsigned int i = 0; i < product.m_genLeptonsFromBosonDecay.size();i++){
		if(std::abs(product.m_genLeptonsFromBosonDecay.at(i)->pdgId) == 13)
			nMuons++;
	}*/
	//return(nMuons>=nMuonsMin);
        if (product.m_genMuons.size() >= nMuonsMin) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "Number of m_genMuons: " << product.m_genMuons.size() << " <= " << nMuonsMax;

        //return (product.m_genLeptonsFromBosonDecay.size() <= nMuonsMax);
        if (product.m_genMuons.size() <= nMuonsMax) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "+++ This filter is applied on ALL genMuons! +++";
        if (settings.GetCutMuonSubPtMin() != -1.0) {
            LOG(DEBUG) << "Using asymmetric pt cut:";
            LOG(DEBUG) << "Leading muon pt cut:" << muonPtMin; 
            LOG(DEBUG) << "Sub-leading muon pt cut: " << muonSubPtMin;
        } else {
            LOG(DEBUG) << "Using symmetric pt cut for leading and sub-leading muon: " << muonPtMin;
        }

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
        if (allPassed) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "+++ This filter is applied on ALL genMuons! +++";
        LOG(DEBUG) << "CutMuonEtaNax: " << muonEtaMax;
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
        if (allPassed) {
            LOG(DEBUG) << this->GetFilterId() << " passed!";
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutPhiStaretaMin: " << phistaretaMin;
        if (product.m_genBosonLVFound) {
            LOG(DEBUG) << "GenPhiStarEta: " << product.GetGenPhiStarEta(event);                 
            if (product.GetGenPhiStarEta(event) > phistaretaMin) {
                LOG(DEBUG) << this->GetFilterId() << " passed!";
                return true;
            } else {
                LOG(DEBUG) << this->GetFilterId() << " not passed!";
                return false;
            }
        } else {
            LOG(DEBUG) << "product.m_genBosonLVFound == false => Event vetoed!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutZPtMin: " << zPtMin;
        LOG(DEBUG) << "Pt: " << product.m_genBosonLV.Pt();

        if (product.m_genBosonLV.Pt() > zPtMin) {
            LOG(DEBUG) <<  this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }
    }

  private:
    float zPtMin = 0;
};

////////////////////
//LeadingGenJet Pt//
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "GetCutLeadingJetPtMin: " << leadingJetPtMin;
        if (product.m_simpleGenJets.size() > 0) {
            LOG(DEBUG) << "Leading GenJet Pt: " << product.m_simpleGenJets.at(0)->p4.Pt();
            if (product.m_simpleGenJets.at(0)->p4.Pt() > leadingJetPtMin) {
                LOG(DEBUG) <<  this->GetFilterId() << " passed!";
                return true;
            } else {
                LOG(DEBUG) << this->GetFilterId() << " not passed!";
                return false;
            }
        } else {
            LOG(DEBUG) << "No m_simpleGenJets available!";
            return false;
        }
    }

  private:
    float leadingJetPtMin = 0;
};

/////////////////////
// Leading Gen Jet Eta //
/////////////////////
class LeadingGenJetEtaCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "LeadingGenJetEtaCut"; }

    LeadingGenJetEtaCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        leadingJetEtaMax = settings.GetCutLeadingJetEtaMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutLeadingJetEtaMax: " << leadingJetEtaMax;
        if (product.m_simpleGenJets.size() > 0) {
            LOG(DEBUG) << "Leading GenJet Eta: " << product.m_simpleGenJets.at(0)->p4.Eta();
            if (std::fabs(product.m_simpleGenJets.at(0)->p4.Eta()) < leadingJetEtaMax) {
                LOG(DEBUG) <<  this->GetFilterId() << " passed!";
                return true;
            } else {
                LOG(DEBUG) << this->GetFilterId() << " not passed!";
                return false;
            }
        } else {
            LOG(DEBUG) << "No m_simpleGenJets available!";
            return false;
        }
    }

  private:
    float leadingJetEtaMax = 0;
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutLeadingJetYMax: " << leadingJetYMax;
        if (product.m_simpleGenJets.size() > 0) {
            LOG(DEBUG) << "Leading GenJet Rapidity: " << product.m_simpleGenJets.at(0)->p4.Rapidity();
            if (std::fabs(product.m_simpleGenJets.at(0)->p4.Rapidity()) < leadingJetYMax) {
                LOG(DEBUG) <<  this->GetFilterId() << " passed!";
                return true;
            } else {
                LOG(DEBUG) << this->GetFilterId() << " not passed!";
                return false;
            }
        } else {
            LOG(DEBUG) << "No m_simpleGenJets available!";
            return false;
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "CutGenHTMax: " << genhtMax;
        LOG(DEBUG) << "GenHT: " << product.GetGenHT(event);
        if (product.GetGenHT(event) < genhtMax) {
            LOG(DEBUG) <<  this->GetFilterId() << " passed!";
            return true;
        } else {
            LOG(DEBUG) << this->GetFilterId() << " not passed!";
            return false;
        }

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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
        LOG(DEBUG) << "ZMassRange: " << ZMassRange;
        if (product.m_genBosonLVFound == false) {
            LOG(DEBUG) << "No valid genBosonLVFound. Cut not passed!";
            return false;
        } else {
            LOG(DEBUG) << "Z gen mass: " << product.m_genBosonLV.mass();
            if(std::fabs(product.m_genBosonLV.mass() - ZMass) < ZMassRange) {
                LOG(DEBUG) << this->GetFilterId() << " passed!";
                return true;
            } else {
                LOG(DEBUG) << this->GetFilterId() << " not passed!";
                return false;
            }
        }
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
        LOG(DEBUG) << "\n[" << this->GetFilterId() << "]";
      for (const size_t metFilterIndex : metFilterBitIndices) {
        if (!event.m_triggerObjects->passesMetFilter(metFilterIndex)) {
          // At least one required MetFilter is not passed. Reject Event.
          LOG(DEBUG) << "METFilter with index: " << metFilterIndex << " not passed!";
          return false;
        }
      }
      LOG(DEBUG) << "All METFilters passed!";
      return true;
    }

  private:
    std::vector<size_t> metFilterBitIndices;
};
