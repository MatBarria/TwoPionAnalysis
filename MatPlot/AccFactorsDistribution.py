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

def AccFactorsDistribution():

    vars = ['Acc', 'FalPos']
    fig, axs = plt.subplots(1, 1, sharey = 'row', sharex = 'col')
    width  = 6
    height = 6/1.2 
    fig.set_size_inches(width, height)
    

    for factor in vars:

        fig, axs = plt.subplots(1, 1, sharey = 'row', sharex = 'col')
        width  = 6
        height = 6/1.2 
        fig.set_size_inches(width, height)
        axs.set_xlim(0.0, 1.)
            # AddCLasPleliminary(axs[i])
        axs.set_ylim(0, .1)
        totalFactors = np.array([])
        for j in range(nPion): # Loops on the number of pions
            for i in range(3): # Loops on the diffrent targets
                with ur.open(inputDirectory + 
                    "AccTuple.root:ntuple_"+ tarList[i] + "_" + str(j+1)) as file:
                    factors  = file.arrays(vars, library = "np")
                    totalFactors = np.concatenate((totalFactors,factors[factor]), axis = 0)

            totalFactors = totalFactors[totalFactors!=0]
            weights = np.ones_like(totalFactors) / float(len(totalFactors))
            axs.hist(totalFactors, bins = 110, range = (-0., 1.1), weights=weights, 
                     color = colorList[j], histtype="step", label = nPionList[j])
            totalFactors = np.array([]) 

        axs.tick_params(right = False, top = False, which = 'both')
        axs.set_xlabel(r'$Factor$', fontsize = 14)
        axs.set_ylabel(r'$dN/d(Factor)$' , loc = "center", fontsize = 15)

        if draw_label: 
            axs.legend(frameon = False, loc = 'upper right', fontsize = 11)
    
        fig.savefig(outputDirectory + factor + "distribution_.pdf", bbox_inches = 'tight')
        print(outputDirectory + factor + "distribution_.pdf Has been created")


def FinalFactorsDistribution():

    vars = ['FinalFactor']
    fig, axs = plt.subplots(1, 1, sharey = 'row', sharex = 'col')
    width  = 6
    height = 6/1.2 
    fig.set_size_inches(width, height)
    


    fig, axs = plt.subplots(1, 1, sharey = 'row', sharex = 'col')
    width  = 6
    height = 6/1.2 
    fig.set_size_inches(width, height)
    axs.set_xlim(0.0, 1.)
        # AddCLasPleliminary(axs[i])
    axs.set_ylim(0, 0.09)
    FFactor = np.array([])
    for j in range(nPion): # Loops on the number of pions
        for i in range(3): # Loops on the diffrent targets
            with ur.open(inputDirectory + 
                "AccTuple.root:ntuple_" + tarList[i] + "_" + str(j+1)) as file:
                factors  = file.arrays(vars, library = "np")
                FFactor = np.concatenate((FFactor,factors['FinalFactor']), axis = 0)
        
        FFactor = FFactor[FFactor != 0]
        weights = np.ones_like(FFactor) / float(len(FFactor))
        axs.hist(FFactor, bins = 110, range = (-0., 1.1), weights=weights, 
                 color = colorList[j], histtype="step", label = nPionList[j])
        FFactor = np.array([])

    axs.tick_params(right = False, top = False, which = 'both')
    axs.set_xlabel(r'$Acc$', fontsize = 14)
    axs.set_ylabel(r'$dN/d(Acc)$' , loc = "center", fontsize = 15)

    if draw_label: 
        axs.legend(frameon = False, loc = 'upper right', fontsize = 11)

    fig.savefig(outputDirectory +  "FinalFactordistribution_.pdf", bbox_inches = 'tight')
    print(outputDirectory +  "FinalFactordistribution_.pdf Has been created")

# AccFactorsDistribution()
FinalFactorsDistribution()
