// This code integrate the histograms generate by AccCorrection.cpp
// To obtain the means of Pt2
// It can be compile with
// g++ -Wall -fPIC -I../include `root-config --cflags` Integration.cpp -o ../bin/Integration  `root-config --glibs` ../include/Integration.h ../include/Pt2Processing.h

#include "../include/Pt2Processing.h"

int main(){

  TStopwatch t;

  std::cout << "PhiPQ integration" << std::endl;
  CallPhiIntegration(inputDirectory , outputDirectory);

  std::cout << "Q2 and Nu integration" << std::endl;
  CallQ2NuIntegration(inputDirectory , outputDirectory);
  
  std::cout << "Q2 and Zh integration" << std::endl;
  CallQ2ZhIntegration(inputDirectory , outputDirectory);
  
  std::cout << "Nu and Zh integration" << std::endl;
  CallNuZhIntegration(inputDirectory , outputDirectory);
  
  std::cout << "Pt2 Processing" << std::endl;
  CallPt2Processing(inputDirectory , outputDirectory);
  
  std::cout << "Q2, Nu and Zh integration" << std::endl;
  CallZhIntegration(inputDirectory , outputDirectory);

  t.Print();

}
