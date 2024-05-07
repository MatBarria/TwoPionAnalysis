import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import uproot as ur
import os

from include import inputDirectory, outputDirectory

plt.style.use(hep.style.ATLAS)  # or ATLAS/LHCb2

nPion = 2

tarList = ['C', "Fe", "Pb", 'DC', "DFe", "DPb"]
disColor = ['blue', '#301437', "lightgreen"]
colorList = ["lightgreen", "orange"]
nPionList = ["One $\pi^+$", "Two $\pi^+$", "Three $\pi^+$"]

xLabel = {"Q2":    r'$Q^2$[GeV^2]',
          "Nu":    r'$\nu$[GeV]',
          "Zh":    r'$Zh_\mathrm{Sum}$',
          # "Pt2":   r'$P_t^2 [GeV^2]$',
          "Pt2":   r'$P_t^{+2} [GeV^2]$',
          "Phi": r'$\phu^2_{PQ}[Deg]$'
          }

binning = {"Q2": [1., 1.30, 1.74, 4.00],
           "Nu": [2.2, 3.36, 3.82, 4.26],
           "Zh": [0., .1, .2, .3, .4, .5, .6, .8, 1.],
           "Pt2": np.linspace(0, 3, 60),
           "Phi": np.linspace(-180, 180, 6)
           }

ZhLabel = [r"$0.0< Z^{+}_h < 0.1$",
           r"$0.1< Z^{+}_h < 0.2$",
           r"$0.2< Z^{+}_h < 0.3$",
           r"$0.3< Z^{+}_h < 0.4$",
           r"$0.4< Z^{+}_h < 0.5$",
           r"$0.5< Z^{+}_h < 0.6$",
           r"$0.6< Z^{+}_h < 0.8$",
           r"$0.8< Z^{+}_h < 1.0$",
           ]


variables = ["Q2", "Nu", "Zh", "Pt2", "Phi"]

flag1 = False
flag2 = True
flag3 = not (flag1 or flag2)


outputDirectory = outputDirectory + "EmptyBins/"
# Create the directory if doesn't exist
os.makedirs(outputDirectory, exist_ok=True)


def SetLargeFigure(fig):

    width = 16*(2/3)  # 7.056870070568701
    height = 4*(len(binning["Zh"]) - 2)
    fig.set_size_inches(width, height)

    fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.09, hspace=0.2)


def SetAxs(axs, ZhBin, var):

    axs[0].annotate(ZhLabel[ZhBin], xy=(0.32, 0.9),
                    xycoords='axes fraction', fontsize=15)
    axs[1].annotate(ZhLabel[ZhBin], xy=(0.32, 0.9),
                    xycoords='axes fraction', fontsize=15)

    axs[0].grid(visible=None, axis='both', color='0.95')
    axs[0].set_axisbelow(True)
    axs[1].grid(visible=None, axis='both', color='0.95')
    axs[1].set_axisbelow(True)

    axs[0].legend(frameon=False, loc='center right', fontsize=11)
    axs[1].legend(frameon=False, loc='center right', fontsize=11)

    axs[1].annotate(r'Solid', xy=(0.04, 1.04), xycoords='axes fraction',
                    fontsize=15)
    axs[0].annotate(r'Liquid',   xy=(0.04, 1.04), xycoords='axes fraction',
                    fontsize=15)

    if not flag3 or ZhBin == 7:

        axs[0].set_xlabel(xLabel[var], fontsize=14)
        axs[1].set_xlabel(xLabel[var], fontsize=14)

    if flag1:

        axs[0].tick_params(right=False, top=False,
                           which='both', labelbottom=True)
        axs[1].tick_params(right=False, top=False,
                           which='both', labelbottom=True)
        axs[0].xaxis.set_label_coords(1.04, -0.09)
        axs[1].xaxis.set_label_coords(1.04, -0.09)

    else:
        axs[0].tick_params(right=False, top=False, which='both')
        axs[1].tick_params(right=False, top=False, which='both')


def SaveFigure(fig, outputDirectory, name):

    fig.savefig(outputDirectory + name + ".pdf", bbox_inches='tight')
    fig.savefig(outputDirectory + name + ".png", bbox_inches='tight', dpi=300)
    print(outputDirectory + name + " Has been created")


