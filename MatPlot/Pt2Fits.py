import ROOT
import numpy as np
import matplotlib.pyplot as plt
from include import inputDirectory
from include import outputDirectory, SaveFigure
import mplhep as hep
import os

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

NZh = 8
nPion = 2
Pt2Bins = 70


def Exp(x, amp, alpha):

    return amp*np.exp(-x/alpha)


def Pt2FittedFunction(target, ZhBin, NPion, fitNum, nameNumber):

    # Create the directory if doesn't exist
    os.makedirs(outputDirectory, exist_ok=True)
    fileGraph = ROOT.TFile.Open(
        inputDirectory + "Pt2_Distribution.root", "READ")
    fileHist = ROOT.TFile.Open(
        inputDirectory + "corr_data_Pt2_processed.root", "READ")
    print(fileHist)

    fig, axs = plt.subplots(1, 1, constrained_layout=True)
    # For one column
    width = 6
    height = width / 1.2
    fig.set_size_inches(width, height)
    axs.set_ylim(0.1, 500000)

    graphName = "Pt2_Distribution_" + target + \
        "_12" + str(ZhBin) + "_" + str(NPion)
    histName = "corr_data_Pt2_" + target + "_12" + \
        str(ZhBin) + "_" + str(NPion) + "_fit" + str(fitNum)
    # print(histName)

    graph = fileGraph.Get(graphName)
    nPoints = graph.GetN()
    x = np.ndarray(nPoints, dtype=float, buffer=graph.GetX())
    y = np.ndarray(nPoints, dtype=float, buffer=graph.GetY())
    ey = np.ndarray(nPoints, dtype=float, buffer=graph.GetEY())

    hist = fileHist.Get(histName)
    fitFunc = hist.GetFunction("FFit")
    amp = fitFunc.GetParameter(0)
    alpha = fitFunc.GetParameter(1)
    chindf = round(fitFunc.GetChisquare()/fitFunc.GetNDF(), 3)

    axs.errorbar(x, y, ey, marker="o", linestyle="",
                 markerfacecolor="black", color="#301437",
                 markersize=4.9, label="Pt2 distribution")

    fitStartPoint = (fitNum)*3/Pt2Bins
    bins = np.linspace(fitStartPoint, 3, num=310)
    yFit = Exp(bins, amp, alpha)
    axs.plot(bins, yFit, color='red', linestyle='-', linewidth=1.8,
             label='Fit $\chi^2_{ndf} = $' + str(chindf), zorder=5)

    axs.set_yscale('log')
    axs.set_ylabel(r'$counts$', loc="center", fontsize=15)

    axs.set_xlabel(r'$P_\mathrm{+T}^{2} [GeV^{2}]$', loc="center", fontsize=14)

    axs.legend(ncol=1, frameon=False, loc='upper right', fontsize=11)

    axs.grid(visible=None, axis='both', color='0.95')
    axs.set_axisbelow(True)

    # fig.savefig(outputDirectory + "Pt2FitFunc_" +
    # str(NPion) + "_" + str(nameNumber) + ".pdf")
    SaveFigure(fig, outputDirectory + "Pt2Dist/",
               "Pt2FitFunc_" + str(NPion) + "_" + str(nameNumber))
    fileGraph.Close()
    fileHist.Close()


print("1")
Pt2FittedFunction('C', 6, 1, 3, 1)
print("2")
Pt2FittedFunction('C', 6, 1, 12, 2)
print("3")
Pt2FittedFunction('C', 6, 2, 3, 1)
print("4")
Pt2FittedFunction('C', 6, 2, 12, 2)
