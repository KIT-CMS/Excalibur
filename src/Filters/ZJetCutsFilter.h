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
	virtual std::string GetFilterId() const override { return "MinNMuonsCut"; }

	MinNMuonsCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) override
	{
		ZJetFilterBase::Init(settings);
		nMuonsMin = settings.GetCutNMuonsMin();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const override
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
	virtual std::string GetFilterId() const override { return "MaxNMuonsCut"; }

	MaxNMuonsCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) override
	{
		ZJetFilterBase::Init(settings);
		nMuonsMax = settings.GetCutNMuonsMax();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const override
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
	virtual std::string GetFilterId() const override { return "MuonPtCut"; }

	MuonPtCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) override
	{
		ZJetFilterBase::Init(settings);
		muonPtMin = settings.GetCutMuonPtMin();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const override
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
	virtual std::string GetFilterId() const override { return "MuonEtaCut"; }

	MuonEtaCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) override
	{
		ZJetFilterBase::Init(settings);
		muonEtaMax = settings.GetCutMuonEtaMax();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const override
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
	virtual std::string GetFilterId() const override { return "LeadingJetPtCut"; }

	LeadingJetPtCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) override
	{
		ZJetFilterBase::Init(settings);
		leadingJetPtMin = settings.GetCutLeadingJetPtMin();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const override
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
	virtual std::string GetFilterId() const override { return "LeadingJetEtaCut"; }

	LeadingJetEtaCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) override
	{
		ZJetFilterBase::Init(settings);
		leadingJetEtaMax = settings.GetCutLeadingJetEtaMax();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const override
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
	virtual std::string GetFilterId() const override { return "ZPtCut"; }

	ZPtCut() : ZJetFilterBase(){};
	
	virtual void Init(ZJetSettings const& settings) override
	{
		ZJetFilterBase::Init(settings);
		zPtMin = settings.GetCutZPtMin();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const override
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
	virtual std::string GetFilterId() const override { return "BackToBackCut"; }

	BackToBackCut() : ZJetFilterBase(){};

	virtual void Init(ZJetSettings const& settings) override
	{
		ZJetFilterBase::Init(settings);
		backToBack = settings.GetCutBackToBack();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const override
	{
		// ||Delta phi(Z, jet1)| - pi| < 0.34
		double deltaPhi = ROOT::Math::VectorUtil::DeltaPhi(
				product.m_z.p4, product.GetValidPrimaryJet(settings, event)->p4);
		return M_PI - std::abs(deltaPhi) < backToBack;
	}

  private:
	double backToBack;
};


///////////
// Alpha //
///////////
class AlphaCut : public ZJetFilterBase
{
  public:
	virtual std::string GetFilterId() const override { return "AlphaCut"; }

	AlphaCut() : ZJetFilterBase(){};

	virtual void Init(ZJetSettings const& settings) override
	{
		ZJetFilterBase::Init(settings);
		alphaMax = settings.GetCutAlphaMax();
	}

	virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const override
	{
		// Always true if there is only one jet in the event
		return (product.GetValidJetCount(settings, event) > 1) ? (product.GetValidJet(settings, event, 1)->p4.Pt() < alphaMax * product.m_z.p4.Pt()) : true;
	}

  private:
	float alphaMax;
};

///////////
// Beta  //
///////////
class BetaCut : public ZJetFilterBase
{
	public:
		virtual std::string GetFilterId() const override { return "BetaCut"; }

		BetaCut() : ZJetFilterBase(){};

		virtual void Init(ZJetSettings const& settings) override
		{
				ZJetFilterBase::Init(settings);
				betaMax = settings.GetCutBetaMax();
		}

		virtual bool DoesEventPass(ZJetEvent const& event, ZJetProduct const& product,
							   ZJetSettings const& settings) const override
		{
			// Always true if there is no radiation jet in the event
			return (product.GetRadiationJetCount(settings, event) > 0) ? (product.GetRadiationJet(settings, event, 0)->p4.Pt() < betaMax * product.m_z.p4.Pt()) : true;
		}

	private:
		float betaMax;
};
