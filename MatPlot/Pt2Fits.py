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
Pt2Bins = 70


def Exp(x, amp, alpha):

    return amp*np.exp(-x/alpha)

def Pt2FittedFunction(target, ZhBin, NPion, fitNum, nameNumber):

    os.makedirs(outputDirectory, exist_ok = True) # Create the directory if doesn't exist
    fileGraph = ROOT.TFile.Open(inputDirectory + "Pt2_Distribution.root", "READ")
    fileHist = ROOT.TFile.Open(inputDirectory + "meanPt2_Zh_processed.root", "READ")


    fig, axs = plt.subplots(1, 1, constrained_layout = True)
    # For one column
    width  = 6
    height = width / 1.2
    fig.set_size_inches(width, height)
    axs.set_ylim(0.1, 500000)

    graphName = "Pt2_Distribution_" + target + "_" + str(ZhBin) + "_" + str(NPion)
    histName  = "corr_data_Pt2_" + target + "_" + str(ZhBin) + "_" + str(NPion) + "_fit" + str(fitNum)

    graph   = fileGraph.Get(graphName)
    nPoints = graph.GetN()
    x  = np.ndarray(nPoints, dtype = float, buffer = graph.GetX())
    y  = np.ndarray(nPoints, dtype = float, buffer = graph.GetY())
    ey = np.ndarray(nPoints, dtype = float, buffer = graph.GetEY())
    
    hist = fileHist.Get(histName)
    fitFunc = hist.GetFunction("FFit")
    amp = fitFunc.GetParameter(0) 
    alpha = fitFunc.GetParameter(1) 
    chindf = round(fitFunc.GetChisquare()/fitFunc.GetNDF(), 3)

    axs.errorbar(x, y, ey, marker = "o" , linestyle = "", 
                 markerfacecolor = "#301437", color = "#301437",
        markersize = 4.5, label = "Pt2 distribution")
    
    
    fitStartPoint = (fitNum)*3/Pt2Bins
    bins = np.linspace(fitStartPoint, 3, num = 310)
    yFit = Exp(bins, amp, alpha)
    axs.plot(bins, yFit, color = 'orange', linestyle = '-', linewidth = 1.6, 
             label = 'Fit $\chi^2_{ndf} = $' + str(chindf), zorder = 5)

    axs.set_yscale('log')
    axs.set_ylabel(r'$counts$', loc = "center", fontsize = 15)

    axs.set_xlabel(r'$P_\mathrm{T}^{2} [GeV^{2}]$', loc = "center", fontsize = 14)

    axs.legend(ncol = 1, frameon = False, loc = 'upper right', fontsize = 11)

    axs.grid(visible = None, axis = 'both', color = '0.95')
    axs.set_axisbelow(True)

    fig.savefig(outputDirectory + "Pt2FitFunc_" + str(NPion) + "_" + str(nameNumber) + ".pdf" )
    print(outputDirectory + "Pt2FitFunc_" + str(NPion) + "_" + str(nameNumber) + ".root" )
    fileGraph.Close()
    fileHist.Close()



Pt2FittedFunction('C', 5, 1, 2 ,1)
Pt2FittedFunction('C', 5, 1, 8 ,2)
Pt2FittedFunction('C', 5, 2, 2 ,1)
Pt2FittedFunction('C', 5, 2, 8 ,2)

