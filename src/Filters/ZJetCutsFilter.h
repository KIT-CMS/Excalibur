#pragma once

#include "ZJetTypes.h"

#include "Artus/Core/interface/FilterBase.h"

/**
 * Filter class with cuts for ZJet analysis.
 * 
 * min nmuons
 * max nmuons
 * muon pt
 * muon eta
 * leading jet pt
 * leading jet eta
 * z pt
 * back to back
 * alpha (second jet pt to z pt)
 * 
 */


////////////////
// Min nMuons //
////////////////
class MinNMuonsCut : public ZJetFilterBase
{
  public:
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE { return "MinNMuonsCut"; }

	MinNMuonsCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) ARTUS_CPP11_OVERRIDE
	{
		ZJetFilterBase::Init(settings);
		nMuonsMin = settings.GetCutNMuonsMin();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		return (product.m_validMuons.size() >= nMuonsMin);
	}

  private:
	float nMuonsMin;
};


////////////////
// Max nMuons //
////////////////
class MaxNMuonsCut : public ZJetFilterBase
{
  public:
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE { return "MaxNMuonsCut"; }

	MaxNMuonsCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) ARTUS_CPP11_OVERRIDE
	{
		ZJetFilterBase::Init(settings);
		nMuonsMax = settings.GetCutNMuonsMax();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		return (product.m_validMuons.size() <= nMuonsMax);
	}

  private:
	float nMuonsMax;
};


/////////////
// Muon Pt //
/////////////
class MuonPtCut : public ZJetFilterBase
{
  public:
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE { return "MuonPtCut"; }

	MuonPtCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) ARTUS_CPP11_OVERRIDE
	{
		ZJetFilterBase::Init(settings);
		muonPtMin = settings.GetCutMuonPtMin();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		// Only the first two muons need to pass this cut
		bool allPassed = true;
		allPassed = allPassed && product.m_validMuons[0]->p4.Pt() > muonPtMin;
		allPassed = product.m_validMuons.size() >= 2 ? (allPassed && product.m_validMuons[1]->p4.Pt() > muonPtMin) : allPassed;
		return allPassed;
	}

  private:
	float muonPtMin;
};


//////////////
// Muon Eta //
//////////////
class MuonEtaCut : public ZJetFilterBase
{
  public:
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE { return "MuonEtaCut"; }

	MuonEtaCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) ARTUS_CPP11_OVERRIDE
	{
		ZJetFilterBase::Init(settings);
		muonEtaMax = settings.GetCutMuonEtaMax();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		// Only the first two muons need to pass this cut
		bool allPassed = true;
		allPassed = allPassed && std::abs(product.m_validMuons[0]->p4.Eta()) < muonEtaMax;
		allPassed = product.m_validMuons.size() >= 2 ? (allPassed && std::abs(product.m_validMuons[1]->p4.Eta()) < muonEtaMax) : allPassed;
		return allPassed;
	}

  private:
	float muonEtaMax;
};


////////////////////
// Leading Jet Pt //
////////////////////
class LeadingJetPtCut : public ZJetFilterBase
{
  public:
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE { return "LeadingJetPtCut"; }

	LeadingJetPtCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) ARTUS_CPP11_OVERRIDE
	{
		ZJetFilterBase::Init(settings);
		leadingJetPtMin = settings.GetCutLeadingJetPtMin();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		return (product.GetValidPrimaryJet(settings, event)->p4.Pt() > leadingJetPtMin);
	}

  private:
	float leadingJetPtMin;
};


/////////////////////
// Leading Jet Eta //
/////////////////////
class LeadingJetEtaCut : public ZJetFilterBase
{
  public:
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE { return "LeadingJetEtaCut"; }

	LeadingJetEtaCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) ARTUS_CPP11_OVERRIDE
	{
		ZJetFilterBase::Init(settings);
		leadingJetEtaMax = settings.GetCutLeadingJetEtaMax();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		return (std::abs(product.GetValidPrimaryJet(settings, event)->p4.Eta()) < leadingJetEtaMax);
	}

  private:
	float leadingJetEtaMax;
};


//////////
// Z Pt //
//////////
class ZPtCut : public ZJetFilterBase
{
  public:
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE { return "ZPtCut"; }

	ZPtCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) ARTUS_CPP11_OVERRIDE
	{
		ZJetFilterBase::Init(settings);
		zPtMin = settings.GetCutZPtMin();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		return (product.m_z.p4.Pt() > zPtMin);
	}

  private:
	float zPtMin;
};


//////////////////
// Back to Back //
//////////////////
class BackToBackCut : public ZJetFilterBase
{
  public:
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE { return "BackToBackCut"; }

	BackToBackCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) ARTUS_CPP11_OVERRIDE
	{
		ZJetFilterBase::Init(settings);
		backToBack = settings.GetCutBackToBack();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		double jet1Phi = product.GetValidPrimaryJet(settings, event)->p4.Phi();
		double zPhi = product.m_z.p4.Phi();
		return (std::abs(std::abs(jet1Phi - zPhi) - ROOT::Math::Pi()) < backToBack);
	}

  private:
	float backToBack;
};


///////////
// Alpha //
///////////
class AlphaCut : public ZJetFilterBase
{
  public:
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE { return "AlphaCut"; }

	AlphaCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) ARTUS_CPP11_OVERRIDE
	{
		ZJetFilterBase::Init(settings);
		alphaMax = settings.GetCutAlphaMax();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		// Always true if there is only one jet in the event
		return (product.GetValidJetCount(settings, event) > 1) ? (product.GetValidJet(settings, event, 1)->p4.Pt()/product.m_z.p4.Pt() < alphaMax) : true;
	}

  private:
	float alphaMax;
};
