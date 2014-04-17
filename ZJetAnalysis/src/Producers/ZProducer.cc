#include "ZJet/ZJetAnalysis/interface/Producers/ZProducer.h"


void ZProducer::ProduceGlobal(ZJetEvent const& event, ZJetProduct& product,
                                         ZJetGlobalSettings const& globalSettings) const
{
	// other than 2 or three muons:
	if (product.m_validmuons.size() < 2 || product.m_validmuons.size() > 3)
		product.has_valid_z = false;

	std::vector<KDataLV> z_candidates;


	// Create all possible Z combinations
	// Note: If we have more than 3 muons in an event, this may produce double counting
	for (unsigned int i = 0; i < product.m_validmuons.size() ; ++i)
	{
		for (unsigned int j = i + 1; j < product.m_validmuons.size(); ++j)
		{
			KDataMuon const& m1 = product.m_validmuons.at(i);
			KDataMuon const& m2 = product.m_validmuons.at(j);

			if (m1.charge + m2.charge == 0)
			{
				KDataLV z;
				z.p4 = m1.p4 + m2.p4;

				if (z.p4.mass() > globalSettings.GetZMassMin() && z.p4.mass() < globalSettings.GetZMassMax())
				{
					z_candidates.push_back(z);
					product.m_decaymuons[0] = & m1;
					product.m_decaymuons[1] = & m2;
				}
			}
		}
	}

	// no ambiguous Z reconstruction:
	if (z_candidates.size() != 1)
		product.has_valid_z = false;
	else
	{
		product.Z = z_candidates[0];
		product.has_valid_z = true;
	}

}


