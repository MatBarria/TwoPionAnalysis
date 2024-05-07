import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import uproot as ur
import os
from include import SaveFigure

from include import dataDirectory, outputDirectory, binning

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

nPion = 2

tarList = ['C', "Fe", "Pb", 'DC', "DFe", "DPb"]
colorList = ['#301437', 'orange', "lightgreen"]
nPionList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]

nBins = 60

binningDist = {'Q2':     np.linspace(1.,    4.,   nBins),
               'Nu':     np.linspace(2.2,   4.26, nBins),
               'Zh':     np.linspace(0.,    1.,   nBins),
               'Pt2':    np.linspace(0.,    1.5,   nBins),
               'PhiPQ':  np.linspace(-180., 180., nBins),
               }

xLabel = {"Q2":    r'$Q^2$[GeV^2]',
          "Nu":    r'$\nu$[GeV]',
          "Zh":    r'$Zh_\mathrm{Sum}$',
          # "Pt2":   r'$P_t^2 [GeV^2]$',
          "Pt2":   r'$P_t^{+2} [GeV^2]$',
          "PhiPQ": r'$\phi_{PQ}[Deg]$'
          }

yLabel = {"Q2":    r'$dN/dQ^2$',
          "Nu":    r'$dN/d\nu$',
          "Zh":    r'$dN/dZh_\mathrm{Sum}$',
          # "Pt2":   r'$dN/dP_t^2$',
          "Pt2":   r'$dN/dP_t^{+2}$',
          "PhiPQ": r'$dN/d\phi_{PQ}$'
          }

dicColor = {"Data": "#301437",
            "Gen":  "orange",
            "Rec":  "lightgreen"
            }

dicLabel = {"Data": ["Data", "Data: Two $\pi^+", "Data"],
            "Gen": ["Gen",  "Gen: Two $\pi^+", "Data"],
            "Rec": ["Rec",  "Rec: Two $\pi^+", "Data"]
            }

lineStyle = ["-", "-", "-"]

xLowLimit = {"Q2": 0.8, "Nu": 2.1, "Zh": 0., "Pt2": 0,  "PhiPQ": -180}
xHighLimit = {"Q2": 4, "Nu": 4.32, "Zh": 1.05, "Pt2": 1.5, "PhiPQ": 180}
yLimit = {"Q2": 0.01, "Nu": 0.01, "Zh": 0.01, "Pt2": 0.01, "PhiPQ": 0.01}

variables = ["Q2", "Nu", "Zh", "Pt2", "PhiPQ"]
# variables = ["Pt2", "PhiPQ"]
# variables = ["Nu"]


def SimVsData(var, pions):

    fig, axs = plt.subplots(1, 1, constrained_layout=True)
    # For one column
    width = 6
    height = width / 1.2
    fig.set_size_inches(width, height)

    outDir = outputDirectory + "Dist/"
    # Create the directory if doesn't exist
    os.makedirs(outDir, exist_ok=True)
    # dic = {"Data" : np.array([]), "ZhBin" : np.array([])}
    for i in range(1):  # Loops on the number of pions

        with ur.open(dataDirectory + "VecSum_Fe.root:ntuple_" +
                     str(pions) + "_pion") as file:
            dicData = file.arrays([var, "VC_TM"], library="np")

        # dicData[var] = dicData[var][dicData["VC_TM"] == 2]
        axs.hist(dicData[var][dicData["VC_TM"] == 2], bins=binningDist[var],
                 weights = np.ones_like(dicData[var][dicData["VC_TM"] == 2]) / float(len(dicData[var][dicData["VC_TM"] == 2])),
                 color='red', histtype="step", label="Solid Target",
                       linestyle=lineStyle[1])
        
        axs.hist(dicData[var][dicData["VC_TM"] == 1], bins=binningDist[var],
                 weights = np.ones_like(dicData[var][dicData["VC_TM"] == 1]) / float(len(dicData[var][dicData["VC_TM"] == 1])),
                 color="blue", histtype="step", label="Liquid Target",
                       linestyle=lineStyle[1])

        # if var == "Pt2":
            # axs.set_yscale('log')
            # axs.set_yscale('log')
            # axs.set_ylim(0.0000001, 1)
            # axs.set_ylim(0.0000001, 1)

        axs.tick_params(right=False, top=False, which='both')

        axs.set_xlabel(xLabel[var], fontsize=14)

        axs.set_ylabel(yLabel[var], loc="center", fontsize=15)

    axs.annotate(r'' + nPionList[pions - 1] + " events", xy=(0.5, 1.04),
                      xycoords='axes fraction', fontsize=15)
    axs.legend(frameon=False, loc='best', fontsize=11)

    SaveFigure(fig, outDir , var + str(pions) + "_dist")



for var in variables:
    SimVsData(var, 1)
    SimVsData(var, 2)

# SimVsData("Pt2", 2)
# SimVsData("Pt2", 1)
# SimVsDataPt2Zh(7)
