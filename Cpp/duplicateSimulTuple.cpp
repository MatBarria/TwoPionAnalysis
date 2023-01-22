// It can be compile with
// g++ -Wall -fpic  `root-config --cflags` duplicateSimulTuple.cpp -o ./bin/duplicateSimulTuple `root-config --glibs`
// For the target name use (D,C,Fe,Pb)

#include <iostream>
#include <string>
#include "TString.h"
#include "TFile.h"
#include "TNtuple.h"
#include "TStopwatch.h"
#include "TROOT.h"

int main(int argc, char* argv[]) {

  if(argc != 2) {
    std::cout << "Insert (just) the target name as a parameter" << std::endl;
    return 0;
  }

  TStopwatch t;

  // For the Target name use (D,C,Fe,Pb)
  std::string target = argv[1];
  // Creating a array of chars instead of a string to use Form method
  int n = target.length();
  char targetArr[n + 1];
  strcpy(targetArr, target.c_str());

  TFile *simFile = new TFile(Form(dataDirectory + "SimulTuple_%sdeltaZ.root", targetArr), "READ");

  const char* VarListGen = "Gen:Rec:Q2_gen:Nu_gen:Zh_gen:Pt2_gen:PhiPQ_gen";
  const char* VarListRec = "Gen:Rec:Q2_rec:Nu_rec:Zh_rec:Pt2_rec:PhiPQ_rec";
  float *varsGen = new Float_t[7];
  float *varsRec = new Float_t[7];

  TNtuple *simulTuple = (TNtuple*) simFile->Get("ntuple_sim");

  if(simulTuple==NULL){std::cout <<"la ptm, que paso ahora\n";}
  // Read the necesary variables
  simulTuple->SetBranchAddress("Gen"       , &varsGen[0]);
  simulTuple->SetBranchAddress("Rec"       , &varsGen[1]);
  simulTuple->SetBranchAddress("Q2_gen"    , &varsGen[2]);
  simulTuple->SetBranchAddress("Nu_gen"    , &varsGen[3]);
  simulTuple->SetBranchAddress("Zh_gen"    , &varsGen[4]);
  simulTuple->SetBranchAddress("Pt2_gen"   , &varsGen[5]);
  simulTuple->SetBranchAddress("PhiPQ_gen" , &varsGen[6]);
  simulTuple->SetBranchAddress("Q2_rec"    , &varsRec[2]);
  simulTuple->SetBranchAddress("Nu_rec"    , &varsRec[3]);
  simulTuple->SetBranchAddress("Zh_rec"    , &varsRec[4]);
  simulTuple->SetBranchAddress("Pt2_rec"   , &varsRec[5]);
  simulTuple->SetBranchAddress("PhiPQ_rec" , &varsRec[6]);

  TFile *outputFile = new TFile(dataDirectory + Form("SimulTuple_%s.root", targetArr), "RECREATE");
  gROOT->cd();
  TNtuple *genTuple = new TNtuple("ntuple_sim_gen", "", VarListGen);
  TNtuple *recTuple = new TNtuple("ntuple_sim_rec", "", VarListRec);

  for(int i = 0; i < simulTuple->GetEntries(); i++) { 
    simulTuple->GetEntry(i);
    varsRec[0] = varsGen[0];
    varsRec[1] = varsGen[1];
    genTuple->Fill(varsGen);
    recTuple->Fill(varsRec); 
  }
  
  outputFile->cd();
  genTuple->Write();
  recTuple->Write();
  gROOT->cd();
 
  delete genTuple;
  delete recTuple;
  outputFile->Close();
  
  simFile->Close();

  return 0;

}
