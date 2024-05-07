import ROOT
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import mplhep as hep
from include import inputDirectory, outputDirectory, systematicDirectory, binning, SaveFigure, AddCLasPleliminary

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

nPion = 2

yLimit = {"Q2": 0.042, "Nu": 0.042, "Zh": 0.17}

xLowLimit = {"Q2": 0.8, "Nu": 2.2, "Zh": 0.075}
xHighLimit = {"Q2": 4, "Nu": 4.22, "Zh": 0.83}

NBins = {"Q2": 3, "Nu": 3, "Zh": 8, "FullIntegrated": 1}

xLabel = {"Q2": r'$Q^2$[GeV^2]', "Nu": r'$\nu$[GeV]', "Zh": r'$Z^{+}_h$'}

xShiftNPion = {"Q2": 0.02, "Nu": 0.02, "Zh": 0.0075}
xShiftTarget = {"Q2": 0., "Nu": 0., "Zh": 0.0075}


tarList = ["C", "Fe", "Pb"]
colorList = ["red", "Blue", "black"]
markerList = ["o", "s", "D"]
labelList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]


CLASPreliminaryFlag = True


class Systematics:

    def __init__(self, variable, nBins, ZhCut=False):

        systematics = [["Normal", "Cutoff"], ["50Bins", "70Bins"], ["DZLow",  "DZHigh"],
                       ["VC_RD",  "VC_HH"], ["TOFLow", "TOFHigh"], [
                           "CT", "CT"], ["RC", "RC"],
                       ["LimitLow", "LimitHigh"], ["NAccept0", "NAccept2"], ["AccInter", "AccInter"]]

        self.sysDic = {"C": [np.repeat(0., nBins), np.repeat(0., nBins)],
                       "Fe": [np.repeat(0., nBins), np.repeat(0., nBins)],
                       "Pb": [np.repeat(0., nBins), np.repeat(0., nBins)],
                       }

        self.ZhCut = ZhCut
        self.variable = variable
        fileName = "Pt_broad_" + variable + ".root"

        if ZhCut:
            fileName = "Pt_broad_" + variable + "ZhCut.root"

        for i in range(3):  # Loops on the diffrent targets
            for j in range(nPion):  # Loops on the number of pions

                fileNominal = ROOT.TFile.Open(
                    inputDirectory + fileName, "READ")
                graphName = "PtBroad_" + variable + \
                    "_" + tarList[i] + "_" + str(j)

                if variable == "FullIntegrated":
                    graphName = "PtBroad_" + variable + \
                        "_" + tarList[i] + "_" + str(j+1)

                graphNom = fileNominal.Get(graphName)
                nPoints = graphNom.GetN()
                nomValues = np.ndarray(
                    nPoints, dtype=float, buffer=graphNom.GetY())
                errorValues = np.ndarray(
                    nPoints, dtype=float, buffer=graphNom.GetEY())
                fileNominal.Close()

                sysErrorArray = np.repeat(0., NBins[variable])

                for systematic in systematics:
                    fileSystematic = [ROOT.TFile.Open(systematicDirectory + systematic[0] + '/' +
                                                      fileName, "READ"),
                                      ROOT.TFile.Open(systematicDirectory + systematic[1] + '/' +
                                                      fileName, "READ")]
                    graphSys = [fileSystematic[0].Get(graphName),
                                fileSystematic[1].Get(graphName)]
                    SysValues = [np.ndarray(nPoints, dtype=float, buffer=graphSys[0].GetY()),
                                 np.ndarray(nPoints, dtype=float, buffer=graphSys[1].GetY())]
                    sysErrorArray += np.square(np.maximum(np.absolute(nomValues-SysValues[0]),
                                                          np.absolute(nomValues-SysValues[1])))/3
                    fileSystematic[0].Close()
                    fileSystematic[1].Close()

                sysErrorArray = np.sqrt(sysErrorArray)
                self.sysDic[tarList[i]][j] = sysErrorArray


# Function definition

