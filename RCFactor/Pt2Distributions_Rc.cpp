// This code generate a histogram and TGraphErrors of the Pt2 Pt2 distribution in the Zh nBins
// It can be compiled using
// g++ -Wall -fPIC -I./include `root-config --cflags` Pt2Distributions_Rc.cpp -o ./bin/Pt2Distributions_Rc  `root-config --glibs` ./include/Broad_Rc.h

#include "Broad_Rc.h"

int Pt2_Distribution(std::string target, TFile* inputFile, TFile* outputFile);

int main() {

  TFile* inputFile   = new TFile(inputDirectory  + "meanPt2_Zh_Rc.root", "READ");
  TFile* outputFile  = new TFile(outputDirectory + "Pt2_Distribution_Rc.root", "RECREATE");
  gROOT->cd();

  Pt2_Distribution("C",   inputFile, outputFile);
  Pt2_Distribution("Fe",  inputFile, outputFile);
  Pt2_Distribution("Pb",  inputFile, outputFile);
  Pt2_Distribution("DC",  inputFile, outputFile);
  Pt2_Distribution("DFe", inputFile, outputFile);
  Pt2_Distribution("DPb", inputFile, outputFile);

  inputFile->Close();
  outputFile->Close();


}

int Pt2_Distribution(std::string target, TFile* inputFile, TFile* outputFile) {

  TStopwatch t;

  std::cout << "Start" << std::endl;

  // Creating a array of chars instead of a string to use Form method
  int n = target.length();
  char targetArr[n + 1];
  strcpy(targetArr, target.c_str());


  for(int nPion = 1; nPion <= N_PION; nPion++) { // Loops in every number of pion
    // Generate a histogram to save Zh for every number of pion in the final event
    for(int ZhCounter = 0 ; ZhCounter < N_Zh ; ZhCounter++) { // Loops in every Zh bin
      // Generate a histogram for every bin of zh
      TGraphErrors* Pt2Distribution;
          // Sum the histograms for every bin of Q2 and Nu
      TH1F* histPt2 = (TH1F*) inputFile->Get(Form("corr_data_Pt2_%s_%i_%i", targetArr,
						        ZhCounter, nPion));

      Pt2Distribution = (TGraphErrors*) TH1TOTGraph(histPt2);
      outputFile->cd();
      histPt2->Write(Form("Pt2_Distribution_Rc_%s_%i_%i-hist", targetArr, ZhCounter, nPion));
      Pt2Distribution->Write(Form("Pt2_Distribution_Rc_%s_%i_%i", targetArr, ZhCounter, nPion));
      gROOT->cd();

      delete histPt2;
      delete Pt2Distribution;
    } // End Zh loop
  } // End number pion event loop

  t.Print();
  return 0;

}
