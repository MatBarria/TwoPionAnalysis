import ROOT
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import os
from include_rc import inputDirectory, outputDirectory

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2
NZh = 8
nPion = 2

tarList = ["C", "Fe", "Pb","DC", "DFe", "DPb"]

def Pt2Distribution():


    fileAcc = ROOT.TFile.Open(inputDirectory + "Pt2_Distribution.root", "READ")
    fileRc  = ROOT.TFile.Open(inputDirectory + "Pt2_Distribution_Rc.root", "READ")

    os.makedirs(outputDirectory + 'Pt2DistRc/', exist_ok = True) # Create it if doesn't exist

    for i in range(6): # Loops on the diffrent targets
        for j in range(nPion): # Loops on the number of pions
            for k in range(NZh): # Loops on Zh bins

                fig, axs = plt.subplots(1, 1, constrained_layout = True)
                # For one column
                width  = 6
                height = width / 1.2
                fig.set_size_inches(width, height)

                graphNameAcc = "Pt2_Distribution_" + tarList[i] + "_" + str(k) + "_" + str(j+1)
                graphNameRc  = "Pt2_Distribution_Rc_"  + tarList[i] + "_" + str(k) + "_" + str(j+1)
                graphAcc     = fileAcc.Get(graphNameAcc)
                graphRc      = fileRc.Get(graphNameRc)
                nPoints = [graphAcc.GetN(), graphRc.GetN()]
                x  = [np.ndarray(nPoints[0], dtype = float, buffer = graphAcc.GetX()),
                      np.ndarray(nPoints[1], dtype = float, buffer = graphRc.GetX())]
                y  = [np.ndarray(nPoints[0], dtype = float, buffer = graphAcc.GetY()),
                      np.ndarray(nPoints[1], dtype = float, buffer = graphRc.GetY())]
                ey = [np.ndarray(nPoints[0], dtype = float, buffer = graphAcc.GetEY()),
                      np.ndarray(nPoints[1], dtype = float, buffer = graphRc.GetEY())]

                axs.errorbar(x[0], y[0], ey[0], marker = "o" , linestyle = "", color = "red",
                             markerfacecolor = "red", markersize = 4.5, label = "Acc")
                axs.errorbar(x[1], y[1], ey[1], marker = "o" , linestyle = "", color = "black", 
                             markerfacecolor = "black", markersize = 4.5, label = "Acc + Rc")

                axs.set_yscale('log')
                axs.set_ylabel(r'$counts$', loc = "center", fontsize = 15)

                axs.set_xlabel(r'$P_\mathrm{T}^{2} [GeV^{2}]$', loc = "center", fontsize = 14)


                axs.legend(ncol = 2, frameon = False, loc = 'upper left', fontsize = 11)

                axs.grid(visible = None, axis = 'both', color = '0.95')
                axs.set_axisbelow(True)


                fig.savefig(outputDirectory + 'Pt2DistRc/' + tarList[i] + str(j+1) + str(k) + 
                            "Pt2Dist.pdf", bbox_inches = 'tight')
                # fig.savefig('my_fig.png', dpi=8)
                print(outputDirectory +  'Pt2DistRc/' + tarList[i] + str(j+1) + str(k) + 
                      "Pt2Dist.pdf Has been created")


    fileAcc.Close()
    fileRc.Close()

Pt2Distribution()
