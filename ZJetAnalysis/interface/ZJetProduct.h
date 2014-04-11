/* Copyright (c) 2013 - All Rights Reserved
 *   Dominik Haitz <dhaitz@cern.ch>
 */

#pragma once

#include "Artus/KappaAnalysis/interface/KappaProduct.h"


class ZJetProduct : public KappaProduct
{
public:
	ZJetProduct() : KappaProduct() {};

	float m_product;

};
