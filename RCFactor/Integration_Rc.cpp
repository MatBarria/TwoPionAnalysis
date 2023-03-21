// This code integrate the histograms generate by AccCorrection.cpp
// To obtain the means of Pt2
// It can be compile with
// g++ -Wall -fPIC -I./include `root-config --cflags` Integration_Rc.cpp -o ./bin/Integration_Rc  `root-config --glibs` ./include/Integration_Rc.h

#include "Pt2Processing_Rc.h"

int main() {

  TStopwatch t;

  std::cout << "PhiPQ integration" << std::endl;
  CallPhiIntegration(inputDirectory , outputDirectory);
  std::cout << "Q2 and Nu integration" << std::endl;
  CallQ2NuIntegration(inputDirectory , outputDirectory);
  std::cout << "Pt2 Processing" << std::endl;
  CallPt2Processing(inputDirectory , outputDirectory);
  std::cout << "Zh integration" << std::endl;
  CallZhIntegration(inputDirectory , outputDirectory);

  t.Print();
  return 0;

}
