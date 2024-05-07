// g++ -Wall -fPIC -I../include `root-config --cflags` Interpolate_Acc_Empty2.cpp -o
// ../bin/Interpolate_Acc_Empty `root-config --glibs` ../include/Binning.h

#include "Binning.h"
#include "TFile.h"
#include "TH1F.h"
#include "TMath.h"
#include "TROOT.h"
#include "TString.h"
#include <iostream>

int ApplyInterpolateAcc(std::string target, TFile *fileData, TFile *fileAccInter,
                        TFile *fileDataCorr);
int InterpolationAcc(std::string target, TFile *fileData, TFile *fileDataEvents,
                     TFile *fileAccInter);
int SetEmptyHistogram(TH1F *hist);

int main() {

    // TString DataEvents =
    // "/home/matias/proyecto/TwoPionAnalysis/Data/AccInter/corr_data_Phi.root"; TFile
    // *fileDataEvents  = new TFile(DataEvents,  "READ");
    TFile *fileDataEvents = new TFile(inputDirectory + "corr_data_Phi.root", "READ");
    TFile *fileData = new TFile(inputDirectory + "corr_data_Phi.root", "READ");
    TFile *fileAccInter = new TFile(outputDirectory + "AccInter.root", "RECREATE");
    TFile *fileDataCorr = new TFile(outputDirectory + "corr_data_Phi_Inter.root", "RECREATE");
    gROOT->cd();

    const char *Targets[2 * N_STARGETS] = {"C", "Fe", "Pb", "DC", "DFe", "DPb"};

    for (int i = 0; i < 2 * N_STARGETS; i++) {
        std::cout << "Interpolating " << Targets[i] << " ";
        InterpolationAcc(Targets[i], fileData, fileDataEvents, fileAccInter);
    }
    fileData->Close();
    fileAccInter->Close();
    delete fileAccInter;
    TFile *fileAccInterRead = new TFile(outputDirectory + "AccInter.root", "READ");

    for (int i = 0; i < 2 * N_STARGETS; i++) {
        std::cout << "Applying Acc Interpolated " << Targets[i] << "\n";
        ApplyInterpolateAcc(Targets[i], fileDataEvents, fileAccInterRead, fileDataCorr);
    }

    fileDataEvents->Close();
    fileAccInterRead->Close();
    fileDataCorr->Close();
    return 0;
}

int ApplyInterpolateAcc(std::string target, TFile *fileData, TFile *fileAccInter,
                        TFile *fileDataCorr) {

    std::cout << "Start" << std::endl;
    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());
    TH1F *histDataCorr = new TH1F("DataCorr2", "", N_Phi, -180, 180);

    for (int nPion = 1; nPion <= N_PION; nPion++) { // Loops number of pions

        for (int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) {         // Loops Q2 bins
            for (int NuCounter = 0; NuCounter < N_Nu; NuCounter++) {     // Loops Nu bins
                for (int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops Zh bins;
                    for (int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { // Pt2 bins;

                        TH1F *histData = (TH1F *)fileData->Get(
                            Form("Data_%s_%i%i%i%i_%i", targetArr, Q2Counter, NuCounter,
                                 ZhCounter, Pt2Counter, nPion));

                        if (histData == NULL) {
                            delete histData;
                            continue;
                        }

                        TH1F *hist = (TH1F *)fileAccInter->Get(
                            Form("FinalFactor_%s_%i%i%i%i_%i", targetArr, Q2Counter, NuCounter,
                                 ZhCounter, Pt2Counter, nPion));

                        histDataCorr->Divide(histData, hist, 1, 1);
                        fileDataCorr->cd();

                        histData->Write(Form("Data_%s_%i%i%i%i_%i", targetArr, Q2Counter,
                                             NuCounter, ZhCounter, Pt2Counter, nPion));
                        histDataCorr->Write(Form("DataCorr2_%s_%i%i%i%i_%i", targetArr,
                                                 Q2Counter, NuCounter, ZhCounter, Pt2Counter,
                                                 nPion));
                        hist->Write(Form("FinalFactor_%s_%i%i%i%i_%i", targetArr, Q2Counter,
                                         NuCounter, ZhCounter, Pt2Counter, nPion));

                        gROOT->cd();

                        histDataCorr->Reset();
                        delete hist;
                        delete histData;
                    }
                }
            }
        }
    }

    delete histDataCorr;
    return 0;
}

