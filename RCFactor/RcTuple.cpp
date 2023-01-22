// g++ -Wall -fPIC -I../include `root-config --cflags` RcHist.cpp -o ../bin/RcHist  `root-config --glibs` ../include/Integration.h

#include "Integration.h"
#include "TNtuple.h"


int RcHist(std::string target, TFile* inputFile, TFile* outputFile);

int main() {

  TStopwatch t;

  TFile* inputFile   = new TFile(inputDirectory  + "RcFactors.root", "READ");
  TFile* outputFile  = new TFile(outputDirectory + "RcTuples.root", "RECREATE");
  gROOT->cd();

  // std::cout << "Start5" << std::endl;
  RcHist("C",   inputFile, outputFile);
  std::cout << "C target is Done!" << std::endl;
  RcHist("Fe",  inputFile, outputFile);
  std::cout << "Fe target is Done!" << std::endl;
  RcHist("Pb",  inputFile, outputFile);
  std::cout << "Pb target is Done!" << std::endl;
  RcHist("DC",  inputFile, outputFile);
  std::cout << "DC target is Done!" << std::endl;
  RcHist("DFe", inputFile, outputFile);
  std::cout << "DFe target is Done!" << std::endl;
  RcHist("DPb", inputFile, outputFile);
  std::cout << "DPb target is Done!" << std::endl;

  inputFile->Close();
  outputFile->Close();

  t.Print();

}

int RcHist(std::string target, TFile* inputFile, TFile* outputFile) {

  std::cout << "Start" << std::endl;
  int n = target.length();
  char targetArr[n + 1];
  strcpy(targetArr, target.c_str());

  TNtuple* RcTuple[N_Zh][N_PION];
  for(int i = 0; i < N_Zh; i++) {
    for(int j = 0; j < N_PION; j++) {
      RcTuple[i][j] = new TNtuple(Form("RcTuple_%s_%i_%i", targetArr, i, j+1), "", "Rc");
    }
  }
  float Q2, Nu, Xb, Zh, Pt;
  float *vars = new float[1];
  float Masa = 0.938; // Mass Nucleon (Proton)

  for(int nPion = 1; nPion <= N_PION ; nPion++) { // Loops in every number of generated pions
    for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) { // Loops in every Q2 bin
      for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
        for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin
          for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { // Loops in every Pt2 bin

            Q2  = (Q2_BINS[Q2Counter] + Q2_BINS[Q2Counter+1])/2;
            Nu  = (Nu_BINS[NuCounter] + Nu_BINS[NuCounter+1])/2;
            Xb  = Q2/(2*Masa*Nu);
            Zh  = (Zh_BINS[ZhCounter] + Zh_BINS[ZhCounter+1])/2;
            Pt  = (TMath::Sqrt(Pt2_BINS[Pt2Counter]) + TMath::Sqrt(Pt2_BINS[Pt2Counter+1]))/2;

            TH1F* histRcFactors = (TH1F*) inputFile->Get(Form("RcFactor_%s_%.3f%.3f%.3f%.3f_%i", 
								targetArr, Q2, Xb, Zh, Pt, nPion));

            if(histRcFactors == NULL)         { continue; }
	    if(EmptyHist(histRcFactors) == 1) { continue; }

            for(int PhiCounter = 0; PhiCounter < N_Phi; PhiCounter++) {
              vars[0] = (float)histRcFactors->GetBinContent(PhiCounter+1);
              if(vars[0] != 0) {
                RcTuple[ZhCounter][nPion-1]->Fill(vars);
              }
            }
            delete histRcFactors;

          } // End Pt2 loop
        } // End Zh loop
      } // End Nu loop
    } // End Q2 loop
  } // End pion number loop
  outputFile->cd();
  for(int i = 0; i < N_Zh; i++) {
    for(int j = 0; j < N_PION; j++) {
      RcTuple[i][j]->Write();
    }
  }
  gROOT->cd();

  for(int i = 0; i < N_Zh; i++) {
    for(int j = 0; j < N_PION; j++) {
      delete RcTuple[i][j];
    }
  }

  return 0;

}
