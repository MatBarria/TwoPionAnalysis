import ROOT
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from include_rc import inputDirectory, outputDirectory

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2


#Shift the data on Zh to make the plot more readability
ZhShift  = 0.0075
# Upper limmit in the y axis

nPion = 2

def PtBroadZhTarSplitAccRatio():

    fig, axs = plt.subplots(1, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None, wspace = 0.02, 
                        hspace = 0.02)

    fileRC = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh_Rc.root", "READ")
    fileAC = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")
    
    tarList   = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]
    labelList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]

    for i in range(3): # Loops on the diffrent targets
        axs[i].set_ylim(.7, 1.2)
        axs[i].set_xlim(0.075, 1.03)
        for j in range(nPion): # Loops on the number of pions
            graphName = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
            graphAC     = fileAC.Get(graphName)
            graphRC     = fileRC.Get(graphName)
            # Extrac the data from the TGraph
            nPoints = graphAC.GetN()
            x  = np.ndarray(nPoints, dtype = float, buffer = graphRC.GetX())
            x  = x + (-ZhShift + ZhShift*2*j) # Shit the data for readability
            yRC  = np.ndarray(nPoints, dtype = float, buffer = graphRC.GetY())
            yAC  = np.ndarray(nPoints, dtype = float, buffer = graphAC.GetY())
            # Generate the plot
            # axs[i].errorbar(x, y, ey, marker = "o", linestyle = "", markerfacecolor = colorList[j],
            #                 color = colorList[j], markersize = 6, label = labelList[j])
            axs[i].plot(x,yAC/yRC, marker = "o", linestyle = "", markerfacecolor = colorList[j],
                       color = colorList[j], markersize = 4, label = labelList[j])

    # Set the labels for the three plots
    axs[0].set_ylabel(r'$\Delta P_\mathrm{T}^{2}(Acc) [GeV^{2}]/P_\mathrm{T}^{2}(Acc+Rc) [GeV^{2}]$',
                      loc = "center", fontsize = 15)
    axs[0].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
    axs[1].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
    axs[2].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)

    axs[0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    axs[0].legend(frameon = True, loc = (.053,.76), fontsize = 11, 
                  handlelength = .5, handleheight = .5)

    fig.align_ylabels(axs[:])

    for i in range(3):
        axs[i].grid(visible = None, axis = 'both', color = '0.95')
        axs[i].set_axisbelow(True)

    fig.savefig(outputDirectory + "RatioAccRC.pdf", bbox_inches = 'tight')
    print(outputDirectory + "RatioDataAcc.pdf Has been created")





# Call funtions

PtBroadZhTarSplitAccRatio()
