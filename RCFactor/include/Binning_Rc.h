#include "TString.h"

// const TString inputDirectory  = "/home/matias/proyecto/TwoPionAnalysis/Data/Bins/60/";
// const TString outputDirectory = "/home/matias/proyecto/TwoPionAnalysis/Data/Bins/60/";
const TString dataDirectory = "/home/matias/proyecto/Pt2Broadening_multi-pion/Data/";

const TString inputDirectory =
    "/home/matias/proyecto/TwoPionAnalysis/Data/AnalysisNote/Systematic/RCInter/";
const TString outputDirectory =
    "/home/matias/proyecto/TwoPionAnalysis/Data/AnalysisNote/Systematic/RCInter/";
const TString sysDirectory =
    "/home/matias/proyecto/TwoPionAnalysis/Data/AnalysisNote/Systematic/";

const int UseCutOff = 1; // Select 1 Use the Cutoff and the interpolation
                         // Select 2 Use the Cutoff
                         // Select 3 Dont use any processing
// Number of  bins
#define N_Q2 3
#define N_Nu 3

// #define N_Zh 8
#define N_Zh 8

// Bin of Zh to take in count in the integration
const int ZH_SUM = 1;

// const int N_Pt2 = 110
// #define N_Pt2 90
#define N_Pt2 60
float Pt2_BINS[N_Pt2 + 1];
#define N_Phi 12
float Phi_BINS[N_Phi + 1];

const float Delta_Pt2 = 3.0 / N_Pt2;
const float Delta_Phi = 360.0 / N_Phi;

// Number of solids targets and max number of pion
const int N_PION = 2;
const int N_STARGETS = 3;

// Limits
const float Q2_MIN = 1.0;
const float Q2_MAX = 4.0;
const float Nu_MIN = 2.2;
const float Nu_MAX = 4.26;
const float Zh_MIN = 0.0;
const float Zh_MAX = 1.0;
const float Pt2_MIN = 0.0;
const float Pt2_MAX = 3.0;
const float Phi_MIN = -180;
const float Phi_MAX = 180;

// B I N N I N G
const float Q2_BINS[N_Q2 + 1] = {1, 1.32, 1.74, 4.0};
const float Nu_BINS[N_Nu + 1] = {2.2, 3.36, 3.82, 4.26};
const float Zh_BINS[N_Zh + 1] = {0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0};
// const float Phi_BINS[N_Phi+1] = {-180, -120, -60, 0, 60, 120, 180};
// const float Phi_BINS[N_Phi+1] = {-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150,
// 180}; const float Phi_BINS[N_Phi+1] = {-180, -140, -100, -60, -20, 20, 60, 100, 140, 180};
// const float Phi_BINS[N_Phi+1] = {-180, -140, -100, -60, -20, 20, 60, 100, 140, 180};

// 90 bins Pt2
// const float Pt2_BINS[N_Pt2+1] = {0, 0.0333333, 0.0666667, 0.1, 0.133333, 0.166667, 0.2,
// 0.233333, 0.266667, 0.3, 0.333333, 0.366667, 0.4, 0.433333, 0.466667, 0.5,
// 0.533333, 0.566667, 0.6, 0.633333, 0.666667, 0.7, 0.733333,
// 0.766667, 0.8, 0.833333, 0.866667, 0.9, 0.933333, 0.966667, 1,
// 1.03333, 1.06667, 1.1, 1.13333, 1.16667, 1.2, 1.23333, 1.26667,
// 1.3, 1.33333, 1.36667, 1.4, 1.43333, 1.46667, 1.5, 1.53333,
// 1.56667, 1.6, 1.63333, 1.66667, 1.7, 1.73333, 1.76667, 1.8,
// 1.83333, 1.86667, 1.9, 1.93333, 1.96667, 2, 2.03333, 2.06667, 2.1,
// 2.13333, 2.16667, 2.2, 2.23333, 2.26667, 2.3, 2.33333, 2.36667,
// 2.4, 2.43333, 2.46667, 2.5, 2.53333, 2.56667, 2.6, 2.63333,
// 2.66667, 2.7, 2.73333, 2.76667, 2.8, 2.83333, 2.86667, 2.9,
// 2.93333, 2.96667, 3};

// 70 bins Pt2
// const float Pt2_BINS[N_Pt2+1] = {0, 0.0428571, 0.0857143, 0.128571, 0.171429, 0.214286,
// 0.257143, 0.3, 0.342857, 0.385714, 0.428571, 0.471429, 0.514286,
// 0.557143, 0.6, 0.642857, 0.685714, 0.728571, 0.771429, 0.814286,
// 0.857143, 0.9, 0.942857, 0.985714, 1.02857, 1.07143, 1.11429,
// 1.15714, 1.2, 1.24286, 1.28571, 1.32857, 1.37143, 1.41429,
// 1.45714, 1.5, 1.54286, 1.58571, 1.62857, 1.67143, 1.71429,
// 1.75714, 1.8, 1.84286, 1.88571, 1.92857, 1.97143, 2.01429,
// 2.05714, 2.1, 2.14286, 2.18571, 2.22857, 2.27143, 2.31429,
// 2.35714, 2.4, 2.44286, 2.48571, 2.52857, 2.57143, 2.61429,
// 2.65714, 2.7, 2.74286, 2.78571, 2.82857, 2.87143, 2.91429,
// 2.95714, 3};

char DC[3] = {'D', 'C', '\0'};
char DFe[4] = {'D', 'F', 'e', '\0'};
char DPb[4] = {'D', 'P', 'b', '\0'};
char C[2] = {'C', '\0'};
char Fe[3] = {'F', 'e', '\0'};
char Pb[3] = {'P', 'b', '\0'};

char cQ2[3] = {'Q', '2', '\0'};
char cNu[3] = {'N', 'u', '\0'};
char cZh[3] = {'Z', 'h', '\0'};
