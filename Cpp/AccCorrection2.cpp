// This code apply the two acceptance factors to the data and
// generate a PhiPq histogram for each bin of Q2, Nu, Zh, Pt2
// The hadrons variables used were calculate taking the vectorial
// sum of the hadrons momentum and using it as hadron momentum for the event
// For simultion use the tuple generate by the code VecSumSimul.cpp
// For data the tuple generate by the code VecSum.cpp
// It can be compile with
// g++ -Wall -fPIC -I../include `root-config --cflags` AccCorrection2.cpp -o
// ,./bin/AccCorrection2  `root-config --glibs` ../include/Acc.h For the target
// name use (C,Fe,Pb) for the solids targets and (DC,DFe,DPb) for the liquid
// target

#include "Acc.h"

int AcceptanceCorrection(std::string target, TFile *fileOutput);

int main() {

    TFile *fileOutput = new TFile(outputDirectory + "corr_data_Phi.root", "RECREATE");

    gROOT->cd();

    std::cout << "Acceptance Correction for C" << std::endl;
    AcceptanceCorrection("C", fileOutput);

    std::cout << "Acceptance Correction for Fe" << std::endl;

    AcceptanceCorrection("Fe", fileOutput);

    std::cout << "Acceptance Correction for Pb" << std::endl;
    AcceptanceCorrection("Pb", fileOutput);
    std::cout << "Acceptance Correction for DC" << std::endl;
    AcceptanceCorrection("DC", fileOutput);
    std::cout << "Acceptance Correction for DFe" << std::endl;
    AcceptanceCorrection("DFe", fileOutput);
    std::cout << "Acceptance Correction for DPb" << std::endl;
    AcceptanceCorrection("DPb", fileOutput);

    fileOutput->Close();
    return 0;
}

