import ROOT
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import mplhep as hep

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

#Shift the data on Zh to make the plot more readability
ZhShift  = 0.015

# Upper limmit in the y axis
YLimit = 40

nPion = 2
N_Zh  = 8

ZhBinning = [0.075, 0.2, 0.3, 0.4,0.5, 0.6, 0.8, 1.03]

binsLabels = { "50" : "50 bins",
         "60" : "60 bins",
         "70" : "70 bins",
         "80" : "80 bins",
         "90" : "90 bins",
                 }

tarList      = ["C", "Fe", "Pb"]
colorListSys = ["darkred", "darkBlue", "black"]
colorListNom = ["red", "Blue", "black"]
markerList   = ["^", "v", "o", "s", "D"]
labelListNom = ["Sta. Error One $\pi +$", "Sta. Error Two $\pi+$", "Sta. Error Three $\pi +$"]

binDirectory = "/home/matias/proyecto/TwoPionAnalysis/Data/Bins/"
plotDir = "/home/matias/proyecto/TwoPionAnalysis/Plots/Bins/" 
ZhYlimit   = 0.09

def SystematicError(systematic):

    fig, axs = plt.subplots(nPion, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4*nPion
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None, wspace = 0.02,
                        hspace = 0.3)

    # fileSystematic = ROOT.TFile.Open(inputDirectory + "Percentaje.root", "READ")
    fileSystematic = [ROOT.TFile.Open(binDirectory + "50" + "/Pt_broad_Zh.root", 
                                     "READ"),
                      ROOT.TFile.Open(binDirectory + "70" + "/Pt_broad_Zh.root", 
                                      "READ"),
                      ROOT.TFile.Open(binDirectory + "80"+ "/Pt_broad_Zh.root", 
                                      "READ"),
                      ROOT.TFile.Open(binDirectory + "90" + "/Pt_broad_Zh.root", 
                                      "READ")]
    fileNominal    = ROOT.TFile.Open(binDirectory + "60" + "/Pt_broad_Zh.root", "READ")


    for i in range(3): # Loops on the diffrent targets
        for j in range(nPion): # Loops on the number of pions

            axs[j][i].set_ylim(0, YLimit)
            axs[j][i].set_xlim(0.075, 1.03)
            graphNameNom = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
            graphNom     = fileNominal.Get(graphNameNom)

            nPointsNom = graphNom.GetN()
            y  = np.ndarray(nPointsNom, dtype = float, buffer = graphNom.GetY())
            ey = np.ndarray(nPointsNom, dtype = float, buffer = graphNom.GetEY())
            for s in range(3):

                graphNameSys = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
                graphSys     = fileSystematic[s].Get(graphNameSys)

                # Extrac the data from the TGraph
                nPointsSys = graphSys.GetN()
                xSys  = np.ndarray(nPointsSys, dtype = float, buffer = graphSys.GetX())
                ySys  = np.ndarray(nPointsSys, dtype = float, buffer = graphSys.GetY())

                print("target: " + tarList[i])
                print("N pions: " + str(j+1))
                print("Sys: " + systematic[s])
                ySys = np.absolute((y-ySys)/ySys)*100              
                print(ySys)

                # Generate the plot
                axs[j][i].plot(xSys, ySys, marker = markerList[s], linestyle = "", 
                               color = colorListSys[j], markerfacecolor = colorListSys[j], 
                               markersize = 6, label = binsLabels[systematic[s]])

                # Extrac the data from the TGraph

            # print("Nom y: " + tarList[i] + str(j))
            # print(y)
            # print("Nom y error: "+ tarList[i] + str(j))
            # print(ey)
            NomError = [0,0,0,0,0,0,0,0]

            NomError[0] = (ey[1]*100)/y[1]
            NomError[N_Zh-1] = (ey[N_Zh-1]*100)/y[N_Zh-1]
            for k in range(N_Zh-1):
                NomError[k+1] = (ey[k+1]*100)/y[k+1]


            axs[j][i].fill_between(ZhBinning, NomError, step = 'pre',
                                   color = colorListNom[j], label = labelListNom[j], 
                                   linewidth = 1.0, alpha = 0.3)            

            axs[j][i].step(ZhBinning, NomError, color = colorListNom[j], linewidth = 1.0)            

    # Set the labels for the three plots

    fileNominal.Close()
    fileSystematic[0].Close()
    fileSystematic[1].Close()

    for i in range(nPion):
        axs[i][0].set_ylabel(r'Devation from Nominal(%)', loc = "center", fontsize = 15)
        axs[i][0].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
        axs[i][1].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
        axs[i][2].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)

        axs[i][0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', 
                           fontsize = 15)
        axs[i][1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction',
                           fontsize = 15)
        axs[i][2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', 
                           fontsize = 15)

        axs[i][0].legend(frameon = False, loc = 'upper center', fontsize = 11)

    fig.align_ylabels(axs[:])

    for i in range(3):
        for j in range(nPion):
            axs[j][i].grid(visible = None, axis = 'both', color = '0.95')
            axs[j][i].set_axisbelow(True)

    fig.savefig(plotDir + "BinsVariation.pdf", 
                bbox_inches = 'tight')
    print("/home/matias/proyecto/TwoPionAnalysis/Plots/Bins/" + 
          "BinsVariation.pdf Has been created")