def EmptyBinsSimVarZh(var="Pt2"):

    varBin = var + "Bin"
    vars = ['Data', varBin, "ZhBin"]

    fig, axs = plt.subplots(7, 2, sharey='row', sharex='col')
    SetLargeFigure(fig)

    for ZhBin in range(1, len(binning["Zh"]) - 1):
        for j in range(1, nPion):  # Loops on the number of pions

            data = np.array([])
            values = np.array([])

            for i in range(0, 3):  # Loops on the diffrent targets

                with ur.open(inputDirectory +
                             "EmptyBins.root:EmptyBins_" + tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library="np")

                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001

                dic[varBin] = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"] = dic["Data"][dic["ZhBin"] == ZhBin]

                values = np.concatenate((values,  dic[varBin]), axis=0)
                data = np.concatenate((data,  dic["Data"]), axis=0)

            axs[ZhBin-1][1].hist(values, bins=binning[var],
                                 color=disColor[j],
                                 label="Data")

            axs[ZhBin-1][1].hist(values[data == 1], bins=binning[var],
                                 color=colorList[j],
                                 label="Data and Sim.", zorder=2)

            data = np.array([])
            values = np.array([])

            for i in range(0, 3):
                with ur.open(inputDirectory +
                             "EmptyBins.root:EmptyBins_D" + tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library="np")

                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001

                dic[varBin] = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"] = dic["Data"][dic["ZhBin"] == ZhBin]

                values = np.concatenate((values,  dic[varBin]), axis=0)
                data = np.concatenate((data,  dic["Data"]), axis=0)

            axs[ZhBin-1][0].hist(values, bins=binning[var],
                                 color=disColor[j],
                                 label="Data",
                                 linestyle='-')

            axs[ZhBin-1][0].hist(values[data == 1], bins=binning[var],
                                 color=colorList[j],
                                 label="Data and Sim", linestyle="-", zorder=2)

        axs[ZhBin-1][0].set_ylabel(r'Bins', loc="center", fontsize=15)
        SetAxs(axs[ZhBin-1], ZhBin, var)

    SaveFigure(fig, outputDirectory, "EmptyBinsSim_" + var + "_Zh")


def EmptyBinsNormSimVarZh(var="Pt2"):

    varBin = var + "Bin"
    vars = ['Data', varBin, "ZhBin"]

    fig, axs = plt.subplots(7, 2, sharey='row', sharex='col')
    SetLargeFigure(fig)

    for ZhBin in range(1, len(binning["Zh"]) - 1):
        for j in range(1, nPion):  # Loops on the number of pions

            data = np.array([])
            values = np.array([])

            for i in range(0, 3):  # Loops on the diffrent targets

                with ur.open(inputDirectory +
                             "EmptyBins.root:EmptyBins_" + tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library="np")

                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001

                dic[varBin] = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"] = dic["Data"][dic["ZhBin"] == ZhBin]

                values = np.concatenate((values,  dic[varBin]), axis=0)
                data = np.concatenate((data,  dic["Data"]), axis=0)

            hist = axs[ZhBin-1][1].hist(values[data == 0], bins=binning[var],
                                        color=colorList[j],
                                        weights=np.ones_like(
                                            values[data == 0])*(100/len(values)),
                                        label="Lost Bins " + nPionList[j], zorder=2)

            data = np.array([])
            values = np.array([])

            for i in range(0, 3):
                with ur.open(inputDirectory +
                             "EmptyBins.root:EmptyBins_D" + tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library="np")

                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001

                dic[varBin] = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"] = dic["Data"][dic["ZhBin"] == ZhBin]

                values = np.concatenate((values,  dic[varBin]), axis=0)
                data = np.concatenate((data,  dic["Data"]), axis=0)

            hist = axs[ZhBin-1][0].hist(values[data == 0], bins=binning[var],
                                        color=colorList[j],
                                        weights=np.ones_like(
                                            values[data == 0])*(100/len(values)),
                                        label="Lost Bins " + nPionList[j], zorder=2)

        axs[ZhBin-1][0].set_ylim(0., 2.5)
        axs[ZhBin-1][1].set_ylim(0., 2.5)

        axs[ZhBin-1][0].set_ylabel(r'Lost Bins(%)', loc="center", fontsize=15)
        SetAxs(axs[ZhBin-1], ZhBin, var)

    SaveFigure(fig, outputDirectory, "EmptyBinsSimNorm_" + var + "_Zh")


