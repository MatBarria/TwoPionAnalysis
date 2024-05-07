import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import uproot as ur
import os

from include import dataDirectory, outputDirectory, binning

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

nPion = 2

tarList = ['C', "Fe", "Pb", 'DC', "DFe", "DPb"]
colorList = ['#301437', 'orange', "lightgreen"]
nPionList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]

nBins = 60

binningDist = {'Q2':     np.linspace(1.,    4.,   nBins),
               'Nu':     np.linspace(2.2,   4.26, nBins),
               'Zh':     np.linspace(0.,    1.,   nBins),
               'Pt2':    np.linspace(0.,    3.,   nBins),
               'PhiPQ':  np.linspace(-180., 180., nBins),
               }

xLabel = {"Q2":    r'$Q^2$[GeV^2]',
          "Nu":    r'$\nu$[GeV]',
          "Zh":    r'$Zh_\mathrm{Sum}$',
          # "Pt2":   r'$P_t^2 [GeV^2]$',
          "Pt2":   r'$P_t^{+2} [GeV^2]$',
          "PhiPQ": r'$\phi_{PQ}[Deg]$'
          }

yLabel = {"Q2":    r'$dN/dQ^2$',
          "Nu":    r'$dN/d\nu$',
          "Zh":    r'$dN/dZh_\mathrm{Sum}$',
          # "Pt2":   r'$dN/dP_t^2$',
          "Pt2":   r'$dN/dP_t^{+2}$',
          "PhiPQ": r'$dN/d\phi_{PQ}$'
          }

dicColor = {"Data": "#301437",
            "Gen":  "orange",
            "Rec":  "lightgreen"
            }

dicLabel = {"Data": ["Data", "Data: Two $\pi^+", "Data"],
            "Gen": ["Gen",  "Gen: Two $\pi^+", "Data"],
            "Rec": ["Rec",  "Rec: Two $\pi^+", "Data"]
            }

lineStyle = ["-", "-", "-"]

xLowLimit = {"Q2": 0.8, "Nu": 2.1, "Zh": 0., "Pt2": 0,  "PhiPQ": -180}
xHighLimit = {"Q2": 4, "Nu": 4.32, "Zh": 1.05, "Pt2": 3.0, "PhiPQ": 180}
yLimit = {"Q2": 0.01, "Nu": 0.01, "Zh": 0.01, "Pt2": 0.01, "PhiPQ": 0.01}

variables = ["Q2", "Nu", "Zh", "Pt2", "PhiPQ"]
# variables = ["Pt2", "PhiPQ"]
# variables = ["Nu"]


