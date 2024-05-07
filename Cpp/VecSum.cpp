// This code generate a tuple with all the events of experimental data
// Saves the electron variables and calculate for the hadrons variables
// calculate vectorial momentum and use it as the hadron momentum for the event
// The code require that you have the number of the event saved in the data tupleName
// if you don't have it you can check by for the paricle has the same Q2 and Nu instead
// It can be compiled with
// g++ -Wall -fPIC -I../include `root-config --cflags` VecSum.cpp -o ../bin/VecSum `root-config
// --glibs` ../include/Binning.h For the target name use (C,Fe,Pb)

#include "Binning.h"
#include "TFile.h"
#include "TMath.h"
#include "TNtuple.h"
#include "TROOT.h"
#include "TStopwatch.h"
#include "TString.h"
#include "TVector2.h"
#include "TVector3.h"
#include <iostream>
#include <string>

double kEbeam = 5.014;

double Momentum(float Px, float Py, float Pz) {
    // Returns the full momentum for the particle in the row k
    return TMath::Sqrt(Px * Px + Py * Py + Pz * Pz);
}

double CosThetaPQ(float Px, float Py, float Pz, float Pxe, float Pye, float Pze, float Q2,
                  float Nu) {
    // Returns the cosine of ThetaPQ for the particle
    return (Pz * (kEbeam - Pze) - Px * Pxe - Py * Pye) /
           (TMath::Sqrt(Nu * Nu + Q2) * Momentum(Px, Py, Pz));
}