def PtBroadVarTarSplit(variable):

    fig, axs = plt.subplots(1, 3, sharey='row', sharex='col')
    width = 16  # 7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.02, hspace=0.02)

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_" +
                           variable + ".root", "READ")
    yLimit = 0
    for i in range(3):  # Loops on the diffrent targets

        # axs[i].set_ylim(0, yLimit[variable])
        axs[i].set_xlim(xLowLimit[variable], xHighLimit[variable])
        # axs[i].set_xlim(xLowLimit[variable], 0.8)
        if CLASPreliminaryFlag:
            AddCLasPleliminary(axs[i])

        for j in range(nPion):  # Loops on the number of pions

            # Get info from the TGraph
            graphName = "PtBroad_" + variable + "_" + tarList[i] + "_" + str(j)
            graph = file.Get(graphName)
            nPoints = graph.GetN()

            x = np.ndarray(nPoints, dtype=float, buffer=graph.GetX())
            y = np.ndarray(nPoints, dtype=float, buffer=graph.GetY())
            if variable == "Zh":
                # Shit the data for readability
                x = x + (-xShiftTarget[variable] + xShiftTarget[variable]*2*j)
                # Removing the las bin for the lack of statistics
                y[-1] = 0
            ey = np.ndarray(nPoints, dtype=float, buffer=graph.GetEY())
            # ey = np.zeros_like(ey)
            # print("Var Target: " + tarList[i]+" NPIon: " + str(j + 1))
            # print(y)
            # Plot with stat errors
            axs[i].errorbar(x, y, ey, marker="o", linestyle="",
                            markerfacecolor=colorList[j], color=colorList[j],
                            markersize=5, label=labelList[j])

            # Plot with stat + Sys errors
            axs[i].errorbar(x, y, np.sqrt(ey*ey +
                                          sysDic[variable][tarList[i]][j]*sysDic[variable][tarList[i]][j]),
                            marker="", linestyle="", markerfacecolor=colorList[j], lw=0,
                            color=colorList[j], markersize=0, capsize=5)

            yLimit = max([np.max(y + np.sqrt(ey*ey +
                                             sysDic[variable][tarList[i]][j]*sysDic[variable][tarList[i]][j]))+0.01, yLimit])

        axs[i].set_xlabel(xLabel[variable], fontsize=14)

    # Set the labels for the three plots

    axs[0].set_ylim(0, yLimit)
    axs[0].set_ylabel(
        r'$\Delta P_\mathrm{T}^{2} [GeV^{2}]$', loc="center", fontsize=15)
    axs[0].annotate(r'Carbon', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(r'Iron',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[2].annotate(r'Lead',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)

    axs[0].legend(frameon=False, loc='upper left', fontsize=11)
    axs[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    fig.align_ylabels(axs[:])
    for i in range(3):
        axs[i].grid(visible=None, axis='both', color='0.95')
        axs[i].set_axisbelow(True)

    SaveFigure(fig, outputDirectory + "Results/",
               "PtBroad_" + variable + "_Target")


def PtBroadVarNPionSplit(variable):

    fig, axs = plt.subplots(1, nPion, sharey='row', sharex='col')
    width = (16/3)*nPion
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.02,
                        hspace=0.02)

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_" +
                           variable + ".root", "READ")
    yLimit = 0

    for i in range(3):  # Loops on the diffrent targets
        for j in range(nPion):  # Loops on the number of pions

            if CLASPreliminaryFlag:
                AddCLasPleliminary(axs[j])

            # axs[j].set_ylim(0, yLimit[variable])
            axs[j].set_xlim(xLowLimit[variable], xHighLimit[variable])
            # Get info from the TGraph
            graphName = "PtBroad_" + variable + "_" + tarList[i] + "_" + str(j)
            graph = file.Get(graphName)
            nPoints = graph.GetN()
            x = np.ndarray(nPoints, dtype=float, buffer=graph.GetX())
            x = x + (-2*xShiftNPion[variable] + 2*xShiftNPion[variable]*i)
            y = np.ndarray(nPoints, dtype=float, buffer=graph.GetY())
            ey = np.ndarray(nPoints, dtype=float, buffer=graph.GetEY())

            # print("NPion Target: " + tarList[i] + " N Pion = " + str(j))
            # print(y)
            # Plot with stat errors
            axs[j].errorbar(x, y, ey, marker="o", linestyle="", label=tarList[i],
                            color=colorList[i], markersize=5, markerfacecolor=colorList[i])

            # Plot with stat + sys errors
            axs[j].errorbar(x, y, np.sqrt(ey*ey +
                                          sysDic[variable][tarList[i]][j]*sysDic[variable][tarList[i]][j]),
                            marker="", linestyle="", markerfacecolor=colorList[i], lw=0,
                            color=colorList[i], markersize=0, capsize=5)

            yLimit = max([np.max(y + np.sqrt(ey*ey +
                                             sysDic[variable][tarList[i]][j]*sysDic[variable][tarList[i]][j])), yLimit])

            axs[j].set_xlabel(xLabel[variable], fontsize=14)

    axs[0].set_ylim(0, yLimit + 0.01)
    axs[0].set_ylabel(
        r'$\Delta P_\mathrm{T}^{2} [GeV^{2}]$', loc="center", fontsize=15)

    fig.align_ylabels(axs[:])

    axs[0].annotate(r'One Pion', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(r'Two Pion', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)

    axs[0].legend(frameon=False, loc='upper left', fontsize=11)
    axs[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    for i in range(nPion):
        axs[i].grid(visible=None, axis='both', color='0.95')
        axs[i].set_axisbelow(True)

    file.Close()
    SaveFigure(fig, outputDirectory + "Results/",
               "PtBroad_" + variable + "_NPion")


def PtBroadFullIntegrated(ZhCut=False):

    fig, axs = plt.subplots(1, 1, constrained_layout=True)
    # For one column
    width = 6
    height = width / 1.2
    fig.set_size_inches(width, height)

    inputName = "Pt_broad_FullIntegrated.root"
    outputName = "PtBroad_FullIntegrated"

    if ZhCut:
        inputName = "Pt_broad_FullIntegratedZhCut.root"
        outputName = "PtBroad_FullIntegratedZhCut"

    file = ROOT.TFile.Open(inputDirectory + inputName, "READ")

    if CLASPreliminaryFlag:
        AddCLasPleliminary(axs)

    for i in range(3):  # Loops on the diffrent targets
        for j in range(nPion):  # Loops on the number of pions

            # axs.set_ylim(0, FullYlimit)
            axs.set_xlim(1.5, 6.5)

            graphName = "PtBroad_FullIntegrated_" + tarList[i] + "_" + str(j+1)
            graph = file.Get(graphName)
            nPoints = graph.GetN()
            x = np.ndarray(nPoints, dtype=float, buffer=graph.GetX())
            # x  = x + (-FullShft + FullShft*2*j)
            y = np.ndarray(nPoints, dtype=float, buffer=graph.GetY())
            ey = np.ndarray(nPoints, dtype=float, buffer=graph.GetEY())
            if j == 0:
                axs.errorbar(x, y, ey, marker=markerList[j], linestyle="",
                             markerfacecolor=colorList[i], color=colorList[i],
                             markersize=4.5, label=tarList[i])
            if i == 2:
                axs.errorbar(x, y, ey, marker=markerList[j], linestyle="",
                             markerfacecolor="grey", color=colorList[i], markersize=4.5,
                             label=labelList[j])

            axs.errorbar(x, y, ey, marker=markerList[j], linestyle="",
                         markerfacecolor=colorList[i], color=colorList[i], markersize=4.5,
                         label=None)

            if ZhCut:
                axs.errorbar(x, y, np.sqrt(ey*ey +
                                           sysDiccFullZhCut[tarList[i]][j]*sysDiccFullZhCut[tarList[i]][j]),
                             marker="", linestyle="", markerfacecolor=colorList[i], lw=0,
                             color=colorList[i], markersize=0, capsize=5)
            else:
                axs.errorbar(x, y, np.sqrt(ey*ey +
                                           sysDiccFull[tarList[i]][j]*sysDiccFull[tarList[i]][j]),
                             marker="", linestyle="", markerfacecolor=colorList[i], lw=0,
                             color=colorList[i], markersize=0, capsize=5)

    if ZhCut:
        axs.set_ylim(0, y[0] + (ey[0]*ey[0] +
                                sysDiccFullZhCut[tarList[2]][1][0]*sysDiccFullZhCut[tarList[2]][1][0])**2 + 0.005)
    else:
        axs.set_ylim(0, y[0] + (ey[0]*ey[0] +
                                sysDiccFull[tarList[2]][1][0]*sysDiccFull[tarList[2]][1][0])**2 + 0.005)
    # axs.set_ylim(0, 0.05)
    axs.set_ylabel(
        r'$\Delta P_\mathrm{T}^{2} [GeV^{2}]$', loc="center", fontsize=15)
    axs.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

    axs.set_xlabel(r'$A^\mathrm{\frac{1}{3}}$', loc="center", fontsize=14)

    if CLASPreliminaryFlag:
        AddCLasPleliminary(axs)

    axs.legend(ncol=2, frameon=False, loc='upper left', fontsize=11)

    axs.grid(visible=None, axis='both', color='0.95')
    axs.set_axisbelow(True)

    SaveFigure(fig, outputDirectory + "Results/", outputName)

    file.Close()


def BroadRatio1Box(variable):

    fig, axs = plt.subplots(1, 1, constrained_layout=True)
    # For one column
    width = 6
    height = width / 1.2
    fig.set_size_inches(width, height)

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_" +
                           variable + ".root", "READ")
    yLimitLow = 10
    yLimitHigh = 0

    for i in range(3):  # Loops on the diffrent targets

        # axs[i].set_ylim(.2, 4)
        axs.set_xlim(xLowLimit[variable], xHighLimit[variable])

        graphName = ["PtBroad_" + variable + "_" + tarList[i] + "_0",
                     "PtBroad_" + variable + "_" + tarList[i] + "_1"]
        graph = [file.Get(graphName[0]), file.Get(graphName[1])]
        nPoints = graph[0].GetN()

        x = np.ndarray(nPoints, dtype=float, buffer=graph[0].GetX())
        x = x + (-2*xShiftNPion[variable] + 2*xShiftNPion[variable]*i)
        y1 = np.ndarray(nPoints, dtype=float, buffer=graph[0].GetY())
        y2 = np.ndarray(nPoints, dtype=float, buffer=graph[1].GetY())
        ey1 = np.ndarray(nPoints, dtype=float, buffer=graph[0].GetEY())
        ey2 = np.ndarray(nPoints, dtype=float, buffer=graph[1].GetEY())
        ey2 = np.ndarray(nPoints, dtype=float, buffer=graph[1].GetEY())
        y = y2/y1
        if variable == "Zh":
            # This is just to avoid erros this bin is not include in the analysis
            y2[0] = 1

        ey = (np.abs(y))*(np.sqrt(((ey1*ey1)/(y1*y1))+((ey2*ey2)/(y2*y2))))

        axs.errorbar(x, y, ey, marker="o", linestyle="",
                     markerfacecolor=colorList[i], color=colorList[i], markersize=5,
                     label=tarList[i])

        ey1 = np.sqrt(ey1*ey1 +
                      sysDic[variable][tarList[i]][0]*sysDic[variable][tarList[i]][0])
        ey2 = np.sqrt(ey2*ey2 +
                      sysDic[variable][tarList[i]][1]*sysDic[variable][tarList[i]][1])

        ey = (np.abs(y2/y1))*(np.sqrt(((ey1*ey1)/(y1*y1))+((ey2*ey2)/(y2*y2))))

        if variable == "Zh":
            # This is just to avoid erros this bin is not include in the analysis
            ey[0] = 0
            y[0] = 1
            # This if you dont want to study the last binning
            y[-1] = 1
            ey[-1] = 0

        axs.errorbar(x, y, ey, marker="", linestyle='', markerfacecolor=colorList[i],
                     lw=0, color=colorList[i], markersize=0, capsize=5)

        axs.set_xlabel(xLabel[variable], fontsize=14)

        yLimitHigh = max([np.max(y+ey), yLimitHigh])
        print(y)
        yLimitLow = min([np.min(y-ey), yLimitLow])
        print(variable)
        print(yLimitLow)

    # Set the labels for the three plots
    print(yLimitLow - 0.6)

    axs.set_ylim(yLimitLow - 0.6, yLimitHigh + 0.6)
    axs.set_ylabel(r'$\Delta P_\mathrm{T}^{2}(2 \pi^+) [GeV^{2}]/P_\mathrm{T}^{2}(1\pi^+) [GeV^{2}]$',
                   loc="center", fontsize=15)

    axs.legend(frameon=False, loc='upper left', fontsize=11)

    for i in range(3):
        axs.grid(visible=None, axis='both', color='0.95')
        axs.set_axisbelow(True)

    SaveFigure(fig, outputDirectory + "Results/", "RatioNPION1Box" + variable)


def BroadRatio(variable):

    fig, axs = plt.subplots(1, 3, sharey='row', sharex='col')
    width = 16  # 7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.02,
                        hspace=0.02)

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_" +
                           variable + ".root", "READ")
    yLimitLow = 10
    yLimitHigh = 0

    for i in range(3):  # Loops on the diffrent targets

        # axs[i].set_ylim(.2, 4)
        axs[i].set_xlim(xLowLimit[variable], xHighLimit[variable])

        graphName = ["PtBroad_" + variable + "_" + tarList[i] + "_0",
                     "PtBroad_" + variable + "_" + tarList[i] + "_1"]
        graph = [file.Get(graphName[0]), file.Get(graphName[1])]
        nPoints = graph[0].GetN()

        x = np.ndarray(nPoints, dtype=float, buffer=graph[0].GetX())
        y1 = np.ndarray(nPoints, dtype=float, buffer=graph[0].GetY())
        y2 = np.ndarray(nPoints, dtype=float, buffer=graph[1].GetY())
        ey1 = np.ndarray(nPoints, dtype=float, buffer=graph[0].GetEY())
        ey2 = np.ndarray(nPoints, dtype=float, buffer=graph[1].GetEY())
        ey2 = np.ndarray(nPoints, dtype=float, buffer=graph[1].GetEY())
        y = y2/y1
        if variable == "Zh":
            # This is just to avoid erros this bin is not include in the analysis
            y2[0] = 1

        ey = (np.abs(y))*(np.sqrt(((ey1*ey1)/(y1*y1))+((ey2*ey2)/(y2*y2))))

        axs[i].errorbar(x, y, ey, marker="o", linestyle="",
                        markerfacecolor=colorList[i], color=colorList[i], markersize=5)

        ey1 = np.sqrt(ey1*ey1 +
                      sysDic[variable][tarList[i]][0]*sysDic[variable][tarList[i]][0])
        ey2 = np.sqrt(ey2*ey2 +
                      sysDic[variable][tarList[i]][1]*sysDic[variable][tarList[i]][1])

        ey = (np.abs(y2/y1))*(np.sqrt(((ey1*ey1)/(y1*y1))+((ey2*ey2)/(y2*y2))))

        if variable == "Zh":
            # This is just to avoid erros this bin is not include in the analysis
            ey[0] = 1
            y[0] = 1
            # This if you dont want to study the last binning
            y[-1] = 0

        axs[i].errorbar(x, y, ey, marker="", linestyle='', markerfacecolor=colorList[i],
                        lw=0, color=colorList[i], markersize=0, capsize=5)

        axs[i].set_xlabel(xLabel[variable], fontsize=14)

        yLimitHigh = max([np.max(y+ey), yLimitHigh])
        yLimitLow = min([np.min(y-ey), yLimitLow])

    # Set the labels for the three plots
    axs[0].set_ylim(yLimitLow - 0.6, yLimitHigh + 0.6)
    axs[0].set_ylabel(r'$\Delta P_\mathrm{T}^{2}(2 \pi^+) [GeV^{2}]/P_\mathrm{T}^{2}(1\pi^+) [GeV^{2}]$',
                      loc="center", fontsize=15)

    axs[0].annotate(r'Carbon', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(r'Iron',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[2].annotate(r'Lead',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)

    # axs[0].legend(frameon = False, loc = 'upper left', fontsize = 11)

    for i in range(3):
        axs[i].grid(visible=None, axis='both', color='0.95')
        axs[i].set_axisbelow(True)

    fig.align_ylabels(axs[:])
    SaveFigure(fig, outputDirectory + "Results/", "RatioNPION" + variable)


sysDic = {"Q2": Systematics("Q2", NBins["Q2"]).sysDic,
          "Nu": Systematics("Nu", NBins["Nu"]).sysDic,
          "Zh": Systematics("Zh", NBins["Zh"]).sysDic}
sysDiccFull = Systematics("FullIntegrated", 1).sysDic
sysDiccFullZhCut = Systematics("FullIntegrated", 1, True).sysDic


# Call funtions
PtBroadFullIntegrated()
# PtBroadFullIntegrated(True)
PtBroadVarTarSplit("Q2")
PtBroadVarTarSplit("Nu")
PtBroadVarTarSplit("Zh")
PtBroadVarNPionSplit("Q2")
PtBroadVarNPionSplit("Nu")
PtBroadVarNPionSplit("Zh")
BroadRatio("Q2")
BroadRatio("Nu")
BroadRatio("Zh")
BroadRatio1Box("Q2")
BroadRatio1Box("Nu")
BroadRatio1Box("Zh")
