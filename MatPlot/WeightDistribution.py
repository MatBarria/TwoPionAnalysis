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

tarList    = ['C', "Fe", "Pb"]
colorList  = ['#301437', 'orange', "lightgreen"]
nPionList  = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]


def WeightsDistribution():

    vars = ['weight' , 'Zh']
    fig, axs = plt.subplots(1, 1, sharey = 'row', sharex = 'col')
    width  = 6
    height = 6/1.2 
    fig.set_size_inches(width, height)
    

    fig, axs = plt.subplots(1, 1, sharey = 'row', sharex = 'col')
    width  = 6
    height = 6/1.2 
    fig.set_size_inches(width, height)
    axs.set_xlim(0.0, 3.)
        # AddCLasPleliminary(axs[i])
    axs.set_ylim(0, 0.1)
    weights = np.array([])
    Zh = np.array([])

    for j in range(nPion): # Loops on the number of pions
        for i in range(3): # Loops on the diffrent targets

            with ur.open(inputDirectory + 
                "WeightTuple.root:ntuple_" + tarList[i] + "_" + str(j+1)) as file:
                factors  = file.arrays(vars, library = "np")
                weights = np.concatenate((weights, factors['weight']), axis = 0)
                Zh = np.concatenate((Zh, factors['Zh']), axis = 0)
        
        # print(weights)
        # print("-----")
        # print(Zh)
        # weights = weights[Zh == 7]
        weightsHist = np.ones_like(weights) / float(len(weights))
        axs.hist(weights, bins = 110, range = (-0., 3.1), weights = weightsHist, 
                 color = colorList[j], histtype="step", label = nPionList[j])

        weights = np.array([])
        Zh = np.array([])

    axs.tick_params(right = False, top = False, which = 'both')
    axs.set_xlabel(r'Weights', fontsize = 14)
    axs.set_ylabel(r'$dN/d(w)$' , loc = "center", fontsize = 15)

    if draw_label: 
        axs.legend(frameon = False, loc = 'upper right', fontsize = 11)

    fig.savefig(outputDirectory +  "WeightsDistribution.pdf", bbox_inches = 'tight')
    print(outputDirectory +  "WeightsDistribution.pdf Has been created")


def WeightsDistribution2D():

    vars = ['weight' , 'Zh', 'Pt2']
    fig, axs = plt.subplots(1, 1, sharey = 'row', sharex = 'col')
    width  = 6
    height = 6/1.2 
    fig.set_size_inches(width, height)
    

    fig, axs = plt.subplots(1, 1, sharey = 'row', sharex = 'col')
    width  = 6
    height = 6/1.2 
    fig.set_size_inches(width, height)
    axs.set_xlim(0.0, 2.)
        # AddCLasPleliminary(axs[i])
    axs.set_ylim(0, 0.08)
    weights = np.array([])
    Zh = np.array([])
    Pt2 = np.array([])
    weightsHist = np.array([]);

    binsX = np.linspace(0., 3, num = 60)
    binsY = np.linspace(0., 2, num = 100)
    cm = plt.cm.twilight_shifted
    
    for j in range(1, 2): # Loops on the number of pions
        for i in range(3): # Loops on the diffrent targets

            with ur.open(inputDirectory + 
                "WeightTuple.root:ntuple_" + tarList[i] + "_" + str(j+1)) as file:
                factors  = file.arrays(vars, library = "np")
                weights = np.concatenate((weights, factors['weight']), axis = 0)
                Zh = np.concatenate((Zh, factors['Zh']), axis = 0)
                Pt2 = np.concatenate((Pt2, factors['Pt2']), axis = 0)
        
            with ur.open(inputDirectory + 
                "WeightTuple.root:ntuple_D" + tarList[i] + "_" + str(j+1)) as file:
                factors  = file.arrays(vars, library = "np")
                weights = np.concatenate((weights, factors['weight']), axis = 0)
                Zh = np.concatenate((Zh, factors['Zh']), axis = 0)
                Pt2 = np.concatenate((Pt2, factors['Pt2']), axis = 0)

        # print(weights)
        # print("-----")
        # weights = weights[Zh != 7]
        # Pt2 = Pt2[Zh != 7]
        # Zh = Zh[Zh != 7]
        # weights = weights[Zh != 1]
        # Pt2 = Pt
        print("weights original: ")
        print(weights)

        weightsHist = Zh;

        print("weights original after copy: ")
        print(weights)
        
        print(Pt2)
        for k in range(60):
            if float(len(weights[Pt2 == k])) != 0 :
                weightsHist[Pt2 == k] = 1 / float(len(weights[Pt2 == k]))
            else:
                weightsHist[Pt2 == k] = 0

        
        Pt2 = Pt2*(3/60)

        print(Pt2)
        print("weights original: ")
        print(weights)
        print("weights hist: ")
        print(weightsHist)

        axs.hist2d(Pt2, weights, bins = (binsX, binsY), weights = weightsHist, cmap = cm, 
                   rasterized = True) 


        weights = np.array([])
        Zh = np.array([])
        Pt2 = np.array([])
        weightsHist = np.array([]);

    axs.tick_params(right = False, top = False, which = 'both')
    axs.set_xlabel(r'Weights', fontsize = 14)
    axs.set_ylabel(r'$dN/d(Acc)$' , loc = "center", fontsize = 15)


    fig.savefig(outputDirectory +  "WeightsDistribution2D.pdf", bbox_inches = 'tight')
    print(outputDirectory +  "WeightsDistribution2d.pdf Has been created")

WeightsDistribution()
WeightsDistribution2D()
