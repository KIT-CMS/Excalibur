
#pragma once

#include "../ZJetTypes.h"
#include "Artus/KappaAnalysis/interface/Producers/ValidJetsProducer.h"


class ZJetValidJetsProducer: public ValidTaggedJetsProducer<ZJetTypes> {
public:

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE 
	{
		return "validjetproducer";
	}

protected:
		virtual bool AdditionalCriteria(KDataPFTaggedJet* jet, event_type const& event,
		 product_type& product, setting_type const& settings) const ARTUS_CPP11_OVERRIDE;
/*
	virtual void Produce(ZJetEvent const& event, ZJetProduct& product,
		ZJetSettings const& settings) const ARTUS_CPP11_OVERRIDE;

protected:

	// function that lets this producer work as both a global and a local producer
	virtual void <KDataPFJet>Produce(ZJetEvent const& event, ZJetProduct& product, std::string const algoname) const ;

	virtual bool JetIsValid(KDataPFTaggedJet const& jet, ZJetProduct const& product) const;
*/
};
