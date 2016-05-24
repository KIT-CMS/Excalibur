#include "Producers/NPUProducer.h"

std::string NPUProducer::GetProducerId() const { return "NPUProducer"; }

void NPUProducer::Init(ZJetSettings const& settings)
{
    std::string file = settings.GetNPUFile();
    float minbxsec = settings.GetMinbxsec();
    float lum(0), xsavg(0), xsrms(0);
    unsigned long run(0), ls(0);
    ZJetProducerBase::Init(settings);

    LOG(INFO) << "Loading pile-up truth from " << file;
    std::ifstream f(file.c_str(), std::ios::in);
    if (!f.is_open())
        LOG(FATAL) << "Error in NPUProducer: Could not open luminosity file: " << file;

    while (f >> run >> ls >> lum >> xsrms >> xsavg) {
        LOG(DEBUG) << run << " " << ls << " " << lum << " " << xsavg << " " << xsrms << ": "
                   << (xsavg * minbxsec * 1000.0f) << " +/- " << (xsrms * minbxsec * 1000.0f);

        if (xsrms < 0)
            LOG(FATAL) << "Error in PileupTruthProducer: RMS = " << xsrms << " < 0";

        m_pumean[run][ls] = xsavg * minbxsec * 1000.0f;
    }
}

void NPUProducer::Produce(ZJetEvent const& event,
                          ZJetProduct& product,
                          ZJetSettings const& settings) const
{
    const unsigned long run = event.m_eventInfo->nRun;
    const unsigned long ls = event.m_eventInfo->nLumi;
    float npu = 0;

    try {
        npu = m_pumean.at(run).at(ls);
    } catch (const std::out_of_range& oor) {
        // warn once per lumi section if npu is unknown
        if (ls != lastls || run != lastrun)
            LOG(INFO) << "Warning in PileupTruthProducer: No luminosity for this run and ls: "
                      << run << ":" << ls;
        lastrun = run;
        lastls = ls;
    }

    product.npumean_data = npu;
}
