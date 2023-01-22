// It can be compile with
// g++ -Wall -fPIC -I./include `root-config --cflags` CountEmptybins.cpp -o ./bin/CountEmptybins  `root-config --glibs` ./include/Integration.h
// For the target name use (C,Fe,Pb) for the solids targets and (DC,DFe,DPb) for the liquid target

#include <iostream>
#include "Integration.h"
#include "TNtuple.h"
#include "TCut.h"
#include "TEventList.h"

int main(int argc, char* argv[]) {

  if(argc != 2) {
    std::cout << "Insert (just) the target name as a parameter" << std::endl;
    return 0;
  }

  TStopwatch t;

  std::cout << "Start" << std::endl;

  std::string target = argv[1];
  // Creating a array of chars instead of a string to use Form method
  int n = target.length();
  char targetArr[n + 1];
  strcpy(targetArr, target.c_str());

  int m;
  TString fileDataName;
  // Select the data for the chosen solid target
  if(targetArr[0] == 'D') { m = n; } 
  else { m = n + 1 } 

  // Select the target of the simultion
  char simulTarget[m];
  if(targetArr[0] == 'D') {
    simulTarget[0] = 'D';
    simulTarget[1] = '\0';
    for(int i = 1; i < n + 1; i++){
      solidTarget[i] = targetArr[i];
    }
  } else{
    for(int i = 0; i < m; i++){
      simulTarget[i] = targetArr[i];
      solidTarget[i] = targetArr[i];
    }
  }
  // Open the input and output files
  TFile* fileData   = new TFile(dataDirectory + Form("VecSum_%s.root", solidTarget), "READ");
  TFile* fileSimul  = new TFile(dataDirectory + Form("SimulTuple_%s.root", simulTarget), "READ");
  gROOT->cd();

  // Create some variables to use inside the for loops
  TString tupleDataName;
  TCut Q2Cut, NuCut, ZhCut, Pt2Cut, PhiCut, VCData, cutsData, cutsSimul, RecCut;
  TCut YCCut = "TMath::Abs(YC)<1.4";
  // Select liquid or solid target
  if(targetArr[0] == 'D') { VCData  = "VC_TM == 1.";}
  else {VCData  = "VC_TM == 2.";}
  
  std::cout << Form("Simul target %s, Target %s", simulTarget, targetArr) << std::endl;

  std::cout << "Q2 Bins = "  << N_Q2  << std::endl;
  std::cout << std::endl;
  std::cout << "Nu Bins = "  << N_Nu  << std::endl;
  std::cout << std::endl;
  std::cout << "Zh Bins = "  << N_Zh  << std::endl;
  std::cout << std::endl;
  std::cout << "Pt2 Bins = " << N_Pt2 << std::endl;
  std::cout << std::endl;
  std::cout << "Phi Bins = " << N_Phi << std::endl;
  std::cout << std::endl;
  std::cout << "Total number of 5Dim bins: " << N_Q2*N_Nu*N_Zh*N_Pt2*N_Phi << std::endl;
  std::cout << std::endl;

  for(int gen = 1; gen <= N_PION ; gen++) { // Loops in every number of generated
    
    DecCut    = Form("Dec == %f", (float)gen);

    for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) { // Loops in every Q2 bin
      for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
        for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin

          // Select the cuts for each bin
          Q2Cut   = Form("Q2>%f&&Q2<%f", Q2_BINS[Q2Counter], Q2_BINS[Q2Counter+1]);
          NuCut   = Form("Nu>%f&&Nu<%f", Nu_BINS[NuCounter], Nu_BINS[NuCounter+1]);
          ZhCut   = Form("Zh>%f&&Zh<%f", Zh_BINS[ZhCounter], Zh_BINS[ZhCounter+1]);
          Q2Cut   = Form("Q2_rec>%f&&Q2_rec<%f", Q2_BINS[Q2Counter], Q2_BINS[Q2Counter+1]);
          NuCut   = Form("Nu_rec>%f&&Nu_rec<%f", Nu_BINS[NuCounter], Nu_BINS[NuCounter+1]);
          ZhCut   = Form("Zh_rec>%f&&Zh_rec<%f", Zh_BINS[ZhCounter], Zh_BINS[ZhCounter+1]);

          cutsData  = Q2Cut&&NuCut&&ZhCut&&YCCut&&VCData;
          cutsSimul = Q2Cut&&NuCut&&ZhCut&&GenCut&&DecCut;


            } // End Pt2 loop
          }// End Phi loop
          delete ntupleData;
          delete ntupleSimul;
          delete evntData;
          delete evntSimul;
        } // End Zh loop
      } // End Nu loop
    } // End Q2 loop

  } // End pion number loop 
  
  fileData->Close();
  fileSimul->Close();
  t.Print();


}