int AcceptanceCorrection(std::string target, TFile *fileOutput) {

    TStopwatch t;

    std::cout << "Start" << std::endl;
    int n = target.length();
    char targetArr[n + 1];
    strcpy(targetArr, target.c_str());

    int m;
    TString fileDataName;
    // Select the data for the chosen solid target
    if (targetArr[0] == 'D') {
        m = 2;
        char solidTarget[n];
        for (int i = 0; i < n; i++) {
            solidTarget[i] = targetArr[i + 1];
        }
        fileDataName = Form(dataDirectory + "VecSum_%s.root", solidTarget);
    } else {
        m = n + 1;
        fileDataName = Form(dataDirectory + "VecSum_%s.root", targetArr);
    }

    // Select the target of the simultion
    char simulTarget[m];
    if (targetArr[0] == 'D') {
        simulTarget[0] = 'D';
        simulTarget[1] = '\0';
    } else {
        for (int i = 0; i < m; i++) {
            simulTarget[i] = targetArr[i];
        }
    }
    // Open the input and output files
    TFile *fileData = new TFile(fileDataName, "READ");
    TFile *fileSimul =
        new TFile(dataDirectory + Form("SimulTuple_%s.root", simulTarget), "READ");
    gROOT->cd();

    // Create some variables to use inside the for loops
    TString tupleDataName;
    TCut Q2Cut, NuCut, ZhCut, Pt2Cut, VCData, cutsData;
    TCut Q2Cut_gen, NuCut_gen, ZhCut_gen, Pt2Cut_gen, cutsSimul_gen, GenCut;
    TCut Q2Cut_rec, NuCut_rec, ZhCut_rec, Pt2Cut_rec, cutsSimul_rec, RecCut;
    TCut YCCut = "TMath::Abs(YC)<1.4";
    // Select liquid or solid target
    if (targetArr[0] == 'D') {
        VCData = "VC_TM == 1.";
    } else {
        VCData = "VC_TM == 2.";
    }
    std::cout << Form("Simul target %s, Target %s", simulTarget, targetArr) << std::endl;

    // Create all the necessary histograms
    TH1F *histTotDetected = new TH1F("TotDetected", "", N_Phi, -180, 180);
    TH1F *histThrown = new TH1F("Thrown", "", N_Phi, -180, 180);
    TH1F *histData = new TH1F("Data", "", N_Phi, -180, 180);
    TH1F *histAccFactors = new TH1F("AccFactor", "", N_Phi, -180, 180);
    TH1F *histDataCorr = new TH1F("DataCorr", "", N_Phi, -180, 180);

    // Store the sum of the weights A.K.A the erros (in the others is done by
    // default)
    histData->Sumw2();
    histThrown->Sumw2();
    histTotDetected->Sumw2();

    for (int gen = 1; gen <= N_PION; gen++) { // Loops in every number of generated pions

        GenCut = Form("Gen == %f", (float)gen);
        RecCut = Form("Rec == %f", (float)gen);
        // GenDecCut = GenCut||RecCut;

        for (int Q2Counter = 0; Q2Counter < N_Q2; Q2Counter++) {     // Loops in every Q2 bin
            for (int NuCounter = 0; NuCounter < N_Nu; NuCounter++) { // Loops in every Nu bin
                for (int ZhCounter = 0; ZhCounter < N_Zh;
                     ZhCounter++) { // Loops in every Zh bin

                    std::cout << "Bin selected: " << gen << Q2Counter << NuCounter << ZhCounter
                              << std::endl;

                    // Select the cuts for each bin
                    Q2Cut = Form("Q2>%f&&Q2<%f", Q2_BINS[Q2Counter], Q2_BINS[Q2Counter + 1]);
                    NuCut = Form("Nu>%f&&Nu<%f", Nu_BINS[NuCounter], Nu_BINS[NuCounter + 1]);
                    ZhCut = Form("Zh>%f&&Zh<%f", Zh_BINS[ZhCounter], Zh_BINS[ZhCounter + 1]);
                    Q2Cut_gen = Form("Q2_gen>%f&&Q2_gen<%f", Q2_BINS[Q2Counter],
                                     Q2_BINS[Q2Counter + 1]);
                    NuCut_gen = Form("Nu_gen>%f&&Nu_gen<%f", Nu_BINS[NuCounter],
                                     Nu_BINS[NuCounter + 1]);
                    ZhCut_gen = Form("Zh_gen>%f&&Zh_gen<%f", Zh_BINS[ZhCounter],
                                     Zh_BINS[ZhCounter + 1]);
                    Q2Cut_rec = Form("Q2_rec>%f&&Q2_rec<%f", Q2_BINS[Q2Counter],
                                     Q2_BINS[Q2Counter + 1]);
                    NuCut_rec = Form("Nu_rec>%f&&Nu_rec<%f", Nu_BINS[NuCounter],
                                     Nu_BINS[NuCounter + 1]);
                    ZhCut_rec = Form("Zh_rec>%f&&Zh_rec<%f", Zh_BINS[ZhCounter],
                                     Zh_BINS[ZhCounter + 1]);

                    cutsData = Q2Cut && NuCut && ZhCut && YCCut && VCData;
                    cutsSimul_gen = Q2Cut_gen && NuCut_gen && ZhCut_gen && GenCut;
                    cutsSimul_rec = Q2Cut_rec && NuCut_rec && ZhCut_rec && RecCut;

                    TNtuple *ntupleData =
                        (TNtuple *)fileData->Get(Form("ntuple_%i_pion", gen));
                    TNtuple *ntupleSimul_gen = (TNtuple *)fileSimul->Get("ntuple_sim_gen");
                    TNtuple *ntupleSimul_rec = (TNtuple *)fileSimul->Get("ntuple_sim_rec");

                    // Apply the cuts to the ntuples to increces the efficiency
                    ntupleData->Draw(">>listData", cutsData);
                    ntupleSimul_gen->Draw(">>listSimul_gen", cutsSimul_gen);
                    ntupleSimul_rec->Draw(">>listSimul_rec", cutsSimul_rec);

                    TEventList *evntData = (TEventList *)gDirectory->Get("listData");
                    TEventList *evntSimul_gen = (TEventList *)gDirectory->Get("listSimul_gen");
                    TEventList *evntSimul_rec = (TEventList *)gDirectory->Get("listSimul_rec");

                    ntupleData->SetEventList(evntData);
                    ntupleSimul_gen->SetEventList(evntSimul_gen);
                    ntupleSimul_rec->SetEventList(evntSimul_rec);

                    for (int Pt2Counter = 0; Pt2Counter < N_Pt2;
                         Pt2Counter++) { // Loops in every Pt2 bin

                        // Select the Pt2 bin
                        Pt2Cut = Form("Pt2>%f&&Pt2<%f", Pt2_BINS[Pt2Counter],
                                      Pt2_BINS[Pt2Counter + 1]);
                        Pt2Cut_gen = Form("Pt2_gen>%f&&Pt2_gen<%f", Pt2_BINS[Pt2Counter],
                                          Pt2_BINS[Pt2Counter + 1]);
                        Pt2Cut_rec = Form("Pt2_rec>%f&&Pt2_rec<%f", Pt2_BINS[Pt2Counter],
                                          Pt2_BINS[Pt2Counter + 1]);

                        ntupleData->Project("Data", "PhiPQ", Pt2Cut);
                        if (EmptyHist(histData) == 1) {
                            continue;
                        } // Skip the bin id there isn't any event
                          // Generate histograms of the all dectected pion, all
                          // generated pion, and the pions that was correct
                          // dectected
                        // ntupleSimul_rec->Project("Detected",    "PhiPQ_rec",
                        // Pt2Cut_rec&&GenCut);
                        ntupleSimul_gen->Project("Thrown", "PhiPQ_gen", Pt2Cut_gen);
                        ntupleSimul_rec->Project("TotDetected", "PhiPQ_rec", Pt2Cut_rec);

                        // Calculate the Acceptance factor
                        histAccFactors->Divide(histThrown, histTotDetected, 1, 1, "B");
                        // Apply the correction factors
                        histDataCorr->Multiply(histData, histAccFactors, 1, 1);

                        // Save the histograms in the output file
                        fileOutput->cd();

                        histData->Write(Form("Data_%s_%i%i%i%i_%i", targetArr, Q2Counter,
                                             NuCounter, ZhCounter, Pt2Counter, gen));
                        histDataCorr->Write(Form("DataCorr_%s_%i%i%i%i_%i", targetArr,
                                                 Q2Counter, NuCounter, ZhCounter, Pt2Counter,
                                                 gen));
                        histAccFactors->Write(Form("AccFactor_%s_%i%i%i%i_%i", targetArr,
                                                   Q2Counter, NuCounter, ZhCounter, Pt2Counter,
                                                   gen));

                        gROOT->cd();

                        // Set the histograms values to 0
                        histData->Reset();
                        histDataCorr->Reset();
                        histAccFactors->Reset();
                        histThrown->Reset();
                        histTotDetected->Reset();

                    } // End Pt2 loop
                    delete ntupleData;
                    delete ntupleSimul_gen;
                    delete ntupleSimul_rec;
                    delete evntData;
                    delete evntSimul_gen;
                    delete evntSimul_rec;
                } // End Q2 loop
            }     // End Nu loop
        }         // End Zh loop
    }             // End pion number loop

    fileData->Close();
    fileSimul->Close();
    t.Print();
    delete histTotDetected;
    delete histThrown;
    delete histData;
    delete histAccFactors;
    delete histDataCorr;
    return 0;
}
