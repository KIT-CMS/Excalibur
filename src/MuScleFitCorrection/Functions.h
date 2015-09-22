/**
 * Scale function classes
 * Author M. De Mattia - 18/11/2008
 * Author S. Casasso   - 25/10/2012
 * Author E. Migliore  - 25/10/2012
 */
#pragma once
#include <iostream>
#include <vector>
#include <cmath>
#include "TMath.h"
#include "TString.h"
#include "TF1.h"
#include "TRandom.h"

/**
 * Used to define parameters inside the functions.
 */

struct ParSet {
    ParSet();
    ParSet(const TString& inputName,
           const double& inputStep,
           const double& inputMini,
           const double& inputMaxi);
    TString name;
    double step, mini, maxi;
};

// ----------------------- //
//     Scale functors      //
// ----------------------- //

template <class T>
class scaleFunctionBase
{
  public:
    virtual double scale(const double& pt,
                         const double& eta,
                         const double& phi,
                         const int chg,
                         const T& parScale) const = 0;
    virtual ~scaleFunctionBase() = 0;
    virtual unsigned long parNum() const { return parNum_; };

  protected:
    unsigned long parNum_;
    virtual void setPar(double* Start,
                        double* Step,
                        double* Mini,
                        double* Maxi,
                        int* ind,
                        TString* parname,
                        const T& parResol,
                        const std::vector<int>& parResolOrder,
                        const std::vector<ParSet>& parSet);
};

template <class T>
inline scaleFunctionBase<T>::~scaleFunctionBase()
{
}  // defined even though it's pure virtual; should be faster this way.

//
// Curvature: (linear eta + sinusoidal in phi (both in 5 eta bins)) * global scale
// ------------------------------------------------------------
template <class T>
class scaleFunction50 : public scaleFunctionBase<T>
{
  public:
    scaleFunction50() { this->parNum_ = 27; }
    virtual double scale(const double& pt,
                         const double& eta,
                         const double& phi,
                         const int chg,
                         const T& parScale) const;
};

// ----------------------- //
//   Resolution functors   //
// ----------------------- //

template <class T>
class resolutionFunctionBase
{
  public:
    virtual double sigmaPt(const double& pt, const double& eta, const T& parval) = 0;

    resolutionFunctionBase() {}
    virtual ~resolutionFunctionBase() = 0;
    virtual unsigned long parNum() const { return parNum_; }

  protected:
    unsigned long parNum_;
};

template <class T>
inline resolutionFunctionBase<T>::~resolutionFunctionBase()
{
}  // defined even though it's pure virtual; should be faster this way.

template <class T>
class resolutionFunction45 : public resolutionFunctionBase<T>
{
  public:
    resolutionFunction45() { this->parNum_ = 13; }

    inline double getGEO(const double& pt, const double& eta, const T& parval);
    inline double getMS(const double& pt, const double& eta, const T& parval);
    virtual double sigmaPt(const double& pt, const double& eta, const T& parval);
};

template <class T>
class resolutionFunction46 : public resolutionFunctionBase<T>
{
  public:
    resolutionFunction46() { this->parNum_ = 13; }
    int etaBin(const double& eta);
    virtual double sigmaPt(const double& pt, const double& eta, const T& parval);
};

// parametrization as sum in quadrature
// Geometric and MSC both as function of eta, adding straight lines between parabolas wrt type51
template <class T>
class resolutionFunction57 : public resolutionFunctionBase<T>
{
  public:
    resolutionFunction57() { this->parNum_ = 17; }

    inline double getGEO(const double& pt, const double& eta, const T& parval);
    inline double centralParabola(const double& pt, const double& eta, const T& parval);
    inline double middleParabola(const double& pt, const double& eta, const T& parval);
    inline double leftParabola(const double& pt, const double& eta, const T& parval);
    inline double rightParabola(const double& pt, const double& eta, const T& parval);
    inline double leftLine(const double& pt, const double& eta, const T& parval);
    inline double rightLine(const double& pt, const double& eta, const T& parval);
    inline double getMSC(const double& pt, const double& eta, const T& parval);
    virtual double sigmaPt(const double& pt, const double& eta, const T& parval);
};

// Service to build the scale functor corresponding to the passed identifier
scaleFunctionBase<double*>* scaleFunctionService(const int identifier);

// Service to build the resolution functor corresponding to the passed identifier
resolutionFunctionBase<double*>* resolutionFunctionService(const int identifier);
