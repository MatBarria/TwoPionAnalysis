import ROOT
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import mplhep as hep
from include import inputDirectory, outputDirectory, systematicDirectory

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2


#Shift the data on Zh to make the plot more readability
ZhShift  = 0.015
Q2Shift  = 0.08
NuShift  = 0.08
FullShft = 0.075

# Upper limmit in the y axis
FullYlimit = 0.027
Q2Ylimit   = 0.08
NuYlimit   = 0.08
ZhYlimit   = 0.18



def PtBroadZhTarSplitAccRatio():

    fig, axs = plt.subplots(1, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None, wspace = 0.02, 
                        hspace = 0.02)

    fileData = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh_Data.root", "READ")
    fileCorr = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")

    tarList   = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]
    labelList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]

    for i in range(3): # Loops on the diffrent targets

        # axs[i].set_ylim(0.8, 5)
        # axs[i].set_xlim(0.075, 1.03)
        axs[i].set_ylim(0.8, 1.5)
        axs[i].set_xlim(.175, 0.88)

        for j in range(2): # Loops on the number of pions

            graphName = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
            graphData = fileData.Get(graphName)
            graphCorr = fileCorr.Get(graphName)
            nPoints = 8

            x  = np.ndarray(nPoints, dtype = float, buffer = graphCorr.GetX())
            x  = x + (-ZhShift + ZhShift*j) # Shit the data for readability
            
            yData  = np.ndarray(nPoints, dtype = float, buffer = graphData.GetY())
            yCorr  = np.ndarray(nPoints, dtype = float, buffer = graphCorr.GetY())

            axs[i].plot(x, yData/yCorr, marker = "o", markerfacecolor = colorList[j],
                       color = colorList[j], markersize = 6, label = labelList[j],
                        linestyle = "")

    # Set the labels for the three plots
    axs[0].set_ylabel(r'$\Delta P_\mathrm{T}^{2}(UnCorr) [GeV^{2}]/P_\mathrm{T}^{2}(Acc) [GeV^{2}]$', loc = "center", fontsize = 15)
    axs[0].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
    axs[1].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
    axs[2].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)

    axs[0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    axs[0].legend(frameon = True, loc = (.683,.76), fontsize = 11, 
                  handlelength = .5, handleheight = .5)

    for i in range(3):
        axs[i].grid(visible = None, axis = 'both', color = '0.95')
        axs[i].set_axisbelow(True)


    fig.align_ylabels(axs[:])
    # fig.savefig(outputDirectory + "RatioDataAcc.pdf", bbox_inches = 'tight')
    fig.savefig(outputDirectory + "RatioDataAccZoom.pdf", bbox_inches = 'tight')
    print(outputDirectory + "PtBroad_Zh_Target-Grid_RatioDataAcc.pdf Has been created")



def PtBroadZhNPionSplitAccRatio():

    fig, axs = plt.subplots(1, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None, wspace = 0.02, hspace = 0.02)

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh_RatioDataAcc.root", "READ")

    tarList   = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]
    #labelList = ["C", "Fe", "Pb"]

    for i in range(3): # Loops on the diffrent targets
        for j in range(3): # Loops on the number of pions
            axs[i].set_ylim(0, 2)
            axs[j].set_xlim(0.075, 1.03)
            graphName = "PtBroad_Zh_" + tarList[i] + "_RatioDataAcc_" + str(j)
            graph     = file.Get(graphName)
            nPoints = graph.GetN()
            x  = np.ndarray(nPoints, dtype = float, buffer = graph.GetX())
            x  = x + (-ZhShift + ZhShift*i)
            y  = np.ndarray(nPoints, dtype = float, buffer = graph.GetY())
            ey = np.ndarray(nPoints, dtype = float, buffer = graph.GetEY())
            axs[j].errorbar(x, y, ey, marker = "o", linestyle = "", markerfacecolor = colorList[i],
                            color = colorList[i], markersize = 6, label = tarList[i])

    axs[0].set_ylabel(r'$\Delta P_\mathrm{T}^{2}(UnCorr) [GeV^{2}]/P_\mathrm{T}^{2}(Acc) [GeV^{2}]$', loc = "center", fontsize = 15)
    axs[0].set_xlabel(r'$Z_\mathrm{h}$', fontsize = 14)
    axs[1].set_xlabel(r'$Z_\mathrm{h}$', fontsize = 14)
    axs[2].set_xlabel(r'$Z_\mathrm{h}$', fontsize = 14)

    axs[0].annotate(r'One Pion',     xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[1].annotate(r'Two Pion',     xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[2].annotate(r'Three Pion',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    axs[0].legend(frameon = False, loc = 'upper left', fontsize = 11)

    fig.show()

    fig.align_ylabels(axs[:])
    fig.savefig(outputDirectory + "PtBroad_Zh_NPion_RatioDataAcc.pdf", bbox_inches = 'tight')
    file.Close()
    print(outputDirectory + "PtBroad_Zh_NPion_RatioDataAcc.pdf Has been created")

    for i in range(3):
        axs[i].grid(visible = None, axis = 'both', color = '0.95')
        axs[i].set_axisbelow(True)

    fig.show()

    fig.align_ylabels(axs[:])
    fig.savefig(outputDirectory + "PtBroad_Zh_NPion-Grid_RatioDataAcc.pdf", bbox_inches = 'tight')
    print(outputDirectory + "PtBroad_Zh_NPion-Grid_RatioDataAcc.pdf Has been created")





# Call funtions

PtBroadZhTarSplitAccRatio()
# PtBroadZhNPionSplitAccRatio()
