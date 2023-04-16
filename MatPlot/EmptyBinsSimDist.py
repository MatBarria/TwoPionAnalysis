import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import ScalarFormatter
import matplotlib.mlab as mlab
import mplhep as hep
import uproot as ur
from scipy.optimize import curve_fit

from include import inputDirectory, outputDirectory

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

class ScalarFormatterClass(ScalarFormatter):
   def _set_format(self):
      self.format = "%1.2f"

yScalarFormatter = ScalarFormatterClass(useMathText=True)
yScalarFormatter.set_powerlimits((0,0))

nPion = 2
draw_label = True
# mpl.use('pgf')

tarList    = ['C', "Fe", "Pb", 'DC', "DFe", "DPb"]
colorList  = ['#301437', 'orange', "lightgreen"]
nPionList  = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]

def EmptyBinsSimZhDist():

    vars = ['Data', 'ZhBin']
    fig, axs = plt.subplots(1, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None,
                        wspace = 0.02, hspace = 0.02)

    bins = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    dic = {"Data" : np.array([]), "Zh" : np.array([])}
    for i in range(3): # Loops on the diffrent targets
        for j in range(nPion): # Loops on the number of pions

            with ur.open(inputDirectory + 
                "EmptyBins.root:EmptyBins_"+ tarList[i] + "_" + str(j+1)) as file:
                temp = file.arrays(vars, library = "np")
                dic["Data"] = np.concatenate((dic["Data"],temp['Data']), axis = 0)
                dic["Zh"] = np.concatenate((dic["Zh"],temp['ZhBin']), axis = 0)
            
            weights = dic["Zh"][dic["Data"] == 0]
            for k in range(8):
                if(len(dic["Zh"][dic["Zh"] == k]) == 0):
                    weights[weights == k] = 0
                else:
                    weights[weights == k] = 1/ float(len(dic["Zh"][dic["Zh"] == k]))

            axs[i].hist(dic["Zh"][dic["Data"] == 0], bins = bins, weights = weights,
                 color = colorList[j], histtype="step", label = nPionList[j])
            dic = {"Data" : np.array([]), "Zh" : np.array([])}
            
            with ur.open(inputDirectory + 
                "EmptyBins.root:EmptyBins_D"+ tarList[i] + "_" + str(j+1)) as file:
                temp = file.arrays(vars, library = "np")
                dic["Data"] = np.concatenate((dic["Data"],temp['Data']), axis = 0)
                dic["Zh"] = np.concatenate((dic["Zh"],temp['ZhBin']), axis = 0)
            
            weights = dic["Zh"][dic["Data"] == 0]
            for k in range(8):
                if(len(dic["Zh"][dic["Zh"] == k]) == 0):
                    weights[weights == k] = 0
                else:
                    weights[weights == k] = 1/ float(len(dic["Zh"][dic["Zh"] == k]))

            axs[i].hist(dic["Zh"][dic["Data"] == 0], bins = bins, weights = weights,
                 color = colorList[j], histtype="step", label = nPionList[j], linestyle = "--")
            axs[i].tick_params(right = False, top = False, which = 'both')
            dic = {"Data" : np.array([]), "Zh" : np.array([])}
        
        axs[i].set_xlabel(r'$Zh Bin$', fontsize = 14)

        axs[0].set_ylabel(r'$EmptyBins$' , loc = "center", fontsize = 15)
    
    axs[0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    if draw_label: 
        axs[0].legend(frameon = False, loc = 'upper left', fontsize = 11)

    fig.savefig(outputDirectory + "EmptyBinSimulationZh.pdf", bbox_inches = 'tight')
    print(outputDirectory + "EmptyBinSimulationZh.pdf Has been created")


def EmptyBinsSimPt2Dist():

    vars = ['Data', 'Pt2Bin']
    fig, axs = plt.subplots(1, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None,
                        wspace = 0.02, hspace = 0.02)

    dic = {"Data" : np.array([]), "Pt2" : np.array([])}
    for i in range(3): # Loops on the diffrent targets
        for j in range(nPion): # Loops on the number of pions

            with ur.open(inputDirectory + 
                "EmptyBins.root:EmptyBins_"+ tarList[i] + "_" + str(j+1)) as file:
                temp = file.arrays(vars, library = "np")
                dic["Data"] = np.concatenate((dic["Data"],temp['Data']), axis = 0)
                dic["Pt2"] = np.concatenate((dic["Pt2"],temp['Pt2Bin']), axis = 0)
            
            weights = dic["Pt2"][dic["Data"] == 0]
            for k in range(60):
                if(len(dic["Pt2"][dic["Pt2"] == k]) == 0):
                    weights[weights == k] = 0
                else:
                    weights[weights == k] = 1/ float(len(dic["Pt2"][dic["Pt2"] == k]))

            axs[i].hist(dic["Pt2"][dic["Data"] == 0], bins = 60, range = (0, 60), weights = weights,
                 color = colorList[j], histtype="step", label = nPionList[j])
            dic = {"Data" : np.array([]), "Pt2" : np.array([])}
            
            with ur.open(inputDirectory + 
                "EmptyBins.root:EmptyBins_D"+ tarList[i] + "_" + str(j+1)) as file:
                temp = file.arrays(vars, library = "np")
                dic["Data"] = np.concatenate((dic["Data"],temp['Data']), axis = 0)
                dic["Pt2"] = np.concatenate((dic["Pt2"],temp['Pt2Bin']), axis = 0)
            
            weights = dic["Pt2"][dic["Data"] == 0]
            for k in range(60):
                if(len(dic["Pt2"][dic["Pt2"] == k]) == 0):
                    weights[weights == k] = 0
                else:
                    weights[weights == k] = 1/ float(len(dic["Pt2"][dic["Pt2"] == k]))

            axs[i].hist(dic["Pt2"][dic["Data"] == 0], bins = 60, range = (0, 60), weights = weights,
                 color = colorList[j], histtype="step", label = nPionList[j], linestyle = "--")
            axs[i].tick_params(right = False, top = False, which = 'both')
            dic = {"Data" : np.array([]), "Pt2" : np.array([])}
        
        axs[i].set_xlabel(r'$Pt2 Bin$', fontsize = 14)

        axs[0].set_ylabel(r'$EmptyBins$' , loc = "center", fontsize = 15)
    
    axs[0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    if draw_label: 
        axs[0].legend(frameon = False, loc = 'upper left', fontsize = 11)

    fig.savefig(outputDirectory + "EmptyBinSimulationZh.pdf", bbox_inches = 'tight')
    print(outputDirectory + "EmptyBinSimulationZh.pdf Has been created")

EmptyBinsSimZhDist()
# EmptyBinsSimPt2Dist()
