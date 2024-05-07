import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import mplhep as hep
import uproot as ur
from include import SaveFigure
from matplotlib import cm

from include import dataDirectory, outputDirectory

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

nPion = 2
draw_label = True
# mpl.use('pgf')

ZhBINS = [.0, .1, .2, .3, .4, .5, .6, .8, 1]
tarList = ['C', "Fe", "Pb", 'DC', "DFe", "DPb"]
colorList = ['red', 'blue', "black", 'green']
label = ["2 pions Xf > 0 ", "1 pions Xf > 0 ", "0 pions Xf > 0 ", "No cuts"]


def Xf_dist():

    vars = ['Zh', 'Xf1', 'Xf2', "VC_TM"]
    bins = [.1, .2, .3, .4, .5, .6, .8, 1]
    fig, axs = plt.subplots(1, 3, sharey='row', sharex='col')
    width = 16  # 7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.02, hspace=0.02)

    for l in range(3):
        for i in range(3):  # Loops on the diffrent targets
            axs[i].set_xlim(0.2, 1.0)

            dic = {}

            with ur.open(dataDirectory +
                         "Xf_" + tarList[i] + ".root:ntuple_2_pion") as file:
                dic = file.arrays(vars, library="np")

            dic["Zh"] = dic["Zh"][dic["VC_TM"] == 2]
            dic["Xf1"] = dic["Xf1"][dic["VC_TM"] == 2]
            dic["Xf2"] = dic["Xf2"][dic["VC_TM"] == 2]

            weights = np.ones_like(dic["Zh"])

            if l == 0:
                condition = (dic['Xf1'] > 0) & (dic['Xf2'] > 0)
                weights[~condition] = 0
            elif l == 1:
                condition = ((dic['Xf1'] > 0) & (dic['Xf2'] < 0)) | (
                    (dic['Xf2'] > 0) & (dic['Xf1'] < 0))
                weights[~condition] = 0
            elif l == 2:
                condition = (dic['Xf1'] < 0) & (dic['Xf2'] < 0)
                weights[~condition] = 0

            weights = weights / float(len(dic["Zh"]))

            if l == 3:
                axs[i].hist(dic["Zh"], bins=bins, weights=weights,
                            color="gray", histtype="step", label="Solid Target")

            axs[i].hist(dic["Zh"], bins=bins, weights=weights,
                        color=colorList[l], histtype="step", label=label[l])

            dic = {}

            with ur.open(dataDirectory +
                         "Xf_" + tarList[i] + ".root:ntuple_2_pion") as file:
                dic = file.arrays(vars, library="np")

            dic["Zh"] = dic["Zh"][dic["VC_TM"] == 1]
            dic["Xf1"] = dic["Xf1"][dic["VC_TM"] == 1]
            dic["Xf2"] = dic["Xf2"][dic["VC_TM"] == 1]

            weights = np.ones_like(dic["Zh"])

            if l == 0:
                condition = (dic['Xf1'] > 0) & (dic['Xf2'] > 0)
                weights[~condition] = 0
            elif l == 1:
                condition = ((dic['Xf1'] > 0) & (dic['Xf2'] < 0)) | (
                    (dic['Xf2'] > 0) & (dic['Xf1'] < 0))
                weights[~condition] = 0
            elif l == 2:
                condition = (dic['Xf1'] < 0) & (dic['Xf2'] < 0)
                weights[~condition] = 0

            weights = weights / float(len(dic["Zh"]))

            if l == 3:
                axs[i].hist(dic["Zh"], bins=bins, weights=weights,
                            color="gray", histtype="step", label="Liquid Target",
                            linestyle="--")
            # axs[i].hist(dic["Zh"], bins=bins, weights=weights,
                # color=colorList[l], histtype="step", linestyle="--")

            # axs[i].tick_params(right=False, top=False, which='both')

        axs[i].set_xlabel(r'$Zh_{Sum}$', fontsize=14)

        axs[0].set_ylabel(r'$EmptyBins$', loc="center", fontsize=15)

    axs[0].annotate(r'Carbon', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(r'Iron',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[2].annotate(r'Lead',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)

    if draw_label:
        axs[0].legend(frameon=False, loc='upper left', fontsize=11, ncol=2)

    SaveFigure(fig, outputDirectory, "Xf_dist")


def Xf_dist_norlized_per_bin():

    vars = ['Zh', 'Xf1', 'Xf2', "VC_TM"]
    bins = [.1, .2, .3, .4, .5, .6, .8, 1]
    fig, axs = plt.subplots(1, 3, sharey='row', sharex='col')
    width = 16  # 7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.02, hspace=0.02)

    for l in range(3):
        for i in range(3):  # Loops on the diffrent targets
            axs[i].set_xlim(0.2, 1.0)

            dic = {}

            with ur.open(dataDirectory +
                         "Xf_" + tarList[i] + ".root:ntuple_2_pion") as file:
                dic = file.arrays(vars, library="np")

            dic["Zh"] = dic["Zh"][dic["VC_TM"] == 2]
            dic["Xf1"] = dic["Xf1"][dic["VC_TM"] == 2]
            dic["Xf2"] = dic["Xf2"][dic["VC_TM"] == 2]

            hist1, bin_edges1 = np.histogram(dic["Zh"], bins=bins)

            if l == 0:
                condition = (dic['Xf1'] > 0) & (dic['Xf2'] > 0)
                dic["Zh"] = dic["Zh"][condition]
            elif l == 1:
                condition = ((dic['Xf1'] > 0) & (dic['Xf2'] < 0)) | (
                    (dic['Xf2'] > 0) & (dic['Xf1'] < 0))
                dic["Zh"] = dic["Zh"][condition]
            elif l == 2:
                condition = (dic['Xf1'] < 0) & (dic['Xf2'] < 0)
                dic["Zh"] = dic["Zh"][condition]

            hist2, bin_edges2 = np.histogram(dic["Zh"], bins=bins)

            if l == 3:
                axs[i].hist(dic["Zh"], bins=bins, weights=weights,
                            color="gray", histtype="step", label="Solid Target")

            divided_hist = hist2 / hist1

            # axs[i].hist(dic["Zh"], bins=bins, weights=weights,
            # color=colorList[l], histtype="step", label=label[l])
            axs[i].hist(bin_edges1[:-1], bins=bin_edges1, weights=divided_hist,
                        color=colorList[l], histtype="step", label=label[l])

            dic = {}

            with ur.open(dataDirectory +
                         "Xf_" + tarList[i] + ".root:ntuple_2_pion") as file:
                dic = file.arrays(vars, library="np")

            dic["Zh"] = dic["Zh"][dic["VC_TM"] == 1]
            dic["Xf1"] = dic["Xf1"][dic["VC_TM"] == 1]
            dic["Xf2"] = dic["Xf2"][dic["VC_TM"] == 1]

            weights = np.ones_like(dic["Zh"])

            if l == 0:
                condition = (dic['Xf1'] > 0) & (dic['Xf2'] > 0)
                weights[~condition] = 0
            elif l == 1:
                condition = ((dic['Xf1'] > 0) & (dic['Xf2'] < 0)) | (
                    (dic['Xf2'] > 0) & (dic['Xf1'] < 0))
                weights[~condition] = 0
            elif l == 2:
                condition = (dic['Xf1'] < 0) & (dic['Xf2'] < 0)
                weights[~condition] = 0

            weights = weights / float(len(dic["Zh"]))

            if l == 3:
                axs[i].hist(dic["Zh"], bins=bins, weights=weights,
                            color="gray", histtype="step", label="Liquid Target",
                            linestyle="--")
            # axs[i].hist(dic["Zh"], bins=bins, weights=weights,
                # color=colorList[l], histtype="step", linestyle="--")

            # axs[i].tick_params(right=False, top=False, which='both')

            axs[i].set_xlabel(r'$Zh_{Sum}$', fontsize=14)

        axs[0].set_ylabel(r'Xf pion percentaje', loc="center", fontsize=15)

    axs[0].annotate(r'Carbon', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(r'Iron',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[2].annotate(r'Lead',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)

    if draw_label:
        axs[0].legend(frameon=False, loc='upper left', fontsize=11, ncol=2)

    SaveFigure(fig, outputDirectory, "Xf_dist_norlized_per_bin")


def Xf_dist_norlized_per_bin_4Box():

    vars = ['Zh', 'Xf1', 'Xf2', "VC_TM"]
    tarList = ["Fe" ,'C', "Fe", "Pb"]
    bins = [.1, .2, .3, .4, .5, .6, .8, 1]
    fig, axs = plt.subplots(2, 2, sharey='row', sharex='col')
    width = 10.6  # 7.056870070568701
    height = 8
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.02, hspace=0.2)

    for l in range(3):
        i = -1
        for a in range(2):  # Loops on the diffrent targets
            for b in range(2):  # Loops on the diffrent targets
                
                i = i + 1
                axs[a][b].set_xlim(0.2, 1.0)

                dic = {}

                with ur.open(dataDirectory +
                             "Xf_" + tarList[i] + ".root:ntuple_2_pion") as file:
                    dic = file.arrays(vars, library="np")

                if  i==0:
                    dic["Zh"] = dic["Zh"][dic["VC_TM"] == 1]
                    dic["Xf1"] = dic["Xf1"][dic["VC_TM"] == 1]
                    dic["Xf2"] = dic["Xf2"][dic["VC_TM"] == 1]
                else:
                    dic["Zh"] = dic["Zh"][dic["VC_TM"] == 2]
                    dic["Xf1"] = dic["Xf1"][dic["VC_TM"] == 2]
                    dic["Xf2"] = dic["Xf2"][dic["VC_TM"] == 2]

                hist1, bin_edges1 = np.histogram(dic["Zh"], bins=bins)

                if l == 0:
                    condition = (dic['Xf1'] > 0) & (dic['Xf2'] > 0)
                    dic["Zh"] = dic["Zh"][condition]
                elif l == 1:
                    condition = ((dic['Xf1'] > 0) & (dic['Xf2'] < 0)) | (
                        (dic['Xf2'] > 0) & (dic['Xf1'] < 0))
                    dic["Zh"] = dic["Zh"][condition]
                elif l == 2:
                    condition = (dic['Xf1'] < 0) & (dic['Xf2'] < 0)
                    dic["Zh"] = dic["Zh"][condition]

                hist2, bin_edges2 = np.histogram(dic["Zh"], bins=bins)

                divided_hist = hist2 / hist1

                # axs[i].hist(dic["Zh"], bins=bins, weights=weights,
                # color=colorList[l], histtype="step", label=label[l])
                axs[a][b].hist(bin_edges1[:-1], bins=bin_edges1, weights=divided_hist,
                            color=colorList[l], histtype="step", label=label[l])

                dic = {}


                axs[a][b].set_xlabel(r'$Zh_{Sum}$', fontsize=14)

            axs[0][0].set_ylabel(r'Xf pions percentaje', loc="center", fontsize=15)
            axs[1][0].set_ylabel(r'Xf pions percentaje', loc="center", fontsize=15)

    axs[0][0].annotate(r'Deuterium', xy=(0.04, 1.04),
                        xycoords='axes fraction', fontsize=15)
    axs[0][1].annotate(r'Carbon', xy=(0.04, 1.04),
                        xycoords='axes fraction', fontsize=15)
    axs[1][0].annotate(r'Iron',   xy=(0.04, 1.04),
                        xycoords='axes fraction', fontsize=15)
    axs[1][1].annotate(r'Lead',   xy=(0.04, 1.04),
                        xycoords='axes fraction', fontsize=15)

    axs[0][0].legend(frameon=False, loc='upper left', fontsize=11, ncol=2)

    SaveFigure(fig, outputDirectory, "Xf_dist_norlized_per_bin_LT")

def Xf_2Ddist():

    vars = ['Xf1', 'Xf2', "VC_TM"]
    tarList = ["Fe" ,'C', "Fe", "Pb"]
    bins = [.1, .2, .3, .4, .5, .6, .8, 1]
    fig, axs = plt.subplots(2, 2, sharey='row', sharex='col')
    width = 10.6  # 7.056870070568701
    height = 8
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.02, hspace=0.2)
    
    x1 = np.linspace(0, 0)
    y1 = np.linspace(-100, 100)
    x2 = np.linspace(-100, 100)
    y2 = np.linspace(0, 0)


    n_bins = 100
    binsX = np.linspace(-.3, .3, num = n_bins)
    binsY = np.linspace(-.3, .3, num = n_bins)
    i = -1
    for a in range(2):  # Loops on the diffrent targets
        for b in range(2):  # Loops on the diffrent targets
            
            i = i + 1
            axs[a][b].set_xlim(0.2, 1.0)

            dic = {}

            with ur.open(dataDirectory +
                         "Xf_" + tarList[i] + ".root:ntuple_2_pion") as file:
                dic = file.arrays(vars, library="np")

            if  i==0:
                dic["Xf1"] = dic["Xf1"][dic["VC_TM"] == 1]
                dic["Xf2"] = dic["Xf2"][dic["VC_TM"] == 1]
            else:
                dic["Xf1"] = dic["Xf1"][dic["VC_TM"] == 2]
                dic["Xf2"] = dic["Xf2"][dic["VC_TM"] == 2]

            # axs[i].hist(dic["Zh"], bins=bins, weights=weights,
            # color=colorList[l], histtype="step", label=label[l])
            cmp = plt.cm.viridis
            cmap = cmp.copy()
            cmap.set_under(color='white')
            h = axs[a][b].hist2d(dic["Xf1"], dic["Xf2"], bins = (binsX, binsY), cmap = cmap,rasterized = True, vmin = 1)

            dic = {}
            axs[a][b].plot(x1, y1,color ='white' , linestyle = '--', linewidth = .9) 
            axs[a][b].plot(x2, y2,color ='white' , linestyle = '--', linewidth = .9) 


            axs[a][b].set_xlabel(r'$Xf_1$', fontsize=14)

        axs[0][0].set_ylabel(r'$Xf_2$', loc="center", fontsize=15)
        axs[1][0].set_ylabel(r'$Xf_2$', loc="center", fontsize=15)

    axs[0][0].annotate(r'Deuterium', xy=(0.04, 1.04),
                        xycoords='axes fraction', fontsize=15)
    axs[0][1].annotate(r'Carbon', xy=(0.04, 1.04),
                        xycoords='axes fraction', fontsize=15)
    axs[1][0].annotate(r'Iron',   xy=(0.04, 1.04),
                        xycoords='axes fraction', fontsize=15)
    axs[1][1].annotate(r'Lead',   xy=(0.04, 1.04),
                        xycoords='axes fraction', fontsize=15)

    # axs[0][0].legend(frameon=False, loc='upper left', fontsize=11, ncol=2)

    SaveFigure(fig, outputDirectory, "Xf_2D")

# Xf_dist()
Xf_dist_norlized_per_bin()
Xf_dist_norlized_per_bin_4Box()
Xf_2Ddist()
