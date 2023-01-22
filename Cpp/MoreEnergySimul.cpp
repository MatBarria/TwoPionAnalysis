// This code generate a tuple with the all the events in the simultion
// The tuple has the number of generate pion , dectected pion, the values of Q2, Nu and
// for the hadrons variables calculate vectorial momentum and use it as the hadron momentum for the event
// The code run over the simulation generated with the code GetSimpleTuple
// https://github.com/utfsm-eg2-data-analysis/GetSimpleTuple
// It can be compile with
// g++ -Wall -fPIC  `root-config --cflags` MoreEnergySimul.cpp -o ./bin/MoreEnergySimul  `root-config --glibs`
// For the target name use (D,C,Fe,Pb)

#include <iostream>
#include <string>
#include "TMath.h"
#include "TString.h"
#include "TFile.h"
#include "TNtuple.h"
#include "TVector2.h"
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

  std::cout << "Start" << std::endl;

  TString inputName;

  // Set the variables that we want to save
  const char* VarList = "Gen:Dec:Q2:Nu:Zh:Pt2:PhiPQ";
  TNtuple* sumTuple = new TNtuple("ntuple_sim", "", VarList);
  float ZhMax; 
  int MaxIndex; 

  for(int folder = 1; folder < 10; folder++) { // Loops in every directory
    for(int sim = 154; sim < 157; sim++) { // Loops in every simulation of the directory
      // Set the name of the file where is the data depends on the target and the folder
      if(targetArr[0] == 'D' ){
        if(folder < 4) {
          inputName = Form("/work/mbarrial/out/GetSimpleTuple_HSim/D2_pb%i/prunedD_%i.root",
			    folder, sim);
        } else {
          inputName = Form("/work/mbarrial/out/GetSimpleTuple_HSim/D2_pb%i_yshiftm03/prunedD_%i.root"
			    , folder, sim);
        }
      } else {
        if(folder < 4) {
          inputName = Form("/work/mbarrial/out/GetSimpleTuple_HSim/%s%i/pruned%s_%i.root", targetArr,
			    folder,targetArr,sim);
        } else {
          inputName = Form("/work/mbarrial/out/GetSimpleTuple_HSim/%s%i_yshiftm03/pruned%s_%i.root",
			    targetArr,folder,targetArr,sim);
        }
      }
      //std::cout << "Checking directory " << folder << "  " << sim << std::endl;
      //inputName = Form("/home/matias/proyecto/Piones/Data/Simul/pruned%s_%i.root",targetArr ,sim);
      // Open the file and check if it's exist
      TFile* fSource = new TFile(inputName,"READ");
      if (fSource->IsZombie()) {
        fSource->Close();
        continue;
      }
      // Open the tuple and check if it's exist
      TNtuple* simulTuple = (TNtuple*)fSource->Get("ntuple_sim");
      if(simulTuple == NULL) {
        delete simulTuple;
        fSource->Close();
        continue;
      }

      gROOT->cd();

      float *vars = new Float_t[7];
      float mcPid, pid, evnt, Q2Evnt, NuEvnt, deltaZEvnt;

      // Read the necesary variables
      simulTuple->SetBranchAddress("evnt",&evnt);
      simulTuple->SetBranchAddress("mc_pid",&mcPid);
      simulTuple->SetBranchAddress("pid",&pid);
      simulTuple->SetBranchAddress("mc_Q2",&Q2Evnt);
      simulTuple->SetBranchAddress("mc_Nu",&NuEvnt);
      simulTuple->SetBranchAddress("mc_Zh",&vars[4]);
      simulTuple->SetBranchAddress("mc_Pt2",&vars[5]);
      simulTuple->SetBranchAddress("mc_PhiPQ",&vars[6]);
      simulTuple->SetBranchAddress("deltaZ",&deltaZEvnt);

      // Create the variables to use inside of the for loops
      vars[0] = 0; // Count how many pions were generated in the event
      vars[1] = 0; // Count how many pions were detected in the event
      int tmpCounter = 0;
      float tmpEvnt;
      float tmpZh[5], tmpPt[5], tmpPhi[5] ;
      int isPion;
      for(int i = 0; i < simulTuple->GetEntries(); i++) { // Loops in every generated particle
	isPion = 0;
        simulTuple->GetEntry(i);
        vars[2] = Q2Evnt;
        vars[3] = NuEvnt;
        // Check the bin of Q2 for the event
        // Check if the generated paricle is a pion+
	if(mcPid == 211 || (pid == 211 && TMath::Abs(deltaZEvnt) < 3.)) {
	  isPion++; 
	  if(mcPid == 211 ){
	    // Save the angle PhiPQ,Zh and Pt if it's a pion
	    tmpZh[0]  = vars[4];
	    tmpPt[0]  = vars[5];
	    tmpPhi[0] = vars[6];
	    vars[0]++;
	  }
	  // Check if the detected paricle is a pion+
	  if(pid == 211 ) { vars[1]++; }
	}
        tmpEvnt = evnt;
        simulTuple->GetEntry(i + 1);
        // Check if the next particle cames from the same event
        while(tmpEvnt == evnt) { // Check all the paricles in the event
	  if(mcPid == 211 || (pid == 211 && TMath::Abs(deltaZEvnt) < 3.)) {
	    isPion++;
	    if(mcPid == 211) { // If the generated paricle is a pi+
	      // Save the angle PhiPQ, Zh and Pt of every pion in the event
	      tmpZh[(int)vars[0]]  = vars[4];
	      tmpPt[(int)vars[0]]  = vars[5];
	      tmpPhi[(int)vars[0]] = vars[6];
	      vars[0]++;
	    }
	    if(pid == 211) { vars[1]++; }
	  }
          tmpCounter++;
          tmpEvnt = evnt;
          // Go to the next particle
          if(i + 1 + tmpCounter > simulTuple->GetEntries() ){ break; }
          simulTuple->GetEntry(i + 1 + tmpCounter);
        }
        vars[4] = 0;
	ZhMax = 0;
	MaxIndex = -1;
        for(int k = 0; k < (int)vars[0]; k++) {
	  ZhMax = tmpZh[k];
	  MaxIndex = -1;
        }
	vars[2] = tmpZh[MaxIndex];
	vars[3] = tmpPt[MaxIndex];
	vars[4] = tmpPhi[MaxIndex];
        // Save the Pt2 of the sum vector
        // Add the variables to the tuple
        if(isPion != 0) {
	  sumTuple->Fill(vars);
        }
	// Reset the gen and dec counters
        vars[0] = 0;
        vars[1] = 0;
        // Jump to the next event
        i += tmpCounter;
        tmpCounter = 0;
      } // End particles loop
      delete simulTuple;
      fSource->Close();
    } // End sim loop
    std::cout << "Directory " << folder << " checked" << std::endl;
  } // End folder loop

  // Save the Ntuple
  TFile *fileOutput= new TFile(Form("/work/mbarrial/Data/MoreEnergySimul_%s.root", targetArr),
				    "RECREATE");
  //TFile *fileOutput= new TFile("hola.root", "RECREATE");
  fileOutput->cd();
  sumTuple->Write();
  gROOT->cd();
  fileOutput->Close();
  t.Print();

}
