#include "Producers/NPUProducer.h"

std::string NPUProducer::GetProducerId() const { return "NPUProducer"; }

void NPUProducer::Init(ZJetSettings const& settings)
{
	std::string file = settings.GetNPUFile();
    double minbxsec = settings.GetMinbxsec();

	//TODO: make this configurable?
	lastrun = -1;
	lastls = -1;

	ZJetProducerBase::Init(settings);
	LOG(INFO) << "Loading pile-up truth from " << file;
		ifstream f(file.c_str(), std::ios::in);
		if (!f.is_open())
			LOG(FATAL) <<"Error in PileupTruthProducer: Could not open luminosity file: " << file;

		int run, ls, cnt(0), cntMax(-1);
		double lum, xsavg, xsrms;
		while (f >> run >> ls >> lum >> xsrms >> xsavg && ++cnt != cntMax)
		{
			if (false && cnt < 10)  // debug
				LOG(DEBUG) << run << " " << ls << " "
					<< lum << " " << xsavg << " " << xsrms
					<< ": " << (xsavg * minbxsec * 1000) << " +/- " << (xsrms * minbxsec * 1000.0);

			if (xsrms < 0)
				LOG(FATAL) <<"Error in PileupTruthProducer: RMS = " << xsrms << " < 0";

			m_pumean[run][ls] = xsavg * minbxsec * 1000.0;
		}

}

void NPUProducer::Produce(ZJetEvent const& event, ZJetProduct& product,
                               ZJetSettings const& settings) const
{		const int run = event.m_eventInfo->nRun;
		const int ls = event.m_eventInfo->nLumi;
		double npu = 0;

		try
		{
			npu = m_pumean.at(run).at(ls);
//			LOG(INFO) << npu;
		}
		catch (const std::out_of_range& oor)
		{
			// warn once per lumi section if npu is unknown
			if (ls != lastls || run != lastrun)
				LOG(INFO) << "Warning in PileupTruthProducer: No luminosity for this run and ls: " << run << ":" << ls;
			lastrun = run;
			lastls = ls;
		}

		//LOG("per event: " << run << ":" << ls << " npu = " << npu);
		product.npudata = npu;
}