double PhiPQ(float Px, float Py, float Pz, float Pxe, float Pye, float Pze) {
    // Returns the azimuthal angle of the particle w.r.t. the virtual photon direction
    // First, it Z-rotates the virtual photon momentum to have Y-component=0
    // Second, it Z-rotates the particle momentum by the same amount
    // Third, it Y-rotates the virtual photon to have X-component=0
    // Lastly, it Y-rotates the particle momentum by the same amount
    // In the end, the values of the particle momentum components will be w.r.t to the virtual
    // photon momentum
    TVector3 Vpi(Px, Py, Pz);
    TVector3 Vvirt(-Pxe, -Pye, kEbeam - Pze);
    Double_t phi_z = TMath::Pi() - Vvirt.Phi();
    Vvirt.RotateZ(phi_z);
    Vpi.RotateZ(phi_z);
    TVector3 Vhelp(0., 0., 1.);
    Double_t phi_y = Vvirt.Angle(Vhelp);
    Vvirt.RotateY(phi_y);
    Vpi.RotateY(phi_y);
    return Vpi.Phi() * TMath::RadToDeg();
}

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

    TFile *file = new TFile(
        "/home/matias/proyecto/Pt2Broadening_multi-pion/Data/prunedC_42011-good.root", "READ");
    TNtuple *tuple = (TNtuple *)file->Get("ntuple_data");

    int tmpCounter = 0;  // Counts how many particles there is in the event
    int pionCounter = 0; // Counts how many pions there is in the event (check Delta Z Cut)
    float tmpEvnt, evnt, Q2Evnt, NuEvnt, XbEvnt, ZhEvnt, Pt2Evnt, PhiEvnt, YCEvnt, VCEvnt,
        DZEvnt, Px, Py, Pz, Pxe, Pye, Pze;
    float tmpZh[5], tmpPt[5], tmpPhi[5], tmpPx[5], tmpPy[5], tmpPz[5];
    float tmpPxe, tmpPye, tmpPze;
    float totPx, totPy, totPz, pid;
    float deltaZcut = 3.;
    int dummyval = -999;
    const char *VarList = "Q2:Nu:Zh:Pt2:PhiPQ:YC:VC_TM:Zh_1:Zh_2:Zh_3:Xb";
    // Variables to fill the tuple
    float *vars = new Float_t[11];
    // Read the necesary variables
    tuple->SetBranchAddress("Q2", &Q2Evnt);
    tuple->SetBranchAddress("Nu", &NuEvnt);
    tuple->SetBranchAddress("Xb", &XbEvnt);
    tuple->SetBranchAddress("Zh", &ZhEvnt);
    tuple->SetBranchAddress("Pt2", &Pt2Evnt);
    tuple->SetBranchAddress("PhiPQ", &PhiEvnt);
    tuple->SetBranchAddress("deltaZ", &DZEvnt);
    tuple->SetBranchAddress("Pex", &Pxe);
    tuple->SetBranchAddress("Pey", &Pye);
    tuple->SetBranchAddress("Pez", &Pze);
    tuple->SetBranchAddress("Px", &Px);
    tuple->SetBranchAddress("Py", &Py);
    tuple->SetBranchAddress("Pz", &Pz);
    tuple->SetBranchAddress("evnt", &evnt);
    tuple->SetBranchAddress("pid", &pid);

    gROOT->cd();

    TNtuple *ntuplePion[5];

    for (int i = 0; i < 5; i++) {
        ntuplePion[i] = new TNtuple(Form("ntuple_%i_pion", i + 1), "", VarList);
    }

    for (int i = 0; i < tuple->GetEntries(); i++) { // Loops in every detected paricle
        tuple->GetEntry(i);
        pionCounter = 0;
        tmpCounter = 0;
        totPx = 0;
        totPy = 0;
        totPz = 0;
        vars[0] = Q2Evnt;
        vars[1] = NuEvnt;
        tmpPxe = Pxe;
        tmpPye = Pye;
        tmpPze = Pze;
        vars[10] = XbEvnt;
        if (TMath::Abs(DZEvnt) < deltaZcut && pid == 211) {
            vars[2] = ZhEvnt;
            vars[3] = Pt2Evnt;
            vars[4] = PhiEvnt;
            vars[5] = YCEvnt;
            vars[6] = VCEvnt;
            tmpZh[pionCounter] = vars[2];
            tmpPt[pionCounter] = TMath::Sqrt(Pt2Evnt);
            tmpPhi[pionCounter] = vars[4];
            tmpPx[pionCounter] = Px;
            tmpPy[pionCounter] = Py;
            tmpPz[pionCounter] = Pz;
            pionCounter++;
        }
        tmpEvnt = evnt;
        tuple->GetEntry(i + 1);
        while (tmpEvnt == evnt) { // Check all the paricles in the event
            tmpCounter++;
            if (TMath::Abs(DZEvnt) < deltaZcut && pid == 211) {
                tmpZh[pionCounter] = ZhEvnt;
                tmpPt[pionCounter] = TMath::Sqrt(Pt2Evnt);
                tmpPhi[pionCounter] = PhiEvnt;
                tmpPx[pionCounter] = Px;
                tmpPy[pionCounter] = Py;
                tmpPz[pionCounter] = Pz;
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
            totPx += tmpPx[k];
            totPy += tmpPy[k];
            totPz += tmpPz[k];
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
        }
        // vars[8] = tmpZh[1];
        // vars[9] = dummyval;
        // }
        if (pionCounter == 2) {
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
        if (pionCounter > 1) {
            std::cout << "--Nominal Method--" << std::endl;
            std::cout << "Number of Pions: " << pionCounter << std::endl;
            std::cout << "ZhSum: " << vars[2] << std::endl;
            std::cout << "Pt2Sum: " << vars[3] << std::endl;
            std::cout << "PhiSum: " << vars[4] << std::endl;
            std::cout << "--Projection method--" << std::endl;
            std::cout << "Number of Pions: " << pionCounter << std::endl;
            std::cout << "ZhSum: " << vars[2] << std::endl;
            std::cout << "Pt2Sum: "
                      << Momentum(totPx, totPy, totPz) * Momentum(totPx, totPy, totPz) *

                             (1 - CosThetaPQ(totPx, totPy, totPz, tmpPxe, tmpPye, tmpPze,
                                             vars[0], vars[1]) *
                                      CosThetaPQ(totPx, totPy, totPz, tmpPxe, tmpPye, tmpPze,
                                                 vars[0], vars[1]))
                      << std::endl;
            std::cout << "PhiSum: " << PhiPQ(totPx, totPy, totPz, tmpPxe, tmpPye, tmpPze)
                      << std::endl;
            std::cout << std::endl;
        }
    } // End paricle loop

    gROOT->cd();
    file->Close();
    std::cout << "Done." << std::endl;
    t.Print();
}
