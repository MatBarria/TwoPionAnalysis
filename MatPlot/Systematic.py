import ROOT
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import optparse
from include import inputDirectory, outputDirectory, systematicDirectory, SaveFigure

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

parser = optparse.OptionParser("usage: %prog [options]\n")
parser.add_option('-y', '--ylength', dest='ylength',
                  default=30, help="Y axis range [0, y]")
parser.add_option('-l', '--logScale', dest='logScale',
                  default=False, help="Use Log Scale")

options, args = parser.parse_args()
# Upper limmit in the y axis
logScale = options.logScale
YLimit = float(options.ylength)

drawStatError = True

nPion = 2
N_Zh = 7


ZhBinning = [0.075, 0.2, 0.3, 0.4, 0.5, 0.6, 0.84, 1.03]

dic_label_sys = {"DZLow": "$\Delta Z < 2.5$ cm",
                 "DZHigh": "$\Delta Z < 3.5$ cm",
                 "50Bins": "50 $Pt^2$ bins",
                 "70Bins": "70 $Pt^2$ bins",
                 "VC_RD": "Vertex Cut RD",
                 "VC_HH": "Vertex Cut HH",
                 "Normal": "Cut off applied",
                 "Cutoff": "No background subtraction",
                 "TOFLow": "TOF Cut P < 2.5 GeV",
                 "TOFHigh": "TOF Cut P < 2.9 GeV",
                 "LimitLow": "Acc > 0.017",
                 "LimitHigh": "Acc > 0.020",
                 "NAccept0": "$N_{a=t}^i$ $\geq$ 0",
                 "NAccept2": "$N_{a=t}^i$ $\geq$ 2",
                 "NAcceptRec": "N Accept Rec $\geq$ 2",
                 "CT": "Clousure Test",
                 "4DAcc": "4D-Acc",
                 "RC": "Radiative Corrections",
                 "RCInter": "RC Interpolated",
                 "AccInter": "Acc Interpolated",
                 }

dicPlotName = {"DZLow": "DZ_Cut",
               "DZHigh": "DZ_Cut",
               "50Bins": "Bins_Variation",
               "70Bins": "Bins_Variation",
               "VC_RD": "Vertex_Cut",
               "VC_HH": "Vertex_Cut",
               "Normal": "BG_Subtraction",
               "Cutoff": "BG_Subtraction",
               "TOFHigh": "TOF_Cut",
               "TOFLow": "TOF_Cut",
               "LimitHigh": "AccLimit",
               "LimitLow": "AccLimit",
               "NAccept0": "N_Accept",
               "NAccept2": "N_Accept",
               "NAcceptRec": "N_Accept",
               "CT": "CT",
               "4DAcc": "4D-Acc",
               "RC": "RC",
               "RCInter": "RC",
               "AccInter": "AccInter",
               }

tarList = ["C", "Fe", "Pb"]
colorListSys = ["darkred", "darkBlue", "black"]
colorListNom = ["red", "Blue", "black"]
markerList = ["^", "v"]
labelListNom = ["Sta. Error One $\pi^+$",
                "Sta. Error Two $\pi^+$", "Sta. Error Three $\pi^+$"]
nPionList = ["One $\pi^+$", "Two $\pi^+$", "Three $\pi^+$"]


