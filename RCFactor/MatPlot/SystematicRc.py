import ROOT
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from include_rc import inputDirectory, outputDirectory

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

#Shift the data on Zh to make the plot more readability
ZhShift  = 0.015

# Upper limmit in the y axis
YLimit = 50

nPion = 2
N_Zh  = 8

ZhBinning = [0.075, 0.2, 0.3, 0.4,0.5, 0.6, 0.8, 1.03]

def SystematicError():

    fig, axs = plt.subplots(nPion, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4*nPion
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None, wspace = 0.02,
                        hspace = 0.3)

    fileSys = ROOT.TFile.Open(inputDirectory + "Percentaje_Rc.root", "READ")
    fileNominal = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")

    tarList      = ["C", "Fe", "Pb"]
    colorListSys = ["darkred", "darkBlue", "black"]
    colorListNom = ["red", "Blue", "black"]
    labelListSys = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]
    labelListNom = ["Sta. Error One $\pi +$", "Sta. Error Two $\pi+$", "Sta. Error Three $\pi +$"]

    for i in range(3): # Loops on the diffrent targets
        for j in range(nPion): # Loops on the number of pions
            axs[j][i].set_ylim(0, YLimit)
            axs[j][i].set_xlim(0.075, 1.03)
            graphNameSys = "Percentaje_" + tarList[i] + "_" + str(j+1)
            graphSys     = fileSys.Get(graphNameSys)
            # Extrac the data from the TGraph
            nPointsSys = graphSys.GetN()
            xSys  = np.absolute(np.ndarray(nPointsSys, dtype = float, buffer = graphSys.GetX()))
            # xSys  = xSys + (-ZhShift + ZhShift*j) # Shit the data for readability
            ySys  = np.ndarray(nPointsSys, dtype = float, buffer = graphSys.GetY())
            ySys  = ySys*100
            # Generate the plot
            axs[j][i].plot(xSys, ySys, marker = "o", linestyle = "", color = colorListSys[j], 
                     markerfacecolor = colorListSys[j], markersize = 6, label = labelListSys[j])
    
            graphNameNom = "PtBroad_Zh_" + tarList[i] + "_" + str(j)
            graphNom     = fileNominal.Get(graphNameNom)
            # Extrac the data from the TGraph
            nPointsNom = graphNom.GetN()
            y  = np.ndarray(nPointsNom, dtype = float, buffer = graphNom.GetY())
            ey = np.ndarray(nPointsNom, dtype = float, buffer = graphNom.GetEY())
            
            NomError = [0,0,0,0,0,0,0,0]
                
            NomError[0] = (ey[1]*100)/y[1]
            NomError[N_Zh-1] = (ey[N_Zh-1]*100)/y[N_Zh-1]
            for k in range(N_Zh-1):
                NomError[k+1] = (ey[k+1]*100)/y[k+1]
    
            
            axs[j][i].fill_between(ZhBinning, NomError, step = 'pre', color = colorListNom[j],
                                    label = labelListNom[j], linewidth = 1.0, alpha = 0.3)            

            axs[j][i].step(ZhBinning, NomError, color = colorListNom[j], linewidth = 1.0)            

    # Set the labels for the three plots
    for i in range(nPion):
        axs[i][0].set_ylabel(r'Devation from Nominal(%)', loc = "center", fontsize = 15)
        axs[i][0].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
        axs[i][1].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)
        axs[i][2].set_xlabel(r'$Zh_\mathrm{SUM}$', fontsize = 14)

        axs[i][0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
        axs[i][1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
        axs[i][2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

        axs[i][0].legend(frameon = False, loc = 'upper left', fontsize = 11)

    fig.align_ylabels(axs[:])

    for i in range(3):
        for j in range(nPion):
            axs[j][i].grid(visible = None, axis = 'both', color = '0.95')
            axs[j][i].set_axisbelow(True)

    fig.savefig(outputDirectory + "Systematic_Rc.pdf", bbox_inches = 'tight')
    print(outputDirectory + "SystematicRc.pdf Has been created")


SystematicError()
