/**
 * MuScleFitCorrector class
 * Author M. De Mattia - 18/11/2008
 * Author S. Casasso	 - 25/10/2012
 * Author E. Migliore	- 25/10/2012
 */

#include <iostream>
#include <fstream>
#include <sstream>
#include "Functions.h"
#include "TRandom3.h"
#include "MuScleFitCorrector.h"

/**
 * This is used to have a common set of functions for the specialized templates to use.
 * The constructor receives the name identifying the parameters for the correction function.
 * It reads the parameters from a txt file in data/.
 */

/**
 * The constructor takes a string identifying the parameters to read. It
 * parses the txt file containing the parameters, extracts the index of the
 * correction function and saves the corresponding pointer. It then fills the
 * vector of parameters.
 */
MuScleFitCorrector::MuScleFitCorrector(const std::string& identifier)
{
    fileName_ = identifier.c_str();
    readParameters(identifier);
    gRandom_ = new TRandom3();
}

MuScleFitCorrector::~MuScleFitCorrector() {}

// Returns a pointer to the selected function
scaleFunctionBase<double*>* MuScleFitCorrector::getScaleFunction() { return scaleFunction_; }

resolutionFunctionBase<double*>* MuScleFitCorrector::getResolFunction()
{
    return resolutionFunction_;
}

// Method to get correct pt
// double MuScleFitCorrector::getCorrectPt(const RMFLV& lorentzVector, const int& chg) const
double MuScleFitCorrector::getCorrectPt(const RMFLV& lorentzVector, const int& chg) const
{
    // Loop on all the functions and apply them iteratively on the pt corrected by the previous
    // function.
    double pt = lorentzVector.Pt();
    pt = (scaleFunction_->scale(pt, lorentzVector.Eta(), lorentzVector.Phi(), chg, scaleParArray_));
    return pt;
}

// Return the squared difference of relative pT resolutions data-MC
double MuScleFitCorrector::getSigmaPtDiffSquared(const double& pt, const double& eta) const
{
    double sigmaPtData = resolutionFunction_->sigmaPt(pt, eta, resolDataParArray_);
    double sigmaPtMC = resolutionFunction_->sigmaPt(pt, eta, resolMCParArray_);
    return (sigmaPtData * sigmaPtData - sigmaPtMC * sigmaPtMC);
}

// Method to get correct pt (baseline)
double MuScleFitCorrector::getSmearedPt(const RMFLV& lorentzVector, const int& chg, bool fake) const
{
    double pt = lorentzVector.Pt();
    double eta = lorentzVector.Eta();
    double squaredDiff = getSigmaPtDiffSquared(pt, eta);
    if (squaredDiff < 0)
        return pt;
    double Cfact = 0.;
    if (fileName_.Contains("smearPrompt"))  // smear Summer12 against 2012 Prompt data
        Cfact = 0.85;
    else if (fileName_.Contains("smearReReco"))  // smear Summer12 against 2012 ReReco data
        Cfact = 0.75;
    else if (fileName_.Contains("2011_MC"))  // smear Fall11 against 2011 ReReco data
        Cfact = 0.8;
    else {
        std::cout << "Are you sure you want to smear data??" << std::endl;
        exit(1);
    }
    double sPar = Cfact * sqrt(squaredDiff);
    double curv = ((double)chg / pt);
    double normSmearFact = gRandom_->Gaus(0, sPar);
    if (fake)
        normSmearFact = sPar;
    double smearedCurv = curv + fabs(curv) * normSmearFact;

    return 1. / ((double)chg * smearedCurv);
}

// Method to apply correction to a RMFLV&
void MuScleFitCorrector::applyPtCorrection(RMFLV& lorentzVector, const int& chg) const
{
    double corrPt = getCorrectPt(lorentzVector, chg);
    lorentzVector.SetPt(corrPt);
}

// Method to apply smearing to a RMFLV&
void MuScleFitCorrector::applyPtSmearing(RMFLV& lorentzVector, const int& chg, bool fake) const
{
    double smearedPt = getSmearedPt(lorentzVector, chg, fake);
    lorentzVector.SetPt(smearedPt);
}

std::vector<double> MuScleFitCorrector::getResolMCParVec() { return resolMCParVec_; }

