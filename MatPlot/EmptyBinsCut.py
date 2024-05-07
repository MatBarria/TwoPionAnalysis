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
yScalarFormatter.set_powerlimits((0, 0))

nPion = 2
draw_label = True
# mpl.use('pgf')

ZhBINS = [.0, .1, .2, .3, .4, .5, .6, .8, 1]
tarList = ['C', "Fe", "Pb", 'DC', "DFe", "DPb"]
colorList = ['#301437', 'orange', "lightgreen"]
nPionList = ["One $\pi +$", "Two $\pi+$", "Three $\pi +$"]


def EmptyBinsSimZhDist():

    vars = ['Cut', 'ZhBin']
    fig, axs = plt.subplots(1, 3, sharey='row', sharex='col')
    width = 16  # 7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.02, hspace=0.02)

    bins = [.1, .2, .3, .4, .5, .6, .8, 1]

    for i in range(3):  # Loops on the diffrent targets
        axs[i].set_xticks([.1, .3, .5, .7])
        for j in range(nPion):  # Loops on the number of pions

            axs[i].set_xlim(.1, .799)
            axs[i].set_ylim(0, .2)
            with ur.open(inputDirectory +
                         "EmptyBinsCut.root:EmptyBins_" + tarList[i] + "_" + str(j+1)) as file:
                dic = file.arrays(vars, library="np")

            weights = dic["ZhBin"][dic["Cut"] == 0]
            Zh = dic["ZhBin"][dic["Cut"] == 0]

            for k in range(8):
                if (len(dic["ZhBin"][dic["ZhBin"] == k]) == 0):
                    weights[weights == k] = 0
                else:
                    weights[weights == k] = 1 / \
                        float(len(dic["ZhBin"][dic["ZhBin"] == k]))

            for t in range(len(Zh)):
                for k in range(8):
                    if Zh[t] == k:
                        Zh[t] = ZhBINS[k] + 0.001

            axs[i].hist(Zh, bins=bins, weights=weights,
                        color=colorList[j], histtype="step", label="Solid " + nPionList[j])

            weights = np.array([])
            Zh = np.array([])

            with ur.open(inputDirectory +
                         "EmptyBinsCut.root:EmptyBins_D" + tarList[i] + "_" + str(j+1)) as file:
                dic = file.arrays(vars, library="np")

            weights = dic["ZhBin"][dic["Cut"] == 0]
            Zh = dic["ZhBin"][dic["Cut"] == 0]
            for k in range(8):
                if (len(dic["ZhBin"][dic["ZhBin"] == k]) == 0):
                    weights[weights == k] = 0
                else:
                    weights[weights == k] = 1 / \
                        float(len(dic["ZhBin"][dic["ZhBin"] == k]))

            for t in range(len(Zh)):
                for k in range(8):
                    if Zh[t] == k:
                        print("Zhbin = " + str(Zh[t]) +
                              " Zh value: " + str(ZhBINS[k]))
                        Zh[t] = ZhBINS[k] + 0.001

            axs[i].hist(Zh, bins=bins, weights=weights,
                        color=colorList[j], histtype="step", label='Liquid ' + nPionList[j],
                        linestyle="--")

            weights = np.array([])
            Zh = np.array([])

            axs[i].tick_params(right=False, top=False, which='both')

        axs[i].set_xlabel(r'$Z_h$', fontsize=14)

        axs[0].set_ylabel(r'Empty Bins', loc="center", fontsize=15)

    axs[0].annotate(r'Carbon', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(r'Iron',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[2].annotate(r'Lead',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)

    for i in range(3):
        axs[i].grid(visible=None, axis='both', color='0.95')
        axs[i].set_axisbelow(True)

    if draw_label:
        axs[0].legend(frameon=False, loc='upper left', fontsize=11, ncol=2)

    fig.savefig(outputDirectory + "EmptyBincutZhNAccept.pdf",
                bbox_inches='tight')
    print(outputDirectory + "EmptyBinCutZh.pdf Has been created")


def EmptyBinsSimPt2Dist():

    vars = ['Cut', 'Pt2Bin']
    fig, axs = plt.subplots(1, 3, sharey='row', sharex='col')
    width = 16  # 7.056870070568701
    height = 4
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.02, hspace=0.02)

    dic = {"Cut": np.array([]), "Pt2": np.array([])}
    for i in range(3):  # Loops on the diffrent targets
        for j in range(nPion):  # Loops on the number of pions

            with ur.open(inputDirectory +
                         "EmptyBinsCut.root:EmptyBins_" + tarList[i] + "_" + str(j+1)) as file:
                temp = file.arrays(vars, library="np")
                dic["Cut"] = np.concatenate((dic["Cut"], temp['Cut']), axis=0)
                dic["Pt2"] = np.concatenate(
                    (dic["Pt2"], temp['Pt2Bin']), axis=0)

            weights = dic["Pt2"][dic["Cut"] == 0]
            for k in range(60):
                if (len(dic["Pt2"][dic["Pt2"] == k]) == 0):
                    weights[weights == k] = 0
                else:
                    weights[weights == k] = 1 / \
                        float(len(dic["Pt2"][dic["Pt2"] == k]))

            axs[i].hist(dic["Pt2"][dic["Cut"] == 0], bins=60, range=(0, 60), weights=weights,
                        color=colorList[j], histtype="step", label=nPionList[j])
            dic = {"Cut": np.array([]), "Pt2": np.array([])}

            with ur.open(inputDirectory +
                         "EmptyBinsCut.root:EmptyBins_D" + tarList[i] + "_" + str(j+1)) as file:
                temp = file.arrays(vars, library="np")
                dic["Cut"] = np.concatenate((dic["Cut"], temp['Cut']), axis=0)
                dic["Pt2"] = np.concatenate(
                    (dic["Pt2"], temp['Pt2Bin']), axis=0)

            weights = dic["Pt2"][dic["Cut"] == 0]
            for k in range(60):
                if (len(dic["Pt2"][dic["Pt2"] == k]) == 0):
                    weights[weights == k] = 0
                else:
                    weights[weights == k] = 1 / \
                        float(len(dic["Pt2"][dic["Pt2"] == k]))

            axs[i].hist(dic["Pt2"][dic["Cut"] == 0], bins=60, range=(0, 60), weights=weights,
                        color=colorList[j], histtype="step", label=nPionList[j], linestyle="--")
            axs[i].tick_params(right=False, top=False, which='both')
            dic = {"Cut": np.array([]), "Pt2": np.array([])}

        axs[i].set_xlabel(r'$Pt2 Bin$', fontsize=14)

        axs[0].set_ylabel(r'$EmptyBins$', loc="center", fontsize=15)

    axs[0].annotate(r'Carbon', xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(r'Iron',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)
    axs[2].annotate(r'Lead',   xy=(0.04, 1.04),
                    xycoords='axes fraction', fontsize=15)

    if draw_label:
        axs[0].legend(frameon=False, loc='upper left', fontsize=11)

    fig.savefig(outputDirectory + "EmptyBincutPt2.pdf", bbox_inches='tight')
    print(outputDirectory + "EmptyBinCutPt2.pdf Has been created")


EmptyBinsSimZhDist()
EmptyBinsSimPt2Dist()
