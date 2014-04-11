#include "ZJet/ZJetAnalysis/interface/Producers/ZProducer.h"


void ZProducer::ProduceGlobal(ZJetEvent const& event, ZJetProduct& product,
                                         ZJetGlobalSettings const& globalSettings) const
{

	if (event.m_muons->size() < 2)
		product.has_valid_z = false;
	else
	{
		KDataLV Z;
		Z.p4 = event.m_muons->at(0).p4 + event.m_muons->at(1).p4;
		product.has_valid_z = true;
	}

}


