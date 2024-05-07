import numpy as np

# inputDirectory  = "~/proyecto/TwoPionAnalysis/Data/Bins/60/NomError/"
# outputDirectory = "/home/matias/proyecto/TwoPionAnalysis/Plots/Bins/60/"

inputDirectory = "~/proyecto/TwoPionAnalysis/Data/AnalysisNote/"
outputDirectory = "/home/matias/proyecto/TwoPionAnalysis/Plots/AnalysisNote/"

binning = {"Q2": [1., 1.30, 1.74, 4.00],
           "Nu": [2.2, 3.36, 3.82, 4.26],
           "Zh": [0., .1, .2, .3, .4, .5, .6, .8, 1.],
           "Pt2": np.linspace(0, 3, 60),
           "Phi": np.linspace(-180, 180, 6)
           }


def SaveFigure(fig, outputDirectory, name):

    fig.savefig(outputDirectory + name, bbox_inches='tight')
    print(outputDirectory + name + " Has been created")
