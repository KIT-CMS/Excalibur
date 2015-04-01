#pragma once

#include "ZJetTypes.h"

#include "Artus/Core/interface/FilterBase.h"

/**
 * Filter class with cuts for ZJet analysis.
 * 
 * muon pt
 * muon eta
 * leading jet pt
 * leading jet eta
 * back to back
 * 
 */

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
		if (product.GetValidPrimaryJet(settings, event)->p4.Pt() > leadingJetPtMin)
		{
			return true;
		}
		return false;
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
		if (std::abs(product.GetValidPrimaryJet(settings, event)->p4.Eta()) < leadingJetEtaMax)
		{
			return true;
		}
		return false;
	}

  private:
	float leadingJetEtaMax;
};
