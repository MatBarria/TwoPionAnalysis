// g++ -Wall -fPIC -I./include `root-config --cflags` Interpolate_Rc.cpp -o ./bin/Interpolate_Rc `root-config --glibs` ./include/Binning_Rc.h

#include <iostream>
#include "Binning_Rc.h"
#include "TFile.h"
#include "TString.h"
#include "TMath.h"
#include "TROOT.h"
#include "TH1F.h"


int InterpolationRc(std::string target, TFile* fileRc, TFile* fileRcInter);
int SetEmptyHistogram(TH1F* hist);

int main() {

    TFile *fileRc      = new TFile(inputDirectory  + "RcFactors.root",      "READ");
    TFile *fileRcInter = new TFile(outputDirectory + "RcFactorsInter.root", "RECREATE");
    gROOT->cd();

    const char* Targets[2*N_STARGETS] = {"C","Fe","Pb","DC","DFe","DPb"};

    for (int i = 0; i < 2*N_STARGETS; i++) {
        std::cout << "Interpolating " << Targets[i] << "\n";
        InterpolationRc(Targets[i],   fileRc, fileRcInter);
    }
        
    fileRc->Close();
    fileRcInter->Close();
    return 0;

}

int InterpolationRc(std::string target, TFile* fileRc, TFile* fileRcInter) {

    std::cout << "Start" << std::endl;
    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());	
    int interCounter = 0;
    float Rc, RcNei, RcNext, RcPrev, RcDiff;

    float RcMin = 0.7;
    float RcMax = 1.4;
    int MaxPt  = 30;
    float MaxDiff = 0.15;

    TH1F* histSafe  = new TH1F("RcFactors", "", N_Phi, -180, 180);
    for(int nPion = 1; nPion <= N_PION; nPion++) { // Loops number of pions
        for(int Q2Counter = 0 ; Q2Counter < N_Q2; Q2Counter++) { // Loops Q2 bins
            for(int NuCounter = 0 ; NuCounter < N_Nu; NuCounter++) { // Loops Nu bins
                for(int ZhCounter = 0 ; ZhCounter < N_Zh; ZhCounter++) { // Loops Zh bins;

                     //---------------------- Low Pt2 Interpolation  ------------------ 
                    for(int Pt2Counter = 1 ; Pt2Counter < MaxPt; Pt2Counter++) { // Pt2 bins;

                        // Read the actual bin an the two neiberhoods

                        TH1F *hist     = (TH1F*) fileRc->Get(Form("RcFactor_%s_%i%i%i%i_%i",
                                targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion));
                        TH1F *histPrev = (TH1F*) fileRc->Get(Form("RcFactor_%s_%i%i%i%i_%i", 
                            targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter -1 , nPion));
                        TH1F *histNext = (TH1F*) fileRc->Get(Form("RcFactor_%s_%i%i%i%i_%i", 
                            targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter + 1 , nPion));


                        // If some hist is empty set tjhe factor as 0 
                        if(histPrev == NULL ) { 
                            histPrev  = new TH1F("EmptyPrev", "", N_Phi, -180, 180);
                            SetEmptyHistogram(histPrev);
                        }
        
                        if(histNext == NULL ) { 
                            histNext  = new TH1F("EmptyNext", "", N_Phi, -180, 180);
                            SetEmptyHistogram(histNext);
                        }

                        for(int PhiCounter = 1 ; PhiCounter <= N_Phi; PhiCounter++) {

                            RcPrev = histPrev->GetBinContent(PhiCounter);
                            RcNext = histNext->GetBinContent(PhiCounter);

                            if(RcPrev > RcMin && RcNext > RcMin) { RcNei = (RcPrev + RcNext)/2; }
                            else if(RcPrev < RcMin && RcNext > RcMin) { RcNei = RcNext; }
                            else if(RcPrev > RcMin && RcNext < RcMin) { RcNei = RcPrev; }
                            //else { RcNei = 1; }

                            if(hist == NULL) {
                                histSafe->SetBinContent(PhiCounter, RcNei); 
                                continue;
                            }

                            Rc = hist->GetBinContent(PhiCounter);
                            RcDiff = TMath::Abs((RcNei-Rc)/RcNei);
                            if(RcDiff > MaxDiff || Rc < RcMin || Rc > RcMax) { 
                                histSafe->SetBinContent(PhiCounter, RcNei); 
                            } else { 
                                histSafe->SetBinContent(PhiCounter, Rc); 
                                RcNei = Rc;
                            }
                        }
                        
                        fileRcInter->cd();
                        histSafe->Write(Form("RcFactor_%s_%i%i%i%i_%i", targetArr, Q2Counter,
                                    NuCounter, ZhCounter, Pt2Counter, nPion));
                        gROOT->cd();

                        histSafe->Reset();
                        delete hist;
                        delete histPrev;
                        delete histNext;


                    } // End Pt2 Loop

                    for(int Pt2Counter = MaxPt ; Pt2Counter < N_Pt2; Pt2Counter++) { // Loops in every Pt2 bin;

                        TH1F *hist = (TH1F*) fileRc->Get(Form("RcFactor_%s_%i%i%i%i_%i", 
                            targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter, nPion));
                        if(hist == NULL) { continue; } 
                        fileRcInter->cd();
                        hist->Write(Form("RcFactor_%s_%i%i%i%i_%i", targetArr, Q2Counter, 
                                    NuCounter, ZhCounter, Pt2Counter, nPion));
                        gROOT->cd();
                        delete hist;

                    } // End Pt2 Loop

                } // End ZhCounter Loop
            }	// End Nu Loop
        } // End Q2Counter Loop
    } // End Number of pions Loop

    std::cout << interCounter << " factors has been intepolated" << std::endl;
    delete histSafe;
    return 0;

}

int SetEmptyHistogram(TH1F* hist) {

    for (int i = 1; i <= N_Phi; i++) {
        hist->SetBinContent(i, 0) ;
    }

    return 0;
}
