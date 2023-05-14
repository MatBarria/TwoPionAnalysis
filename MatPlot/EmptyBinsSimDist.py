import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import uproot as ur
import os

from include import inputDirectory, outputDirectory

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

nPion = 2
draw_label = True
# mpl.use('pgf')

tarList    = ['C', "Fe", "Pb", 'DC', "DFe", "DPb"]
# colorList  = ['#301437', 'orange', "lightgreen"]
# disColor = ["blue", "lightgreen"]
disColor  = [ 'blue', '#301437', "lightgreen"]
colorList = ["lightgreen", "orange"]
nPionList  = ["One $\pi^+$", "Two $\pi^+$", "Three $\pi^+$"]

xLabel = { "Q2":    r'$Q^2$[GeV^2]', 
           "Nu":    r'$\nu$[GeV]', 
           "Zh":    r'$Zh_\mathrm{Sum}$',
           "Pt2":   r'$P_t^2 [GeV^2]$', 
           "Phi": r'$\phi_{PQ}[Deg]$'
         }
binning = { "Q2": [1., 1.30, 1.74, 4.00],
            "Nu": [2.2, 3.36, 3.82, 4.26],
            "Zh": [0., .1, .2, .3, .4, .5, .6 , .8 ,1.],
           "Pt2": np.linspace(0, 3, 60),
           "Phi": np.linspace(-180, 180, 6)
           }
ZhLabel = [ r"$0.0< Zh_{Sum} < 0.1$",
            r"$0.1< Zh_{Sum} < 0.2$",
            r"$0.2< Zh_{Sum} < 0.3$",
            r"$0.3< Zh_{Sum} < 0.4$",
            r"$0.4< Zh_{Sum} < 0.5$",
            r"$0.5< Zh_{Sum} < 0.6$",
            r"$0.6< Zh_{Sum} < 0.8$",
            r"$0.8< Zh_{Sum} < 1.0$",
           ]

variables = ["Q2","Nu", "Zh", "Pt2", "Phi"]

outputDirectory = outputDirectory + "EmptyBins/"
os.makedirs(outputDirectory, exist_ok = True) # Create the directory if doesn't exist

