import ROOT
import numpy as np
import matplotlib.pyplot as plt
from include import inputDirectory
from include import outputDirectory
import mplhep as hep
import os

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

NZh = 8
nPion = 2
Pt2Bins = 60


def FitFunc(x, a, b, c):

    return a + b*np.cos(x*(3.1415/180)) + c*np.cos(2*x*(3.1415/180))


def FindMax(values, firstBin, lastBin):

    max = -1000
    for i in range(firstBin, lastBin):

        if values[i] > max:
            max = values[i]

    return round(max, 2)


def FindMin(values, firstBin, lastBin):

    min = 1000
    for i in range(firstBin, lastBin):

        if values[i] < min:
            min = values[i]

    return round(min, 2)


def PhiFittedFunction(target, NPion, Q2, Xb, Zh, Pt, PhiBins):

    inputDirectory = "/home/matias/proyecto/TwoPionAnalysis/Data/Bins/60/"
    if PhiBins == 6:
        inputDirectory = "/home/matias/proyecto/TwoPionAnalysis/Data/Bins/60/RCFit6bins/"

    # Create the directory if doesn't exist
    os.makedirs(outputDirectory, exist_ok=True)
    fileHist = ROOT.TFile.Open(inputDirectory + target + "newphihist" + str(NPion) + ".root",
                               "READ")

    fig, axs = plt.subplots(1, 1, constrained_layout=True)
    # For one column
    width = 6
    height = width / 1.2
    fig.set_size_inches(width, height)
    axs.set_xlim(-180, 180)

    histName = "PhiDist Q2=" + \
        str(Q2) + " Nu=" + str(Xb) + " Zh=" + str(Zh) + " Pt2=" + str(Pt)

    hist = fileHist.Get(histName)
    fitFunc = hist.GetFunction("fit")
    a = fitFunc.GetParameter(0)
    b = fitFunc.GetParameter(1)
    c = fitFunc.GetParameter(2)
    chindf = round(fitFunc.GetChisquare()/fitFunc.GetNDF(), 3)

    binWidth = 360/PhiBins

    x = np.repeat(0., PhiBins)
    y = np.repeat(0., PhiBins)
    ey = np.repeat(0., PhiBins)

    for i in range(PhiBins):
        x[i] = -180 + i*binWidth + binWidth/2
        y[i] = hist.GetBinContent(i+1)
        ey[i] = hist.GetBinError(i+1)

    axs.set_ylim(0.9*FindMin(y, 0, PhiBins), 1.1*FindMax(y, 0, PhiBins))
    print("x: ")
    print(x)
    print("y: ")
    print(y)
    print("ey: ")
    print(ey)

    axs.errorbar(x, y, ey, marker="_", linestyle="",
                 markerfacecolor="#301437", color="#301437",
                 markersize=44.5, label="Pt2 distribution")

    # fitStartPoint = (fitNum)*3/Pt2Bins
    bins = np.linspace(-180, 180, num=310)
    yFit = FitFunc(bins, a, b, c)
    axs.plot(bins, yFit, color='orange', linestyle='-', linewidth=1.6,
             label='Fit $\chi^2_{ndf} = $' + str(chindf), zorder=5)

    # axs.set_yscale('log')
    axs.set_ylabel(r'$dN/dPhi_{PQ}$', loc="center", fontsize=15)

    axs.set_xlabel(r'$Phi_{PQ} [Deg]$', loc="center", fontsize=14)

    axs.legend(ncol=1, frameon=False, loc='upper right', fontsize=11)

    axs.grid(visible=None, axis='both', color='0.95')
    axs.set_axisbelow(True)

    fig.savefig(outputDirectory + "PhiFitFunc_" +
                str(NPion) + "_" + str(PhiBins) + ".pdf")
    print(outputDirectory + "PhiFitFunc_" +
          str(NPion) + "_" + str(PhiBins) + ".pdf")
    fileHist.Close()


PhiFittedFunction('Fe', 1, 1, 2, 6, 25, 6)
PhiFittedFunction('Fe', 1, 1, 2, 6, 25, 12)
PhiFittedFunction('Fe', 2, 1, 2, 6, 21, 6)
PhiFittedFunction('Fe', 2, 1, 2, 6, 21, 12)
