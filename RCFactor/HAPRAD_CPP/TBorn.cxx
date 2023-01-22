#include "TBorn.h"
#include "TRadCor.h"
#include "TKinematicalVariables.h"
#include "TLorentzInvariants.h"
#include "THadronKinematics.h"
#include "haprad_constants.h"
#include "square_power.h"
#include <iostream>

TBorn::TBorn(const TRadCor* rc) : fH(rc) {
  fKin = rc->GetKinematicalVariables();
  fInv = rc->GetLorentzInvariants();
  fHadKin = rc->GetHadronKinematics();

  const Double_t& M = kMassProton;
  const Double_t& m_h = kMassDetectedHadron;

  fThetaB[0] = fInv->Q2();
  // std::cout <<  "fThetaB[0]  "<<fThetaB[0] << std::endl;
  fThetaB[1] = (fInv->S() * fInv->X() - SQ(M) * fInv->Q2()) / 2.;
  fThetaB[2] = (fHadKin->V1() * fHadKin->V2() - SQ(m_h) * fInv->Q2()) / 2;
  fThetaB[3] = (fHadKin->V2() * fInv->S() + fHadKin->V1() * fInv->X() - fKin->Z() * fInv->Q2() * fInv->Sx()) / 2;
    // std::cout <<  "fThetaB[1]  "<<fThetaB[1] << std::endl;
    //   std::cout <<  "fThetaB[2]  "<<fThetaB[2] << std::endl;
    //     std::cout <<  "fThetaB[3]  "<<fThetaB[3] << std::endl;
}

TBorn::~TBorn() {}

Double_t TBorn::Evaluate(void) {
  fH.Evaluate(0., 0., 0.);

  Double_t sum = 0.;
  for (Int_t i = 0; i < 4; ++i) {
    sum = sum + fThetaB[i] * fH(i);
      // std::cout << "Fh " << fH(i) << std::endl;
  }
  return 2 * sum / SQ(fInv->Q2());
}
