/**
 * MuScleFitCorrector class
 * Author M. De Mattia - 18/11/2008
 * Author S. Casasso	 - 25/10/2012
 * Author E. Migliore	- 25/10/2012
 */
#pragma once
//#include "GlobalInclude.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include "Functions.h"
#include "TLorentzVector.h"
#include <Math/PtEtaPhiM4D.h>
#include <Math/LorentzVector.h>
#include "TRandom3.h"
#include "Kappa/DataFormats/interface/KBasic.h"

/**
 * This is used to have a common set of functions for the specialized templates to use.
 * The constructor receives the name identifying the parameters for the correction function.
 * It reads the parameters from a txt file in data/.
 */
class MuScleFitCorrector
{
  public:
    /**
     * The constructor takes a string identifying the parameters to read. It
     * parses the txt file containing the parameters, extracts the index of the
     * correction function and saves the corresponding pointer. It then fills the
     * vector of parameters.
     */
    MuScleFitCorrector(const std::string& identifier);
    ~MuScleFitCorrector();

    // Returns a pointer to the selected function
    scaleFunctionBase<double*>* getScaleFunction();
    resolutionFunctionBase<double*>* getResolFunction();

    // Method to get correct pt
    // double getCorrectPt(const RMFLV& lorentzVector, const int& chg) const;
    double getCorrectPt(const RMFLV& lorentzVector, const int& chg) const;

    // Return the squared difference of relative pT resolutions data-MC
    double getSigmaPtDiffSquared(const double& pt, const double& eta) const;

    // Method to get correct pt (baseline)
    double getSmearedPt(const RMFLV& lorentzVector, const int& chg, bool fake = false) const;

    // Method to apply correction to a TLorentzVector
    void applyPtCorrection(RMFLV& lorentzVector, const int& chg) const;

    // Method to apply smearing to a TLorentzVector
    void applyPtSmearing(RMFLV& lorentzVector, const int& chg, bool fake = false) const;

    std::vector<double> getResolMCParVec();

  protected:
    // File name
    TString fileName_;

    // Identification numbers
    int scaleFunctionId_;
    int resolutionFunctionId_;

    // Vectors of parameters
    std::vector<double> scaleParVec_;
    std::vector<double> resolDataParVec_;
    std::vector<double> resolMCParVec_;

    // We will use the array for the function calls because it is faster than the vector for random
    // access.
    double* scaleParArray_;
    double* resolDataParArray_;
    double* resolMCParArray_;

    // Convert vectors to arrays for faster random access. The first pointer is replaced, thus it is
    // taken by reference.
    void convertToArrays();

    //----------------------------//
    // Parser of the parameters file
    void readParameters(const TString& fileName);

    // Functions
    scaleFunctionBase<double*>* scaleFunction_;
    resolutionFunctionBase<double*>* resolutionFunction_;

    // Pointer for TRandom3 access
    TRandom3* gRandom_;

    // Bool for using resolution function or not (value depends from the information on the
    // parameters txt file)
    bool useResol_;
};
