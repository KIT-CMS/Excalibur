#include <stdexcept>

TH2F* makeTH2FFromBinsAndContent(
    std::string name, std::string title,
    const std::vector<double>& xBinEdges,
    const std::vector<double>& yBinEdges,
    const std::vector<std::vector<double>>& binContents
) {

    double xBinEdgeArr[xBinEdges.size()];
    std::copy(xBinEdges.begin(), xBinEdges.end(), xBinEdgeArr);
    double yBinEdgeArr[yBinEdges.size()];
    std::copy(yBinEdges.begin(), yBinEdges.end(), yBinEdgeArr);

    if (binContents.size() != xBinEdges.size() - 1) {
        std::stringstream errMessage;
        errMessage << "Expected `binContents` to have " << xBinEdges.size() - 1 <<
                      " entries, found " << binContents.size();
        throw std::length_error(errMessage.str());
    }

    TH2F* h = new TH2F(
        name.c_str(), title.c_str(),
        xBinEdges.size() - 1, xBinEdgeArr,
        yBinEdges.size() - 1, yBinEdgeArr
    );

    for (size_t iX = 0; iX < binContents.size(); ++iX) {
        const auto& binContentsRow = binContents[iX];

        if (binContentsRow.size() != yBinEdges.size() - 1) {
            std::stringstream errMessage;
            errMessage << "Expected `binContents` row " << iX << " to have " <<
                          yBinEdges.size() - 1 << " entries, found " << binContentsRow.size();
            throw std::length_error(errMessage.str());
        }

        for (size_t iY = 0; iY < binContentsRow.size(); ++iY) {
            h->SetBinContent(iX+1, iY+1, binContentsRow[iY]);
        }
    }

    return h;
}

void makeWorkingPointHistFile() {
    std::vector<double> ptBins = {0, 10, 20, 30, 40, 50};
    std::vector<double> absEtaBins = {0, 2.5, 2.75, 3.0, 5.0};

    TFile* f = new TFile("puJetIDMVAWorkingPoints.root", "RECREATE");

    // values below from https://twiki.cern.ch/twiki/bin/view/CMS/PileupJetIDUL#Recommendations_for_2016_UL_data (14-DEC-2021)

    std::map<std::string, std::vector<std::vector<double>>> minPUJetIDValueMap;

    // 2016
    minPUJetIDValueMap["2016UL_Tight"] = {
        { 0.71, -0.32, -0.30, -0.22},  // Pt0To10
        { 0.71, -0.32, -0.30, -0.22},  // Pt10To20
        { 0.87, -0.08, -0.16, -0.12},  // Pt20To30
        { 0.94,  0.24,  0.05,  0.10},  // Pt30To40
        { 0.97,  0.48,  0.26,  0.29}   // Pt40To50
    };

    minPUJetIDValueMap["2016UL_Medium"] = {
        { 0.20, -0.56, -0.43, -0.38},  // Pt0To10
        { 0.20, -0.56, -0.43, -0.38},  // Pt10To20
        { 0.62, -0.39, -0.32, -0.29},  // Pt20To30
        { 0.86, -0.10, -0.15, -0.08},  // Pt30To40
        { 0.93,  0.19,  0.04,  0.12}   // Pt40To50
    };

    minPUJetIDValueMap["2016UL_Loose"] = {
        {-0.95, -0.70, -0.52, -0.49},  // Pt0To10
        {-0.95, -0.70, -0.52, -0.49},  // Pt10To20
        {-0.90, -0.57, -0.43, -0.42},  // Pt20To30
        {-0.71, -0.36, -0.29, -0.23},  // Pt30To40
        {-0.42, -0.09, -0.14, -0.02}   // Pt40To50
    };

    // 2017
    minPUJetIDValueMap["2017UL_Tight"] = {
        { 0.77,  0.38, -0.31, -0.21},  // Pt0To10
        { 0.77,  0.38, -0.31, -0.21},  // Pt10To20
        { 0.90,  0.60, -0.12, -0.13},  // Pt20To30
        { 0.96,  0.82,  0.20,  0.09},  // Pt30To40
        { 0.98,  0.92,  0.47,  0.29}   // Pt40To50
    };

    minPUJetIDValueMap["2017UL_Medium"] = {
        { 0.26, -0.33, -0.54, -0.37},  // Pt0To10
        { 0.26, -0.33, -0.54, -0.37},  // Pt10To20
        { 0.68, -0.04, -0.43, -0.30},  // Pt20To30
        { 0.90,  0.36, -0.16, -0.09},  // Pt30To40
        { 0.96,  0.61,  0.14,  0.12}   // Pt40To50
    };

    minPUJetIDValueMap["2017UL_Loose"] = {
        {-0.95, -0.72, -0.68, -0.47},  // Pt0To20
        {-0.95, -0.72, -0.68, -0.47},  // Pt10To20
        {-0.88, -0.55, -0.60, -0.43},  // Pt20To30
        {-0.63, -0.18, -0.43, -0.24},  // Pt30To40
        {-0.19,  0.22, -0.13, -0.03}   // Pt40To50
    };

    // 2018 (same as 2017)
    minPUJetIDValueMap["2018UL_Tight"]  = minPUJetIDValueMap["2017UL_Tight"];
    minPUJetIDValueMap["2018UL_Medium"] = minPUJetIDValueMap["2017UL_Medium"];
    minPUJetIDValueMap["2018UL_Loose"]  = minPUJetIDValueMap["2017UL_Loose"];

    for (const auto& minPUJetIDWorkingPointValues : minPUJetIDValueMap) {
        std::string histName = "puJetIDMVAWorkingPoint_AK4PFCHS_" +
            minPUJetIDWorkingPointValues.first;

        TH2F *h = makeTH2FFromBinsAndContent(
            histName, histName,
            ptBins, absEtaBins,
            minPUJetIDWorkingPointValues.second
        );
        h->Write();
    }

    f->Close();
}
