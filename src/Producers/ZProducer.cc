#include "Producers/ZProducer.h"

std::string ZProducer::GetProducerId() const { return "ZProducer"; }

void ZProducer::Produce(ZJetEvent const& event, ZJetProduct& product,
                        ZJetSettings const& settings) const
{
	// Create all possible Z combinations
	// Note: If we have more than 3 muons in an event, this may produce double
	// counting
	std::vector<KLV> z_cand;
	for (unsigned int i = 0; i < product.m_validMuons.size(); ++i)
	{
		for (unsigned int j = i + 1; j < product.m_validMuons.size(); ++j)
		{
			KMuon* const m1 = product.m_validMuons.at(i);
			KMuon* const m2 = product.m_validMuons.at(j);
			if (m1->charge() + m2->charge() == 0)
			{
				KLV z;
				z.p4 = m1->p4 + m2->p4;
				if (z.p4.mass() >
				        settings.GetZMass() - settings.GetZMassRange() &&
				    z.p4.mass() <
				        settings.GetZMass() + settings.GetZMassRange())
				{
					z_cand.emplace_back(z);
				}
			}
		}
	}
	// If there is more than one valid Z candidate we chose the one with its
	// mass closest to the Z mass.
	if (z_cand.size() > 0)
	{
		unsigned int best_z_cand = 9999;
		for (unsigned int i = 0; i < z_cand.size(); ++i)
		{
			if (best_z_cand == 9999 ||
			    fabs(z_cand[i].p4.mass() - settings.GetZMass()) <=
			        fabs(z_cand[best_z_cand].p4.mass() - settings.GetZMass()))
			{
				best_z_cand = i;
			}
		}
		product.m_z = z_cand[best_z_cand];
		product.m_validZ = true;
	}
	else
	{
		product.m_validZ = false;
		return;
	}
}
