#include "Consumers/ZJetTreeConsumer.h"

std::string ZJetTreeConsumer::GetConsumerId() const
{
	return "ZJetTreeConsumer";
}

void ZJetTreeConsumer::Init(ZJetSettings const& settings)
{
	// Add possible quantities for the lambda ntuples consumers
	
	///////
	// Z //
	///////
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zpt", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Pt();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zeta", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Eta();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zphi", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Phi();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zy", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Rapidity();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zmass", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.mass();
	} );
	
	//////////
	// Jets //
	//////////
	
	// Leading jet
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 0) ?  product.GetValidPrimaryJet(settings, event)->p4.Pt() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1eta", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 0) ?  product.GetValidPrimaryJet(settings, event)->p4.Eta() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1y", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 0) ?  product.GetValidPrimaryJet(settings, event)->p4.Rapidity() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1phi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 0) ? product.GetValidPrimaryJet(settings, event)->p4.Phi() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1pf", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 0) ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->photonFraction : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1ef", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 0) ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->electronFraction : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1chf", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 0) ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->chargedHadronFraction : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1nhf", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 0) ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->neutralHadronFraction : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1mf", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 0) ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->muonFraction : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1hfhf", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 0) ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->hfHadronFraction : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1hfemf", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 0) ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->hfEMFraction : DefaultValues::UndefinedDouble;
	} );
	/*
	 * TODO
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1unc", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->??;
	} );
	*/

	// Second leading jet
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet2pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 1) ? product.GetValidJet(settings, event, 1)->p4.Pt() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet2phi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 1) ? product.GetValidJet(settings, event, 1)->p4.Phi() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet2eta", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 1) ? product.GetValidJet(settings, event, 1)->p4.Eta() : DefaultValues::UndefinedDouble;
	} );
	
	// General jet stuff
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("njets", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetValidJetCount(settings, event);
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("njetsinv", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetInvalidJetCount(settings, event);
	} );
	
	// Gen jets
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genjet1pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (event.m_genJets != NULL && event.m_genJets->size() > 0) ? event.m_genJets->at(0).p4.Pt() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genjet1eta", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (event.m_genJets != NULL && event.m_genJets->size() > 0) ? event.m_genJets->at(0).p4.Eta() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genjet1phi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (event.m_genJets != NULL && event.m_genJets->size() > 0) ? event.m_genJets->at(0).p4.Phi() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genjet2pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (event.m_genJets != NULL && event.m_genJets->size() > 1) ? event.m_genJets->at(1).p4.Pt() : DefaultValues::UndefinedDouble;
	} );
	
	// Reco jet - gen parton matches
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("matchedgenparton1pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		KGenParticle* genParton = product.GetMatchedGenParton(event, settings, 0);
		return (genParton != 0) ? genParton->p4.Pt() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("matchedgenparton1flavour", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		KGenParticle* genParton = product.GetMatchedGenParton(event, settings, 0);
		return (genParton != 0) ? genParton->pdgId() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("matchedgenparton2pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		KGenParticle* genParton = product.GetMatchedGenParton(event, settings, 1);
		return (genParton != 0) ? genParton->p4.Pt() : DefaultValues::UndefinedDouble;
	} );
	
	// Reco jet - gen jet matches
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("matchedgenjet1pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		KLV* genJet = product.GetMatchedGenJet(event, settings, 0);
		return (genJet != 0) ? genJet->p4.Pt() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("matchedgenjet2pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		KLV* genJet = product.GetMatchedGenJet(event, settings, 1);
		return (genJet != 0) ? genJet->p4.Pt() : DefaultValues::UndefinedDouble;
	} );
	
	// TODO if needed
	// njets30, njets30barrel, genjet1ptneutrinos,
	// deltaRgenjet1genjet2, deltaRjet1jet2, deltaRjet1genjet1, deltaRjet2genjet2
	
	/////////
	// MET //
	/////////
	
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("metpt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event)->p4.Pt();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("metphi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event)->p4.Phi();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("sumet", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event)->sumEt;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("rawmetpt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event, "None")->p4.Pt();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("rawmetphi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMet(settings, event, "None")->p4.Phi();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mpf", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMPF(product.GetMet(settings, event));
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("rawmpf", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetMPF(product.GetMet(settings, event, "None"));
	} );
	
	///////////
	// MUONS //
	///////////
	
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("nmuons", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_validMuons.size();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mupluspt", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == 1) return (*muon)->p4.Pt();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mupluseta", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == 1) return (*muon)->p4.Eta();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muplusphi", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == 1) return (*muon)->p4.Phi();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muplusiso", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == 1) return (*muon)->pfIso();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muminuspt", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == -1) return (*muon)->p4.Pt();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muminuseta", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == -1) return (*muon)->p4.Eta();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muminusphi", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == -1) return (*muon)->p4.Phi();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muminusiso", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == -1) return (*muon)->pfIso();
		}
		return 0.;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mu1pt", [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mu1phi", [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mu1eta", [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size() >= 1 ? product.m_validMuons[0]->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mu2pt", [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mu2phi", [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mu2eta", [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size() >= 2 ? product.m_validMuons[1]->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	
	// TODO if needed
	// genmupluspt, genmupluseta, genmuplusphi, genminuspt, genminuseta, genminusphi
	// ngenmuons, ninternalmuons, nintermediatemuons, ptdiff13, ptdiff12, ptdiff23


	// Needs to be called at the end
	KappaLambdaNtupleConsumer::Init(settings);
}