int InterpolationAcc(std::string target, TFile *fileData, TFile *fileDataEvents,
                     TFile *fileAccInter) {

    std::cout << "Start" << std::endl;
    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());
    double Acc, AccPrevQ2, AccNextQ2, AccPrevNu, AccNextNu, AccPrevZh, AccNextZh, AccPrevPt2,
        AccNextPt2, AccPrevPhi, AccNextPhi, AccSum;
    double AccErr, AccErrPrevQ2, AccErrNextQ2, AccErrPrevNu, AccErrNextNu, AccErrPrevZh,
        AccErrNextZh, AccErrPrevPt2, AccErrNextPt2, AccErrPrevPhi, AccErrNextPhi, AccErrSum;
    double AccNei[10];
    double AccErrNei[10];
    int counter;

    double AccArray[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi];
    double AccErrArray[N_Q2][N_Nu][N_Zh][N_Pt2][N_Phi];

    int nInterpolatedBins;

    for (int nPion = 1; nPion <= N_PION; nPion++) { // Loops number of pions

        nInterpolatedBins = 0;
        std::cout << "number of pion: " << nPion << std::endl;
        for (int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) {         // Loops Q2 bins
            for (int NuCounter = 0; NuCounter < N_Nu; NuCounter++) {     // Loops Nu bins
                for (int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops Zh bins;
                    for (int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { // Pt2 bins;
                        for (int PhiCounter = 0; PhiCounter < N_Phi; PhiCounter++) {
                            AccArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter][PhiCounter] =
                                -1;
                            AccErrArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                       [PhiCounter] = -1;
                        }
                    }
                }
            }
        }

        for (int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) {         // Loops Q2 bins
            for (int NuCounter = 0; NuCounter < N_Nu; NuCounter++) {     // Loops Nu bins
                for (int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops Zh bins;
                    for (int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { // Pt2 bins;

                        // Read the actual bin an the two neiberhoods
                        TH1F *histData = (TH1F *)fileDataEvents->Get(
                            Form("Data_%s_%i%i%i%i_%i", targetArr, Q2Counter, NuCounter,
                                 ZhCounter, Pt2Counter, nPion));

                        if (histData == NULL) {
                            delete histData;
                            continue;
                        }

                        TH1F *hist = (TH1F *)fileData->Get(
                            Form("FinalFactor_%s_%i%i%i%i_%i", targetArr, Q2Counter, NuCounter,
                                 ZhCounter, Pt2Counter, nPion));

                        // TH1F *hist = (TH1F *)fileData->Get(
                        // Form("AccFactor_%s_%i%i%i%i_%i", targetArr, Q2Counter, NuCounter,
                        // ZhCounter, Pt2Counter, nPion));

                        // TH1F *hist = new TH1F("FinalFactor", "", N_Phi, -180, 180);
                        // TH1F *histAcc = (TH1F *)fileData->Get(
                        // Form("AccFactor_%s_%i%i%i%i_%i", targetArr, Q2Counter, NuCounter,
                        // ZhCounter, Pt2Counter, nPion));
                        // TH1F *histFal = (TH1F *)fileData->Get(
                        // Form("FalPosFactor_%s_%i%i%i%i_%i", targetArr, Q2Counter,
                        // NuCounter, ZhCounter, Pt2Counter, nPion));

                        // if (histAcc == NULL || histFal == NULL) {
                        // hist = new TH1F(Form("FinalFactor_%s_%i%i%i%i_%i", targetArr,
                        // Q2Counter, NuCounter, ZhCounter, Pt2Counter,
                        // nPion),
                        //"", N_Phi, -180, 180);
                        // SetEmptyHistogram(hist);
                        //} else {
                        // hist->Divide(histAcc, histFal, 1, 1);
                        //}

                        if (hist == NULL) {
                            hist = new TH1F(Form("FinalFactor_%s_%i%i%i%i_%i", targetArr,
                                                 Q2Counter, NuCounter, ZhCounter, Pt2Counter,
                                                 nPion),
                                            "", N_Phi, -180, 180);
                            SetEmptyHistogram(hist);
                        }

                        for (int PhiCounter = 1; PhiCounter <= N_Phi; PhiCounter++) {

                            if (histData->GetBinContent(PhiCounter) != 0) {
                                // Acc = hist->GetBinContent(PhiCounter);
                                if (hist->GetBinContent(PhiCounter) <= 1) {

                                    AccArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                            [PhiCounter - 1] = hist->GetBinContent(PhiCounter);
                                    AccErrArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                               [PhiCounter - 1] =
                                                   hist->GetBinError(PhiCounter);
                                    continue;

                                } else {
                                    AccArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                            [PhiCounter - 1] = 0;
                                    AccErrArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                               [PhiCounter - 1] = 0;
                                    continue;
                                }
                            } else {
                                AccArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                        [PhiCounter - 1] = -1;
                                AccErrArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                           [PhiCounter - 1] = -1;
                            }
                        }

                        delete hist;
                        delete histData;

                        // delete histAcc;
                        // delete histFal;

                    } // End Pt2 Loop
                }     // End ZhCounter Loop
            }         // End Nu Loop
        }             // End Q2Counter Loop

        for (int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) {         // Loops Q2 bins
            for (int NuCounter = 0; NuCounter < N_Nu; NuCounter++) {     // Loops Nu bins
                for (int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops Zh bins;
                    for (int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { // Pt2 bins;
                        for (int PhiCounter = 0; PhiCounter < N_Phi; PhiCounter++) {

                            for (int i = 0; i < 10; i++) {
                                AccNei[i] = 0;
                                AccErrNei[i] = 0;
                            }

                            if (AccArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                        [PhiCounter] == -1) {
                                continue;
                            }

                            if (AccArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                        [PhiCounter] != 0) {
                                continue;
                            }

                            nInterpolatedBins++;
                            if (Q2Counter - 1 < -0.1) {
                                AccPrevQ2 = 0;
                            } else {
                                AccPrevQ2 = AccArray[Q2Counter - 1][NuCounter][ZhCounter]
                                                    [Pt2Counter][PhiCounter];
                                AccErrPrevQ2 = AccErrArray[Q2Counter - 1][NuCounter][ZhCounter]
                                                          [Pt2Counter][PhiCounter];
                            }
                            if (Q2Counter + 1 > N_Q2 - 0.1) {
                                AccNextQ2 = 0;
                            } else {
                                AccNextQ2 = AccArray[Q2Counter + 1][NuCounter][ZhCounter]
                                                    [Pt2Counter][PhiCounter];
                                AccErrNextQ2 = AccErrArray[Q2Counter + 1][NuCounter][ZhCounter]
                                                          [Pt2Counter][PhiCounter];
                            }
                            if (NuCounter - 1 < -0.1) {
                                AccPrevNu = 0;
                            } else {
                                AccPrevNu = AccArray[Q2Counter][NuCounter - 1][ZhCounter]
                                                    [Pt2Counter][PhiCounter];
                                AccErrPrevNu = AccErrArray[Q2Counter][NuCounter - 1][ZhCounter]
                                                          [Pt2Counter][PhiCounter];
                            }
                            if (NuCounter + 1 > N_Nu - 0.1) {
                                AccNextNu = 0;
                            } else {
                                AccNextNu = AccArray[Q2Counter][NuCounter + 1][ZhCounter]
                                                    [Pt2Counter][PhiCounter];
                                AccErrNextNu = AccErrArray[Q2Counter][NuCounter + 1][ZhCounter]
                                                          [Pt2Counter][PhiCounter];
                            }
                            if (ZhCounter - 1 < -0.1) {
                                AccPrevZh = 0;
                            } else {
                                AccPrevZh = AccArray[Q2Counter][NuCounter][ZhCounter - 1]
                                                    [Pt2Counter][PhiCounter];
                                AccErrPrevZh = AccErrArray[Q2Counter][NuCounter][ZhCounter - 1]
                                                          [Pt2Counter][PhiCounter];
                            }
                            if (ZhCounter + 1 > N_Zh - 0.1) {
                                AccNextZh = 0;
                            } else {
                                AccNextZh = AccArray[Q2Counter][NuCounter][ZhCounter + 1]
                                                    [Pt2Counter][PhiCounter];
                                AccErrNextZh = AccErrArray[Q2Counter][NuCounter][ZhCounter + 1]
                                                          [Pt2Counter][PhiCounter];
                            }
                            if (Pt2Counter - 1 < -0.1) {
                                AccPrevPt2 = 0;
                            } else {
                                AccPrevPt2 = AccArray[Q2Counter][NuCounter][ZhCounter]
                                                     [Pt2Counter - 1][PhiCounter];
                                AccErrPrevPt2 = AccErrArray[Q2Counter][NuCounter][ZhCounter]
                                                           [Pt2Counter - 1][PhiCounter];
                            }
                            if (Pt2Counter + 1 > N_Pt2 - 0.1) {
                                AccNextPt2 = 0;
                            } else {
                                AccNextPt2 = AccArray[Q2Counter][NuCounter][ZhCounter]
                                                     [Pt2Counter + 1][PhiCounter];
                                AccErrNextPt2 = AccErrArray[Q2Counter][NuCounter][ZhCounter]
                                                           [Pt2Counter + 1][PhiCounter];
                            }

                            if (PhiCounter - 1 < -0.1) {
                                AccPrevPhi = 0;
                            } else {
                                AccPrevPhi = AccArray[Q2Counter][NuCounter][ZhCounter]
                                                     [Pt2Counter][PhiCounter - 1];
                                AccErrPrevPhi = AccErrArray[Q2Counter][NuCounter][ZhCounter]
                                                           [Pt2Counter][PhiCounter - 1];
                            }
                            if (PhiCounter + 1 > N_Phi - 0.1) {
                                AccNextPhi = 0;
                            } else {
                                AccNextPhi = AccArray[Q2Counter][NuCounter][ZhCounter]
                                                     [Pt2Counter][PhiCounter + 1];
                                AccErrNextPhi = AccErrArray[Q2Counter][NuCounter][ZhCounter]
                                                           [Pt2Counter][PhiCounter + 1];
                            }

                            AccNei[0] = AccPrevQ2;
                            AccNei[1] = AccNextQ2;
                            AccNei[2] = AccPrevNu;
                            AccNei[3] = AccNextNu;
                            AccNei[4] = AccPrevZh;
                            AccNei[5] = AccNextZh;
                            AccNei[6] = AccPrevPt2;
                            AccNei[7] = AccNextPt2;
                            AccNei[8] = AccPrevPhi;
                            AccNei[9] = AccNextPhi;

                            AccErrNei[0] = AccErrPrevQ2;
                            AccErrNei[1] = AccErrNextQ2;
                            AccErrNei[2] = AccErrPrevNu;
                            AccErrNei[3] = AccErrNextNu;
                            AccErrNei[4] = AccErrPrevZh;
                            AccErrNei[5] = AccErrNextZh;
                            AccErrNei[6] = AccErrPrevPt2;
                            AccErrNei[7] = AccErrNextPt2;
                            AccErrNei[8] = AccErrPrevPhi;
                            AccErrNei[9] = AccErrNextPhi;

                            // for (int i = 0; i < 10; i++) {
                            // std::cout << AccNei[i] << " & ";
                            //}
                            // std::cout << std::endl;

                            counter = 0;
                            int countermenos1 = 0;
                            AccSum = 0;
                            AccErrSum = 0;
                            for (int i = 0; i < 10; i++) {

                                if (AccNei[i] != 0 && AccNei[i] != -1) {
                                    AccSum += AccNei[i];
                                    AccErrSum += AccErrNei[i];
                                    counter++;
                                }

                                if (AccNei[i] != -1) {
                                    countermenos1++;
                                }
                            }

                            if (counter == 0) {
                                AccArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                        [PhiCounter] = Acc;
                                AccErrArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                           [PhiCounter] = AccErr;
                            }

                            else {
                                Acc = AccSum / counter;
                                AccErr = AccErrSum / counter;
                                AccArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                        [PhiCounter] = AccSum / counter;
                                AccErrArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                           [PhiCounter] = AccErrSum / counter;
                            }
                        }
                    }
                }
            }
        }

        std::cout << "Interpolated Bins: " << nInterpolatedBins << std::endl;

        TH1F *histSave = new TH1F("histSave", "", N_Phi, -180, 180);
        for (int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) {         // Loops Q2 bins
            for (int NuCounter = 0; NuCounter < N_Nu; NuCounter++) {     // Loops Nu bins
                for (int ZhCounter = 0; ZhCounter < N_Zh; ZhCounter++) { // Loops Zh bins;
                    for (int Pt2Counter = 0; Pt2Counter < N_Pt2; Pt2Counter++) { // Pt2 bins;
                        // std::cout << " Zh Counter: " << ZhCounter << std::endl;

                        int counterData = 0;
                        for (int PhiCounter = 0; PhiCounter < N_Phi; PhiCounter++) {

                            if (AccArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                        [PhiCounter] == -1) {
                                // std::cout <<" suma "
                                // <<nPion<<"--"<<Q2Counter<<"--"<<NuCounter<<"--"<<ZhCounter<<"--"<<Pt2Counter<<"--"<<std::endl;
                                counterData++;
                            }
                        }

                        if (counterData == N_Phi) {
                            continue;
                        }

                        for (int PhiCounter = 0; PhiCounter < N_Phi; PhiCounter++) {

                            if (AccArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                        [PhiCounter] == -1) {
                                histSave->SetBinContent(PhiCounter + 1, 0);
                                histSave->SetBinError(PhiCounter + 1, 0);
                            }

                            else if (AccArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                             [PhiCounter] == 0) {
                                histSave->SetBinContent(PhiCounter + 1, 0);
                                histSave->SetBinError(PhiCounter + 1, 0);
                            }

                            else if (AccArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                             [PhiCounter] != 0) {
                                histSave->SetBinContent(
                                    PhiCounter + 1, AccArray[Q2Counter][NuCounter][ZhCounter]
                                                            [Pt2Counter][PhiCounter]);
                                histSave->SetBinError(
                                    PhiCounter + 1,
                                    AccErrArray[Q2Counter][NuCounter][ZhCounter][Pt2Counter]
                                               [PhiCounter]);
                            }
                        }

                        fileAccInter->cd();
                        histSave->Write(Form("FinalFactor_%s_%i%i%i%i_%i", targetArr,
                                             Q2Counter, NuCounter, ZhCounter, Pt2Counter,
                                             nPion));
                        gROOT->cd();
                        histSave->Reset();
                    }
                }
            }
        }

        delete histSave;

    } // End Number of pions Loop

    return 0;
}

int SetEmptyHistogram(TH1F *hist) {

    for (int i = 1; i <= N_Phi; i++) {
        hist->SetBinContent(i, 0);
    }

    return 0;
}
