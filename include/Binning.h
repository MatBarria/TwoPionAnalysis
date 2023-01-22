#include "TString.h"

const TString dataDirectory  = "/home/matias/proyecto/Pt2Broadening_multi-pion/Data/";
const TString inputDirectory  = "/home/matias/proyecto/TwoPionAnalysis/Data/Acc2/";
const TString outputDirectory = "/home/matias/proyecto/TwoPionAnalysis/Data/Acc2/";
//const TString inputDirectory  = "/home/matias/proyecto/TwoPionAnalysis/Data/ME/";
//const TString outputDirectory = "/home/matias/proyecto/TwoPionAnalysis/Data/ME/";

const int UseCutOff = 1; // Select 1 Use the Cutoff and the interpolation
            			// Select 2 Use the Cutoff 
			            // Select 3 Dont use any processing 
                        //
// Number of  bins
const int N_Q2 = 3;
const int N_Nu = 3;
const int N_Zh = 8;
const int N_Pt2 = 90;
const int N_Phi = 6;

// Bin of Zh to take in count in the integration
const int ZH_SUM = 1;

const float Delta_PT2 = 3.0/N_Pt2;
const float Delta_Phi = 360.0/N_Phi;

// Number of solids targets an qd max number of pion
//const int N_PION = 3;
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

// Stlip one pion events equaly
//const float Q2_BINS[N_Q2+1] = {1, 1.3, 1.8, 4.0};	
//const float Nu_BINS[N_Nu+1] = {2.2, 3.2, 3.7, 4.26};

// Stlip Two pion events equaly
const float Q2_BINS[N_Q2+1] = {1, 1.32, 1.74, 4.0};	
const float Nu_BINS[N_Nu+1] = {2.2, 3.36, 3.82, 4.26};


// Stlip Three pion events equaly
//const float Q2_BINS[N_Q2+1] = {1, 1.29, 1.68, 4.0};
//const float Nu_BINS[N_Nu+1] = {2.2, 3.59, 3.96, 4.26};

const float Zh_BINS[N_Zh+1] = {0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 , 0.8 , 1.0};

//const float Phi_BINS[N_Phi+1] = {-180, -90, 0, 90, 180};
const float Phi_BINS[N_Phi+1] = {-180, -120, -60, 0, 60, 120, 180};
//const float Phi_BINS[N_Phi+1] = {-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180};


// 60 bins Pt2
//const float Pt2_BINS[N_Pt2+1] = {0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
				 //0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1, 1.05,
				 //1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6,
				 //1.65, 1.7, 1.75, 1.8, 1.85, 1.9, 1.95, 2, 2.05, 2.1, 2.15,
				 //2.2, 2.25, 2.3, 2.35, 2.4, 2.45, 2.5, 2.55, 2.6, 2.65, 2.7,
				 //2.75, 2.8, 2.85, 2.9, 2.95, 3};
 //90 bins Pt2
const float Pt2_BINS[N_Pt2+1] = {0, 0.0333333, 0.0666667, 0.1, 0.133333, 0.166667, 0.2, 
                 0.233333, 0.266667, 0.3, 0.333333, 0.366667, 0.4, 0.433333, 0.466667, 0.5, 
				 0.533333, 0.566667, 0.6, 0.633333, 0.666667, 0.7, 0.733333, 
				 0.766667, 0.8, 0.833333, 0.866667, 0.9, 0.933333, 0.966667, 1, 
				 1.03333, 1.06667, 1.1, 1.13333, 1.16667, 1.2, 1.23333, 1.26667,
				 1.3, 1.33333, 1.36667, 1.4, 1.43333, 1.46667, 1.5, 1.53333, 
				 1.56667, 1.6, 1.63333, 1.66667, 1.7, 1.73333, 1.76667, 1.8, 
				 1.83333, 1.86667, 1.9, 1.93333, 1.96667, 2, 2.03333, 2.06667, 2.1,
				 2.13333, 2.16667, 2.2, 2.23333, 2.26667, 2.3, 2.33333, 2.36667, 
				 2.4, 2.43333, 2.46667, 2.5, 2.53333, 2.56667, 2.6, 2.63333, 
				 2.66667, 2.7, 2.73333, 2.76667, 2.8, 2.83333, 2.86667, 2.9,
				 2.93333, 2.96667, 3};

// 110 bins Pt2
// const float Pt2_BINS[N_Pt2+1] = {0, 0.0272727, 0.0545455, 0.0818182, 0.109091, 0.136364, 
//                  0.163636, 0.190909, 0.218182, 0.245455, 0.272727, 0.3, 0.327273, 0.354545, 
// 				    0.381818, 0.409091, 0.436364, 0.463636, 0.490909, 0.518182,
// 				    0.545455, 0.572727, 0.6, 0.627273, 0.654545, 0.681818, 0.709091, 
// 				    0.736364, 0.763636, 0.790909, 0.818182, 0.845455, 0.872727,
//                  0.9, 0.927273, 0.954545, 0.981818, 1.00909, 1.03636, 1.06364, 
//                  1.09091, 1.11818, 1.14545, 1.17273, 1.2, 1.22727, 1.25455,
//                  1.28182, 1.30909, 1.33636, 1.36364, 1.39091, 1.41818, 1.44545,
//                  1.47273, 1.5, 1.52727, 1.55455, 1.58182, 1.60909, 1.63636, 
//                  1.66364, 1.69091, 1.71818, 1.74545, 1.77273, 1.8, 1.82727, 
//                  1.85455, 1.88182, 1.90909, 1.93636, 1.96364, 1.99091, 2.01818, 
//                  2.04545, 2.07273, 2.1, 2.12727, 2.15455, 2.18182, 2.20909, 
//                  2.23636, 2.26364, 2.29091, 2.31818, 2.34545, 2.37273, 2.4, 
//                  2.42727, 2.45455, 2.48182, 2.50909, 2.53636, 2.56364, 2.59091,
//                  2.61818, 2.64545, 2.67273, 2.7, 2.72727, 2.75455, 2.78182, 
//                  2.80909, 2.83636, 2.86364, 2.89091, 2.91818, 2.94545, 2.97273,
//                                  3};



const char* Targets[2*N_STARGETS] = {"C","Fe","Pb","DC","DFe","DPb"};
const char* SolTargets[N_STARGETS] = {"C","Fe","Pb"};
const char* LiqTargets[N_STARGETS] = {"DC","DFe","DPb"};


char DC[3] = {'D', 'C', '\0' }; char DFe[4] = {'D', 'F', 'e', '\0'}; 
char DPb[4] = {'D', 'P', 'b', '\0'}; char C[2]  = {'C', '\0'}; 
char Fe[3]  = {'F', 'e', '\0'}; char Pb[3]  = {'P', 'b', '\0'};
