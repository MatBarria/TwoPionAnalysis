// g++ -Wall -fPIC -I../include `root-config --cflags` CountEmptyBins.cpp -o ../bin/CountEmptyBins  `root-config --glibs` ../include/Binning.h


#include <iostream>
#include <string>
#include "Binning.h"
#include "TFile.h"
#include "TNtuple.h"
#include "TString.h"
#include "TStopwatch.h"
#include "TROOT.h"
#include "TH1F.h"



int CountEmptyBinsSim(std::string target, TFile* inputFile, TFile* outputFile);
int SetEmptyHistogram(TH1F* hist);

int main() {

    TFile* inputFile   = new TFile(inputDirectory  + "corr_data_Phi.root", "READ");
    TFile* outputFile  = new TFile(outputDirectory + "EmptyBins.root", "RECREATE");
    gROOT->cd();

    std::cout << "Start" << std::endl;

    CountEmptyBinsSim("C",   inputFile, outputFile);
    CountEmptyBinsSim("Fe",  inputFile, outputFile);
    CountEmptyBinsSim("Pb",  inputFile, outputFile);
    CountEmptyBinsSim("DC",  inputFile, outputFile);
    CountEmptyBinsSim("DFe", inputFile, outputFile);
    CountEmptyBinsSim("DPb", inputFile, outputFile);

    inputFile->Close();
    outputFile->Close();


}

int CountEmptyBinsSim(std::string target, TFile* inputFile, TFile* outputFile) {

    TStopwatch t;

    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());

    
    for(int nPion = 1; nPion <= N_PION ; nPion++) { // Loops in every number of generated pions

        TNtuple* saveTuple = new TNtuple(Form("EmptyBins_%s_%i", targetArr, nPion), "", 
                                        "Q2Bin:NuBin:ZhBin:Pt2Bin:PhiBin:Data:Evnts");
        for(int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++ ) {
            for(int NuCounter = 0; NuCounter < N_Nu; NuCounter++ ) {
                for(int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++ ) {
                    for(int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++ ) {
                        TH1F* dataHist = (TH1F*) inputFile->Get(Form("Data_%s_%i%i%i%i_%i", 
                                    targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter,
                                    nPion));
                        TH1F* facHist = (TH1F*) inputFile->Get(Form("FinalFactor_%s_%i%i%i%i_%i",
                                    targetArr, Q2Counter, NuCounter, ZhCounter, Pt2Counter,
                                    nPion));
                        if(dataHist == NULL) {
                            delete dataHist;
                            delete facHist;
                            continue;
                        }
                        if(facHist == NULL) {
                            facHist = new TH1F("FactorHist", "", N_Phi, -180, 180);
                            SetEmptyHistogram(facHist);
                        }
                        for(int PhiCounter = 0; PhiCounter < N_Phi; PhiCounter++) {
                            if(dataHist->GetBinContent(PhiCounter + 1) != 0 
                                    && facHist->GetBinContent(PhiCounter + 1) == 0) {
                                saveTuple->Fill(Q2Counter, NuCounter, ZhCounter, Pt2Counter, 
                                        PhiCounter, 0, 
                                        dataHist->GetBinContent(PhiCounter+1));
                            } else if(dataHist->GetBinContent(PhiCounter + 1) != 0 
                                    && facHist->GetBinContent(PhiCounter + 1) != 0){
                                saveTuple->Fill(Q2Counter, NuCounter, ZhCounter, Pt2Counter, 
                                        PhiCounter, 1, 
                                        dataHist->GetBinContent(PhiCounter+1));
                            }
                        } // End Phi loop
                    delete dataHist;
                    delete facHist;
                    } // End Pt2 loop
                } // End Zh loop
            } // End Nu loop
        } // End Q2 loop
        
        outputFile->cd();
        saveTuple->Write();
        gROOT->cd();
        delete saveTuple;
    } // End number of pion loop
    return 0;
}


int SetEmptyHistogram(TH1F* hist) {

    for (int i = 1; i <= N_Phi; i++) {
        hist->SetBinContent(i, 0) ;
    }
    //std::cout << "Empty" << std::endl;

    return 0;
}
