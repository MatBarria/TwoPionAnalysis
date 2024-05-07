import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.ticker as ticker
import matplotlib.colors as mcolors
import mplhep as hep
import uproot as ur
import ROOT

# from matplotlib import colorsp

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2
# hep.style.use(["ATLAS", "fira", "firamath"])

inputDirectory = "~/proyecto/Pt2Broadening_multi-pion/Data/Broad2Split/"
dataDirectory = "~/proyecto/Pt2Broadening_multi-pion/Data/Final/"
outputDirectory = "/home/matias/proyecto/Pt2Broadening_multi-pion/Plots/Broad2Split/"

nPion = 2

# cm = plt.cm.viridis
# cm = plt.cm.twilight_shifted
cm = plt.cm.RdPu
textColor1 = "black"
textColor2 = "white"
colorLimit = [.3, 0.12, .3]
vars = ['Zh_1', 'Zh_2', 'Broad', 'Error']
tarList = ["C", "Fe", "Pb"]
colorList = ["red", "Blue", "black"]
labelList = ["One $\pi +$",      "Two $\pi+$", "Three $\pi +$"]
# binsX = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9 ,1.]
binsX = [0, .1, .2, .3, .4, .5,    .6, .8, 1.]
binsY = [0, .1, .2, .3, .4, .5]


def PtBroad2DZhSum():

    width = 6
    height = width / 1.1

    vars = ['Zh_1', 'Zh', 'Broad', 'Error']
    binsY = [0, .1, .2, .3, .4, .5, .6, .8, 1.]
    binsX = [.1, .2, .3, .4, .5, .6, .8, 1.]
    for i in range(3):  # Loops on the diffrent targets
        fig, axs = plt.subplots(1, 1, constrained_layout=True)
        fig.set_size_inches(width, height)
        with ur.open(inputDirectory + "PtBroadZhSplitWeight-2.root:Pt2Broad_2_" + tarList[i]) as file:
            data = file.arrays(vars, library="np")

        hError = plt.hist2d(data['Zh'], data['Zh_1'], bins=(
            binsX, binsY), weights=data['Error'])
        hBroad = axs.hist2d(data['Zh'], data['Zh_1'], bins=(
            binsX, binsY), weights=data['Broad'], cmap=cm)

        flag1 = True
        flag2 = True

        colorLimit = np.amax(data['Broad'])*0.75
        for j in range(len(hBroad[2])-1):
            for k in range(len(hBroad[1])-1):
                deltaX = (hBroad[1][k+1] - hBroad[1][k])/2
                deltaY = (hBroad[2][j+1] - hBroad[2][j])/2
                # print(hBroad[2][j])
                if j <= k+1 and hBroad[1][k+1]/2. <= hBroad[2][j+1]:
                    if hBroad[0].T[j, k] < colorLimit:
                        color = textColor1
                    else:
                        color = textColor2
                    axs.text(hBroad[1][k]+deltaX, hBroad[2][j]+deltaY+0.027, round(hBroad[0].T[j, k], 3),
                             color=color, ha="center", va="center", fontsize=10, fontweight="bold")
                    axs.text(hError[1][k]+deltaX, hError[2][j]+deltaY-0.027, round(hError[0].T[j, k], 3),
                             color=color, ha="center", va="center", fontsize=10, fontweight="bold")
                    axs.text(hError[1][k]+deltaX, hError[2][j]+deltaY-0.0, '$\pm$',
                             color=color, ha="center", va="center", fontsize=10, fontweight="bold")
                elif hBroad[1][k] < hBroad[2][j]:
                    if flag1:
                        axs.fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), 1, hBroad[2][j], color='grey', label='$Zh_1>Zh_{Sum}$')
                        flag1 = False
                    else:
                        axs.fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), 1, hBroad[2][j], color='grey')
                else:
                    if flag2:
                        axs.fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), hBroad[2][j+1], 0, color='lightgrey', label='$Zh_2>Zh_1$')
                        flag2 = False
                    else:
                        axs.fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), hBroad[2][j+1], 0, color='lightgrey')
                # elif k < jbb:
                    # print("hola")
                    # axs.fill_between((hBroad[1][k],hBroad[1][k+1]), 0.5, hBroad[2][j],color='grey')
    # Set the labels for the three plots
        # axs.set_xlabel(r'$Zh_{SUM}$', loc="center", fontsize=15)
        axs.set_xlabel(r'$Z^{+}_{h}$', loc="center", fontsize=15)
        axs.set_ylabel(r'$Zh_1$', loc="center", fontsize=15)

        axs.legend(frameon=True, loc='lower right', fontsize=10, framealpha=1)

        axs.set_xticks([.2, .4, .6, .8, 1])
        axs.set_xticks([.1, .2, .3, .4, .5, .6, .8, 1], minor=True)
        axs.set_yticks([0, .1, .2, .3, .4, .5, .6, .8, 1], minor=True)
        axs.set_xticklabels([.2, .4, .6, .8, 1])
        axs.tick_params(right=False, top=False, left=False,
                        bottom=False, which='minor')
        cb = fig.colorbar(hBroad[3])

        cb.formatter.set_powerlimits((0, 0))
        cb.ax.yaxis.set_offset_position('left')
        cb.update_ticks()

        axs.grid(which='both', axis='both', color='black', alpha=1)
        # axs.set_axisbelow(True)

        # fig.align_ylabels(axs[:])
        fig.savefig(outputDirectory + "PtBroad2DZhSum_" +
                    tarList[i] + "-w.pdf", bbox_inches='tight')
        print(outputDirectory + "PtBroad2DZhSum-w.pdf Has been created")