def SystematicError(systematic):

    fig, axs = plt.subplots(nPion, 3, sharey='row', sharex='col')
    width = 16  # 7.056870070568701
    height = 4*nPion
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.02,
                        hspace=0.3)

    # fileSystematicdd = ROOT.TFile.Open(inputDirectory + "Percentaje.root", "READ")
    fileSystematic = [ROOT.TFile.Open(systematicDirectory + systematic[0] + "/Pt_broad_Zh.root",
                                      "READ"),
                      ROOT.TFile.Open(systematicDirectory + systematic[1] + "/Pt_broad_Zh.root",
                                      "READ")]
    fileNominal = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")

    print(systematicDirectory + systematic[1] + "/Pt_broad_Zh.root")
    for i in range(3):  # Loops on the diffrent targets
        axs[1][i].set_xticks([.1, .3, .5, .7])
        # axs[1][i].set_xticklabels([.1, .3, .5, .7])
        for j in range(0, nPion):  # Loops on the number of pions

            axs[j][i].set_ylim(0., YLimit)
            axs[j][i].set_xlim(0.1, .79999)
            # axs[j][i].set_ylim(0, 21)
            # axs[j][i].set_xlim(0.2, 0.8)
            graphNameNom = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
            graphNom = fileNominal.Get(graphNameNom)

            NSys = 2
            if systematic[0] == systematic[1]:
                NSys = 1

            for s in range(NSys):

                graphNameSys = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
                graphSys = fileSystematic[s].Get(graphNameSys)

                # Extrac the data from the TGraph
                nPointsSys = graphSys.GetN()
                xSys = np.ndarray(nPointsSys, dtype=float,
                                  buffer=graphSys.GetX())
                ySys = np.ndarray(nPointsSys, dtype=float,
                                  buffer=graphSys.GetY())
                nPointsNom = graphNom.GetN()
                y = np.ndarray(nPointsNom, dtype=float, buffer=graphNom.GetY())
                ey = np.ndarray(nPointsNom, dtype=float,
                                buffer=graphNom.GetEY())

                print("Target: " + tarList[i] + " ;N pions: " + str(j+1) +
                      " ;Sys: " + systematic[s])
                ySys = np.absolute((y-ySys)/y)*100
                print(ySys)

                # Generate the plot
                axs[j][i].plot(xSys, ySys, marker=markerList[s], linestyle="",
                               color=colorListSys[j], markerfacecolor=colorListSys[j],
                               markersize=6, label=dic_label_sys[systematic[s]])

                # Extrac the data from the TGraph
            if drawStatError:
                NomError = [0, 0, 0, 0, 0, 0, 0, 0]

                NomError[0] = (ey[1]*100)/y[1]
                NomError[N_Zh-1] = (ey[N_Zh-1]*100)/y[N_Zh-1]
                for k in range(N_Zh-1):
                    NomError[k+1] = (ey[k+1]*100)/y[k+1]

                axs[j][i].fill_between(ZhBinning, NomError, step='pre',
                                       color=colorListNom[j], label=labelListNom[j],
                                       linewidth=1.0, alpha=0.3)
                axs[j][i].step(ZhBinning, NomError,
                               color=colorListNom[j], linewidth=1.0)

            if logScale:
                axs[j][i].set_yscale('log')
                axs[j][i].set_ylim(1., YLimit)
    # Set the labels for the three plots

    fileNominal.Close()
    fileSystematic[0].Close()
    fileSystematic[1].Close()

    for i in range(nPion):
        axs[i][0].set_ylabel(r'Deviation from Nominal(%)',
                             loc="center", fontsize=15)
        axs[i][0].set_xlabel(r'$Z^{+}_h$', fontsize=14)
        axs[i][1].set_xlabel(r'$Z^{+}_h$', fontsize=14)
        axs[i][2].set_xlabel(r'$Z^{+}_h$', fontsize=14)

        axs[i][0].annotate(r'Carbon - ' + nPionList[i], xy=(0.04, 1.04),
                           xycoords='axes fraction', fontsize=15)
        axs[i][1].annotate(r'Iron - ' + nPionList[i], xy=(0.04, 1.04),
                           xycoords='axes fraction', fontsize=15)
        axs[i][2].annotate(r'Lead - ' + nPionList[i],   xy=(0.04, 1.04),
                           xycoords='axes fraction', fontsize=15)

        axs[i][0].legend(frameon=False, loc='upper center', fontsize=11)

    fig.align_ylabels(axs[:])

    for i in range(3):
        for j in range(nPion):
            axs[j][i].grid(visible=None, axis='both', color='0.95')
            axs[j][i].set_axisbelow(True)

    SaveFigure(fig, outputDirectory + "Systematic/",
               dicPlotName[systematic[0]])


SystematicError(["TOFLow", "TOFHigh"])
SystematicError(["VC_RD",  "VC_HH"])
SystematicError(["DZLow",  "DZHigh"])
SystematicError(["Normal", "Cutoff"])
SystematicError(["50Bins", "70Bins"])
SystematicError(["NAccept0", "NAccept2"])
SystematicError(["LimitHigh", "LimitLow"])
SystematicError(["CT", "CT"])
SystematicError(["AccInter", "AccInter"])
SystematicError(["RC", "RCInter"])
