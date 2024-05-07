import ROOT
import numpy as np
import matplotlib.pyplot as plt
from include import inputDirectory, SaveFigure, AddCLasPleliminary
from include import outputDirectory as outDir
import mplhep as hep
import os

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

NZh = 8
nPion = 2

tarList = ["C", "Fe", "Pb", "DC", "DFe", "DPb"]
labelList = ["> cutoff", "Distribution", "Interpolated values"]
colorList = ["red", "black", "blue"]

CLASPreliminaryFlag = True


def Pt2Distribution():

    outputDirectory = outDir + "Pt2Dist/"
    # Create the directory if doesn't exist
    os.makedirs(outputDirectory, exist_ok=True)
    file = ROOT.TFile.Open(inputDirectory + "Pt2_Distribution.root", "READ")

    for i in range(6):  # Loops on the diffrent targets
        for j in range(nPion):  # Loops on the number of pions
            for k in range(1, NZh):  # Loops on Zh bins
                for Q2 in range(3):  # Loops on Zh bins
                    for Nu in range(3):  # Loops on Zh bins

                        fig, axs = plt.subplots(1, 1, constrained_layout=True)
                        # For one column
                        width = 6
                        height = width / 1.2
                        fig.set_size_inches(width, height)

                        graphName = ["Pt2_Distribution_" + tarList[i] + "_" + str(Q2) + str(Nu) + str(k) + "_" + str(j+1),
                                     "Pt2_Distribution_Clean_" +
                                     tarList[i] + "_" + str(Q2) + str(Nu) +
                                     str(k) + "_" + str(j+1),
                                     "Pt2_Distribution_Inter_" + tarList[i] + "_" + str(Q2) + str(Nu) + str(k) + "_" + str(j+1)]
                        order = [0, 2, 1]
                        for n in order:
                            graph = file.Get(graphName[n])
                            nPoints = graph.GetN()
                            x = np.ndarray(nPoints, dtype=float,
                                           buffer=graph.GetX())
                            y = np.ndarray(nPoints, dtype=float,
                                           buffer=graph.GetY())
                            ey = np.ndarray(nPoints, dtype=float,
                                            buffer=graph.GetEY())

                            axs.errorbar(x, y, ey, marker="o", linestyle="",
                                         markerfacecolor=colorList[n], color=colorList[n],
                                         markersize=4.5, label=labelList[n])

                        axs.set_yscale('log')
                        axs.set_ylabel(r'$counts$', loc="center", fontsize=15)

                        axs.set_xlabel(
                            r'$P_\mathrm{T}^{+2} [GeV^{2}]$', loc="center", fontsize=14)
                        axs.legend(ncol=1, frameon=False,
                                   loc='upper right', fontsize=11)

                        axs.grid(visible=None, axis='both', color='0.95')
                        axs.set_axisbelow(True)
                        if CLASPreliminaryFlag:
                            AddCLasPleliminary(axs)

                        SaveFigure(fig, outputDirectory,
                                   tarList[i] + str(j+1) + "-" + str(Q2) + str(Nu) + str(k) + "Pt2Dist")
                        # fig.savefig(outputDirectory + tarList[i] + str(j+1) + str(k) + "Pt2Dist.pdf",
                        # bbox_inches='tight')
                        # print(outputDirectory + tarList[i] + str(j+1) + str(k)
                        # + "Pt2Dist.pdf has been created")

    file.Close()


Pt2Distribution()
