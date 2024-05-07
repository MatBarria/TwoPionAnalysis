import ROOT
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import mplhep as hep
from include import inputDirectory, outputDirectory, systematicDirectory, SaveFigure

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2


# Shift the data on Zh to make the plot more readability
ZhShift = 0.015
Q2Shift = 0.08
NuShift = 0.08
FullShft = 0.075

# Upper limmit in the y axis
FullYlimit = 0.027
Q2Ylimit = 0.08
NuYlimit = 0.08
ZhYlimit = 0.18


def PtBroadZhTarSplitAccRatio():

    fig, axs = plt.subplots(1, 3, sharey='row', sharex='col')
    width = 16  # 7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.02,
                        hspace=0.02)

    fileData = ROOT.TFile.Open(
        inputDirectory + "Pt_broad_Zh_Data.root", "READ")
    fileCorr = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")

    tarList = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]
    labelList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]

    for i in range(3):  # Loops on the diffrent targets

        axs[i].set_ylim(0.8, 5)
        axs[i].set_xlim(0.075, 0.799)
        axs[i].set_ylim(0.8, 2.5)
        axs[i].set_xticks([.1, .3, .5, .7])
        # axs[i].set_xlim(.175, 0.88)

        for j in range(2):  # Loops on the number of pions

            graphName = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
            graphData = fileData.Get(graphName)
            graphCorr = fileCorr.Get(graphName)
            nPoints = 8

            x = np.ndarray(nPoints, dtype=float, buffer=graphCorr.GetX())
            x = x + (-ZhShift + ZhShift*j)  # Shit the data for readability

            yData = np.ndarray(nPoints, dtype=float, buffer=graphData.GetY())
            yCorr = np.ndarray(nPoints, dtype=float, buffer=graphCorr.GetY())

            yCorr[0] = 1  # Just to avoid divide by zero, this bin was no studied

            axs[i].plot(x, yData/yCorr, marker="o", markerfacecolor=colorList[j],
                        color=colorList[j], markersize=6, label=labelList[j],
                        linestyle="")

    # Set the labels for the three plots
    axs[0].set_ylabel(r'$\Delta P_\mathrm{T}^{2}(UnCorr) [GeV^{2}]/P_\mathrm{T}^{2}(Acc) [GeV^{2}]$',
                      loc="center", fontsize=15)
    axs[0].set_xlabel(r'$Z_h$', fontsize=14)
    axs[1].set_xlabel(r'$Z_h$', fontsize=14)
    axs[2].set_xlabel(r'$Z_h$', fontsize=14)

    axs[0].annotate(r'Carbon', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(r'Iron',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[2].annotate(r'Lead',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)

    axs[0].legend(frameon=True, loc=(.683, .76), fontsize=11,
                  handlelength=.5, handleheight=.5)

    for i in range(3):
        axs[i].grid(visible=None, axis='both', color='0.95')
        axs[i].set_axisbelow(True)

    fig.align_ylabels(axs[:])
    # fig.savefig(outputDirectory + "RatioDataAcc.pdf", bbox_inches = 'tight')
    fig.savefig(outputDirectory + "RatioDataAcc.pdf", bbox_inches='tight')
    print(outputDirectory + "RatioDataAccpdf Has been created")


def AccRCRatio():

    fig, axs = plt.subplots(1, 3, sharey='row', sharex='col')
    width = 16  # 7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.02,
                        hspace=0.02)

    fileData = ROOT.TFile.Open(
        inputDirectory + "Pt_broad_Zh_Data.root", "READ")
    fileCorr = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")
    fileRC = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh_RC.root", "READ")

    tarList = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]
    labelList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]

    for i in range(3):  # Loops on the diffrent targets

        axs[i].set_ylim(0.8, 5)
        axs[i].set_xlim(0.075, 0.799)
        axs[i].set_ylim(0.8, 2.5)
        axs[i].set_xticks([.1, .3, .5, .7])
        # axs[i].set_xlim(.175, 0.88)

        for j in range(2):  # Loops on the number of pions

            graphName = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
            graphData = fileData.Get(graphName)
            graphCorr = fileCorr.Get(graphName)
            graphRC = fileRC.Get(graphName)
            nPoints = 8

            x = np.ndarray(nPoints, dtype=float, buffer=graphCorr.GetX())
            x = x + (-ZhShift + ZhShift*j)  # Shit the data for readability

            yData = np.ndarray(nPoints, dtype=float, buffer=graphData.GetY())
            yCorr = np.ndarray(nPoints, dtype=float, buffer=graphCorr.GetY())
            yRC = np.ndarray(nPoints, dtype=float, buffer=graphRC.GetY())
            print(yRC)
            yCorr[0] = 1  # Just to avoid divide by zero, this bin was no studied
            yRC[0] = 1  # Just to avoid divide by zero, this bin was no studied

            axs[i].plot(x, yData/yCorr, marker="o", markerfacecolor=colorList[j],
                        color=colorList[j], markersize=6, label=labelList[j] + " Acc",
                        linestyle="")
            axs[i].plot(x, yCorr/yRC, marker="o", markerfacecolor="none",
                        color=colorList[j], markersize=6, label=labelList[j] + " Rc",
                        linestyle="")

    # Set the labels for the three plots
    axs[0].set_ylabel(r'$\Delta P_\mathrm{T}^{2}(UnCorr) [GeV^{2}]/P_\mathrm{T}^{2}(Acc) [GeV^{2}]$',
                      loc="center", fontsize=15)
    axs[0].set_xlabel(r'$Z_h$', fontsize=14)
    axs[1].set_xlabel(r'$Z_h$', fontsize=14)
    axs[2].set_xlabel(r'$Z_h$', fontsize=14)

    axs[0].annotate(r'Carbon', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(r'Iron',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[2].annotate(r'Lead',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)

    axs[0].legend(frameon=True, loc=(.683, .76), fontsize=11,
                  handlelength=.5, handleheight=.5)

    for i in range(3):
        axs[i].grid(visible=None, axis='both', color='0.95')
        axs[i].set_axisbelow(True)

    fig.align_ylabels(axs[:])
    # fig.savefig(outputDirectory + "RatioDataAcc.pdf", bbox_inches = 'tight')
    fig.savefig(outputDirectory + "RatioDataAccRC.pdf", bbox_inches='tight')
    print(outputDirectory + "RatioDataAccRCpdf Has been created")


def AccRCPercentaje():

    fig, axs = plt.subplots(1, 3, sharey='row', sharex='col')
    width = 16  # 7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.02,
                        hspace=0.02)

    fileData = ROOT.TFile.Open(
        inputDirectory + "Pt_broad_Zh_Data.root", "READ")
    fileCorr = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")
    fileRC = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh_RC.root", "READ")

    tarList = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]
    labelList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]

    for i in range(3):  # Loops on the diffrent targets

        axs[i].set_ylim(0.8, 5)
        axs[i].set_xlim(0.075, 0.799)
        axs[i].set_ylim(0., 70)
        axs[i].set_xticks([.1, .3, .5, .7])
        # axs[i].set_xlim(.175, 0.88)

        for j in range(2):  # Loops on the number of pions

            graphName = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
            graphData = fileData.Get(graphName)
            graphCorr = fileCorr.Get(graphName)
            graphRC = fileRC.Get(graphName)
            nPoints = 8

            x = np.ndarray(nPoints, dtype=float, buffer=graphCorr.GetX())
            x = x + (-ZhShift + ZhShift*j)  # Shit the data for readability

            yData = np.ndarray(nPoints, dtype=float, buffer=graphData.GetY())
            yCorr = np.ndarray(nPoints, dtype=float, buffer=graphCorr.GetY())
            yRC = np.ndarray(nPoints, dtype=float, buffer=graphRC.GetY())
            print(yRC)
            yCorr[0] = 1  # Just to avoid divide by zero, this bin was no studied
            yRC[0] = 1  # Just to avoid divide by zero, this bin was no studied

            axs[i].plot(x, np.absolute((yData-yCorr)/yData)*100, marker="o",
                        markerfacecolor=colorList[j], color=colorList[j], markersize=6,
                        label=labelList[j] + " Acc", linestyle="")
            axs[i].plot(x, np.absolute((yCorr-yRC)/yCorr)*100, marker="o", markerfacecolor="none",
                        color=colorList[j], markersize=6, label=labelList[j] + " Rc",
                        linestyle="")
            print(np.absolute((yCorr-yRC)/yCorr)*100)

    # Set the labels for the three plots
    axs[0].set_ylabel(r'$\Delta P_\mathrm{T}^{2}(UnCorr) [GeV^{2}]/P_\mathrm{T}^{2}(Acc) [GeV^{2}]$',
                      loc="center", fontsize=15)
    axs[0].set_xlabel(r'$Z_h$', fontsize=14)
    axs[1].set_xlabel(r'$Z_h$', fontsize=14)
    axs[2].set_xlabel(r'$Z_h$', fontsize=14)

    axs[0].annotate(r'Carbon', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(r'Iron',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[2].annotate(r'Lead',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)

    axs[0].legend(frameon=True, loc=(.683, .76), fontsize=11,
                  handlelength=.5, handleheight=.5)

    for i in range(3):
        axs[i].grid(visible=None, axis='both', color='0.95')
        axs[i].set_axisbelow(True)

    fig.align_ylabels(axs[:])
    # fig.savefig(outputDirectory + "RatioDataAcc.pdf", bbox_inches = 'tight')
    fig.savefig(outputDirectory + "PercentageDataAccRC.pdf",
                bbox_inches='tight')
    print(outputDirectory + "PercentageDataAccRCpdf Has been created")


def AccInterRatio():

    fig, axs = plt.subplots(1, 3, sharey='row', sharex='col')
    width = 16  # 7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.02,
                        hspace=0.02)

    fileAcc = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")
    fileAccInter = ROOT.TFile.Open(
        systematicDirectory + "AccInter/Pt_broad_Zh.root", "READ")

    tarList = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]
    labelList = ["One $\pi^+$", "Two $\pi^+$", "Three $\pi^+$"]

    for i in range(3):  # Loops on the diffrent targets

        axs[i].set_ylim(0., 80)
        # axs[i].set_yscale('log')
        axs[i].set_xlim(0.075, 1.03)

        graphName = "PtBroad_Zh_" + tarList[i] + "_" + str(1)
        graphAcc = fileAcc.Get(graphName)
        graphAccInter = fileAccInter.Get(graphName)
        nPoints = 8

        x = np.ndarray(nPoints, dtype=float, buffer=graphAcc.GetX())

        yAcc = np.ndarray(nPoints, dtype=float, buffer=graphAcc.GetY())
        yAccError = np.ndarray(nPoints, dtype=float, buffer=graphAcc.GetEY())
        yAccInter = np.ndarray(nPoints, dtype=float,
                               buffer=graphAccInter.GetY())
        yAccInterError = np.ndarray(
            nPoints, dtype=float, buffer=graphAccInter.GetEY())

        yAcc[0] = 1  # Just to avoid divide by zero, this bin was no studied

        ySys = np.absolute((yAcc-yAccInter)/yAcc)*100
        # ySysError = (ySys)*np.sqrt(np.sqrt(((yAccError*yAccError)/(yAcc*yAcc))+((yAccInterError*yAccInterError)/(yAccInter*yAccInter))))
        print("Deviaton percentage: " + tarList[i])
        print(ySys)
        axs[i].plot(x, ySys, marker="o", markerfacecolor=colorList[i],
                    color=colorList[i], markersize=6,
                    linestyle="")
        # axs[i].errorbar(x, ySys, ySysError, marker = "o", markerfacecolor = colorList[i],
        # color = colorList[i], markersize = 6,
        # linestyle = "")

    # Set the labels for the three plots
    axs[0].set_ylabel(r'Percentage of difference(%)',
                      loc="center", fontsize=15)
    axs[0].set_xlabel(r'$Zh_\mathrm{Sum}$', fontsize=14)
    axs[1].set_xlabel(r'$Zh_\mathrm{Sum}$', fontsize=14)
    axs[2].set_xlabel(r'$Zh_\mathrm{Sum}$', fontsize=14)

    axs[0].annotate(r'Carbon ' + labelList[1], xy=(0.04, 1.04), xycoords='axes fraction',
                    fontsize=15)
    axs[1].annotate(r'Iron ' + labelList[1], xy=(0.04, 1.04), xycoords='axes fraction',
                    fontsize=15)
    axs[2].annotate(r'Lead ' + labelList[1], xy=(0.04, 1.04), xycoords='axes fraction',
                    fontsize=15)

    # axs[0].legend(frameon = True, loc = (.683,.76), fontsize = 11,
    # handlelength = .5, handleheight = .5)

    for i in range(3):
        axs[i].grid(visible=None, axis='both', color='0.95')
        axs[i].set_axisbelow(True)

    fig.align_ylabels(axs[:])

    SaveFigure(fig, outputDirectory, "DeviationInterAcc")