def EmptyBinsSimVar(var):

    varBin = var + "Bin"
    vars = ['Data', varBin]

    fig, axs = plt.subplots(1, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None,
                        wspace = 0.02, hspace = 0.02)

    for i in range(3): # Loops on the diffrent targets
        for j in range(nPion): # Loops on the number of pions

            with ur.open(inputDirectory + 
                "EmptyBins.root:EmptyBins_"+ tarList[i] + "_" + str(j+1)) as file:
                dic = file.arrays(vars, library = "np")
            
            
            for t in range(len(dic[varBin])):
                for k in range(len(binning[var])):
                    if dic[varBin][t] == k:
                        dic[varBin][t] = binning[var][k]
            
            weights = dic[varBin][dic["Data"] == 0].copy()

            if var == "Zh":
                axs[i].set_xlim(.1, 1)
                axs[i].set_ylim(0,0.3)

            for k in binning[var]:
                if(len(dic[varBin][dic[varBin] == k]) == 0):
                    weights[weights == k] = 0
                else:
                    weights[weights == k] = 1/ float(len(dic[varBin][dic[varBin] == k]))

            
            axs[i].hist(dic[varBin][dic["Data"] == 0], bins = binning[var], weights = weights,
                 color = colorList[j], histtype="step", label = "Solid - " + nPionList[j])
            
            with ur.open(inputDirectory + 
                "EmptyBins.root:EmptyBins_D"+ tarList[i] + "_" + str(j+1)) as file:
                dic = file.arrays(vars, library = "np")
            
            for t in range(len(dic[varBin])):
                for k in range(len(binning[var])):
                    if dic[varBin][t] == k:
                        dic[varBin][t] = binning[var][k] 
            
            weights = dic[varBin][dic["Data"] == 0].copy()

            for k in binning[var]:
                if(len(dic[varBin][dic[varBin] == k]) == 0):
                    weights[weights == k] = 0
                else:
                    weights[weights == k] = 1/ float(len(dic[varBin][dic[varBin] == k]))
            

            axs[i].hist(dic[varBin][dic["Data"] == 0], bins = binning[var], weights = weights,
                                     color = colorList[j], histtype="step",
                                     label = "Liquid - " + nPionList[j], linestyle = "--")

            axs[i].tick_params(right = False, top = False, which = 'both')
        
        axs[i].set_xlabel(xLabel[var], fontsize = 14)

        axs[0].set_ylabel(r'Empty Bins' , loc = "center", fontsize = 15)
    
    axs[0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    
    axs[0].legend(frameon = False, loc = 'upper right', fontsize = 11)

    fig.savefig(outputDirectory + "EmptyBinsSim_" + var + ".pdf", bbox_inches = 'tight')
    print(outputDirectory + "EmptyBinsSim_" + var + ".pdf Has been created")

def EmptyBinsSimVarZh(var = "Pt2"):

    varBin = var + "Bin"
    vars = ['Data', varBin, "ZhBin"]


    for ZhBin in range(1, len(binning["Zh"]) - 1):
        
        fig, axs = plt.subplots(1, 3, sharey = 'row', sharex = 'col')
        width  = 16 #7.056870070568701
        height = 4
        fig.set_size_inches(width, height)

        fig.subplots_adjust(left = None, bottom = None, right = None, top = None,
                            wspace = 0.02, hspace = 0.02)

        for i in range(3): # Loops on the diffrent targets
            for j in range(nPion): # Loops on the number of pions

                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                
                
                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001 
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                weights = dic[varBin][dic["Data"] == 0].copy()

               
                for k in binning[var]:
                    if(len(dic[varBin][dic[varBin] == k + 0.001]) == 0):
                        weights[weights == k + 0.001] = 0
                    else:
                        weights[weights == k+ 0.001] = 1/ float(len(dic[varBin][dic[varBin] == k + 0.001]))
                
                axs[i].hist(dic[varBin][dic["Data"] == 0], bins = binning[var], weights = weights,
                     color = colorList[j], histtype="step", label = "Solid - " + nPionList[j])
                
                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_D"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                
                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                weights = dic[varBin][dic["Data"] == 0].copy()
                
                for k in binning[var]:
                    if(len(dic[varBin][dic[varBin] == k + 0.001]) == 0):
                        weights[weights == k + 0.001] = 0
                    else:
                        weights[weights == k + 0.001] = 1/ float(len(dic[varBin][dic[varBin] == k + 0.001]))
                

                axs[i].hist(dic[varBin][dic["Data"] == 0], bins = binning[var], 
                            weights = weights, color = colorList[j], histtype="step",
                            label = "Liquid - " + nPionList[j], linestyle = "--")

                axs[i].tick_params(right = False, top = False, which = 'both')
            
            axs[i].set_xlabel(xLabel[var], fontsize = 14)

            axs[0].set_ylabel(r'Empty Bins' , loc = "center", fontsize = 15)
        
        axs[0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
        axs[1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
        axs[2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
        
        axs[0].legend(frameon = False, loc = 'upper right', fontsize = 11)

        fig.savefig(outputDirectory + "EmptyBinsSim_" + var + "_ZhBin" + str(ZhBin) + ".pdf", bbox_inches = 'tight')
        print(outputDirectory + "EmptyBinsSim_" + var + "_ZhBin" + str(ZhBin) + ".pdf.pdf Has been created")

def EmptyBinsSimVarZhOnePlotNorm(var = "Pt2"):

    varBin = var + "Bin"
    vars = ['Data', varBin, "ZhBin"]


    fig, axs = plt.subplots(7, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4*(len(binning["Zh"]) - 2)
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None,
                            wspace = 0.02, hspace = 0.2)

    for ZhBin in range(1, len(binning["Zh"]) - 1):
        for i in range(3): # Loops on the diffrent targets
            for j in range(1, nPion): # Loops on the number of pions

                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                
                
                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001 
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                weights = dic[varBin][dic["Data"] == 0].copy()
        
                max = np.max(np.histogram(dic[varBin],binning[var])[0])
                for k in binning[var]:
                    if(len(dic[varBin][dic[varBin] == k + 0.001]) == 0):
                        weights[weights == k + 0.001] = 0
                    else:
                        weights[weights == k+ 0.001] = 1/ float(len(dic[varBin][dic[varBin] == k + 0.001]))
                
                axs[ZhBin-1][i].hist(dic[varBin][dic["Data"] == 0], bins = binning[var], 
                                    weights = weights, color = colorList[j], histtype="step",
                                    label = "Solid - " + nPionList[j])
               
                axs[ZhBin-1][i].hist(dic[varBin], bins = binning[var], 
                                     weights = np.repeat(1/max, len(dic[varBin])),
                                    color = disColor[j], histtype="step",
                                    label = "Distribution " + nPionList[j])


                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_D"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                

                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                weights = dic[varBin][dic["Data"] == 0].copy()
                
                max = np.max(np.histogram(dic[varBin], binning[var])[0])
                for k in binning[var]:
                    if(len(dic[varBin][dic[varBin] == k + 0.001]) == 0):
                        weights[weights == k + 0.001] = 0
                    else:
                        weights[weights == k + 0.001] = 1/ float(len(dic[varBin][dic[varBin] == k + 0.001]))
                

                axs[ZhBin-1][i].hist(dic[varBin][dic["Data"] == 0], bins = binning[var],
                                weights = weights, color = colorList[j], histtype="step", 
                                label = "Liquid - " + nPionList[j], linestyle = "--")

                axs[ZhBin-1][i].hist(dic[varBin], bins = binning[var], 
                                    weights = np.repeat(1/max, len(dic[varBin])),
                                    color = disColor[j], histtype="step",
                                    label = "Distribution " + nPionList[j],
                                    linestyle = '--')

                axs[ZhBin-1][i].tick_params(right = False, top = False, which = 'both')
            
            axs[ZhBin-1][i].set_xlabel(xLabel[var], fontsize = 14)

            axs[ZhBin-1][0].set_ylabel(r'Empty Bins' , loc = "center", fontsize = 15)
            axs[ZhBin-1][1].annotate(ZhLabel[ZhBin], xy = (0.34, 1.04), 
                                   xycoords = 'axes fraction', fontsize = 15)
        
        
    axs[0][0].legend(frameon = False, loc = 'upper right', fontsize = 11)

    axs[0][0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[0][1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[0][2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    fig.savefig(outputDirectory + "EmptyBinsSim_" + var + "_ZhBinNorm.pdf", bbox_inches = 'tight')
    print(outputDirectory + "EmptyBinsSim_" + var + "_ZhBin.pdf Has been created")

def EmptyBinsSimVarZhOnePlot(var = "Pt2"):

    varBin = var + "Bin"
    vars = ['Data', varBin, "ZhBin"]


    fig, axs = plt.subplots(7, 3, sharey = 'row', sharex = 'col')
    width  = 16 #7.056870070568701
    height = 4*(len(binning["Zh"]) - 2)
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None,
                            wspace = 0.02, hspace = 0.2)

    for ZhBin in range(1, len(binning["Zh"]) - 1):
        for i in range(3): # Loops on the diffrent targets
            for j in range(1, nPion): # Loops on the number of pions

                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                
                
                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001 
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                weights = dic[varBin][dic["Data"] == 0].copy()
        
                axs[ZhBin-1][i].hist(dic[varBin][dic["Data"] == 0], bins = binning[var], 
                                     color = colorList[j], histtype="step",
                                    label = "Solid - " + nPionList[j])
               
                axs[ZhBin-1][i].hist(dic[varBin], bins = binning[var], 
                                    color = disColor[j], histtype="step",
                                    label = "Distribution " + nPionList[j])


                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_D"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                

                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                
                axs[ZhBin-1][i].hist(dic[varBin][dic["Data"] == 0], bins = binning[var],
                                 color = colorList[j], histtype="step", 
                                label = "Liquid - " + nPionList[j], linestyle = "--")

                axs[ZhBin-1][i].hist(dic[varBin], bins = binning[var], 
                                    color = disColor[j], histtype="step",
                                    label = "Distribution " + nPionList[j],
                                    linestyle = '--')

                axs[ZhBin-1][i].tick_params(right = False, top = False, which = 'both')
            
            axs[ZhBin-1][i].set_xlabel(xLabel[var], fontsize = 14)

            axs[ZhBin-1][0].set_ylabel(r'Empty Bins' , loc = "center", fontsize = 15)
            axs[ZhBin-1][1].annotate(ZhLabel[ZhBin], xy = (0.34, 1.04), 
                                   xycoords = 'axes fraction', fontsize = 15)
        
        
    axs[0][0].legend(frameon = False, loc = 'upper right', fontsize = 11)

    axs[0][0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[0][1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[0][2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    fig.savefig(outputDirectory + "EmptyBinsSim_" + var + "_ZhBin.pdf", bbox_inches = 'tight')
    print(outputDirectory + "EmptyBinsSim_" + var + "_ZhBin.pdf Has been created")


def EmptyBinsSimVarZhOnePlotNorm2Box(var = "Pt2"):

    varBin = var + "Bin"
    vars = ['Data', varBin, "ZhBin"]


    fig, axs = plt.subplots(7, 2, sharey = 'row', sharex = 'col')
    width  = 16*(2/3) #7.056870070568701
    height = 4*(len(binning["Zh"]) - 2)
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None,
                            wspace = 0.04, hspace = 0.2)

    for ZhBin in range(1, len(binning["Zh"]) - 1):
        for j in range(1, nPion): # Loops on the number of pions

            data = np.array([])
            values = np.array([])
            
            for i in range(3): # Loops on the diffrent targets
                
                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                    
                values = np.concatenate((values, dic[varBin]), axis = 0)
                data =   np.concatenate((data,  dic["Data"]), axis = 0)

            for t in range(len(values)):
                for k in range(len(binning[var])):
                    if values[t] == k:
                        values[t] = binning[var][k] 

            weights = values[data == 0].copy()
    
            max = np.max(np.histogram(values, binning[var])[0])
            for k in binning[var]:
                if(len(values[values == k]) == 0):
                    weights[weights == k] = 0
                else:
                    weights[weights == k] = 1 / float(len(values[values == k]))
           
            axs[ZhBin-1][0].hist(values[data == 0], bins = binning[var], 
                                weights = weights, color = colorList[j], histtype="step",
                                label = "Solid - " + nPionList[j])
           
            axs[ZhBin-1][0].hist(values, bins = binning[var], 
                                 weights = np.repeat(1/max, len(values)),
                                 color = disColor[j], histtype="step",
                                 label = "Distribution " + nPionList[j])

            data = np.array([])
            values = np.array([])
            
            for i in range(3):
                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_D"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                    
                values = np.concatenate((values,  dic[varBin]), axis = 0)
                data =   np.concatenate((data,  dic["Data"]), axis = 0)

            for t in range(len(values)):
                for k in range(len(binning[var])):
                    if values[t] == k:
                        values[t] = binning[var][k] 

            weights = values[data == 0].copy()
            
            max = np.max(np.histogram(values, binning[var])[0])
            for k in binning[var]:
                if(len(values[values == k]) == 0):
                    weights[weights == k] = 0
                else:
                    weights[weights == k] = 1/ float(len(values[values == k]))
            

            axs[ZhBin-1][1].hist(values[data == 0], bins = binning[var],
                            weights = weights, color = colorList[j], histtype="step", 
                            label = "Empty Bins- " + nPionList[j], linestyle = "--")

            axs[ZhBin-1][1].hist(values, bins = binning[var], 
                                weights = np.repeat(1/max, len(values)),
                                color = disColor[j], histtype="step",
                                label = "Bins " + nPionList[j],
                                linestyle = '-')

            axs[ZhBin-1][0].tick_params(right = False, top = False, which = 'both')
            axs[ZhBin-1][1].tick_params(right = False, top = False, which = 'both')
            
            axs[ZhBin-1][0].set_xlabel(xLabel[var], fontsize = 14)
            axs[ZhBin-1][1].set_xlabel(xLabel[var], fontsize = 14)

            axs[ZhBin-1][0].set_ylabel(r'Bins' , loc = "center", fontsize = 15)
            axs[ZhBin-1][0].annotate(ZhLabel[ZhBin], xy = (0.30, 0.9), 
                                   xycoords = 'axes fraction', fontsize = 15)
            axs[ZhBin-1][1].annotate(ZhLabel[ZhBin], xy = (0.30, 0.9), 
                                   xycoords = 'axes fraction', fontsize = 15)
        
        
    axs[0][0].legend(frameon = False, loc = 'upper right', fontsize = 11)

    axs[0][0].annotate(r'Solid', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[0][1].annotate(r'Liquid',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    fig.savefig(outputDirectory + "EmptyBinsSim_" + var + "_ZhBinNorm2Box.pdf", bbox_inches = 'tight')
    print(outputDirectory + "EmptyBinsSim_" + var + "_ZhBin2Box.pdf Has been created")




def EmptyBinsSimVarZhOnePlot2Box(var = "Pt2"):

    varBin = var + "Bin"
    vars = ['Data', varBin, "ZhBin"]


    fig, axs = plt.subplots(7, 2, sharey = 'row', sharex = 'col')
    width  = 16*(2/3) #7.056870070568701
    height = 4*(len(binning["Zh"]) - 2)
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None,
                            wspace = 0.26, hspace = 0.2)

    for ZhBin in range(1, len(binning["Zh"]) - 1):
        for j in range(1, nPion): # Loops on the number of pions

            data = np.array([])
            values = np.array([])
            
            for i in range(3): # Loops on the diffrent targets
                
                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                
                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001 
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                    
                values = np.concatenate((values,  dic[varBin]), axis = 0)
                data =   np.concatenate((data,  dic["Data"]), axis = 0)


            axs[ZhBin-1][1].hist(values, bins = binning[var], 
                                color = disColor[j], 
                                label = "Data")
            
            axs[ZhBin-1][1].hist(values[data == 1], bins = binning[var], 
                                 color = colorList[j],
                                label = "Data but Not Sim.", zorder = 2)
          

            data = np.array([])
            values = np.array([])

            for i in range(3):
                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_D"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                
                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001 
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                    
                values = np.concatenate((values,  dic[varBin]), axis = 0)
                data =   np.concatenate((data,  dic["Data"]), axis = 0)
            
            axs[ZhBin-1][0].hist(values, bins = binning[var], 
                                color = disColor[j], 
                                label = "Data",
                                linestyle = '-')

            axs[ZhBin-1][0].hist(values[data == 1], bins = binning[var],
                            color = colorList[j],  
                            label = "Data but not Sim.", linestyle = "-", zorder = 2)


        axs[ZhBin-1][0].tick_params(right = False, top = False, which = 'both', 
                                    labelbottom = True)
        axs[ZhBin-1][1].tick_params(right = False, top = False, which = 'both')
            
        axs[ZhBin-1][0].set_xlabel(xLabel[var], fontsize = 14)
        axs[ZhBin-1][1].set_xlabel(xLabel[var], fontsize = 14)
        axs[ZhBin-1][0].xaxis.set_label_coords(1.24, -0.05)

        axs[ZhBin-1][0].set_ylabel(r'Bins' , loc = "center", fontsize = 15)
        axs[ZhBin-1][0].annotate(ZhLabel[ZhBin], xy = (0.32, 0.9), 
                                   xycoords = 'axes fraction', fontsize = 15)
        axs[ZhBin-1][1].annotate(ZhLabel[ZhBin], xy = (0.32, 0.9), 
                                   xycoords = 'axes fraction', fontsize = 15)

        axs[ZhBin-1][0].grid(visible = None, axis = 'both', color = '0.95')
        axs[ZhBin-1][0].set_axisbelow(True)
        axs[ZhBin-1][1].grid(visible = None, axis = 'both', color = '0.95')
        axs[ZhBin-1][1].set_axisbelow(True)

        axs[ZhBin-1][0].legend(frameon = False, loc = 'center right', fontsize = 11)
        axs[ZhBin-1][1].legend(frameon = False, loc = 'center right', fontsize = 11)
    # axs[0][0].legend(frameon = False, fontsize = 11)

        axs[ZhBin-1][1].annotate(r'Solid', xy = (0.04, 1.04), xycoords = 'axes fraction', 
                                 fontsize = 15)
        axs[ZhBin-1][0].annotate(r'Liquid',   xy = (0.04, 1.04), xycoords = 'axes fraction',
                                 fontsize = 15)
    fig.savefig(outputDirectory + "EmptyBinsSim_" + var + "_ZhBin2Box.pdf", bbox_inches = 'tight')
    print(outputDirectory + "EmptyBinsSim_" + var + "_ZhBin2Box.pdf Has been created")


def EmptyDataSimVarZhOnePlot2Box(var = "Pt2"):

    varBin = var + "Bin"
    vars = ['Data', varBin, "ZhBin", "Evnts"]

    fig, axs = plt.subplots(7, 2, sharey = 'row', sharex = 'col')
    width  = 16*(2/3) #7.056870070568701
    height = 4*(len(binning["Zh"]) - 2)
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None,
                            wspace = 0.06, hspace = 0.2)

    for ZhBin in range(1, len(binning["Zh"]) - 1):
        for j in range(1, nPion): # Loops on the number of pions

            data = np.array([])
            values = np.array([])
            events = np.array([])
            
            for i in range(3): # Loops on the diffrent targets
                
                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                
                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001 
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                dic["Evnts"] = dic["Evnts"][dic["ZhBin"] == ZhBin]
                
                    
                values = np.concatenate((values, dic[varBin]),  axis = 0)
                data =   np.concatenate((data,   dic["Data"]),  axis = 0)
                events = np.concatenate((events, dic["Evnts"]), axis = 0)
            
            axs[ZhBin-1][1].hist(values, bins = binning[var], 
                                color = disColor[j], weights = events,
                                label = "Data")

            axs[ZhBin-1][1].hist(values[data == 1], bins = binning[var], 
                                 color = colorList[j], weights = events[data == 1],
                                label = "Data but not Sim", zorder =2)
           

            data = np.array([])
            values = np.array([])
            events = np.array([])

            for i in range(3):
                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_D"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                
                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001 
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                dic["Evnts"]  = dic["Evnts"][dic["ZhBin"] == ZhBin]
                    
                values = np.concatenate((values,  dic[varBin]), axis = 0)
                data =   np.concatenate((data,  dic["Data"]), axis = 0)
                events =   np.concatenate((events,  dic["Evnts"]), axis = 0)
            

            axs[ZhBin-1][0].hist(values, bins = binning[var], 
                                color = disColor[j], weights = events,
                                label = "Data")
            
            axs[ZhBin-1][0].hist(values[data == 1], bins = binning[var], 
                                 color = colorList[j], weights = events[data == 1],
                                label = "Data but not Sim", zorder = 2)
            


            axs[ZhBin-1][0].tick_params(right = False, top = False, which = 'both', zorder = 3)
            axs[ZhBin-1][1].tick_params(right = False, top = False, which = 'both', zorder = 3)
            
            axs[ZhBin-1][0].set_xlabel(xLabel[var], fontsize = 14)
            axs[ZhBin-1][1].set_xlabel(xLabel[var], fontsize = 14)

            axs[ZhBin-1][0].set_ylabel(r'dN/d'+ var , loc = "center", fontsize = 15)
            axs[ZhBin-1][0].annotate(ZhLabel[ZhBin], xy = (0.32, 0.9), 
                                   xycoords = 'axes fraction', fontsize = 15)
            axs[ZhBin-1][1].annotate(ZhLabel[ZhBin], xy = (0.32, 0.9), 
                                   xycoords = 'axes fraction', fontsize = 15)

            axs[ZhBin-1][0].grid(visible = None, axis = 'both', color = '0.95', zorder = 3)
            axs[ZhBin-1][0].set_axisbelow(True)
            axs[ZhBin-1][1].grid(visible = None, axis = 'both', color = '0.95', zorder = 3)
            axs[ZhBin-1][1].set_axisbelow(True)
        
            axs[ZhBin-1][0].set_yscale('log')
            axs[ZhBin-1][1].set_yscale('log')
        
            axs[ZhBin-1][0].set_ylim(0.5, 400000)
            axs[ZhBin-1][1].set_ylim(0.5, 400000)
            
            axs[ZhBin-1][1].annotate(r'Solid', xy = (0.04, 1.04), xycoords = 'axes fraction',
                                     fontsize = 15)
            axs[ZhBin-1][0].annotate(r'Liquid',   xy = (0.04, 1.04), xycoords = 'axes fraction',
                                     fontsize = 15)

            axs[ZhBin-1][0].legend(frameon = False, loc = 'center right', fontsize = 11)
            axs[ZhBin-1][1].legend(frameon = False, loc = 'center right', fontsize = 11)
    # axs[0][0].legend(frameon = False, fontsize = 11)

    axs[0][1].annotate(r'Solid', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[0][0].annotate(r'Liquid',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)

    fig.savefig(outputDirectory + "EmptyDataSim_" + var + "_ZhBin2Box.pdf", bbox_inches = 'tight')
    print(outputDirectory + "EmptyDataSim_" + var + "_ZhBin2Box.pdf Has been created")



def EmptyDataNormSimVarZhOnePlot2Box(var = "Pt2"):

    varBin = var + "Bin"
    vars = ['Data', varBin, "ZhBin", "Evnts"]


    fig, axs = plt.subplots(7, 2, sharey = 'row', sharex = 'col')
    width  = 16*(2/3) #7.056870070568701
    height = 4*(len(binning["Zh"]) - 2)
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None,
                            wspace = 0.06, hspace = 0.2)

    for ZhBin in range(1, len(binning["Zh"]) - 1):
        for j in range(1, nPion): # Loops on the number of pions

            data = np.array([])
            values = np.array([])
            events = np.array([])
            
            for i in range(3): # Loops on the diffrent targets
                
                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                
                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001 
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                dic["Evnts"] = dic["Evnts"][dic["ZhBin"] == ZhBin]
                
                    
                values = np.concatenate((values, dic[varBin]),  axis = 0)
                data =   np.concatenate((data,   dic["Data"]),  axis = 0)
                events = np.concatenate((events, dic["Evnts"]), axis = 0)
                
            hist = axs[ZhBin-1][1].hist(values[data == 0], bins = binning[var], 
                                color = colorList[j],
                                weights = (events[data == 0]/np.sum(events))*100,
                                label = "Lost Data" + nPionList[j], zorder =2)
            
            print("Solids targets " + str(j+1) + " pions in " + ZhLabel[ZhBin] + 
                  " percentaje of loss events: ", end="")
            print(round(np.sum(hist[0]),3))

            data = np.array([])
            values = np.array([])
            events = np.array([])

            for i in range(3):
                with ur.open(inputDirectory + 
                    "EmptyBins.root:EmptyBins_D"+ tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library = "np")
                
                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001 
                
                dic[varBin]  = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"]  = dic["Data"][dic["ZhBin"] == ZhBin]
                dic["Evnts"]  = dic["Evnts"][dic["ZhBin"] == ZhBin]
                    
                values = np.concatenate((values,  dic[varBin]), axis = 0)
                data =   np.concatenate((data,  dic["Data"]), axis = 0)
                events =   np.concatenate((events,  dic["Evnts"]), axis = 0)
            
            hist = axs[ZhBin-1][0].hist(values[data == 0], bins = binning[var], 
                                 color = colorList[j],
                                 weights = (events[data == 0]*100)/np.sum(events),
                                 label = "Lost Data" + nPionList[j], zorder = 2)
            
            print("Liquid targets " + str(j+1) + " pions in " + ZhLabel[ZhBin] + 
                  " percentaje of loss events: ", end = "")
            print(round(np.sum(hist[0])))

            axs[ZhBin-1][0].tick_params(right = False, top = False, which = 'both')
            axs[ZhBin-1][1].tick_params(right = False, top = False, which = 'both')
            
            axs[ZhBin-1][0].set_xlabel(xLabel[var], fontsize = 14)
            axs[ZhBin-1][1].set_xlabel(xLabel[var], fontsize = 14)

            axs[ZhBin-1][0].set_ylabel(r'Lost events (%)' , loc = "center", fontsize = 15)
            axs[ZhBin-1][0].annotate(ZhLabel[ZhBin], xy = (0.32, 0.9), 
                                   xycoords = 'axes fraction', fontsize = 15)
            axs[ZhBin-1][1].annotate(ZhLabel[ZhBin], xy = (0.32, 0.9), 
                                   xycoords = 'axes fraction', fontsize = 15)
            axs[ZhBin-1][0].grid(visible = None, axis = 'both', color = '0.95')
            axs[ZhBin-1][0].set_axisbelow(True)
            axs[ZhBin-1][1].grid(visible = None, axis = 'both', color = '0.95')
            axs[ZhBin-1][1].set_axisbelow(True)
        
            axs[ZhBin-1][0].set_ylim(0, 1.25)
            axs[ZhBin-1][1].set_ylim(0, 1.25)
           
            if ZhBin != 7:
                axs[ZhBin-1][0].set_ylim(0, 0.125)
                axs[ZhBin-1][1].set_ylim(0, 0.125)

            axs[ZhBin-1][0].legend(frameon = False, loc = 'center right', fontsize = 11)
            axs[ZhBin-1][1].legend(frameon = False, loc = 'center right', fontsize = 11)
    # axs[0][0].legend(frameon = False, fontsize = 11)

            axs[ZhBin-1][1].annotate(r'Solid', xy = (0.04, 1.04), xycoords = 'axes fraction', 
                                     fontsize = 15)
            axs[ZhBin-1][0].annotate(r'Liquid',   xy = (0.04, 1.04), xycoords = 'axes fraction',
                                     fontsize = 15)

    fig.savefig(outputDirectory + "EmptyNormDataSim_" + var + "_ZhBin2Box.pdf",
                bbox_inches = 'tight')
    print(outputDirectory + "EmptyNormDataSim_" + var + "_ZhBin2Box.pdf Has been created")

# for var in variables:
    # EmptyBinsSimVar(var)

# EmptyBinsSimVarZh(var = "Pt2")
# EmptyBinsSimVarZhOnePlotNorm()
# EmptyBinsSimVarZhOnePlot()
# EmptyBinsSimVarZhOnePlotNorm2Box()
EmptyBinsSimVarZhOnePlot2Box()
# EmptyDataNormSimVarZhOnePlot2Box()
# EmptyDataSimVarZhOnePlot2Box()
