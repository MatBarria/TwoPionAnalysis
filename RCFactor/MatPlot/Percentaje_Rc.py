import ROOT
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from include_rc import inputDirectory, outputDirectory

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

#Shift the data on Zh to make the plot more readability
ZhShift  = 0.015
# Upper limmit in the y axis
YLimit = 100

NPion = 2

def PercentajeTarSplit():

    fig, axs = plt.subplots(1, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None, wspace = 0.02,
                        hspace = 0.02)

    file = ROOT.TFile.Open(inputDirectory + "Percentaje_Rc.root", "READ")

    tarList   = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]
    labelList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]

    for i in range(3): # Loops on the diffrent targets
        axs[i].set_ylim(0, YLimit)
        axs[i].set_xlim(0.075, 1.03)
        for j in range(NPion): # Loops on the number of pions
            graphName = "Percentaje_" + tarList[i] + "_" + str(j+1)
            graph     = file.Get(graphName)
            # Extrac the data from the TGraph
            nPoints = graph.GetN()
            x  = np.ndarray(nPoints, dtype = float, buffer = graph.GetX())
            x  = x + (-ZhShift + ZhShift*j) # Shit the data for readability
            y  = np.ndarray(nPoints, dtype = float, buffer = graph.GetY())
            y  = y*100
            ey = np.ndarray(nPoints, dtype = float, buffer = graph.GetEY())
            # Generate the plot
            axs[i].errorbar(x, y, ey, marker = "o", linestyle = "", markerfacecolor = colorList[j],
                            color = colorList[j], markersize = 6, label = labelList[j])
            # axs[i].plot(x, y, marker = "o", linestyle = "", markerfacecolor = colorList[j],
                       # color = colorList[j], markersize = 6, label = labelList[j])

    # Set the labels for the three plots
    axs[0].set_ylabel(r'Devation Due Rc(%)', loc = "center", fontsize = 15)
    axs[0].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
    axs[1].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
    axs[2].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)

    axs[0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    axs[0].legend(frameon = False, loc = 'upper right', fontsize = 11)

    fig.show()

    fig.align_ylabels(axs[:])
    # fig.savefig(outputDirectory + "Percentaje_Target_Rc.pdf", bbox_inches = 'tight')
    # print(outputDirectory + "Percentaje_Target_Rc.pdf Has been created")

    for i in range(3):
        axs[i].grid(visible = None, axis = 'both', color = '0.95')
        axs[i].set_axisbelow(True)

    fig.show()

    fig.align_ylabels(axs[:])
    fig.savefig(outputDirectory + "Percentaje_Target-Grid-Rc.pdf", bbox_inches = 'tight')
    print(outputDirectory + "Percentaje_Target-Grid-Rc.pdf Has been created")


# Call funtions
PercentajeTarSplit()
