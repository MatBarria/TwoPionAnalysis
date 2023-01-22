import ROOT
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import mplhep as hep
from include_rc import inputDirectory, outputDirectory

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

#Shift the data on Zh to make the plot more readability
ZhShift  = 0.015
FullShft = 0.075

# Upper limmit in the y axis
FullYlimit = 0.027
ZhYlimit   = 0.1

nPion = 2

# Generate three plots of Pt broadening in function of Zh separated by the target
def PtBroadZhTarSplit():

    fig, axs = plt.subplots(1, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None, wspace = 0.02, 
                        hspace = 0.02)


    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh_Rc.root", "READ")

    tarList   = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]
    labelList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]

    for i in range(3): # Loops on the diffrent targets
        axs[i].set_ylim(0, ZhYlimit)
        axs[i].set_xlim(0.075, 1.03)
        for j in range(nPion): # Loops on the number of pions
            graphName = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
            graph     = file.Get(graphName)
            # Extrac the data from the TGraph
            nPoints = graph.GetN()
            x  = np.ndarray(nPoints, dtype = float, buffer = graph.GetX())
            x  = x + (-ZhShift + ZhShift*j) # Shit the data for readability
            y  = np.ndarray(nPoints, dtype = float, buffer = graph.GetY())
            ey = np.ndarray(nPoints, dtype = float, buffer = graph.GetEY())
            # Generate the plot
            axs[i].errorbar(x, y, ey, marker = "o", linestyle = "", markerfacecolor = colorList[j],
                            color = colorList[j], markersize = 6, label = labelList[j])

    # Set the labels for the three plots
    axs[0].set_ylabel(r'$\Delta P_\mathrm{T}^{2} [GeV^{2}]$', loc = "center", fontsize = 15)
    axs[0].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
    axs[1].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
    axs[2].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)

    axs[0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    axs[0].legend(frameon = False, loc = 'upper left', fontsize = 11)

    fig.align_ylabels(axs[:])

    for i in range(3):
        axs[i].grid(visible = None, axis = 'both', color = '0.95')
        axs[i].set_axisbelow(True)

    fig.savefig(outputDirectory + "PtBroad_Zh_Target_Rc.pdf", bbox_inches = 'tight')
    print(outputDirectory + "PtBroad_Zh_Target-Grid_Rc.pdf Has been created")



def PtBroadFullIntegrated():

    fig, axs = plt.subplots(1, 1, constrained_layout = True)
    # For one column
    width  = 6
    height = width / 1.2
    fig.set_size_inches(width, height)

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_FullIntegrated_Rc.root", "READ")

    tarList    = ["C", "Fe", "Pb"]
    colorList  = ["red", "Blue", "black"]
    nPionList  = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]
    markerList = ["o", "s", "D"]

    for i in range(3): # Loops on the diffrent targets
        for j in range(nPion): # Loops on the number of pions
            axs.set_ylim(0, FullYlimit)
            axs.set_xlim(1.5, 6.5)
            graphName = "PtBroad_FullIntegrated_" + tarList[i] + "_" + str(j)
            graph     = file.Get(graphName)
            nPoints = graph.GetN()
            x  = np.ndarray(nPoints, dtype = float, buffer = graph.GetX())
            x  = x + (-FullShft + FullShft*j)
            y  = np.ndarray(nPoints, dtype = float, buffer = graph.GetY())
            ey = np.ndarray(nPoints, dtype = float, buffer = graph.GetEY())
            if j == 0:
                axs.errorbar(x, y, ey, marker = markerList[j], linestyle = "", label = tarList[i],
                             markerfacecolor = colorList[i], color = colorList[i], markersize = 4.5)
            if i == 2:
                axs.errorbar(x, y, ey, marker = markerList[j], linestyle = "", label = nPionList[j], 
                        markerfacecolor = "grey", color = colorList[i], markersize = 4.5)

            axs.errorbar(x, y, ey, marker = markerList[j], linestyle = "", label = None, 
                        markerfacecolor = colorList[i], color = colorList[i], markersize = 4.5)



    axs.set_ylabel(r'$\Delta P_\mathrm{T}^{2} [GeV^{2}]$', loc = "center", fontsize = 15)
    axs.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

    axs.set_xlabel(r'$A^\mathrm{\frac{1}{3}}$', loc = "center", fontsize = 14)


    axs.legend(ncol = 2, frameon = False, loc = 'upper left', fontsize = 11)

    fig.savefig(outputDirectory + "PtBroad_FullIntegrated_Rc.pdf", bbox_inches = 'tight')
    file.Close()
    print(outputDirectory + "PtBroad_FullIntegrated_Rc.pdf Has been created")

    axs.grid(visible = None, axis = 'both', color = '0.95')
    axs.set_axisbelow(True)

    axs.grid(visible = None, axis = 'both', color = '0.95')
    axs.set_axisbelow(True)

    fig.savefig(outputDirectory + "PtBroad_FullIntegrated_Rc.pdf", bbox_inches = 'tight')
    print(outputDirectory + "PtBroad_FullIntegrated-Grid_Rc.pdf Has been created")





# Call funtions
PtBroadZhTarSplit()
PtBroadFullIntegrated()
