#include "TH1.h"

#include "Excalibur/Compile/interface/Producers/ZJetPUWeightProducer.h"


std::string ZJetPUWeightProducer::GetProducerId() const {
	return "ZJetPUWeightProducer";
}

void ZJetPUWeightProducer::Init(ZJetSettings const& settings) {
	ZJetProducerBase::Init(settings);

    if(settings.GetZJetPUWeightFiles().size()!= settings.GetZJetPUWeightSuffixes().size())
    {
        LOG(FATAL) << "[ZJetPUWeightProducer] Number of PUWeight-files " << settings.GetZJetPUWeightFiles().size() << " differs from corresponding number of PUWeight-names " << settings.GetZJetPUWeightSuffixes().size();
    }

    const std::string histogramName = "pileup";
    m_pileupWeights.resize(settings.GetZJetPUWeightFiles().size());
    m_bins.resize(settings.GetZJetPUWeightFiles().size());
    m_pileupWeightNames.resize(settings.GetZJetPUWeightFiles().size());
    LOG(DEBUG) << "[ZJetPUWeightProducer] Loading pile-up weights from files...";

    for(size_t iPUfile = 0; iPUfile < settings.GetZJetPUWeightFiles().size(); iPUfile++)
    {
        LOG(DEBUG) << "[ZJetPUWeightProducer] \t" << settings.GetZJetPUWeightFiles()[iPUfile] << "/" << histogramName;
        if(settings.GetZJetPUWeightSuffixes()[iPUfile].empty())
        {
            LOG(FATAL) << "[ZJetPUWeightProducer] \t\tPUWeight-suffix at position " << iPUfile+1 << "is empty";
        }
        m_pileupWeightNames[iPUfile] = "puWeight" + settings.GetZJetPUWeightSuffixes()[iPUfile];
        
        TFile file(settings.GetZJetPUWeightFiles()[iPUfile].c_str(), "READONLY");
        TH1D* pileupHistogram = dynamic_cast<TH1D*>(file.Get(histogramName.c_str()));

        m_pileupWeights[iPUfile].clear();
        for (int i = 1; i <= pileupHistogram->GetNbinsX(); ++i)
        {
            m_pileupWeights[iPUfile].push_back(pileupHistogram->GetBinContent(i));
        }
        m_bins[iPUfile] = 1.0 / pileupHistogram->GetBinWidth(1);
        delete pileupHistogram;
        file.Close();
    }

	
}

void ZJetPUWeightProducer::Produce(ZJetEvent const& event, ZJetProduct& product,
                     ZJetSettings const& settings) const
{
	assert(event.m_genEventInfo != nullptr);

	for(size_t iPUweight = 0; iPUweight < m_pileupWeights.size(); iPUweight++)
    {
        unsigned int puBin = static_cast<unsigned int>(static_cast<double>(event.m_genEventInfo->nPUMean) * m_bins[iPUweight]);
        if (puBin < m_pileupWeights[iPUweight].size())
            product.m_weights[m_pileupWeightNames[iPUweight]] = m_pileupWeights[iPUweight].at(puBin);
        else
            product.m_weights[m_pileupWeightNames[iPUweight]] = 1.0;
    }
}