def EmptyDataSimVarZh(var="Pt2"):

    varBin = var + "Bin"
    vars = ['Data', varBin, "ZhBin", "Evnts"]

    fig, axs = plt.subplots(7, 2, sharey='row', sharex='col')
    SetLargeFigure(fig)

    for ZhBin in range(1, len(binning["Zh"]) - 1):
        for j in range(1, nPion):  # Loops on the number of pions

            data = np.array([])
            values = np.array([])
            events = np.array([])

            for i in range(0, 3):  # Loops on the diffrent targets

                with ur.open(inputDirectory +
                             "EmptyBins.root:EmptyBins_" + tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library="np")

                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001

                dic[varBin] = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"] = dic["Data"][dic["ZhBin"] == ZhBin]
                dic["Evnts"] = dic["Evnts"][dic["ZhBin"] == ZhBin]

                values = np.concatenate((values, dic[varBin]),  axis=0)
                data = np.concatenate((data,   dic["Data"]),  axis=0)
                events = np.concatenate((events, dic["Evnts"]), axis=0)

            axs[ZhBin-1][1].hist(values, bins=binning[var],
                                 color=disColor[j], weights=events,
                                 label="Data")

            axs[ZhBin-1][1].hist(values[data == 1], bins=binning[var],
                                 color=colorList[j], weights=events[data == 1],
                                 label="Data and Sim", zorder=2)

            data = np.array([])
            values = np.array([])
            events = np.array([])

            for i in range(0, 3):
                with ur.open(inputDirectory +
                             "EmptyBins.root:EmptyBins_D" + tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library="np")

                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001

                dic[varBin] = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"] = dic["Data"][dic["ZhBin"] == ZhBin]
                dic["Evnts"] = dic["Evnts"][dic["ZhBin"] == ZhBin]

                values = np.concatenate((values,  dic[varBin]), axis=0)
                data = np.concatenate((data,  dic["Data"]), axis=0)
                events = np.concatenate((events,  dic["Evnts"]), axis=0)

            axs[ZhBin-1][0].hist(values, bins=binning[var],
                                 color=disColor[j], weights=events,
                                 label="Data")

            axs[ZhBin-1][0].hist(values[data == 1], bins=binning[var],
                                 color=colorList[j], weights=events[data == 1],
                                 label="Data and Sim", zorder=2)

        axs[ZhBin-1][0].set_yscale('log')
        axs[ZhBin-1][1].set_yscale('log')
        axs[ZhBin-1][0].set_ylim(0.5, 400000)
        axs[ZhBin-1][1].set_ylim(0.5, 400000)
        axs[ZhBin-1][0].set_ylabel(r'dN/d'+var, loc="center", fontsize=15)

        SetAxs(axs[ZhBin-1], ZhBin, var)

    SaveFigure(fig, outputDirectory, "EmptyDataSim_" + var + "_ZhBin")


def EmptyDataNormSimVarZh(var="Pt2"):

    varBin = var + "Bin"
    vars = ['Data', varBin, "ZhBin", "Evnts"]

    fig, axs = plt.subplots(7, 2, sharey='row', sharex='col')
    SetLargeFigure(fig)

    for ZhBin in range(1, len(binning["Zh"]) - 1):
        for j in range(1, nPion):  # Loops on the number of pions

            data = np.array([])
            values = np.array([])
            events = np.array([])

            for i in range(0, 3):
                with ur.open(inputDirectory +
                             "EmptyBins.root:EmptyBins_D" + tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library="np")

                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001

                dic[varBin] = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"] = dic["Data"][dic["ZhBin"] == ZhBin]
                dic["Evnts"] = dic["Evnts"][dic["ZhBin"] == ZhBin]

                values = np.concatenate((values,  dic[varBin]), axis=0)
                data = np.concatenate((data,  dic["Data"]), axis=0)
                events = np.concatenate((events,  dic["Evnts"]), axis=0)

            hist = axs[ZhBin-1][0].hist(values[data == 0], bins=binning[var],
                                        color=colorList[j],
                                        weights=(
                                            events[data == 0]*100)/np.sum(events),
                                        label="Lost Data " + nPionList[j], zorder=2)

            # print("Solids targets " + str(j+1) + " pions in " + ZhLabel[ZhBin] +
            # " percentaje of loss events: ", end="")
            print(ZhLabel[ZhBin] + " & ", end="")
            print(round(np.sum(hist[0]), 3), end="")

            data = np.array([])
            values = np.array([])
            events = np.array([])

            for i in range(0, 3):  # Loops on the diffrent targets

                with ur.open(inputDirectory +
                             "EmptyBins.root:EmptyBins_" + tarList[i] + "_" + str(j+1)) as file:
                    dic = file.arrays(vars, library="np")

                for t in range(len(dic[varBin])):
                    for k in range(len(binning[var])):
                        if dic[varBin][t] == k:
                            dic[varBin][t] = binning[var][k] + 0.001

                dic[varBin] = dic[varBin][dic["ZhBin"] == ZhBin]
                dic["Data"] = dic["Data"][dic["ZhBin"] == ZhBin]
                dic["Evnts"] = dic["Evnts"][dic["ZhBin"] == ZhBin]

                values = np.concatenate((values, dic[varBin]),  axis=0)
                data = np.concatenate((data,   dic["Data"]),  axis=0)
                events = np.concatenate((events, dic["Evnts"]), axis=0)

            hist = axs[ZhBin-1][1].hist(values[data == 0], bins=binning[var],
                                        color=colorList[j],
                                        weights=(
                                            events[data == 0]/np.sum(events))*100,
                                        label="Lost Data " + nPionList[j], zorder=2)

            # print("Liquid targets " + str(j+1) + " pions in " + ZhLabel[ZhBin] +
            # " percentaje of loss events: ", end = "")
            print(" & ", end="")
            print(round(np.sum(hist[0]), 3), end="")
            print("\\\\ \hline")

        axs[ZhBin-1][0].set_ylim(0., 1.25)
        axs[ZhBin-1][1].set_ylim(0., 1.25)

        axs[ZhBin-1][0].set_ylabel(r'Lost events(%)',
                                   loc="center", fontsize=15)

        # if ZhBin != 7:
        # axs[ZhBin-1][0].set_ylim(0., 0.125)
        # axs[ZhBin-1][1].set_ylim(0., 0.125)

        SetAxs(axs[ZhBin-1], ZhBin, var)

    SaveFigure(fig, outputDirectory, "EmptyNormDataSim_" + var + "_Zh")


