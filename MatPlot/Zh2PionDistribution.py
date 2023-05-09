import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import mplhep as hep
import uproot as ur
from include import inputDirectory, outputDirectory, dataDirectory

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

tarList    = ["C", "Fe", "Pb"]
cm = plt.cm.RdPu
textColor1 = "black"
textColor2 = "white"

def Zh2DDistribution():

    fig, axs = plt.subplots(1, 3, sharey = 'row', sharex = 'col', 
                            gridspec_kw = {'width_ratios': [4, 4, 5]})
    width  = 16 #7.056870070568701
    height = 6
    fig.set_size_inches(width, height)

    # vars = ['Zh_1', 'Zh', "Acc", "FalPos"]
    vars = ['Zh_1', 'Zh', "Zh_2"]
    # binsY = [0, .1, .2, .3, .4, .5, .6, .8, 1.]
    # binsX = [.1, .2, .3, .4, .5, .6, .8, 1.]
    # binsY = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.]
    # binsX = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1.]
    binsY = np.linspace(0, 1, 11)
    binsX = np.linspace(.1, 1, 10)
    # cm = plt.cm.twilight_shifted

    fig.subplots_adjust(left = None, bottom = None, right = None, top = None, wspace = 0.04, 
                        hspace = 0.02)
                
    for i in range(3): # Loops on the diffrent targets

        with ur.open(dataDirectory + "VecSum_" + tarList[i] + ".root:ntuple_2_pion") as file:
            data = file.arrays(vars, library = "np")

        Zhweight = np.ones_like(data["Zh"])

        for k in range(len(data['Zh'])):
            for Zhbin in range(len(binsY) - 1):
                if data['Zh'][k] > binsY[Zhbin] and data['Zh'][k] < binsY[Zhbin + 1]:
                    # print(k)
                    # print(data['Zh'][k])
                    # print(Zhbin)
                    Zhweight[k] = Zhbin

        hBroad = axs[i].hist2d(data['Zh'], data['Zh_1'], bins = (binsX, binsY) , cmap = cm) 

        flag1 = True
        flag2 = True

        total = 0

        # for j in range(len(hBroad[2])-1):
            # for k in range(len(hBroad[1])-1): 

                # total = total + hBroad[0].T[j,k]
        
        print(Zhweight)
        weights = np.ones_like(data['Zh'])

        for Zhbin in range(len(binsY)-1):
            if len(Zhweight[Zhweight == Zhbin]) !=0 :
                weights[Zhweight == Zhbin] = 1 / float(len(Zhweight[Zhweight == Zhbin]))

        hBroad2 = axs[i].hist2d(data['Zh'], data['Zh_1'], weights = weights,
                                bins = (binsX, binsY) , cmap = cm) 

        # print(hBroad2[0])
        colorLimit = .5

        for j in range(len(hBroad[2])-1):
            for k in range(len(hBroad[1])-1): 

                deltaX = (hBroad[1][k+1] - hBroad[1][k])/2
                deltaY = (hBroad[2][j+1] - hBroad[2][j])/2
                
                if j<= k+1 and hBroad[1][k+1]/2. <= hBroad[2][j+1]: 
                    if hBroad2[0].T[j,k] < colorLimit:
                        color = textColor1
                    else:
                        color = textColor2

                    axs[i].text(hBroad[1][k]+deltaX, hBroad[2][j] + deltaY, 
                                    round(hBroad2[0].T[j,k], 2), 
                                    color=color, ha="center", va="center", 
                                    fontsize = 8, fontweight="bold")

                # if hBroad[1][k] < hBroad[2][j]:
                elif k + 1.5< j:

                    if flag1:
                        axs[i].fill_between((hBroad[1][k], hBroad[1][k+1]), 1, hBroad[2][j],
                                            color='grey', label = '$Zh_1>Zh_{Sum}$')
                        flag1 = False
                    else:
                        axs[i].fill_between((hBroad[1][k], hBroad[1][k+1]), 1, 
                                            hBroad[2][j], color = 'grey') 
                else:
                   
                    if flag2:
                        axs[i].fill_between((hBroad[1][k], hBroad[1][k+1]), hBroad[2][j+1], 0, 
                                            color = 'lightgrey', label = '$Zh_2>Zh_1$')
                        flag2 = False
                    else:
                        axs[i].fill_between((hBroad[1][k],hBroad[1][k+1]),hBroad[2][j+1], 0,
                                            color = 'lightgrey')

        # x = np.array([0.05, .15, .25, .35, .45, .55, .7, .9,1 ])
        # for j in range(8):
            # axs[i].plot(x+0.1, x[j] - x +0.1,color ='orange', linestyle= '--', alpha = 0.5)

    # Set the labels for the three plots
    axs[0].set_ylabel(r'$Zh_1$', loc = "center", fontsize = 15)
    axs[0].set_xlabel(r'$Zh_{SUM}$', fontsize = 14)
    axs[1].set_xlabel(r'$Zh_{SUM}$', fontsize = 14)
    axs[2].set_xlabel(r'$Zh_{SUM}$', fontsize = 14)

    axs[0].legend(frameon = True, loc = 'upper left', fontsize = 11, framealpha = 1)
    
    axs[0].annotate(r'Carbon', xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[1].annotate(r'Iron',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    axs[2].annotate(r'Lead',   xy = (0.04, 1.04), xycoords = 'axes fraction', fontsize = 15)
    # cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.colorbar(hBroad2[3], ax = axs[2])
    for i in range(3):
        axs[i].set_xticks([.2, .4, .6, .8, 1])
        axs[i].set_xticks(binsX, minor=True)
        axs[i].set_yticks(binsY, minor=True)
        axs[i].set_xticklabels([.2, .4, .6, .8, 1])
        axs[i].tick_params(right = False, top = False, left = False, bottom = False,which = 'minor')
    

    for i in range(3):
        # axs[i].set_xticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.8])
        # axs[i].set_yticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.8])
        axs[i].grid(which = 'both', axis = 'both', color = 'black', alpha =1 ) 
        # axs[i].set_axisbelow(True)

    fig.align_ylabels(axs[:])
    fig.savefig(outputDirectory + "Zh2Ddistribution.pdf", bbox_inches = 'tight')
    print(outputDirectory + "Zh2Ddistribution.pdf Has been created")


def Zh2DDistZhSumNorm():

    fig, axs = plt.subplots(1, 1, sharey = 'row', sharex = 'col')
    width  = 6
    height = 6/1.1 
    fig.set_size_inches(width, height)

    # vars = ['Zh_1', 'Zh', "Acc", "FalPos"]
    vars = ['Zh_1', 'Zh', "Zh_2"]
    binsY = np.linspace(0, 1, 17)
    binsX = np.linspace(0, 1, 17)
    # cm = plt.cm.twilight_shifted


    with ur.open(dataDirectory + "VecSum_C.root:ntuple_2_pion") as file:
        data = file.arrays(vars, library = "np")

    Zhweight = np.ones_like(data["Zh"])

    for k in range(len(data['Zh'])):
        for Zhbin in range(len(binsY) - 1):
            if data['Zh'][k] > binsY[Zhbin] and data['Zh'][k] < binsY[Zhbin + 1]:
                Zhweight[k] = Zhbin

    hBroad = axs.hist2d(data['Zh'], data['Zh_1'], bins = (binsX, binsY) , cmap = cm) 

    flag1 = True
    flag2 = True

    weights = np.ones_like(data['Zh'])

    for Zhbin in range(len(binsY)-1):
        if len(Zhweight[Zhweight == Zhbin]) !=0 :
            weights[Zhweight == Zhbin] = 1 / float(len(Zhweight[Zhweight == Zhbin]))

    hBroad2 = axs.hist2d(data['Zh'], data['Zh_1'], weights = weights,
                            bins = (binsX, binsY) , cmap = cm) 

    # print(hBroad2[0])
    colorLimit = .5

    for j in range(len(hBroad[2])-1):
        for k in range(len(hBroad[1])-1): 

            deltaX = (hBroad[1][k+1] - hBroad[1][k])/2
            deltaY = (hBroad[2][j+1] - hBroad[2][j])/2
            
            if j<= k and hBroad[1][k+1]/2. <= hBroad[2][j+1]: 
                if hBroad2[0].T[j,k] < colorLimit:
                    color = textColor1
                else:
                    color = textColor2

                axs.text(hBroad[1][k]+deltaX, hBroad[2][j] + deltaY, 
                                    round(hBroad2[0].T[j,k], 2), 
                                    color=color, ha="center", va="center", 
                                    fontsize = 6, fontweight="bold")

            # if hBroad[1][k] < hBroad[2][j]:
            elif k + .5 < j:

                if flag1:
                    axs.fill_between((hBroad[1][k], hBroad[1][k+1]), 1, hBroad[2][j],
                                        color='grey', label = '$Zh_1>Zh_{Sum}$')
                    flag1 = False
                else:
                    axs.fill_between((hBroad[1][k], hBroad[1][k+1]), 1, 
                                        hBroad[2][j], color = 'grey') 
            else:
               
                if flag2:
                    axs.fill_between((hBroad[1][k], hBroad[1][k+1]), hBroad[2][j+1], 0, 
                                        color = 'lightgrey', label = '$Zh_2>Zh_1$')
                    flag2 = False
                else:
                    axs.fill_between((hBroad[1][k],hBroad[1][k+1]),hBroad[2][j+1], 0,
                                        color = 'lightgrey')

        # x = np.array([0.05, .15, .25, .35, .45, .55, .7, .9,1 ])
        # for j in range(8):
            # axs[i].plot(x+0.1, x[j] - x +0.1,color ='orange', linestyle= '--', alpha = 0.5)

    # Set the labels for the three plots
    axs.set_ylabel(r'$Zh_1$', loc = "center", fontsize = 15)
    axs.set_xlabel(r'$Zh_{SUM}$', fontsize = 14)

    axs.legend(frameon = True, loc = 'upper left', fontsize = 11, framealpha = 1)
    
    fig.colorbar(hBroad2[3], ax = axs)

    print("Bin x: ")
    print(binsX)
    print("Bin y: ")
    print(binsY)

    axs.set_xticks([.2, .4, .6, .8, 1])
    axs.set_xticks(binsX, minor=True)
    axs.set_yticks(binsY, minor=True)
    axs.set_xticklabels([.2, .4, .6, .8, 1])
    axs.tick_params(right = False, top = False, left = False, bottom = False, which = 'both')
    

    axs.grid(which = 'minor', axis = 'both', color = 'black', alpha =1 ) 
    axs.grid(which = 'minor', axis = 'both', color = 'black', alpha =1 ) 

    fig.savefig(outputDirectory + "Zh2DdistributionZhSumNorm.pdf", bbox_inches = 'tight')
    print(outputDirectory + "Zh2DdistributionZhSumNorm.pdf Has been created")


def Zh2DDist():

    fig, axs = plt.subplots(1, 1, sharey = 'row', sharex = 'col')
    width  = 6
    height = 6/1.1 
    fig.set_size_inches(width, height)

    # vars = ['Zh_1', 'Zh', "Acc", "FalPos"]
    vars = ['Zh_1', 'Zh', "Zh_2"]
    binsY = np.linspace(0, 1, 15)
    binsX = np.linspace(0, 1, 15)
    # cm = plt.cm.twilight_shifted


    with ur.open(dataDirectory + "VecSum_C.root:ntuple_2_pion") as file:
        data = file.arrays(vars, library = "np")

    Zhweight = np.ones_like(data["Zh"])

    for k in range(len(data['Zh'])):
        for Zhbin in range(len(binsY) - 1):
            if data['Zh'][k] > binsY[Zhbin] and data['Zh'][k] < binsY[Zhbin + 1]:
                Zhweight[k] = Zhbin

    hBroad = axs.hist2d(data['Zh'], data['Zh_1'], bins = (binsX, binsY) , cmap = cm) 

    flag1 = True
    flag2 = True

    weights = np.ones_like(data['Zh']) /  float(len(data['Zh']))

    hBroad2 = axs.hist2d(data['Zh'], data['Zh_1'], weights = weights,
                            bins = (binsX, binsY) , cmap = cm) 

    colorLimit = np.amax(hBroad2[0])*0.65

    for j in range(len(hBroad[2])-1):
        for k in range(len(hBroad[1])-1): 

            deltaX = (hBroad[1][k+1] - hBroad[1][k])/2
            deltaY = (hBroad[2][j+1] - hBroad[2][j])/2
            
            if j<= k and hBroad[1][k+1]/2. <= hBroad[2][j+1]: 
                if hBroad2[0].T[j,k] < colorLimit:
                    color = textColor1
                else:
                    color = textColor2

                axs.text(hBroad[1][k]+deltaX, hBroad[2][j] + deltaY, 
                                    round(hBroad2[0].T[j,k], 4), 
                                    color=color, ha="center", va="center", 
                                    fontsize = 6, fontweight="bold",
                                    rotation = 45)

            # if hBroad[1][k] < hBroad[2][j]:
            elif k + .5 < j:

                if flag1:
                    axs.fill_between((hBroad[1][k], hBroad[1][k+1]), 1, hBroad[2][j],
                                        color='grey', label = '$Zh_1>Zh_{Sum}$')
                    flag1 = False
                else:
                    axs.fill_between((hBroad[1][k], hBroad[1][k+1]), 1, 
                                        hBroad[2][j], color = 'grey') 
            else:
               
                if flag2:
                    axs.fill_between((hBroad[1][k], hBroad[1][k+1]), hBroad[2][j+1], 0, 
                                        color = 'lightgrey', label = '$Zh_2>Zh_1$')
                    flag2 = False
                else:
                    axs.fill_between((hBroad[1][k],hBroad[1][k+1]),hBroad[2][j+1], 0,
                                        color = 'lightgrey')

        # x = np.array([0.05, .15, .25, .35, .45, .55, .7, .9,1 ])
        # for j in range(8):
            # axs[i].plot(x+0.1, x[j] - x +0.1,color ='orange', linestyle= '--', alpha = 0.5)

    # Set the labels for the three plots
    axs.set_ylabel(r'$Zh_1$', loc = "center", fontsize = 15)
    axs.set_xlabel(r'$Zh_{SUM}$', fontsize = 14)

    axs.legend(frameon = True, loc = 'upper left', fontsize = 11, framealpha = 1)
    
    fig.colorbar(hBroad2[3], ax = axs)

    print("Bin x: ")
    print(binsX)
    print("Bin y: ")
    print(binsY)

    axs.set_xticks([.2, .4, .6, .8, 1])
    axs.set_xticks(binsX, minor=True)
    axs.set_yticks(binsY, minor=True)
    axs.set_xticklabels([.2, .4, .6, .8, 1])
    axs.tick_params(right = False, top = False, left = False, bottom = False, which = 'both')
    

    axs.grid(which = 'minor', axis = 'both', color = 'black', alpha =1 ) 
    axs.grid(which = 'minor', axis = 'both', color = 'black', alpha =1 ) 

    fig.savefig(outputDirectory + "Zh2Ddistribution.pdf", bbox_inches = 'tight')
    print(outputDirectory + "Zh2Ddistribution.pdf Has been created")



# Zh2DDistribution()
Zh2DDistZhSumNorm()
Zh2DDist()