def SimVsData(var):

    fig, axs = plt.subplots(2, nPion, sharey='row', sharex='col')
    width = 16*(nPion/3)  # 7.056870070568701
    height = 8
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.02, hspace=0.3)

    outDir = outputDirectory + "SimVsData/"
    # Create the directory if doesn't exist
    os.makedirs(outDir, exist_ok=True)
    # dic = {"Data" : np.array([]), "ZhBin" : np.array([])}
    for j in range(nPion):  # Loops on the number of pions

        varGen = var + "_gen"
        varRec = var + "_rec"
        axs[0][j].set_xlim(xLowLimit[var], xHighLimit[var])
        axs[1][j].set_xlim(xLowLimit[var], xHighLimit[var])

        with ur.open(dataDirectory + "VecSum_Pb.root:ntuple_" +
                     str(j+1) + "_pion") as file:
            dicData = file.arrays([var, "VC_TM"], library="np")

        with ur.open(dataDirectory + "SimulTuple_Pb.root:ntuple_sim_gen") as file:
            dicGen = file.arrays([varGen, "Gen"], library="np")

        with ur.open(dataDirectory + "SimulTuple_Pb.root:ntuple_sim_rec") as file:
            dicRec = file.arrays([varRec, "Rec"], library="np")

        dicData[var] = dicData[var][dicData["VC_TM"] == 2]
        dicGen[varGen] = dicGen[varGen][dicGen["Gen"] == j+1]
        dicRec[varRec] = dicRec[varRec][dicRec["Rec"] == j+1]

        weightsData = np.ones_like(dicData[var]) / float(len(dicData[var]))
        weightsGen = np.ones_like(dicGen[varGen]) / float(len(dicGen[varGen]))
        weightsRec = np.ones_like(dicRec[varRec]) / float(len(dicRec[varRec]))

        axs[1][j].hist(dicData[var], bins=binningDist[var], weights=weightsData,
                       color=dicColor["Data"], histtype="step", label=dicLabel['Data'][j],
                       linestyle=lineStyle[j])
        axs[1][j].hist(dicGen[varGen], bins=binningDist[var], weights=weightsGen,
                       color=dicColor["Gen"], histtype="step", label=dicLabel['Gen'][j],
                       linestyle=lineStyle[j])
        axs[1][j].hist(dicRec[varRec], bins=binningDist[var], weights=weightsRec,
                       color=dicColor["Rec"], histtype="step", label=dicLabel['Rec'][j],
                       linestyle=lineStyle[j])

        with ur.open(dataDirectory + "VecSum_Pb.root:ntuple_" +
                     str(j+1) + "_pion") as file:
            dicData = file.arrays([var, "VC_TM"], library="np")

        with ur.open(dataDirectory + "SimulTuple_D.root:ntuple_sim_gen") as file:
            dicGen = file.arrays([varGen, "Gen"], library="np")

        with ur.open(dataDirectory + "SimulTuple_D.root:ntuple_sim_rec") as file:
            dicRec = file.arrays([varRec, "Rec"], library="np")

        dicData[var] = dicData[var][dicData["VC_TM"] == 1]
        dicGen[varGen] = dicGen[varGen][dicGen["Gen"] == j+1]
        dicRec[varRec] = dicRec[varRec][dicRec["Rec"] == j+1]

        weightsData = np.ones_like(dicData[var]) / float(len(dicData[var]))
        weightsGen = np.ones_like(dicGen[varGen]) / float(len(dicGen[varGen]))
        weightsRec = np.ones_like(dicRec[varRec]) / float(len(dicRec[varRec]))

        axs[0][j].hist(dicData[var], bins=binningDist[var], weights=weightsData,
                       color=dicColor["Data"], histtype="step", label=dicLabel['Data'][j],
                       linestyle=lineStyle[j])
        axs[0][j].hist(dicGen[varGen], bins=binningDist[var], weights=weightsGen,
                       color=dicColor["Gen"], histtype="step", label=dicLabel['Gen'][j],
                       linestyle=lineStyle[j])
        axs[0][j].hist(dicRec[varRec], bins=binningDist[var], weights=weightsRec,
                       color=dicColor["Rec"], histtype="step", label=dicLabel['Rec'][j],
                       linestyle=lineStyle[j])

        if var == "Pt2":
            axs[0][j].set_yscale('log')
            axs[1][j].set_yscale('log')
            axs[0][j].set_ylim(0.0000001, 1)
            axs[1][j].set_ylim(0.0000001, 1)

        axs[0][j].tick_params(right=False, top=False, which='both')
        axs[1][j].tick_params(right=False, top=False, which='both')

        axs[0][j].set_xlabel(xLabel[var], fontsize=14)
        axs[1][j].set_xlabel(xLabel[var], fontsize=14)

        axs[0][0].set_ylabel(yLabel[var], loc="center", fontsize=15)
        axs[1][0].set_ylabel(yLabel[var], loc="center", fontsize=15)

    axs[1][0].annotate(r'Solid Targets - ' + nPionList[0], xy=(0.5, 1.04),
                       xycoords='axes fraction', fontsize=15)
    axs[1][1].annotate(r'Solid Targets - ' + nPionList[1], xy=(0.5, 1.04),
                       xycoords='axes fraction', fontsize=15)

    axs[0][0].annotate(r'Liquid Target - ' + nPionList[0], xy=(0.5, 1.04),
                       xycoords='axes fraction', fontsize=15)
    axs[0][1].annotate(r'Liquid Target - ' + nPionList[1], xy=(0.5, 1.04),
                       xycoords='axes fraction', fontsize=15)

    axs[0][0].legend(frameon=False, loc='best', fontsize=11)

    fig.savefig(outDir + "SimVsData_" +
                var + ".pdf", bbox_inches='tight')
    fig.savefig(outDir + "SimVsData_" +
                var + ".png", bbox_inches='tight', dpi=300)
    print(outputDirectory + "SimVsData_" + var + ".pdf Has been created")


