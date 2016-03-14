#pragma once

#include "ZJetTypes.h"

#include "Artus/Core/interface/FilterBase.h"

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
////////////////
// Min nLeptons //
////////////////
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

////////////////
// Max nLeptons //
////////////////
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
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        // Only the first two muons need to pass this cut
        bool allPassed = true;
        allPassed = allPassed && product.m_validMuons[0]->p4.Pt() > muonPtMin;
        allPassed = product.m_validMuons.size() >= 2
                        ? (allPassed && product.m_validMuons[1]->p4.Pt() > muonPtMin)
                        : allPassed;
        return allPassed;
    }

  private:
    float muonPtMin = 0;
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

/////////////
// Electron Pt //
/////////////
class ElectronPtCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "ElectronPtCut"; }

    ElectronPtCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        electronPtMin = settings.GetCutElectronPtMin();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        // Only the first two Electrons need to pass this cut
        bool allPassed = true;
        allPassed = allPassed && product.m_validElectrons[0]->p4.Pt() > electronPtMin;
        allPassed = product.m_validElectrons.size() >= 2
                        ? (allPassed && product.m_validElectrons[1]->p4.Pt() > electronPtMin)
                        : allPassed;
        return allPassed;
    }

  private:
    float electronPtMin = 0;
};

//////////////
// Electron Eta //
//////////////
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
        return (product.GetValidPrimaryJet(settings, event)->p4.Pt() > leadingJetPtMin);
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
        return (std::abs(product.GetValidPrimaryJet(settings, event)->p4.Eta()) < leadingJetEtaMax);
    }

  private:
    float leadingJetEtaMax = 0;
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
// Beta  //
///////////
class BetaCut : public ZJetFilterBase
{
  public:
    std::string GetFilterId() const override { return "BetaCut"; }

    BetaCut() : ZJetFilterBase() {}

    void Init(ZJetSettings const& settings) override
    {
        ZJetFilterBase::Init(settings);
        betaMax = settings.GetCutBetaMax();
    }

    bool DoesEventPass(ZJetEvent const& event,
                       ZJetProduct const& product,
                       ZJetSettings const& settings) const override
    {
        // Always true if there is no radiation jet in the event
        return (product.GetRadiationJetCount(settings, event) > 0)
                   ? (product.GetRadiationJet(settings, event, 0)->p4.Pt() <
                      betaMax * product.m_z.p4.Pt())
                   : true;
    }

  private:
    float betaMax = 0;
};
