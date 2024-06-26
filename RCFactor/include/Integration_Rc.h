#include "Binning_Rc.h"
#include "TFile.h"
#include "TH1.h"
#include "TMath.h"
#include "TROOT.h"
#include "TStopwatch.h"
#include "TString.h"
#include <iostream>

// If the histogram if empty return 1 if not return 0
int EmptyHist(TH1F *h) {

    int empty = 0;
    for (int i = 1; i <= h->GetNbinsX(); i++) {
        if (h->GetBinContent(i) == 0) {
            empty++;
        }
    }
    if (empty == h->GetNbinsX()) {
        return 1;
    } else {
        return 0;
    }
}

// Integrate the PhiPQ histograms and generate a Pt2 histogram for each Q2, Nu, Zh bin
void PhiIntegration(TFile *inputFile, TFile *outputFile, char target[]) {

    std::cout << Form("Target %s", target) << std::endl;
    for (int nPion = 1; nPion <= N_PION; nPion++) { // Loops in every number of pion
        for (int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) {     // Loops in every Q2 bin
            for (int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
                for (int ZhCounter = 0; ZhCounter < N_Zh;
                     ZhCounter++) { // Loops in every Zh bin;
                    TH1F *histPt2 = new TH1F(Form("corr_data_Pt2_%s_%i%i%i_%i", target,
                                                  Q2Counter, NuCounter, ZhCounter, nPion),
                                             "", N_Pt2, Pt2_MIN, Pt2_MAX);
                    for (int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) {
                        TH1F *histPhi = (TH1F *)inputFile->Get(
                            Form("DataCorrRc_%s_%i%i%i%i_%i", target, Q2Counter, NuCounter,
                                 ZhCounter, Pt2Counter, nPion));
                        // If the histogram is null or empty skip this Pt2 bin
                        if (histPhi == NULL) {
                            continue;
                        }
                        if (EmptyHist(histPhi) == 1) {
                            continue;
                        }
                        // Integrate on PhiPQ
                        // double errors_array[1] = {};
                        double error;
                        double integral = histPhi->IntegralAndError(1, N_Phi, error);
                        // Save the value in the Pt2 histogram
                        histPt2->SetBinContent(Pt2Counter + 1, integral);
                        // histPt2->SetBinError(Pt2Counter + 1, errors_array[0]);
                        histPt2->SetBinError(Pt2Counter + 1, error);
                        delete histPhi;
                    } // End Pt2 loop
                      // If the histogram if not empty, save it
                    if (EmptyHist(histPt2) == 0) {
                        outputFile->cd();
                        histPt2->Write();
                        gROOT->cd();
                    }
                    delete histPt2;
                } // End Zh loop
            }     // End Nu loop
        }         // End Q2 loop
    }             // End number pion event loop
}

// Integrate the Pt2 histograms for Q2 and Nu bins
void Q2NuIntegration(TFile *inputFile, TFile *outputFile, char target[]) {

    for (int nPion = 1; nPion <= N_PION; nPion++) { // Loops in every number of pion
        // Generate a histogram to save Zh for every number of pion in the final event
        TH1F *histZh = new TH1F(Form("corr_data_%s_%i_Zh", target, nPion), "", N_Zh, Zh_BINS);
        for (int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin
            // Generate a histogram for every bin of zh
            TH1F *histPt2Integrated = new TH1F("histPt2Sum", "", N_Pt2, Pt2_MIN, Pt2_MAX);
            for (int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
                for (int Q2Counter = 0; Q2Counter < N_Q2;
                     Q2Counter++) { // Loops in every Q2 bin
                    // Sum the histograms for every bin of Q2 and Nu
                    TH1F *histPt2 =
                        (TH1F *)inputFile->Get(Form("corr_data_Pt2_%s_%i%i%i_%i", target,
                                                    Q2Counter, NuCounter, ZhCounter, nPion));
                    histPt2Integrated->Add(histPt2);
                    delete histPt2;
                } // End Q2 loop
            }     // End Nu loop

            outputFile->cd();
            histPt2Integrated->Write(Form("corr_data_Pt2_%s_%i_%i", target, ZhCounter, nPion));
            gROOT->cd();
            // Take the mean and save in the Zh histogram
            histZh->SetBinContent(ZhCounter + 1, histPt2Integrated->GetMean());
            histZh->SetBinError(ZhCounter + 1, histPt2Integrated->GetMeanError());

            // Open the direction of the output file and save the data
            delete histPt2Integrated;
        } // End Zh loop

        // Open the direction of the output file and save the data
        outputFile->cd();
        histZh->Write(Form("meanPt2_%s_%i", target, nPion));
        gROOT->cd();
        delete histZh;
    } // End number pion event loop
}

