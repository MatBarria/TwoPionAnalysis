// It can be compile with
// g++ -Wall -fPIC -I./include `root-config --cflags` Pt2Broad2D.cpp -o ./bin/Pt2Broad2D `root-config --glibs` ./include/Binning.h

#include "Binning.h"
#include "TFile.h"
#include "TROOT.h"
#include <iostream>
#include "TStopwatch.h"
#include "TString.h"
#include "TNtuple.h"
#include "TH1F.h"
#include "TMath.h"

int MeanPt2(std::string target, TFile* fileOutput);

int main() {

  TFile* fileOutput = new TFile(outputDirectory +  "/Broad2D/PtBroad2D.root","RECREATE");
  gROOT->cd();

  std::cout << "Mean Pt2 for C" << std::endl;
  MeanPt2("C",   fileOutput);
  std::cout << "Mean Pt2 for Fe" << std::endl;
  MeanPt2("Fe",  fileOutput);
  std::cout << "Mean Pt2 for Pb" << std::endl;
  MeanPt2("Pb",  fileOutput);
 
  fileOutput->Close();
  return 0;
}



int MeanPt2(std::string target, TFile* fileOutput) {

  TStopwatch t;

  std::cout << "Startoo" << std::endl;
  int n = target.length();
  char targetArr[n + 1];
  strcpy(targetArr, target.c_str());	

  TFile* fileData  = new TFile(Form(dataDirectory + "VecSum_%s_Acc.root", targetArr), "READ");
  gROOT->cd();
  // Create some variables to use inside the for loops
  TNtuple* ntupleData = (TNtuple*) fileData->Get("ntuple_2_pion");
  TNtuple* ntuplesave = new TNtuple(Form("Pt2Broad_2_%s", targetArr), "", "Zh:Zh_1:Broad:Error");
  float vars[4];
  TH1F *histPt2Sol[N_Zh][N_Zh], *histPt2Liq[N_Zh][N_Zh];

  for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin
    for(int ZhCounter2 = 0; ZhCounter2 < N_Zh; ZhCounter2++) { // Loops in every Zh bin
      
      histPt2Sol[ZhCounter][ZhCounter2] = new TH1F(Form("HistSol_%i%i", ZhCounter, ZhCounter2), "",
						   N_Pt2, Pt2_BINS);
      histPt2Liq[ZhCounter][ZhCounter2] = new TH1F(Form("HistLiq_%i%i", ZhCounter, ZhCounter2), "",
						   N_Pt2, Pt2_BINS);

    }
  }

  float Zh1Evnt, Zh2Evnt, ZhEvnt, Q2Evnt, NuEvnt, YCEvnt, Pt2Evnt, Acc, FalPos, Vc, weight;
  int Zh1Bin, ZhBin;

  ntupleData->SetBranchAddress("Q2",     &Q2Evnt);
  ntupleData->SetBranchAddress("Nu",     &NuEvnt);
  ntupleData->SetBranchAddress("Zh_1",   &Zh1Evnt);
  ntupleData->SetBranchAddress("Zh_2",   &Zh2Evnt);
  ntupleData->SetBranchAddress("Zh",     &ZhEvnt);
  ntupleData->SetBranchAddress("Pt2",    &Pt2Evnt);
  ntupleData->SetBranchAddress("Acc",    &Acc);
  ntupleData->SetBranchAddress("FalPos", &FalPos);
  ntupleData->SetBranchAddress("VC_TM",  &Vc);
  ntupleData->SetBranchAddress("YC",     &YCEvnt);

  for(int i = 0; i < ntupleData->GetEntries() ; i++) { // Loops in every detected paricle

    ntupleData->GetEntry(i);

    if(ZhEvnt > 1 || Zh2Evnt < 0 || Q2Evnt < Q2_BINS[0] || Q2Evnt > Q2_BINS[N_Q2] ||
	NuEvnt < Nu_BINS[0] || NuEvnt > Nu_BINS[N_Nu] || TMath::Abs(YCEvnt) > 1.4) { continue; }

    for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin
      
      if(Zh1Evnt > Zh_BINS[ZhCounter] && Zh1Evnt < Zh_BINS[ZhCounter+ 1]) {
	Zh1Bin = ZhCounter;
	break;
      }

    } // End zh loop
    
    for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Q2 bin
      
      if(ZhEvnt > Zh_BINS[ZhCounter] && ZhEvnt < Zh_BINS[ZhCounter+ 1]) {
	ZhBin = ZhCounter;
	break;
      }

    } // End  loop

    if ( Acc != 0 ) { 
      weight = FalPos/Acc;
    } else {
      weight = 0;
    }
    
    if(Vc == 2) { histPt2Sol[ZhBin][Zh1Bin]->Fill(Pt2Evnt, weight);}
    if(Vc == 1) { histPt2Liq[ZhBin][Zh1Bin]->Fill(Pt2Evnt, weight);}
   

  } // End paricle loop

  for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin
    for(int ZhCounter2 = 0; ZhCounter2 < N_Zh; ZhCounter2++) { // Loops in every Zh bin



      vars[0] = (Zh_BINS[ZhCounter] + Zh_BINS[ZhCounter+1])/2;
      vars[1] = (Zh_BINS[ZhCounter2] + Zh_BINS[ZhCounter2+1])/2;
      
      if(Zh_BINS[ZhCounter+1] <= Zh_BINS[ZhCounter2]) {
	vars[2] = 0; 
	vars[3] = 0; 
      } else {
	vars[2] = histPt2Sol[ZhCounter][ZhCounter2]->GetMean() - 
		  histPt2Liq[ZhCounter][ZhCounter2]->GetMean();
	vars[3] = TMath::Sqrt(TMath::Power(histPt2Sol[ZhCounter][ZhCounter2]->GetMeanError(), 2) + 
	                      TMath::Power(histPt2Liq[ZhCounter][ZhCounter2]->GetMeanError(), 2));
      }
      ntuplesave->Fill(vars);
      
    } // End Zh1 loop
  } // End Zh2 loop

  fileOutput->cd();
  ntuplesave->Write(Form("Pt2Broad_2_%s", targetArr));
  gROOT->cd();

  for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin
    for(int ZhCounter2 = 0; ZhCounter2 < N_Zh; ZhCounter2++) { // Loops in every Zh bin
      
      delete histPt2Sol[ZhCounter][ZhCounter2];
      delete histPt2Liq[ZhCounter][ZhCounter2];
      gDirectory->rmdir(Form("HistSol_%i%i", ZhCounter, ZhCounter2));
      gDirectory->rmdir(Form("HistLiq_%i%i", ZhCounter, ZhCounter2));

    }
  }

  delete ntuplesave;
  delete ntupleData;
  
  return 0;

}
