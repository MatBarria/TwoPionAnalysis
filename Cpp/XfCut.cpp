// g++ -Wall -fPIC -I../include `root-config --cflags` XfCut.cpp -o ../bin/XfCut `root-config --glibs` ../include/Binning.h
//
// For the target name use (C,Fe,Pb)

#include "Binning.h"
#include "TFile.h"
#include "TMath.h"
#include "TNtuple.h"
#include "TROOT.h"
#include "TStopwatch.h"
#include "TString.h"
#include "TVector2.h"
#include <iostream>
#include <string>

int main(int argc, char *argv[]) {

    if (argc != 2) {
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

    TFile *file = new TFile(Form(dataDirectory + "PiPlusData_%s.root", targetArr), "READ");
    TNtuple *tuple = (TNtuple *)file->Get("ntuple_data");

    int tmpCounter = 0;  // Counts how many particles there is in the event
    int pionCounter = 0; // Counts how many pions there is in the event (check Delta Z Cut)
    float tmpEvnt, evnt, Q2Evnt, NuEvnt, XfEvnt, ZhEvnt, Pt2Evnt, PhiEvnt, YCEvnt, VCEvnt,
        DZEvnt;
    float tmpZh[5], tmpPt[5], tmpPhi[5], tmpXf[5];
    float deltaZcut = 3.;
    int dummyval = -999;
    const char *VarList = "Q2:Nu:Zh:Pt2:PhiPQ:YC:VC_TM:Zh_1:Zh_2:Zh_3:Xf1:Xf2:Xf3";
    // Variables to fill the tuple
    float *vars = new Float_t[13];
    // Read the necesary variables
    tuple->SetBranchAddress("Q2", &Q2Evnt);
    tuple->SetBranchAddress("Nu", &NuEvnt);
    tuple->SetBranchAddress("Xf", &XfEvnt);
    tuple->SetBranchAddress("Zh", &ZhEvnt);
    tuple->SetBranchAddress("Pt2", &Pt2Evnt);
    tuple->SetBranchAddress("PhiPQ", &PhiEvnt);
    tuple->SetBranchAddress("YC", &YCEvnt);
    tuple->SetBranchAddress("VC_TM", &VCEvnt);
    tuple->SetBranchAddress("deltaZ", &DZEvnt);
    tuple->SetBranchAddress("NEvnt", &evnt);

    gROOT->cd();

    TNtuple *ntuplePion[5];

    for (int i = 0; i < 5; i++) {
        ntuplePion[i] = new TNtuple(Form("ntuple_%i_pion", i + 1), "", VarList);
    }

    for (int i = 0; i < tuple->GetEntries(); i++) { // Loops in every detected paricle
        tuple->GetEntry(i);
        pionCounter = 0;
        tmpCounter = 0;
        vars[0] = Q2Evnt;
        vars[1] = NuEvnt;
        if (TMath::Abs(DZEvnt) < deltaZcut) {
            vars[2] = ZhEvnt;
            vars[3] = Pt2Evnt;
            vars[4] = PhiEvnt;
            vars[5] = YCEvnt;
            vars[6] = VCEvnt;
            tmpZh[pionCounter] = vars[2];
            tmpPt[pionCounter] = TMath::Sqrt(Pt2Evnt);
            tmpPhi[pionCounter] = vars[4];
            tmpXf[pionCounter] = XfEvnt;
            pionCounter++;
        }
        tmpEvnt = evnt;
        tuple->GetEntry(i + 1);
        while (tmpEvnt == evnt) { // Check all the paricles in the event
            tmpCounter++;
            if (TMath::Abs(DZEvnt) < deltaZcut) {
                tmpZh[pionCounter] = ZhEvnt;
                tmpPt[pionCounter] = TMath::Sqrt(Pt2Evnt);
                tmpPhi[pionCounter] = PhiEvnt;
                tmpXf[pionCounter] = XfEvnt;
                pionCounter++;
            }
            if (i + 1 + tmpCounter >= tuple->GetEntries()) {
                break;
            }
            tuple->GetEntry(i + 1 + tmpCounter);
        }
        // Jump to the next event
        i += tmpCounter;

        vars[2] = 0;
        TVector2 *vec = new TVector2(0, 0);
        for (int k = 0; k < pionCounter; k++) {
            // Calculate de tranvers momentum vector
            TVector2 *tmpVec =
                new TVector2(tmpPt[k] * TMath::Cos((tmpPhi[k] + 180) * TMath::DegToRad()),
                             tmpPt[k] * TMath::Sin((tmpPhi[k] + 180) * TMath::DegToRad()));
            // Sum the vector and save the sum of Zh
            vars[2] += tmpZh[k];
            *vec += *tmpVec;
            // vecTemp->Print();
            delete tmpVec;
        }
        delete vec;
        // Save the Pt2 of the sum vector
        vars[3] = std::pow(vec->Mod(), 2);
        // Save the PhiPQ of the sum vector
        vars[4] = vec->Phi() * TMath::RadToDeg() - 180;
        if (pionCounter == 0) {
            continue;
        }
        if (pionCounter == 1) {
            vars[7] = tmpZh[0];
            vars[8] = dummyval;
            vars[9] = dummyval;
            vars[10] = tmpXf[0];
            vars[11] = dummyval;
            vars[12] = dummyval;
        }
        // rs[8] = tmpZh[1];
        // vars[9] = dummyval;
        // }
        if (pionCounter == 2) {
            vars[9] = dummyval;
            vars[12] = dummyval;
            if (tmpZh[0] > tmpZh[1]) {
                vars[7] = tmpZh[0];
                vars[8] = tmpZh[1];
                vars[10] = tmpXf[0];
                vars[11] = tmpXf[1];
            }
            if (tmpZh[0] < tmpZh[1]) {
                vars[7] = tmpZh[1];
                vars[8] = tmpZh[0];
                vars[10] = tmpXf[1];
                vars[11] = tmpXf[0];
            }
        }
        ntuplePion[pionCounter - 1]->Fill(vars);
    } // End paricle loop

    // Save the tuples
    TFile *fOutput = new TFile(Form(dataDirectory + "Xf_%s.root", targetArr), "RECREATE");
    fOutput->cd();

    ntuplePion[1]->Write();
    for (int i = 0; i < N_PION + 1; i++) {
        delete ntuplePion[i];
    }

    gROOT->cd();
    fOutput->Close();
    file->Close();
    std::cout << "Done." << std::endl;
    t.Print();
}