def EmptyDataNormSimVar(var="Pt2"):

    varBin = var + "Bin"
    vars = ['Data', varBin, "Evnts"]

    fig, axs = plt.subplots(1, 2, sharey='row', sharex='col')
    width = 16*(2/3)  # 7.056870070568701
    height = 4
    fig.set_size_inches(width, height)
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.06, hspace=0.2)

    for j in range(1, nPion):  # Loops on the number of pions

        data = np.array([])
        values = np.array([])
        events = np.array([])

        for i in range(0, 3):  # Loops on the diffrent targets

            with ur.open(inputDirectory +
                         "EmptyBins.root:EmptyBins_" + tarList[i] + "_" + str(j+1)) as file:
                dic = file.arrays(vars, library="np")

            for t in range(len(dic[varBin])):
                for k in range(len(binning[var])):
                    if dic[varBin][t] == k:
                        dic[varBin][t] = binning[var][k] + 0.001

            values = np.concatenate((values, dic[varBin]),  axis=0)
            data = np.concatenate((data,   dic["Data"]),  axis=0)
            events = np.concatenate((events, dic["Evnts"]), axis=0)

        hist = axs[1].hist(values[data == 0], bins=binning[var],
                           color=colorList[j],
                           weights=(events[data == 0]/np.sum(events))*100,
                           label="Lost Data " + nPionList[j], zorder=2)

        print("Solids targets " + str(j+1) +
              " pions in percentaje of loss events: ", end="")
        print(round(np.sum(hist[0]), 3))

        data = np.array([])
        values = np.array([])
        events = np.array([])

        for i in range(0, 3):
            with ur.open(inputDirectory +
                         "EmptyBins.root:EmptyBins_D" + tarList[i] + "_" + str(j+1)) as file:
                dic = file.arrays(vars, library="np")

            for t in range(len(dic[varBin])):
                for k in range(len(binning[var])):
                    if dic[varBin][t] == k:
                        dic[varBin][t] = binning[var][k] + 0.001

            values = np.concatenate((values,  dic[varBin]), axis=0)
            data = np.concatenate((data,  dic["Data"]), axis=0)
            events = np.concatenate((events,  dic["Evnts"]), axis=0)

        hist = axs[0].hist(values[data == 0], bins=binning[var],
                           color=colorList[j],
                           weights=(events[data == 0]*100)/np.sum(events),
                           label="Lost Data " + nPionList[j], zorder=2)

        axs[0].set_ylim(0., 0.125)
        axs[1].set_ylim(0., 0.125)

        print("Liquid targets " + str(j+1) +
              " pions in percentaje of loss events: ", end="")
        print(round(np.sum(hist[0]), 3))

    SetAxs(axs, 7, var)

    SaveFigure(fig, outputDirectory, "EmptyNormDataSim_" + var)


EmptyBinsSimVarZh()
EmptyBinsNormSimVarZh()
EmptyDataSimVarZh()
EmptyDataNormSimVarZh()
# EmptyDataNormSimVar()
