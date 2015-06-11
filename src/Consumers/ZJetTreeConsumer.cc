#include "Consumers/ZJetTreeConsumer.h"

std::string ZJetTreeConsumer::GetConsumerId() const
{
	return "ZJetTreeConsumer";
}

void ZJetTreeConsumer::Init(ZJetSettings const& settings)
{
	// Add possible quantities for the lambda ntuples consumers
	
	////////////////////////
	// General quantities //
	////////////////////////
	LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity("npu", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return event.m_genEventInfo->nPU;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("npumean", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return event.m_genEventInfo->nPUMean;
	} );
	
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
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zeta", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Eta();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zy", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.Rapidity();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("zmass", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_z.p4.mass();
	} );
	
	// Gen Z
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genzpt", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		KGenParticle* genZ = product.GetGenZ();
		return (genZ != 0) ? genZ->p4.Pt() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genzeta", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		KGenParticle* genZ = product.GetGenZ();
		return (genZ != 0) ? genZ->p4.Eta() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genzphi", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		KGenParticle* genZ = product.GetGenZ();
		return (genZ != 0) ? genZ->p4.Phi() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genzeta", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		KGenParticle* genZ = product.GetGenZ();
		return (genZ != 0) ? genZ->p4.Eta() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genzy", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		KGenParticle* genZ = product.GetGenZ();
		return (genZ != 0) ? genZ->p4.Rapidity() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genzmass", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		KGenParticle* genZ = product.GetGenZ();
		return (genZ != 0) ? genZ->p4.mass() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("deltarzgenz", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		KGenParticle* genZ = product.GetGenZ();
		return (genZ != 0) ? ROOT::Math::VectorUtil::DeltaR(genZ->p4, product.m_z.p4) : DefaultValues::UndefinedDouble;
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
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1btag", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 0) ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->getTag("CombinedSecondaryVertexBJetTags", event.m_jetMetadata) : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet1qgtag", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 0) ? static_cast<KJet*>(product.GetValidPrimaryJet(settings, event))->getTag("QGlikelihood", event.m_jetMetadata) : DefaultValues::UndefinedDouble;
	} );

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

	// 3rd leading jet
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet3pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 2) ? product.GetValidJet(settings, event, 2)->p4.Pt() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet3phi", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 2) ? product.GetValidJet(settings, event, 2)->p4.Phi() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("jet3eta", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return (product.GetValidJetCount(settings, event) > 2) ? product.GetValidJet(settings, event, 2)->p4.Eta() : DefaultValues::UndefinedDouble;
	} );
	
	// General jet stuff
	LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity("njets", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.GetValidJetCount(settings, event);
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity("njetsinv", [settings](ZJetEvent const& event, ZJetProduct const& product)
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
	LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity("matchedgenparton1flavour", [settings](ZJetEvent const& event, ZJetProduct const& product)
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
	
	LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity("nmuons", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_validMuons.size();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mupluspt", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == 1) return (*muon)->p4.Pt();
		}
		return DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("mupluseta", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == 1) return (*muon)->p4.Eta();
		}
		return DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muplusphi", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == 1) return (*muon)->p4.Phi();
		}
		return DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muplusiso", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == 1) return (*muon)->pfIso();
		}
		return DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muminuspt", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == -1) return (*muon)->p4.Pt();
		}
		return DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muminuseta", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == -1) return (*muon)->p4.Eta();
		}
		return DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muminusphi", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == -1) return (*muon)->p4.Phi();
		}
		return DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("muminusiso", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KMuon*>::const_iterator muon = product.m_validMuons.begin(); muon != product.m_validMuons.end(); muon++)
		{
			if ((*muon)->charge() == -1) return (*muon)->pfIso();
		}
		return DefaultValues::UndefinedDouble;
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

	// Gen muons
	LambdaNtupleConsumer<ZJetTypes>::AddIntQuantity("ngenmuons", [](ZJetEvent const& event, ZJetProduct const& product)
	{
		return product.m_genMuons.size();
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genmupluspt", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin(); genMuon != product.m_genMuons.end(); genMuon++)
		{
			if ((*genMuon)->charge() == 1) return (*genMuon)->p4.Pt();
		}
		return DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genmupluseta", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin(); genMuon != product.m_genMuons.end(); genMuon++)
		{
			if ((*genMuon)->charge() == 1) return (*genMuon)->p4.Eta();
		}
		return DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genmuplusphi", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin(); genMuon != product.m_genMuons.end(); genMuon++)
		{
			if ((*genMuon)->charge() == 1) return (*genMuon)->p4.Phi();
		}
		return DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genmuminuspt", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin(); genMuon != product.m_genMuons.end(); genMuon++)
		{
			if ((*genMuon)->charge() == -1) return (*genMuon)->p4.Pt();
		}
		return DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genmuminuseta", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin(); genMuon != product.m_genMuons.end(); genMuon++)
		{
			if ((*genMuon)->charge() == -1) return (*genMuon)->p4.Phi();
		}
		return DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("genmuminusphi", [](ZJetEvent const& event, ZJetProduct const& product) -> float
	{
		for (std::vector<KGenParticle*>::const_iterator genMuon = product.m_genMuons.begin(); genMuon != product.m_genMuons.end(); genMuon++)
		{
			if ((*genMuon)->charge() == -1) return (*genMuon)->p4.Eta();
		}
		return DefaultValues::UndefinedDouble;
	} );

	// Reco muon - gen muon matches
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("matchedgenmuon1pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		KGenParticle* genMuon = product.GetMatchedGenMuon(event, settings, 0);
		return (genMuon != 0) ? genMuon->p4.Pt() : DefaultValues::UndefinedDouble;
	} );
	LambdaNtupleConsumer<ZJetTypes>::AddFloatQuantity("matchedgenmuon2pt", [settings](ZJetEvent const& event, ZJetProduct const& product)
	{
		KGenParticle* genMuon = product.GetMatchedGenMuon(event, settings, 1);
		return (genMuon != 0) ? genMuon->p4.Pt() : DefaultValues::UndefinedDouble;
	} );


	// Needs to be called at the end
	KappaLambdaNtupleConsumer::Init(settings);
}
