#pragma once

#include "ZJetTypes.h"

/** Producer class for Z boson reconstruction from muons/electrons.
 *
 *	Needs to run after the valid object producers.
 * 	Needs min 2 valid leptons and max 3 valid leptons!
 */

template<class TLepton>
class ZProducerBase : public ZJetProducerBase
{
  public:

	ZProducerBase(std::vector<TLepton*> ZJetProduct::*validLeptons) : ZJetProducerBase(), m_validLeptonsMember(validLeptons) {};

	virtual void Produce(ZJetEvent const& event, ZJetProduct& product,
	                     ZJetSettings const& settings) const override

{
	// Create all possible Z combinations
	// Note: If we have more than 3 muons in an event, this may produce double
	// counting
	std::vector<KLV> z_cand;
	for (unsigned int i = 0; i < (product.*m_validLeptonsMember).size(); ++i)
	{
		for (unsigned int j = i + 1; j < (product.*m_validLeptonsMember).size(); ++j)
		{
			KLepton* const m1 = (product.*m_validLeptonsMember).at(i);
			KLepton* const m2 = (product.*m_validLeptonsMember).at(j);
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

;
 private:
	std::vector<TLepton*> ZJetProduct::*m_validLeptonsMember;
};


class ZmmProducer: public ZProducerBase<KMuon>{
public:
	virtual std::string GetProducerId() const override {return "ZmmProducer";};
	ZmmProducer(): ZProducerBase<KMuon>(&ZJetProduct::m_validMuons){}
};

class ZeeProducer: public ZProducerBase<KElectron>{
public:
	virtual std::string GetProducerId() const override {return "ZeeProducer";};
	ZeeProducer(): ZProducerBase<KElectron>(&ZJetProduct::m_validElectrons){}
};


