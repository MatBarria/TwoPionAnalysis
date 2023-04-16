// g++ -Wall -fPIC -I./include `root-config --cflags` Interpolate_Rc_Empty.cpp -o ./bin/Interpolate_Rc_Empty `root-config --glibs` ./include/Binning_Rc.h

#include <iostream>
#include "Binning_Rc.h"
#include "TFile.h"
#include "TString.h"
#include "TMath.h"
#include "TROOT.h"
#include "TH1F.h"


int InterpolationRc(std::string target, TFile* fileRc, TFile* fileRcInter, TFile* fileData);
int SetEmptyHistogram(TH1F* hist);

int main() {

    //TFile *fileRc      = new TFile(inputDirectory  + "RcFactors.root",      "READ");
    TFile *fileRc      = new TFile(inputDirectory  + "RcFactorsInter.root",      "READ");
    TFile *fileData    = new TFile(inputDirectory  + "corr_data_Phi_Evnt.root",  "READ");
    TFile *fileRcInter = new TFile(outputDirectory + "RcFactorsInterEmpty.root", "RECREATE");
    gROOT->cd();

    const char* Targets[2*N_STARGETS] = {"C","Fe","Pb","DC","DFe","DPb"};

    for (int i = 0; i < 2*N_STARGETS; i++) {
        std::cout << "Interpolating " << Targets[i] << "\n";
        InterpolationRc(Targets[i], fileRc, fileRcInter, fileData);
    }
        
    fileRc->Close();
    fileRcInter->Close();
    return 0;

}

int InterpolationRc(std::string target, TFile* fileRc, TFile* fileRcInter, TFile* fileData) {

    std::cout << "Start" << std::endl;
    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());	
    float RcNei, RcNext, RcPrev;

    for(int nPion = 1; nPion <= N_PION; nPion++) { // Loops number of pions
        for(int Q2Counter = 0 ; Q2Counter < N_Q2; Q2Counter++) { // Loops Q2 bins
            for(int NuCounter = 0 ; NuCounter < N_Nu; NuCounter++) { // Loops Nu bins
                for(int ZhCounter = 0 ; ZhCounter < N_Zh; ZhCounter++) { // Loops Zh bins;
                    RcNei = .9;
                     //---------------------- Low Pt2 Interpolation  ------------------ 
                    for(int Pt2Counter = 0 ; Pt2Counter < N_Pt2 - 1; Pt2Counter++) { // Pt2 bins;

                        // Read the actual bin an the two neiberhoods
                        TH1F *histData  = (TH1F*) fileData->Get(Form("DataCorr2_%s_%i%i%i%i_%i",
                                targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion));

                        if(histData == NULL) { 
                            delete histData;
                            continue; 
                        }
                        TH1F *hist     = (TH1F*) fileRc->Get(Form("RcFactor_%s_%i%i%i%i_%i",
                                targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion));

                        TH1F *histPrev = (TH1F*) fileRc->Get(Form("RcFactor_%s_%i%i%i%i_%i", 
                            targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter -1 , nPion));
                        TH1F *histNext = (TH1F*) fileRc->Get(Form("RcFactor_%s_%i%i%i%i_%i", 
                            targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter + 1 , nPion));

                        if(hist == NULL) {
                            hist  = new TH1F(Form("RcFactor_%s_%i%i%i%i_%i",
                                targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion), 
                                    "", N_Phi, -180, 180);
                            SetEmptyHistogram(hist);
                        } 

                        if(histPrev == NULL ) { 
                            histPrev  = new TH1F("EmptyPrev", "", N_Phi, -180, 180);
                            SetEmptyHistogram(histPrev);
                        }
        
                        if(histNext == NULL ) { 
                            histNext  = new TH1F("EmptyNext", "", N_Phi, -180, 180);
                            SetEmptyHistogram(histNext);
                        }

                        for(int PhiCounter = 1; PhiCounter <= N_Phi; PhiCounter++) {

                            if(hist->GetBinContent(PhiCounter) != 0) { continue; }
                             
                            RcPrev = histPrev->GetBinContent(PhiCounter);
                            RcNext = histNext->GetBinContent(PhiCounter);
                            if(RcPrev > 0.8 && RcPrev < 1.2 && RcNext > 0.8 && RcNext < 1.2) {
                                RcNei = (RcPrev + RcNext)/2;
                            }
                            else if(RcPrev > 0.8 && RcPrev < 1.2) { RcNei = RcPrev; }
                            else if(RcNext > 0.8 && RcNext < 1.2) { RcNei = RcNext; }
                            if(RcNei >= 1){
                                std::cout <<"es mayor que 1 igual a: " << RcNei << std::endl;
                            }
                            hist->SetBinContent(PhiCounter, RcNei);
                        }
                        
                        fileRcInter->cd();
                        hist->Write(Form("RcFactor_%s_%i%i%i%i_%i",
                                targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion));
                        gROOT->cd();

                        delete hist;
                        delete histData;
                        delete histPrev;
                        delete histNext;


                    } // End Pt2 Loop
                } // End ZhCounter Loop
            }	// End Nu Loop
        } // End Q2Counter Loop
    } // End Number of pions Loop

    return 0;

}

int SetEmptyHistogram(TH1F* hist) {

    for (int i = 1; i <= N_Phi; i++) {
        hist->SetBinContent(i, 0) ;
    }

    return 0;
}