// Integrate the Pt2 histograms for Q2, Nu and Zh bins
void ZhIntegration(TFile *inputFile, TFile *outputFile, char target[]) {

    for (int nPion = 1; nPion <= N_PION; nPion++) { // Loops in every number of pion
        TH1F *hist = new TH1F(Form("corr_data_%s", target), "", 1, 0, 1);
        // To save the sum of the histograms
        TH1F *histPt2Integrated =
            new TH1F(Form("corr_data_%s_Pt2", target), "", N_Pt2, Pt2_MIN, Pt2_MAX);
        // Starts in the second bin because there is not broadening iz Zh<0.2
        for (int ZhCounter = ZH_SUM; ZhCounter < N_Zh; ZhCounter++) { // Loops in every Zh bin

            TH1F *histPt2;
            if (UseCutOff == 1) {
                histPt2 = (TH1F *)inputFile->Get(
                    Form("corr_data_Pt2_%s_%i_%i_interpolated", target, ZhCounter, nPion));
            }
            if (UseCutOff == 2) {
                histPt2 = (TH1F *)inputFile->Get(
                    Form("corr_data_Pt2_%s_%i_%i_clean", target, ZhCounter, nPion));
            }
            if (UseCutOff == 3) {
                histPt2 = (TH1F *)inputFile->Get(
                    Form("corr_data_Pt2_%s_%i_%i", target, ZhCounter, nPion));
            }

            histPt2Integrated->Add(histPt2);
            delete histPt2;
        } // End Zh loop
          // Take the mean and save it
        hist->SetBinContent(1, histPt2Integrated->GetMean());
        hist->SetBinError(1, histPt2Integrated->GetMeanError());

        // Open the direction of the output file and save the data
        outputFile->cd();
        hist->Write(Form("meanPt2_%s_%i", target, nPion));
        gROOT->cd();
        delete hist;
        delete histPt2Integrated;
    } // End number pion event loop
}

void CallPhiIntegration(TString inputDirectory, TString outputDirectory) {

    TFile *inputFile = new TFile(inputDirectory + "corr_data_Phi_Rc.root", "READ");
    TFile *outputFile = new TFile(outputDirectory + "corr_data_Pt2_Rc.root", "RECREATE");
    gROOT->cd();

    PhiIntegration(inputFile, outputFile, DC);
    PhiIntegration(inputFile, outputFile, DFe);
    PhiIntegration(inputFile, outputFile, DPb);

    PhiIntegration(inputFile, outputFile, C);
    PhiIntegration(inputFile, outputFile, Fe);
    PhiIntegration(inputFile, outputFile, Pb);

    inputFile->Close();
    outputFile->Close();
}

void CallQ2NuIntegration(TString inputDirectory, TString outputDirectory) {

    TFile *inputFile = new TFile(inputDirectory + "corr_data_Pt2_Rc.root", "READ");
    TFile *outputFile = new TFile(outputDirectory + "meanPt2_Zh_Rc.root", "RECREATE");
    gROOT->cd();

    Q2NuIntegration(inputFile, outputFile, DC);
    Q2NuIntegration(inputFile, outputFile, DFe);
    Q2NuIntegration(inputFile, outputFile, DPb);

    Q2NuIntegration(inputFile, outputFile, C);
    Q2NuIntegration(inputFile, outputFile, Fe);
    Q2NuIntegration(inputFile, outputFile, Pb);

    inputFile->Close();
    outputFile->Close();
}

void CallZhIntegration(TString inputDirectory, TString outputDirectory) {

    TFile *inputFile = new TFile(inputDirectory + "meanPt2_Zh_processed_Rc.root", "READ");
    TFile *outputFile = new TFile(outputDirectory + "meanPt2_Rc.root", "RECREATE");
    gROOT->cd();

    ZhIntegration(inputFile, outputFile, DC);
    ZhIntegration(inputFile, outputFile, DFe);
    ZhIntegration(inputFile, outputFile, DPb);

    ZhIntegration(inputFile, outputFile, C);
    ZhIntegration(inputFile, outputFile, Fe);
    ZhIntegration(inputFile, outputFile, Pb);

    inputFile->Close();
    outputFile->Close();
}