def PtBroad2DZhSumOne():

    fig, axs = plt.subplots(1, 3, sharey='row', sharex='col', gridspec_kw={
                            'width_ratios': [4, 4, 5]})
    width = 16  # 7.056870070568701
    height = 6
    fig.set_size_inches(width, height)

    vars = ['Zh_1', 'Zh', 'Broad', 'Error']
    binsY = [0, .1, .2, .3, .4, .5, .6, .8, 1.]
    binsX = [.1, .2, .3, .4, .5, .6, .8, 1.]

    fig.subplots_adjust(left=None, bottom=None, right=None,
                        top=None, wspace=0.04, hspace=0.02)

    for i in range(3):  # Loops on the diffrent targets
        with ur.open(inputDirectory + "PtBroadZhSplitWeight-2.root:Pt2Broad_2_" + tarList[i]) as file:
            data = file.arrays(vars, library="np")
        print(np.amax(data['Broad']))
        # Generate the plot
        hError = plt.hist2d(data['Zh'], data['Zh_1'], bins=(
            binsX, binsY), weights=data['Error'])
        hBroad = axs[i].hist2d(data['Zh'], data['Zh_1'], bins=(
            binsX, binsY), weights=data['Broad'], cmap=cm, vmax=0.0884)

        colorLimit = np.amax(data['Broad'])*0.75

        flag1 = True
        flag2 = True

        for j in range(len(hBroad[2])-1):
            for k in range(len(hBroad[1])-1):
                deltaX = (hBroad[1][k+1] - hBroad[1][k])/2
                deltaY = (hBroad[2][j+1] - hBroad[2][j])/2
                if j <= k+1 and hBroad[1][k+1]/2. <= hBroad[2][j+1]:
                    if hBroad[0].T[j, k] < colorLimit:
                        color = textColor1
                    else:
                        color = textColor2
                    axs[i].text(hBroad[1][k]+deltaX, hBroad[2][j]+deltaY+0.027, round(hBroad[0].T[j, k], 3),
                                color=color, ha="center", va="center", fontsize=10, fontweight="bold")
                    axs[i].text(hError[1][k]+deltaX, hError[2][j]+deltaY-0.027, round(hError[0].T[j, k], 3),
                                color=color, ha="center", va="center", fontsize=10, fontweight="bold")
                    axs[i].text(hError[1][k]+deltaX, hError[2][j]+deltaY-0.0, '$\pm$',
                                color=color, ha="center", va="center", fontsize=10, fontweight="bold")
                elif hBroad[1][k] < hBroad[2][j]:
                    if flag1:
                        axs[i].fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), 1, hBroad[2][j], color='grey', label='$Zh_1>Zh_{Sum}$')
                        flag1 = False
                    else:
                        axs[i].fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), 1, hBroad[2][j], color='grey')
                else:
                    if flag2:
                        axs[i].fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), hBroad[2][j+1], 0, color='lightgrey', label='$Zh_2>Zh_1$')
                        flag2 = False
                    else:
                        axs[i].fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), hBroad[2][j+1], 0, color='lightgrey')

    axs[0].set_ylabel(r'$Zh_1$', loc="center", fontsize=15)
    # axs[0].set_xlabel(r'$Zh_{SUM}$', fontsize=14)
    # axs[1].set_xlabel(r'$Zh_{SUM}$', fontsize=14)
    # axs[2].set_xlabel(r'$Zh_{SUM}$', fontsize=14)
    axs[0].set_xlabel(r'$Z^{+}_{h}$', fontsize=14)
    axs[1].set_xlabel(r'$Z^{+}_{h}$', fontsize=14)
    axs[2].set_xlabel(r'$Z^{+}_{h}$', fontsize=14)

    for i in range(3):
        axs[i].set_xticks([.2, .4, .6, .8, 1])
        axs[i].set_xticks([.1, .2, .3, .4, .5, .6, .8, 1], minor=True)
        axs[i].set_yticks([0, .1, .2, .3, .4, .5, .6, .8, 1], minor=True)
        axs[i].set_xticklabels([.2, .4, .6, .8, 1])
        axs[i].tick_params(right=False, top=False, left=False,
                           bottom=False, which='minor')
        axs[i].grid(which='both', axis='both', color='black', alpha=1)

    axs[0].annotate(r'Carbon', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(r'Iron',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[2].annotate(r'Lead',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)

    cb = fig.colorbar(hBroad[3], ax=axs[2])
    cb.formatter.set_powerlimits((0, 0))
    cb.ax.yaxis.set_offset_position('left')
    cb.update_ticks()

    axs[0].legend(frameon=True, loc='upper left', fontsize=11, framealpha=1)

    fig.align_ylabels(axs[:])
    fig.savefig(outputDirectory + "PtBroad2DZhsum-w.pdf", bbox_inches='tight')
    print(outputDirectory + "PtBroad2DZhsum-w.pdf Has been created")


def Zh2DDistribution():

    fig, axs = plt.subplots(1, 3, sharey='row', sharex='col', gridspec_kw={
                            'width_ratios': [4, 4, 5]})
    width = 16  # 7.056870070568701
    height = 6
    fig.set_size_inches(width, height)

    inputDirectory = "~/proyecto/Pt2Broadening_multi-pion/Data/"
    vars = ['Zh_1', 'Zh', "Acc", "FalPos"]
    binsY = [0, .1, .2, .3, .4, .5, .6, .8, 1.]
    binsX = [.1, .2, .3, .4, .5, .6, .8, 1.]

    # cm = plt.cm.twilight_shifted

    fig.subplots_adjust(left=None, bottom=None, right=None,
                        top=None, wspace=0.04, hspace=0.02)

    for i in range(3):  # Loops on the diffrent targets
        with ur.open(inputDirectory + "VecSum_" + tarList[i] + "_Acc.root:ntuple_2_pion") as file:
            data = file.arrays(vars, library="np")
        # data['Broad'][data['Broad']<0] = 0
        # print(np.amax(data['Broad']))
        # Generate the plot
        # hError = plt.hist2d(data['Zh'], data['Zh_1'], bins = (binsX, binsY), weights = data['Error'])
        data['Zh'] = data['Zh'][data['Acc'] != 0]
        data['Zh_1'] = data['Zh_1'][data['Acc'] != 0]
        data['FalPos'] = data['FalPos'][data['Acc'] != 0]
        data['Acc'] = data['Acc'][data['Acc'] != 0]
        hBroad = axs[i].hist2d(
            data['Zh'], data['Zh_1'], weights=data['FalPos']/data["Acc"], bins=(binsX, binsY), cmap=cm)

        flag1 = True
        flag2 = True

        total = 0

        for j in range(len(hBroad[2])-1):
            for k in range(len(hBroad[1])-1):
                total = total + hBroad[0].T[j, k]
        hBroad2 = axs[i].hist2d(data['Zh'], data['Zh_1'], weights=data['FalPos'] /
                                (data["Acc"]*total), bins=(binsX, binsY), cmap=cm)
        colorLimit = np.amax(hBroad[0])*0.75
        for j in range(len(hBroad[2])-1):
            for k in range(len(hBroad[1])-1):
                deltaX = (hBroad[1][k+1] - hBroad[1][k])/2
                deltaY = (hBroad[2][j+1] - hBroad[2][j])/2
                if j <= k+1 and hBroad[1][k+1]/2. <= hBroad[2][j+1]:
                    if hBroad[0].T[j, k] < colorLimit:
                        color = textColor1
                    else:
                        color = textColor2
                    axs[i].text(hBroad[1][k]+deltaX, hBroad[2][j]+deltaY+0.027, round(hBroad[0].T[j, k]/total, 3),
                                color=color, ha="center", va="center", fontsize=10, fontweight="bold")
                elif hBroad[1][k] < hBroad[2][j]:
                    if flag1:
                        axs[i].fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), 1, hBroad[2][j], color='grey', label='$Zh_1>Zh_{Sum}$')
                        flag1 = False
                    else:
                        axs[i].fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), 1, hBroad[2][j], color='grey')
                else:
                    if flag2:
                        axs[i].fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), hBroad[2][j+1], 0, color='lightgrey', label='$Zh_2>Zh_1$')
                        flag2 = False
                    else:
                        axs[i].fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), hBroad[2][j+1], 0, color='lightgrey')

        # x = np.array([0.05, .15, .25, .35, .45, .55, .7, .9,1 ])
        # for j in range(8):
            # axs[i].plot(x+0.1, x[j] - x +0.1,color ='orange', linestyle= '--', alpha = 0.5)

    # Set the labels for the three plots
    axs[0].set_ylabel(r'$Zh_1$', loc="center", fontsize=15)
    # axs[0].set_xlabel(r'$Zh_{SUM}$', fontsize=14)
    # axs[1].set_xlabel(r'$Zh_{SUM}$', fontsize=14)
    # axs[0].set_xlabel(r'$Z_{SUM}$', fontsize=14)
    axs[1].set_xlabel(r'$Z^{+}_{h}$', fontsize=14)
    axs[2].set_xlabel(r'$Z^{+}_{h}$', fontsize=14)
    axs[2].set_xlabel(r'$Z^{+}_{h}$', fontsize=14)

    axs[0].legend(frameon=True, loc='upper left', fontsize=11, framealpha=1)

    axs[0].annotate(r'Carbon', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(r'Iron',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[2].annotate(r'Lead',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    # cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.colorbar(hBroad2[3], ax=axs[2])
    for i in range(3):
        axs[i].set_xticks([.2, .4, .6, .8, 1])
        axs[i].set_xticks([.1, .2, .3, .4, .5, .6, .8, 1], minor=True)
        axs[i].set_yticks([0, .1, .2, .3, .4, .5, .6, .8, 1], minor=True)
        axs[i].set_xticklabels([.2, .4, .6, .8, 1])
        axs[i].tick_params(right=False, top=False, left=False,
                           bottom=False, which='minor')

    # fig.colorbar(im, ax=axs.ravel().tolist())
    # axs[0].legend(frameon = False, loc = 'upper left', fontsize = 11)
    # axs[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    for i in range(3):
        # axs[i].set_xticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.8])
        # axs[i].set_yticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.8])
        axs[i].grid(which='both', axis='both', color='black', alpha=1)
        # axs[i].set_axisbelow(True)

    fig.align_ylabels(axs[:])
    fig.savefig(outputDirectory + "Zh2Ddistribution-w.pdf",
                bbox_inches='tight')
    fig.savefig(outputDirectory + "Zh2Ddistribution-w.png",
                bbox_inches='tight', dpi=600)
    print(outputDirectory + "Zh2Ddistribution-w.pdf Has been created")


def PtBroad2DZhSumExtra():

    width = 6
    height = width / 0.95

    vars = ['Zh_1', 'Zh', 'Broad', 'Error']
    binsY = [0, .1, .2, .3, .4, .5, .6, .8, 1.]
    binsX = [.1, .2, .3, .4, .5, .6, .8, 1.]
    for i in range(3):  # Loops on the diffrent targets
        fig, axs = plt.subplots(2, 1, constrained_layout=True, gridspec_kw={
                                'height_ratios': [1, 9]})
        fig.set_size_inches(width, height)
        # fig.subplots_adjust(left = None, bottom = None, right = None, top = None, wspace = 0.06, hspace = 0.08)
        with ur.open(inputDirectory + "PtBroadZhSplitWeight-2.root:Pt2Broad_2_" + tarList[i]) as file:
            data = file.arrays(vars, library="np")

        hError = plt.hist2d(data['Zh'], data['Zh_1'], bins=(
            binsX, binsY), weights=data['Error'])
        hBroad = axs[1].hist2d(data['Zh'], data['Zh_1'], bins=(
            binsX, binsY), weights=data['Broad'], cmap=cm)

        flag1 = True
        flag2 = True

        colorLimit = np.amax(data['Broad'])*0.75
        for j in range(len(hBroad[2])-1):
            for k in range(len(hBroad[1])-1):
                deltaX = (hBroad[1][k+1] - hBroad[1][k])/2
                deltaY = (hBroad[2][j+1] - hBroad[2][j])/2
                # print(hBroad[2][j])
                if j <= k+1 and hBroad[1][k+1]/2. <= hBroad[2][j+1]:
                    if hBroad[0].T[j, k] < colorLimit:
                        color = textColor1
                    else:
                        color = textColor2
                    axs[1].text(hBroad[1][k]+deltaX, hBroad[2][j]+deltaY+0.027, round(hBroad[0].T[j, k], 3),
                                color=color, ha="center", va="center", fontsize=10, fontweight="bold")
                    axs[1].text(hError[1][k]+deltaX, hError[2][j]+deltaY-0.027, round(hError[0].T[j, k], 3),
                                color=color, ha="center", va="center", fontsize=10, fontweight="bold")
                    axs[1].text(hError[1][k]+deltaX, hError[2][j]+deltaY-0.0, '$\pm$',
                                color=color, ha="center", va="center", fontsize=10, fontweight="bold")
                elif hBroad[1][k] < hBroad[2][j]:
                    if flag1:
                        axs[1].fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), 1, hBroad[2][j], color='grey', label='$Zh_1>Zh_{Sum}$')
                        flag1 = False
                    else:
                        axs[1].fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), 1, hBroad[2][j], color='grey')
                else:
                    if flag2:
                        axs[1].fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), hBroad[2][j+1], 0, color='lightgrey', label='$Zh_2>Zh_1$')
                        flag2 = False
                    else:
                        axs[1].fill_between(
                            (hBroad[1][k], hBroad[1][k+1]), hBroad[2][j+1], 0, color='lightgrey')
                # elif k < jbb:
                    # print("hola")
                    # axs[0].fill_between((hBroad[1][k],hBroad[1][k+1]), 0.5, hBroad[2][j],color='grey')
    # Set the labels for the three plots
        axs[1].set_xlabel(r'$Z^{+}_{h}$', loc="center", fontsize=15)
        axs[1].set_ylabel(r'$Zh_1$', loc="center", fontsize=15)

        axs[1].legend(frameon=True, loc='lower right',
                      fontsize=10, framealpha=1)

        axs[1].set_xticks([.2, .4, .6, .8, 1])
        axs[1].set_xticks([.1, .2, .3, .4, .5, .6, .8, 1], minor=True)
        axs[1].set_yticks([0, .1, .2, .3, .4, .5, .6, .8, 1], minor=True)
        axs[1].set_xticklabels([.2, .4, .6, .8, 1])
        axs[1].tick_params(right=False, top=False, left=False,
                           bottom=False, which='minor')
        cb = fig.colorbar(hBroad[3], ax=axs[1])

        cb.formatter.set_powerlimits((0, 0))
        cb.ax.yaxis.set_offset_position('left')
        cb.update_ticks()

        axs[1].grid(which='both', axis='both', color='black', alpha=1)
        # axs[0].set_axisbelow(True)

        file = ROOT.TFile.Open(dataDirectory + "Pt_broad_Zh.root", "READ")
        graphName = "PtBroad_Zh_" + tarList[i] + "_1"
        graph = file.Get(graphName)
        nPoints = graph.GetN()
        weight = np.ndarray(nPoints, dtype=float, buffer=graph.GetY())
        errors = np.ndarray(nPoints, dtype=float, buffer=graph.GetEY())

        YBin = [0, 1]
        x = [.05, .15, .25, .35, .45, .55, .7, .9]
        y = np.linspace(0.5, 0.5, len(x))
        # cmap_white = mcolors.ListedColormap(['white'])
        cmap_white = cm
        hBroad1DError = axs[0].hist2d(x, y, bins=(
            binsX, YBin), weights=errors, cmap=cmap_white)
        hBroad1D = axs[0].hist2d(x, y, bins=(
            binsX, YBin), weights=weight, cmap=cmap_white)

        colorLimit = np.amax(weight)*0.75
        for j in range(len(hBroad1D[2])-1):
            for k in range(len(hBroad1D[1])-1):
                deltaX = (hBroad1D[1][k+1] - hBroad1D[1][k])/2
                deltaY = (hBroad1D[2][j+1] - hBroad1D[2][j])/2
                # print(hBroad1D[2][j])
                if hBroad1D[0].T[j, k] < colorLimit:
                    color = textColor1
                else:
                    color = textColor2
                axs[0].text(hBroad1D[1][k]+deltaX, hBroad1D[2][j]+deltaY+0.24, round(hBroad1D[0].T[j, k], 3),
                            color=color, ha="center", va="center", fontsize=10, fontweight="bold")
                axs[0].text(hBroad1DError[1][k]+deltaX, hError[2][j]+deltaY-0.24, round(hBroad1DError[0].T[j, k], 3),
                            color=color, ha="center", va="center", fontsize=10, fontweight="bold")
                axs[0].text(hError[1][k]+deltaX, hError[2][j]+deltaY-0.0, '$\pm$',
                            color=color, ha="center", va="center", fontsize=10, fontweight="bold")

        axs[0].tick_params(right=False, top=False, left=False,
                           bottom=False, which='minor')
        axs[0].set_xticks([.2, .4, .6, .8, 1])
        axs[0].set_xticks([.1, .2, .3, .4, .5, .6, .8, 1], minor=True)
        axs[0].set_yticks([0, 1], minor=True)
        axs[0].set_xticklabels([.2, .4, .6, .8, 1])
        axs[0].xaxis.set_tick_params(labeltop=True, labelbottom=False)
        axs[0].yaxis.set_tick_params(labelleft=False)
        axs[0].tick_params(right=False, top=False, left=False,
                           bottom=False, which='minor')
        cb1D = fig.colorbar(hBroad1D[3], ax=axs[0])

        cb1D.formatter.set_powerlimits((0, 0))
        cb1D.ax.yaxis.set_offset_position('left')
        cb1D.update_ticks()

        axs[0].grid(which='both', axis='both', color='black', alpha=1)

        file.Close()
        fig.savefig(outputDirectory + "PtBroad2DZhSum_" +
                    tarList[i] + "-wExtra.pdf", bbox_inches='tight')
        fig.savefig(outputDirectory + "PtBroad2DZhSum_" +
                    tarList[i] + "-wExtra.png", bbox_inches='tight', dpi=400)
        fig.savefig(outputDirectory + "PtBroad2DZhSum_" +
                    tarList[i] + "-wExtra.eps", bbox_inches='tight', format='eps')
        print(outputDirectory + "PtBroad2DZhSum-wExtra.pdf Has been created")


# PtBroad2DZhSum()
# PtBroad2DZhSumExtra()
# PtBroad2DZhSumOne()
Zh2DDistribution()
