// g++ -Wall -fPIC -I../include `root-config --cflags` CountEmptyBinsCut.cpp -o
// ../bin/CountEmptyBinsCut  `root-config --glibs` ../include/Binning.h

#include "Binning.h"
#include "TFile.h"
#include "TH1F.h"
#include "TNtuple.h"
#include "TROOT.h"
#include "TStopwatch.h"
#include "TString.h"
#include <iostream>
#include <string>

int CountEmptyBinsSim(std::string target, TFile *noCutFile, TFile *cutFile, TFile *outputFile);
int SetEmptyHistogram(TH1F *hist);

int main() {

    TString cutDirectory = "/home/matias/proyecto/TwoPionAnalysis/Data/60Systematic/NAccept2/";
    TFile *cutFile = new TFile(cutDirectory + "corr_data_Phi.root", "READ");
    TFile *noCutFile = new TFile(inputDirectory + "corr_data_Phi.root", "READ");
    TFile *outputFile = new TFile(outputDirectory + "EmptyBinsCut.root", "RECREATE");
    gROOT->cd();

    CountEmptyBinsSim("C", noCutFile, cutFile, outputFile);
    CountEmptyBinsSim("Fe", noCutFile, cutFile, outputFile);
    CountEmptyBinsSim("Pb", noCutFile, cutFile, outputFile);
    CountEmptyBinsSim("DC", noCutFile, cutFile, outputFile);
    CountEmptyBinsSim("DFe", noCutFile, cutFile, outputFile);
    CountEmptyBinsSim("DPb", noCutFile, cutFile, outputFile);

    noCutFile->Close();
    cutFile->Close();
    outputFile->Close();
}

int CountEmptyBinsSim(std::string target, TFile *noCutFile, TFile *cutFile,
                      TFile *outputFile) {

    TStopwatch t;

    std::cout << "Start" << std::endl;
    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());

    for (int nPion = 1; nPion <= N_PION; nPion++) { // Loops in every number of generated pions

        TNtuple *saveTuple = new TNtuple(Form("EmptyBins_%s_%i", targetArr, nPion), "",
                                         "Q2Bin:NuBin:ZhBin:Pt2Bin:PhiBin:Cut");
        for (int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) {
            for (int NuCounter = 0; NuCounter < N_Nu; NuCounter++) {
                for (int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) {
                    for (int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) {
                        TH1F *noCutHist = (TH1F *)noCutFile->Get(
                            Form("DataCorr2_%s_%i%i%i%i_%i", targetArr, Q2Counter, NuCounter,
                                 ZhCounter, Pt2Counter, nPion));
                        TH1F *cutHist = (TH1F *)cutFile->Get(
                            Form("DataCorr2_%s_%i%i%i%i_%i", targetArr, Q2Counter, NuCounter,
                                 ZhCounter, Pt2Counter, nPion));
                        if (noCutHist == NULL) {
                            delete noCutHist;
                            delete cutHist;
                            continue;
                        }
                        if (cutHist == NULL) {
                            cutHist = new TH1F("CutHist", "", N_Phi, -180, 180);
                            SetEmptyHistogram(cutHist);
                        }
                        for (int PhiCounter = 0; PhiCounter < N_Phi; PhiCounter++) {
                            if (noCutHist->GetBinContent(PhiCounter + 1) != 0 &&
                                cutHist->GetBinContent(PhiCounter + 1) == 0) {
                                saveTuple->Fill(Q2Counter, NuCounter, ZhCounter, Pt2Counter,
                                                PhiCounter, 0);
                            } else if (noCutHist->GetBinContent(PhiCounter + 1) != 0 &&
                                       cutHist->GetBinContent(PhiCounter + 1) != 0) {
                                saveTuple->Fill(Q2Counter, NuCounter, ZhCounter, Pt2Counter,
                                                PhiCounter, 1);
                            }
                        } // End Phi loop
                        delete noCutHist;
                        delete cutHist;
                    } // End Pt2 loop
                }     // End Zh loop
            }         // End Nu loop
        }             // End Q2 loop

        outputFile->cd();
        saveTuple->Write();
        gROOT->cd();
        delete saveTuple;
    } // End number of pion loop
    return 0;
}

int SetEmptyHistogram(TH1F *hist) {

    for (int i = 1; i <= N_Phi; i++) {
        hist->SetBinContent(i, 0);
    }

    return 0;
}
