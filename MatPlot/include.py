
dataDirectory = "/home/matias/proyecto/Pt2Broadening_multi-pion/Data/"

# inputDirectory = "/home/matias/proyecto/TwoPionAnalysis/Data/Bins/40/"
# outputDirectory = "/home/matias/proyecto/TwoPionAnalysis/Plots/Bins/40/"
# systematicDirectory = "~/proyecto/TwoPionAnalysis/Data/60Systematic/"

# inputDirectory = "~/proyecto/TwoPionAnalysis/Data/AccInter/"
# outputDirectory = "/home/matias/proyecto/TwoPionAnalysis/Plots/AccInter/"
inputDirectory = "~/proyecto/TwoPionAnalysis/Data/AnalysisNote/"
outputDirectory = "/home/matias/proyecto/TwoPionAnalysis/Plots/AnalysisNote/"
systematicDirectory = "~/proyecto/TwoPionAnalysis/Data/AnalysisNote/Systematic/"

binning = {"Q2": [1., 1.30, 1.74, 4.00],
           "Nu": [2.2, 3.36, 3.82, 4.26],
           "Zh": [0., .1, .2, .3, .4, .5, .6, .8, 1.],
           "Pt2": np.linspace(0, 3, 60),
           "Phi": np.linspace(-180, 180, 6)
           }


def SaveFigure(fig, outputDirectory, name):

    # Create the directory if doesn't exist
    os.makedirs(outputDirectory, exist_ok=True)
    fig.savefig(outputDirectory + name + ".pdf", bbox_inches='tight')
    fig.savefig(outputDirectory + name + ".png", bbox_inches='tight', dpi=300)
    print(outputDirectory + name + " Has been created")


def AddCLasPleliminary(ax):
    ax.text(0.5, 0.5, 'CLAS Preliminary',
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes,
            color="lightgrey",
            fontsize="xx-large",
            fontweight="bold",
            alpha=0.7,
            zorder=1
            )