// Convert vectors to arrays for faster random access.
// The first pointer is replaced, thus it is taken by reference.
void MuScleFitCorrector::convertToArrays()
{
    int resolParNum = resolutionFunction_->parNum();
    int scaleParNum = scaleFunction_->parNum();

    int resolDataParVecSize = resolDataParVec_.size();
    int resolMCParVecSize = resolMCParVec_.size();
    int scaleParVecSize = scaleParVec_.size();

    useResol_ = false;
    if (resolDataParVecSize != 0 && resolMCParVecSize != 0)
        useResol_ = true;

    if (resolParNum != resolDataParVecSize && useResol_) {
        std::cout << "Error: inconsistent number of parameters: resolutionFunction has "
                  << resolParNum << " parameters but " << resolDataParVecSize
                  << " have been read from file" << std::endl;
        exit(1);
    }

    if (resolParNum != resolMCParVecSize && useResol_) {
        std::cout << "Error: inconsistent number of parameters: resolutionFunction has "
                  << resolParNum << " parameters but " << resolMCParVecSize
                  << " have been read from file" << std::endl;
        exit(1);
    }

    if (scaleParNum != scaleParVecSize) {
        std::cout << "Error: inconsistent number of parameters: scaleFunction has " << scaleParNum
                  << " parameters but " << scaleParVecSize << " have been read from file"
                  << std::endl;
        exit(1);
    }

    std::vector<double>::const_iterator scaleParIt = scaleParVec_.begin();
    std::vector<double>::const_iterator resolDataParIt = resolDataParVec_.begin();
    std::vector<double>::const_iterator resolMCParIt = resolMCParVec_.begin();

    scaleParArray_ = new double[scaleParNum];
    resolDataParArray_ = new double[resolParNum];
    resolMCParArray_ = new double[resolParNum];

    for (int iPar = 0; iPar < scaleParNum; ++iPar) {
        double parameter = *scaleParIt;
        scaleParArray_[iPar] = parameter;
        ++scaleParIt;
    }

    if (useResol_) {
        for (int iPar = 0; iPar < resolParNum; ++iPar) {
            double parameter = *resolDataParIt;
            resolDataParArray_[iPar] = parameter;
            ++resolDataParIt;
        }

        for (int iPar = 0; iPar < resolParNum; ++iPar) {
            double parameter = *resolMCParIt;
            resolMCParArray_[iPar] = parameter;
            ++resolMCParIt;
        }
    }
}

//----------------------------//
// Parser of the parameters file
void MuScleFitCorrector::readParameters(const TString& fileName)
{
    scaleParArray_ = nullptr;
    resolDataParArray_ = nullptr;
    resolMCParArray_ = nullptr;

    // Read the parameters file
    ifstream parametersFile(fileName.Data());

    if (!parametersFile.is_open()) {
        std::cout << "Error: file " << fileName << " not found. Aborting." << std::endl;
        abort();
    }

    std::string line;
    int nReadPar = 0;
    std::string iteration("Iteration ");
    // Loop on the file lines
    while (parametersFile) {
        getline(parametersFile, line);
        size_t lineInt = line.find("value");
        size_t iterationSubStr = line.find(iteration);

        if (iterationSubStr != std::string::npos) {
            std::stringstream sLine(line);
            std::string num;
            int scaleFunctionNum = 0;
            int resolutionFunctionNum = 0;
            int wordCounter = 0;

            // Warning: this strongly depends on the parameters file structure.
            while (sLine >> num) {
                ++wordCounter;
                if (wordCounter == 8) {
                    std::stringstream in(num);
                    in >> resolutionFunctionNum;
                }

                if (wordCounter == 9) {
                    std::stringstream in(num);
                    in >> scaleFunctionNum;
                }
            }

            scaleFunctionId_ = scaleFunctionNum;
            scaleFunction_ = scaleFunctionService(scaleFunctionNum);
            resolutionFunctionId_ = resolutionFunctionNum;
            resolutionFunction_ = resolutionFunctionService(resolutionFunctionNum);

            /*			 std::cout<<"Function IDs: "<<std::endl; */
            /*			 std::cout<<"		 scale function number "<<scaleFunctionId_<<std::endl;
             */
            /*			 std::cout<<"		 resolution function number
             * "<<resolutionFunctionId_<<std::endl; */
        }

        int nScalePar = scaleFunction_->parNum();
        int nResolPar = resolutionFunction_->parNum();

        if (lineInt != std::string::npos) {
            size_t subStr1 = line.find("value");
            std::stringstream paramStr;
            double param = 0;
            paramStr << line.substr(subStr1 + 5);
            paramStr >> param;
            // Fill the last vector of parameters, which corresponds to this iteration.
            if (nReadPar < nScalePar) {
                scaleParVec_.push_back(param);
            } else if (nReadPar < (nScalePar + nResolPar)) {
                resolDataParVec_.push_back(param);
            } else if (nReadPar < (nScalePar + 2 * nResolPar)) {
                resolMCParVec_.push_back(param);
            }
            ++nReadPar;
        }
    }
    convertToArrays();

    /*	 std::cout<<"Scale function n. "<<scaleFunctionId_<<" has
     * "<<scaleFunction_->parNum()<<"parameters:"<<std::endl; */
    /*	 for (int ii=0; ii<scaleFunction_->parNum(); ++ii){ */
    /*		 std::cout<<"par["<<ii<<"] = "<<scaleParArray_[ii]<<std::endl; */
    /*	 } */
}