def SimVsDataPt2Zh(ZhBin, var="Pt2"):

    fig, axs = plt.subplots(2, nPion, sharey='row', sharex='col')
    width = 16*(nPion/3)  # 7.056870070568701
    height = 8
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.02, hspace=0.3)

    # dic = {"Data" : np.array([]), "ZhBin" : np.array([])}
    for j in range(nPion):  # Loops on the number of pions

        varGen = var + "_gen"
        varRec = var + "_rec"

        axs[0][j].set_xlim(xLowLimit[var], xHighLimit[var])
        axs[1][j].set_xlim(xLowLimit[var], xHighLimit[var])

        with ur.open(dataDirectory + "VecSum_Pb.root:ntuple_" +
                     str(j+1) + "_pion") as file:
            dicData = file.arrays([var, "VC_TM", "Zh"], library="np")

        with ur.open(dataDirectory + "SimulTuple_Pb.root:ntuple_sim_gen") as file:
            dicGen = file.arrays([varGen, "Gen", "Zh_gen"], library="np")

        with ur.open(dataDirectory + "SimulTuple_Pb.root:ntuple_sim_rec") as file:
            dicRec = file.arrays([varRec, "Rec", "Zh_rec"], library="np")

        dicData[var] = dicData[var][dicData["VC_TM"] == 2]
        dicGen[varGen] = dicGen[varGen][dicGen["Gen"] == j+1]
        dicRec[varRec] = dicRec[varRec][dicRec["Rec"] == j+1]
        dicData["Zh"] = dicData["Zh"][dicData["VC_TM"] == 2]
        dicGen["Zh_gen"] = dicGen["Zh_gen"][dicGen["Gen"] == j+1]
        dicRec["Zh_rec"] = dicRec["Zh_rec"][dicRec["Rec"] == j+1]

        dicData[var] = dicData[var][dicData["Zh"] < binning["Zh"][ZhBin+1]]
        dicGen[varGen] = dicGen[varGen][dicGen["Zh_gen"]
                                        < binning["Zh"][ZhBin+1]]
        dicRec[varRec] = dicRec[varRec][dicRec["Zh_rec"]
                                        < binning["Zh"][ZhBin+1]]

        dicData["Zh"] = dicData["Zh"][dicData["Zh"] < binning["Zh"][ZhBin+1]]
        dicGen["Zh_gen"] = dicGen["Zh_gen"][dicGen["Zh_gen"]
                                            < binning["Zh"][ZhBin+1]]
        dicRec["Zh_rec"] = dicRec["Zh_rec"][dicRec["Zh_rec"]
                                            < binning["Zh"][ZhBin+1]]

        dicData[var] = dicData[var][dicData["Zh"] > binning["Zh"][ZhBin]]
        dicGen[varGen] = dicGen[varGen][dicGen["Zh_gen"] > binning["Zh"][ZhBin]]
        dicRec[varRec] = dicRec[varRec][dicRec["Zh_rec"] > binning["Zh"][ZhBin]]

        dicData["Zh"] = dicData["Zh"][dicData["Zh"] > binning["Zh"][ZhBin]]
        dicGen["Zh_gen"] = dicGen["Zh_gen"][dicGen["Zh_gen"]
                                            > binning["Zh"][ZhBin]]
        dicRec["Zh_rec"] = dicRec["Zh_rec"][dicRec["Zh_rec"]
                                            > binning["Zh"][ZhBin]]

        weightsData = np.ones_like(dicData[var]) / float(len(dicData[var]))
        weightsGen = np.ones_like(dicGen[varGen]) / float(len(dicGen[varGen]))
        weightsRec = np.ones_like(dicRec[varRec]) / float(len(dicRec[varRec]))

        weightsData = np.ones_like(dicData[var])
        weightsGen = np.ones_like(dicGen[varGen])
        weightsRec = np.ones_like(dicRec[varRec])
        axs[1][j].hist(dicData[var], bins=binning[var], weights=weightsData,
                       color=dicColor["Data"], histtype="step", label=dicLabel['Data'][j],
                       linestyle=lineStyle[j])
        axs[1][j].hist(dicGen[varGen], bins=binning[var], weights=weightsGen,
                       color=dicColor["Gen"], histtype="step", label=dicLabel['Gen'][j],
                       linestyle=lineStyle[j])
        axs[1][j].hist(dicRec[varRec], bins=binning[var], weights=weightsRec,
                       color=dicColor["Rec"], histtype="step", label=dicLabel['Rec'][j],
                       linestyle=lineStyle[j])

        with ur.open(dataDirectory + "VecSum_Pb.root:ntuple_" +
                     str(j+1) + "_pion") as file:
            dicData = file.arrays([var, "VC_TM", "Zh"], library="np")

        with ur.open(dataDirectory + "SimulTuple_D.root:ntuple_sim_gen") as file:
            dicGen = file.arrays([varGen, "Gen", "Zh_gen"], library="np")

        with ur.open(dataDirectory + "SimulTuple_D.root:ntuple_sim_rec") as file:
            dicRec = file.arrays([varRec, "Rec", "Zh_rec"], library="np")

        dicData[var] = dicData[var][dicData["VC_TM"] == 1]
        dicGen[varGen] = dicGen[varGen][dicGen["Gen"] == j+1]
        dicRec[varRec] = dicRec[varRec][dicRec["Rec"] == j+1]
        dicData["Zh"] = dicData["Zh"][dicData["VC_TM"] == 1]
        dicGen["Zh_gen"] = dicGen["Zh_gen"][dicGen["Gen"] == j+1]
        dicRec["Zh_rec"] = dicRec["Zh_rec"][dicRec["Rec"] == j+1]

        dicData[var] = dicData[var][dicData["Zh"] < binning["Zh"][ZhBin+1]]
        dicGen[varGen] = dicGen[varGen][dicGen["Zh_gen"]
                                        < binning["Zh"][ZhBin+1]]
        dicRec[varRec] = dicRec[varRec][dicRec["Zh_rec"]
                                        < binning["Zh"][ZhBin+1]]

        dicData["Zh"] = dicData["Zh"][dicData["Zh"] < binning["Zh"][ZhBin+1]]
        dicGen["Zh_gen"] = dicGen["Zh_gen"][dicGen["Zh_gen"]
                                            < binning["Zh"][ZhBin+1]]
        dicRec["Zh_rec"] = dicRec["Zh_rec"][dicRec["Zh_rec"]
                                            < binning["Zh"][ZhBin+1]]

        dicData[var] = dicData[var][dicData["Zh"] > binning["Zh"][ZhBin]]
        dicGen[varGen] = dicGen[varGen][dicGen["Zh_gen"] > binning["Zh"][ZhBin]]
        dicRec[varRec] = dicRec[varRec][dicRec["Zh_rec"] > binning["Zh"][ZhBin]]

        weightsData = np.ones_like(dicData[var]) / float(len(dicData[var]))
        weightsGen = np.ones_like(dicGen[varGen]) / float(len(dicGen[varGen]))
        weightsRec = np.ones_like(dicRec[varRec]) / float(len(dicRec[varRec]))

        weightsData = np.ones_like(dicData[var])
        weightsGen = np.ones_like(dicGen[varGen])
        weightsRec = np.ones_like(dicRec[varRec])

        axs[0][j].hist(dicData[var], bins=binning[var], weights=weightsData,
                       color=dicColor["Data"], histtype="step", label=dicLabel['Data'][j],
                       linestyle=lineStyle[j])
        axs[0][j].hist(dicGen[varGen], bins=binning[var], weights=weightsGen,
                       color=dicColor["Gen"], histtype="step", label=dicLabel['Gen'][j],
                       linestyle=lineStyle[j])
        axs[0][j].hist(dicRec[varRec], bins=binning[var], weights=weightsRec,
                       color=dicColor["Rec"], histtype="step", label=dicLabel['Rec'][j],
                       linestyle=lineStyle[j])

        if var == "Pt2":
            axs[0][j].set_yscale('log')
            axs[1][j].set_yscale('log')
            # axs[0][j].set_ylim(0.0000001, 1)
            # axs[1][j].set_ylim(0.0000001, 1)

        axs[0][j].tick_params(right=False, top=False, which='both')
        axs[1][j].tick_params(right=False, top=False, which='both')

        axs[0][j].set_xlabel(xLabel[var], fontsize=14)
        axs[1][j].set_xlabel(xLabel[var], fontsize=14)

        axs[0][0].set_ylabel(yLabel[var], loc="center", fontsize=15)
        axs[1][0].set_ylabel(yLabel[var], loc="center", fontsize=15)

    axs[1][0].annotate(r'Solid Targets - ' + nPionList[0], xy=(0.5, 1.04),
                       xycoords='axes fraction', fontsize=15)
    axs[1][1].annotate(r'Solid Targets - ' + nPionList[1], xy=(0.5, 1.04),
                       xycoords='axes fraction', fontsize=15)

    axs[0][0].annotate(r'Liquid Target - ' + nPionList[0], xy=(0.5, 1.04),
                       xycoords='axes fraction', fontsize=15)
    axs[0][1].annotate(r'Liquid Target - ' + nPionList[1], xy=(0.5, 1.04),
                       xycoords='axes fraction', fontsize=15)

    axs[0][0].legend(frameon=False, loc='best', fontsize=11)

    fig.savefig(outputDirectory + "SimVsData_" + var + "Zh" +
                str(ZhBin) + ".pdf", bbox_inches='tight')
    print(outputDirectory + "SimVsData_" + var +
          "Zh" + str(ZhBin) + " Has been created")


for var in variables:
    SimVsData(var)

# SimVsDataPt2Zh(7)