def PtBroadZhNPionSplitAccRatio():

    fig, axs = plt.subplots(1, 3, sharey='row', sharex='col')
    width = 16  # 7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None,
                        top=None, wspace=0.02, hspace=0.02)

    fig, axs = plt.subplots(1, 2, sharey='row', sharex='col')
    width = 16  # 7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.02,
                        hspace=0.02)

    fileData = ROOT.TFile.Open(
        inputDirectory + "Pt_broad_Zh_Data.root", "READ")
    fileCorr = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")

    tarList = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]
    labelList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]

    for i in range(3):  # Loops on the diffrent targets

        axs[i].set_ylim(0.8, 5)
        axs[i].set_xlim(0.075, 1.03)
        # axs[i].set_ylim(0.8, 1.5)
        # axs[i].set_xlim(.175, 0.88)

        for j in range(2):  # Loops on the number of pions

            graphName = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
            graphData = fileData.Get(graphName)
            graphCorr = fileCorr.Get(graphName)
            nPoints = 8

            x = np.ndarray(nPoints, dtype=float, buffer=graphCorr.GetX())
            x = x + (-ZhShift + ZhShift*j)  # Shit the data for readability

            yData = np.ndarray(nPoints, dtype=float, buffer=graphData.GetY())
            yCorr = np.ndarray(nPoints, dtype=float, buffer=graphCorr.GetY())

            axs[i].plot(x, yData/yCorr, marker="o", markerfacecolor=colorList[j],
                        color=colorList[j], markersize=6, label=labelList[j],
                        linestyle="")

    # Set the labels for the three plots
    axs[0].set_ylabel(
        r'$\Delta P_\mathrm{T}^{2}(UnCorr) [GeV^{2}]/P_\mathrm{T}^{2}(Acc) [GeV^{2}]$', loc="center", fontsize=15)
    axs[0].set_xlabel(r'$Zh_\mathrm{Sum}$', fontsize=14)
    axs[1].set_xlabel(r'$Zh_\mathrm{Sum}$', fontsize=14)
    axs[2].set_xlabel(r'$Zh_\mathrm{Sum}$', fontsize=14)

    axs[0].annotate(r'Carbon', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(r'Iron',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[2].annotate(r'Lead',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)

    axs[0].legend(frameon=True, loc=(.683, .76), fontsize=11,
                  handlelength=.5, handleheight=.5)

    for i in range(3):
        axs[i].grid(visible=None, axis='both', color='0.95')
        axs[i].set_axisbelow(True)

    fig.align_ylabels(axs[:])
    # fig.savefig(outputDirectory + "RatioDataAcc.pdf", bbox_inches = 'tight')
    fig.savefig(outputDirectory + "RatioDataAccZoom.pdf", bbox_inches='tight')
    print(outputDirectory + "PtBroad_Zh_Target-Grid_RatioDataAcc.pdf Has been created")


# Call funtions
PtBroadZhTarSplitAccRatio()
# AccInterRatio()
AccRCRatio()
AccRCPercentaje()
# PtBroadZhNPionSplitAccRatio()