def PtBroadZhTarSplit():

    fig, axs = plt.subplots(1, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None,
                        wspace = 0.02, hspace = 0.02)

    file = [ROOT.TFile.Open(binDirectory + "50" + "/Pt_broad_Zh.root", 
                                     "READ"),
                      ROOT.TFile.Open(binDirectory + "60" + "/Pt_broad_Zh.root", 
                                      "READ"),
                      ROOT.TFile.Open(binDirectory + "70"+ "/Pt_broad_Zh.root", 
                                      "READ"),
                      ROOT.TFile.Open(binDirectory + "80"+ "/Pt_broad_Zh.root", 
                                      "READ"),
                      ROOT.TFile.Open(binDirectory + "90" + "/Pt_broad_Zh.root", 
                                      "READ")]
    tarList   = ["C", "Fe", "Pb"]
    colorList = ["red", "Blue", "black"]
    labelList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]

    for f in range(5):
        for i in range(3): # Loops on the diffrent targets
            # AddCLasPleliminary(axs[i])
            axs[i].set_ylim(0, ZhYlimit)
            axs[i].set_xlim(0.075, 1.03)
            for j in range(nPion): # Loops on the number of pions
                graphName = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
                graph     = file[f].Get(graphName)
                # Extrac the data from the TGraph
                nPoints = graph.GetN()
                x  = np.ndarray(nPoints, dtype = float, buffer = graph.GetX())
                x  = x + (-ZhShift + ZhShift*2*j) # Shit the data for readability
                y  = np.ndarray(nPoints, dtype = float, buffer = graph.GetY())
                ey = np.ndarray(nPoints, dtype = float, buffer = graph.GetEY())
                # print(ey)
                # Generate the plot
                axs[i].errorbar(x, y, ey, marker = markerList[f], linestyle = "",
                                markerfacecolor = colorList[j], color = colorList[j], 
                                markersize = 6, label = labelList[j])
            # container = axs[i].errorbar(x, y, ey + systematicDiccionary[tarList[i]][j], 
                                        # marker = "", linestyle = "", markerfacecolor = colorList[j], lw = 0,
                                        # color = colorList[j], markersize = 0, alpha = 0.2, capsize = 5)

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

    fig.savefig(plotDir + "BinsVariationBroad.pdf", 
                bbox_inches = 'tight')
    print( "PtBroad_Zh_Target-Grid.pdf Has been created")

SystematicError(["50", "70", "80", "90"])
PtBroadZhTarSplit()
