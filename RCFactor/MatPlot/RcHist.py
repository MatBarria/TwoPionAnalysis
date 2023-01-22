import ROOT
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from include_rc import inputDirectory, outputDirectory

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

def RcFactorsHistZhDiffTarSplit():

    tarList    = ["C", "Fe", "Pb", "DC", "DFe", "DPb"]
    colorList  = ["r", "b", "y", "g"]
    ecList  = ["darkred", "darkblue", "gold", "darkgreen"]
    labelList  = ["$0.1<Z_h<0.4$", "$0.4<Z_h<0.6$", "$0.6<Z_h<0.8$", "$0.8<Z_h<1.0$"]
    bins = np.linspace(0.0, 2.0, num = 81)

    for i in range(1, nPion):  # Loops in number of pions
        fig, axs = plt.subplots(2, 3, sharey = 'row', sharex = 'col')
        width  = 16 #7.056870070568701
        height = 8
        fig.set_size_inches(width, height)

        fig.subplots_adjust(left = None, bottom = None, right = None, top = None, wspace = 0.02,
                             hspace = 0.2)
        file = ROOT.TFile.Open(inputDirectory + "RcTuples.root", "READ")
        for a in range(2):
            for j in range(3): # Loops in diffrent solid targets
                emptyList = []
                AllRcFactors = [np.empty(emptyList), np.empty(emptyList), np.empty(emptyList),
                                np.empty(emptyList)]
                for k in range(1, 4): # Loops in bins of Zh
                    RcFactorsList    = []
                    tupleName    = "RcTuple_" + tarList[j+3*a] + "_" + str(k) + "_" + str(i)
                    tuple        = file.Get(tupleName)
                    for event in tuple:
                        # print(event.Rc)
                        RcFactorsList.append(event.Rc)

                    RcFactorsArray = np.array(RcFactorsList)
                    AllRcFactors[0] = np.append(AllRcFactors[0], RcFactorsArray)

                for k in range(4, 6): # Loops in bins of Zh
                    RcFactorsList    = []
                    tupleName    = "RcTuple_" + tarList[j+3*a] + "_" + str(k) + "_" + str(i)
                    tuple        = file.Get(tupleName)
                    for event in tuple:
                        # print(event.Rc)
                        RcFactorsList.append(event.Rc)

                    RcFactorsArray = np.array(RcFactorsList)
                    AllRcFactors[1] = np.append(AllRcFactors[1], RcFactorsArray)

                for k in range(6, 7): # Loops in bins of Zh
                    RcFactorsList    = []
                    tupleName    = "RcTuple_" + tarList[j+3*a] + "_" + str(k) + "_" + str(i)
                    tuple        = file.Get(tupleName)
                    for event in tuple:
                        # print(event.Rc)
                        RcFactorsList.append(event.Rc)

                    RcFactorsArray = np.array(RcFactorsList)
                    AllRcFactors[2] = np.append(AllRcFactors[2], RcFactorsArray)

                for k in range(7, 8): # Loops in bins of Zh
                    RcFactorsList    = []
                    tupleName    = "RcTuple_" + tarList[j+3*a] + "_" + str(k) + "_" + str(i)
                    tuple        = file.Get(tupleName)
                    for event in tuple:
                        # print(event.Rc)
                        RcFactorsList.append(event.Rc)

                    RcFactorsArray = np.array(RcFactorsList)
                    AllRcFactors[3] = np.append(AllRcFactors[3], RcFactorsArray)

                if a == 0 and j == 0:
                    axs[a, j].hist(AllRcFactors[0], bins, color = colorList[0], ec = "black",
                                  label = labelList[0], alpha = 0.5)
                    axs[a, j].hist(AllRcFactors[1], bins, color = colorList[1], ec = "black", 
                                  label = labelList[1], alpha = 0.5)
                    axs[a, j].hist(AllRcFactors[2], bins, color = colorList[2], ec = "black", 
                                  label = labelList[2], alpha = 0.5)
                    axs[a, j].hist(AllRcFactors[3], bins, color = colorList[3], ec = "black", 
                                  label = labelList[3], alpha = 0.5)
                else:
                    axs[a, j].hist(AllRcFactors[0], bins, color = colorList[0], ec = "black", 
                                  alpha = 0.5)
                    axs[a, j].hist(AllRcFactors[1], bins, color = colorList[1], ec = "black", 
                                  alpha = 0.5)
                    axs[a, j].hist(AllRcFactors[2], bins, color = colorList[2], ec = "black", 
                                  alpha = 0.5)
                    axs[a, j].hist(AllRcFactors[3], bins, color = colorList[3], ec = "black", 
                                  alpha = 0.5)



        for j in range(2):
            for q in range(3):
                axs[j, q].set_xticks([0.1, 0.55, 1, 1.45, 1.9])
            axs[j, 0].set_ylabel(r'$Counts$', loc = "center", fontsize = 15)
            axs[j, 0].set_xlabel(r'Rc Factors', fontsize = 12)
            axs[j, 1].set_xlabel(r'Rc Factors', fontsize = 12)
            axs[j, 2].set_xlabel(r'Rc Factors', fontsize = 12)

        axs[0, 0].annotate(r'C',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
        axs[0, 1].annotate(r'Fe',  xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
        axs[0, 2].annotate(r'Pb',  xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
        axs[1, 0].annotate(r'DC',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
        axs[1, 1].annotate(r'DFe',  xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
        axs[1, 2].annotate(r'DPb',  xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)



        axs[0, 0].legend(frameon = False, loc = 'upper left', fontsize = 11)


        fig.align_ylabels(axs[:])
        fig.savefig(outputDirectory + "RcFactors_" + str(i) + "_NPionZhDiff-hist.pdf",
                    bbox_inches = 'tight')
        file.Close()
        print(outputDirectory + "RcFactors_" + str(i) + "_NPionZhDiff-hist.pdf Has been created")


RcFactorsHistZhDiffTarSplit()
