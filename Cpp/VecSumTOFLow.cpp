// This code generate a tuple with all the events of experimental data
// Saves the electron variables and calculate for the hadrons variables
// calculate vectorial momentum and use it as the hadron momentum for the event
// The code require that you have the number of the event saved in the data tupleName
// if you don't have it you can check by for the paricle has the same Q2 and Nu instead
// It can be compiled with
// g++ -Wall -fPIC -I../include `root-config --cflags` VecSum.cpp -o ../bin/VecSum  `root-config --glibs` ../include/Binning.h
// For the target name use (C,Fe,Pb)

#include <iostream>
#include <string>
#include "Binning.h"
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
    std::cout << "Start" << std::endl;

    std::string target = argv[1];
    // Creating a array of chars instead of a string to use Form method
    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());

    TFile* file = new TFile(Form(dataDirectory + "%s_data_Npion_TOF_Pl25.root", targetArr), "READ");
    TNtuple* tuple = (TNtuple*)file->Get("ntuple_data");

    int tmpCounter = 0; // Counts how many particles there is in the event
    int pionCounter = 0; // Counts how many pions there is in the event (check Delta Z Cut)
    float tmpQ2, tmpNu, Q2Evnt, NuEvnt, XbEvnt, ZhEvnt, Pt2Evnt, PhiEvnt, YCEvnt, VCEvnt,
          DZEvnt;
    float tmpZh[5], tmpPt[5], tmpPhi[5] ;
    float deltaZcut = 3.;
    int dummyval = -999;
    const char* VarList = "Q2:Nu:Zh:Pt2:PhiPQ:YC:VC_TM:Zh_1:Zh_2:Zh_3:Xb";
    // Variables to fill the tuple
    float *vars         = new Float_t[11];
    // Read the necesary variables
    tuple->SetBranchAddress("Q2",&Q2Evnt);
    tuple->SetBranchAddress("Nu",&NuEvnt);
    tuple->SetBranchAddress("Xb",&XbEvnt);
    tuple->SetBranchAddress("Zh",&ZhEvnt);
    tuple->SetBranchAddress("Pt2",&Pt2Evnt);
    tuple->SetBranchAddress("PhiPQ",&PhiEvnt);
    tuple->SetBranchAddress("YC",&YCEvnt);
    tuple->SetBranchAddress("VC_TM",&VCEvnt);
    tuple->SetBranchAddress("deltaZ",&DZEvnt);
    tuple->SetBranchAddress("NEvnt",&evnt);

    gROOT->cd();

    TNtuple* ntuplePion[5];

    for(int i = 0; i < 5; i++) {
        ntuplePion[i] = new TNtuple(Form("ntuple_%i_pion", i + 1), "", VarList);
    }

    for(int i = 0; i < tuple->GetEntries() ; i++) { // Loops in every detected paricle
        tuple->GetEntry(i);
        pionCounter = 0;
        tmpCounter = 0;
        vars[0]  = Q2Evnt;
        vars[1]  = NuEvnt;
        vars[10] = XbEvnt;
        vars[5]  = YCEvnt;
        vars[6]  = VCEvnt;
        if(TMath::Abs(DZEvnt) < deltaZcut){
            vars[2]  = ZhEvnt;
            vars[3]  = Pt2Evnt;
            vars[4]  = PhiEvnt;
            tmpZh[pionCounter]  = vars[2];
            tmpPt[pionCounter]  = TMath::Sqrt(Pt2Evnt);
            tmpPhi[pionCounter] = vars[4];
            pionCounter++;
        }
        tmpQ2 = Q2Evnt;
        tmpNu = NuEvnt;
        tuple->GetEntry(i + 1);
        while(tmpQ2 == Q2Evnt && tmpNu = NuEvnt) { // Check all the paricles in the event
            tmpCounter++;
            if(TMath::Abs(DZEvnt) < deltaZcut) {
                tmpZh[pionCounter]  = ZhEvnt;
                tmpPt[pionCounter]  = TMath::Sqrt(Pt2Evnt);
                tmpPhi[pionCounter] = PhiEvnt;
                pionCounter++;
            }
            if(i + 1 + tmpCounter >= tuple->GetEntries() ){ break; }
            tuple->GetEntry(i + 1 + tmpCounter);
        }
        // Jump to the next event
        i += tmpCounter;

        vars[2] = 0;
        TVector2* vec = new TVector2(0,0);
        for(int k = 0; k < pionCounter; k++) {
            // Calculate de tranvers momentum vector
            TVector2 *tmpVec = new 
                TVector2(tmpPt[k]*TMath::Cos((tmpPhi[k] + 180)*TMath::DegToRad()),
                         tmpPt[k]*TMath::Sin((tmpPhi[k] + 180)*TMath::DegToRad()));
            // Sum the vector and save the sum of Zh
            vars[2] += tmpZh[k];
            *vec += *tmpVec;
            //vecTemp->Print();
            delete tmpVec;
        }
        delete vec;
        // Save the Pt2 of the sum vector
        vars[3] = std::pow(vec->Mod(),2);
        // Save the PhiPQ of the sum vector
        vars[4] = vec->Phi()*TMath::RadToDeg()-180;
        if(pionCounter == 0) { continue; }
        if(pionCounter == 1) {
            vars[7] = tmpZh[0];
            vars[8] = dummyval;
            vars[9] = dummyval;
        }
        //vars[8] = tmpZh[1];
        //vars[9] = dummyval;
        //}
        if(pionCounter == 2) {
            vars[9] = dummyval;
            if (tmpZh[0] > tmpZh[1]) {
                vars[7] = tmpZh[0];
                vars[8] = tmpZh[1];
            }
            if (tmpZh[0] < tmpZh[1]) {
                vars[7] = tmpZh[1];
                vars[8] = tmpZh[0];
            }
        }
        ntuplePion[pionCounter - 1]->Fill(vars);
    } // End paricle loop

    // Save the tuples
    TFile* fOutput = new TFile(Form(dataDirectory + "VecSum_%sTOFLow.root", targetArr), "RECREATE");
    fOutput->cd();

    for(int i = 0; i < N_PION +1 ; i++) {
        ntuplePion[i]->Write();
        delete ntuplePion[i];
    }

    gROOT->cd();
    fOutput->Close();
    file->Close();
    std::cout << "Done." << std::endl;
    t.Print();

}
