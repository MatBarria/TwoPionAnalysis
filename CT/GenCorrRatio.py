import ROOT
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

inputDirectory  = "~/proyecto/TwoPionAnalysis/Data/CT/"
outputDirectory = "/home/matias/proyecto/TwoPionAnalysis/Plots/CT/"

#Shift the data on Zh to make the plot more readability
ZhShift  = 0.0075
nPion = 2

def PtBroadZhTarSplitAccRatio():

    fig, axs = plt.subplots(1, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None, wspace = 0.02,
                        hspace = 0.02)

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh_RatioGenCorr.root", "READ")

    tarList   = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]
    labelList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]

    for i in range(3): # Loops on the diffrent targets
        axs[i].set_ylim(0.7, 1.3)
        axs[i].set_xlim(0.075, 1.03)
        for j in range(nPion): # Loops on the number of pions
            graphName = "PtBroad_Zh_" + tarList[i] + "_RatioGenCorr" + str(j)
            graph     = file.Get(graphName)
            # Extrac the data from the TGraph
            nPoints = graph.GetN()
            x  = np.ndarray(nPoints, dtype = float, buffer = graph.GetX())
            x  = x + (-ZhShift + ZhShift*2*j) # Shit the data for readability
            y  = np.ndarray(nPoints, dtype = float, buffer = graph.GetY())
            ey = np.ndarray(nPoints, dtype = float, buffer = graph.GetEY())
            # Generate the plot
            print(y)
            # axs[i].errorbar(x, y, ey, marker = "o", linestyle = "", markerfacecolor = colorList[j],
                            # color = colorList[j], markersize = 6, label = labelList[j])
            axs[i].plot(x, y, marker = "o", linestyle = "", markerfacecolor = colorList[j],
                       color = colorList[j], markersize = 6, label = labelList[j])

    # Set the labels for the three plots
    axs[0].set_ylabel(r'$\Delta P_\mathrm{T}^{2}(Corr) [GeV^{2}]/P_\mathrm{T}^{2}(Gen) [GeV^{2}]$',
                      loc = "center", fontsize = 15)
    axs[0].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
    axs[1].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
    axs[2].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)

    axs[0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    axs[0].legend(frameon = False, loc = 'upper right', fontsize = 11)


    fig.align_ylabels(axs[:])
    for i in range(3):
        axs[i].grid(visible = None, axis = 'both', color = '0.95')
        axs[i].set_axisbelow(True)

    fig.savefig(outputDirectory + "ClousureTest.pdf", bbox_inches = 'tight')
    print(outputDirectory + "ClousureTest.pdf Has been created")



# Call funtions

PtBroadZhTarSplitAccRatio()
