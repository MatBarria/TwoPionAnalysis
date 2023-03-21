import ROOT
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import mplhep as hep
from include import inputDirectory, outputDirectory, systematicDirectory

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

#Shift the data on Zh to make the plot more readability
ZhShift  = 0.0075
FullShft = 0.0375

# Upper limmit in the y axis
FullYlimit = 0.035
ZhYlimit   = 0.09

nPion = 2;

left, width = .25, .5
bottom, height = .25, .5
right = left + width
top = bottom + height
    
tarList    = ["C", "Fe", "Pb"]
colorList  = ["red", "Blue", "black"]
nPionList  = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]
markerList = ["o", "s", "D"]

def AddCLasPleliminary(ax):
     ax.text(0.5, 0.5, 'CLAS Preliminary',
                 horizontalalignment='center',
                 verticalalignment='center',
                 transform=axs[i].transAxes,
                 color = "lightgrey" ,
                 fontsize = "xx-large",
                 fontweight = "bold" ,
                 alpha = 0.7    ,     
                 zorder=0
                 )


def PtBroadZhTarSplit():

    fig, axs = plt.subplots(1, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None,
                        wspace = 0.02, hspace = 0.02)

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")

    tarList   = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]
    labelList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]


    for i in range(3): # Loops on the diffrent targets
        # AddCLasPleliminary(axs[i])
        axs[i].set_ylim(0, ZhYlimit)
        axs[i].set_xlim(0.075, 1.03)
        for j in range(nPion): # Loops on the number of pions
            graphName = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
            graph     = file.Get(graphName)
            # Extrac the data from the TGraph
            nPoints = graph.GetN()
            x  = np.ndarray(nPoints, dtype = float, buffer = graph.GetX())
            x  = x + (-ZhShift + ZhShift*2*j) # Shit the data for readability
            y  = np.ndarray(nPoints, dtype = float, buffer = graph.GetY())
            ey = np.ndarray(nPoints, dtype = float, buffer = graph.GetEY())
            # Generae the plot
            print("broadening:")
            print(y)
            print("error")
            print(ey)
            axs[i].errorbar(x, y, ey, marker = "o", linestyle = "",
                            markerfacecolor = colorList[j], color = colorList[j], 
                            markersize = 6, label = labelList[j])
            # container = axs[i].errorbar(x, y, ey + systematicDiccionary[tarList[i]][j], 
                            # marker = "", linestyle = "", markerfacecolor = colorList[j], lw = 0,
                            # color = colorList[j], markersize = 0, capsize = 5)

    # Set the labels for the three plots
    axs[0].set_ylabel(r'$\Delta P_\mathrm{T}^{2} [GeV^{2}]$', loc = "center", 
                    fontsize = 15)
    axs[0].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
    axs[1].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
    axs[2].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)

    axs[0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', 
                    fontsize = 15)
    axs[1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    axs[0].legend(frameon = False, loc = 'upper left', fontsize = 11)
    axs[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    fig.align_ylabels(axs[:])
    for i in range(3):
        axs[i].grid(visible = None, axis = 'both', color = '0.95')
        axs[i].set_axisbelow(True)

    fig.savefig(outputDirectory + "PtBroad_Zh_Target.pdf", bbox_inches = 'tight')
    print(outputDirectory + "PtBroad_Zh_Target-Grid.pdf Has been created")



def PtBroadZhNPionSplit():

    fig, axs = plt.subplots(1, nPion, sharey = 'row', sharex = 'col')
    width  = (16/3)*nPion 
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None, wspace = 0.02,
                        hspace = 0.02)

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")

    tarList   = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]

    for i in range(3): # Loops on the diffrent targets
        for j in range(nPion): # Loops on the number of pions
            axs[j].set_ylim(0, ZhYlimit)
            axs[j].set_xlim(0.075, 1.03)
            graphName = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
            graph     = file.Get(graphName)
            nPoints = graph.GetN()
            x  = np.ndarray(nPoints, dtype = float, buffer = graph.GetX())
            x  = x + (-ZhShift + ZhShift*2*i)
            y  = np.ndarray(nPoints, dtype = float, buffer = graph.GetY())
            ey = np.ndarray(nPoints, dtype = float, buffer = graph.GetEY())
            axs[j].errorbar(x, y, ey, marker = "o", linestyle = "", label = tarList[i],
                            color = colorList[i], markersize = 6, markerfacecolor = colorList[i])

    axs[0].set_ylabel(r'$\Delta P_\mathrm{T}^{2} [GeV^{2}]$', loc = "center", fontsize = 15)
    axs[0].set_xlabel(r'$Z_\mathrm{h}$', fontsize = 14)
    axs[1].set_xlabel(r'$Z_\mathrm{h}$', fontsize = 14)

    axs[0].annotate(r'One Pion', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[1].annotate(r'Two Pion', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    axs[0].legend(frameon = False, loc = 'upper left', fontsize = 11)
    axs[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    fig.align_ylabels(axs[:])
    # fig.savefig(outputDirectory + "PtBroad_Zh_NPion.pdf", bbox_inches = 'tight')
    # print(outputDirectory + "PtBroad_Zh_NPion.pdf Has been created")

    for i in range(nPion):
        axs[i].grid(visible = None, axis = 'both', color = '0.95')
        axs[i].set_axisbelow(True)

    fig.savefig(outputDirectory + "PtBroad_Zh_NPion.pdf", bbox_inches = 'tight')
    # print(outputDirectory + "PtBroad_Zh_NPion-Grid.pdf Has been created")
    file.Close()



def PtBroadFullIntegrated():

    fig, axs = plt.subplots(1, 1, constrained_layout = True)
    # For one column
    width  = 6
    height = width / 1.2
    fig.set_size_inches(width, height)

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_FullIntegrated.root", "READ")

    # AddCLasPleliminary(Axs)
    for i in range(3): # Loops on the diffrent targets
        for j in range(nPion): # Loops on the number of pions
            axs.set_ylim(0, FullYlimit)
            axs.set_xlim(1.5, 6.5)
            graphName = "PtBroad_FullIntegrated_" + tarList[i] + "_" + str(j+1)
            graph     = file.Get(graphName)
            nPoints = graph.GetN()
            x  = np.ndarray(nPoints, dtype = float, buffer = graph.GetX())
            x  = x + (-FullShft + FullShft*2*j)
            y  = np.ndarray(nPoints, dtype = float, buffer = graph.GetY())
            ey = np.ndarray(nPoints, dtype = float, buffer = graph.GetEY())
            if j == 0:
                axs.errorbar(x, y, ey, marker = markerList[j], linestyle = "",
                             markerfacecolor = colorList[i], color = colorList[i], 
                             markersize = 4.5, label = tarList[i])
            if i == 2:
                axs.errorbar(x, y, ey, marker = markerList[j], linestyle = "", 
                             markerfacecolor = "grey", color = colorList[i], markersize = 4.5,
                             label = nPionList[j])

            axs.errorbar(x, y, ey, marker = markerList[j], linestyle = "", 
                         markerfacecolor = colorList[i], color = colorList[i], markersize = 4.5, 
                         label = None)



    axs.set_ylabel(r'$\Delta P_\mathrm{T}^{2} [GeV^{2}]$', loc = "center", fontsize = 15)
    axs.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))


    axs.set_xlabel(r'$A^\mathrm{\frac{1}{3}}$', loc = "center", fontsize = 14)


    axs.legend(ncol = 2, frameon = False, loc = 'upper left', fontsize = 11)

    # fig.savefig(outputDirectory + "PtBroad_FullIntegrated.pdf", bbox_inches = 'tight')
    # print(outputDirectory + "PtBroad_FullIntegrated.pdf Has been created")

    axs.grid(visible = None, axis = 'both', color = '0.95')
    axs.set_axisbelow(True)

    fig.savefig(outputDirectory + "PtBroad_FullIntegrated.pdf", bbox_inches = 'tight')
    print(outputDirectory + "PtBroad_FullIntegrated-Grid.pdf Has been created")
    
    file.Close()



def CalculateTotalSystematic(systematics, sysErrorArray, i, j):

    fileNominal = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")
    graphName   = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
    graphNom    = fileNominal.Get(graphName)
    nPoints = graphNom.GetN()
    nomValues  = np.ndarray(nPoints, dtype = float, buffer = graphNom.GetY())
    fileNominal.Close()
 
    for systematic in systematics:
        fileSystematic = [ROOT.TFile.Open(systematicDirectory + systematic[0] + 
                                          "/Pt_broad_Zh.root", "READ"),
                           ROOT.TFile.Open(systematicDirectory + systematic[1] + 
                                           "/Pt_broad_Zh.root", "READ")]
        graphSys     = [fileSystematic[0].Get(graphName), 
                        fileSystematic[1].Get(graphName)]
        SysValues = [np.ndarray(nPoints, dtype = float, buffer = graphSys[0].GetY()),
                     np.ndarray(nPoints, dtype = float, buffer = graphSys[1].GetY())]
        
        print(nomValues-SysValues)
        sysErrorArray += np.square(np.maximum(np.absolute(nomValues-SysValues[0]), 
                                              np.absolute(nomValues-SysValues[1]))/3**.5)
        fileSystematic[0].Close()
        fileSystematic[1].Close()
    
    sysErrorArray = np.sqrt(sysErrorArray)


systematicDiccionary = { "C"  : [np.repeat(0., 8), np.repeat(0., 8)],
                         "Fe" : [np.repeat(0., 8), np.repeat(0., 8)],
                         "Pb" : [np.repeat(0., 8), np.repeat(0., 8)],
                       }

systematics = [["Normal", "Cutoff"], ["70Bins", "110Bins"], ["DZLow",  "DZHigh"],
               ["VC_RD",  "VC_HH"], ["TOFLow", "TOFHigh"], ["NAccept0", "NAccept2"]] 
               


def CallCalculateTotalSystemtic(systematicDiccionary):

    for i in range(3): # Loops on the diffrent targets
        for j in range(nPion): # Loops on the number of pions
            CalculateTotalSystematic(systematics, systematicDiccionary[tarList[i]][j], i, j)
            # print(systematicDiccionary[tarList[i]][j])



# CallCalculateTotalSystemtic(systematicDiccionary)
# print(systematicDiccionary)

# Call funtions
PtBroadZhTarSplit()
PtBroadZhNPionSplit()
PtBroadFullIntegrated()
