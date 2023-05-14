import ROOT
import numpy as np
from include import inputDirectory, outputDirectory, systematicDirectory


targets = ["C", "Fe", "Pb"]
targetsNames = {"C"  : "Carbon", "Fe" : "Iron", "Pb" : "Lead"}

binsLabel = { "Q2" : ["1.00 - 1.32" ,"1.32 - 1.74" ,"1.74 - 4.00"],
              "Nu" : ["2.20 - 3.36" ,"3.36 - 3.82" ,"3.82 - 4.26"],
              "Zh" : ["0.0 - 0.1" ,"0.1 - 0.2" ,"0.2 - 0.3" ,"0.3 - 0.4" ,"0.4 - 0.5",
             "0.5 - 0.6" ,"0.6 - 0.8" ,"0.8 - 1.0"],
            "FullIntegrated": "Target"
             }

nBins = {"Q2": 3, "Nu": 3, "Zh": 8, "FullIntegrated": 1}

systematics = [["TOFLow", "TOFHigh"], ["VC_RD",  "VC_HH"], ["DZLow",  "DZHigh"], 
               ["Normal", "Cutoff"], ["50Bins", "70Bins"], ["NAccept0", "NAccept2"], 
               ["LimitLow", "LimitHigh"], ["CT", "CT"], ["RC", "RC"]]

variable = "FullIntegrated"
firstBin = 0
lastBin = 1

decimals = 4

def GetBroadening(target, numberPion):

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_" + variable + ".root", "READ")
    graphName = "PtBroad_" + variable + "_" + target + "_" + str(numberPion)
    graph     = file.Get(graphName)
    nPoints = graph.GetN()

    return np.ndarray(nPoints, dtype = float, buffer = graph.GetY())


def GetStatError(target, numberPion):

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_" + variable + ".root", "READ")
    graphName = "PtBroad_" + variable + "_" + target + "_" + str(numberPion)
    graph     = file.Get(graphName)
    nPoints = graph.GetN()

    return np.ndarray(nPoints, dtype = float, buffer = graph.GetEY())

def GetSysError(target, numberPion, variable):

    fileNominal = ROOT.TFile.Open(inputDirectory + "Pt_broad_" + variable + ".root", "READ")
    graphName   = "PtBroad_" + variable + "_" + target + "_" + str(numberPion)
    graphNom    = fileNominal.Get(graphName)
    nPoints = graphNom.GetN()
    nomValues  = np.ndarray(nPoints, dtype = float, buffer = graphNom.GetY())
    errorValues  = np.ndarray(nPoints, dtype = float, buffer = graphNom.GetEY())
    fileNominal.Close()
 
    sysErrorArray = np.repeat(0., 8)
    
    for systematic in systematics:

        fileSystematic = [ROOT.TFile.Open(systematicDirectory + systematic[0] + 
                                          "/Pt_broad_" + variable + ".root", "READ"),
                           ROOT.TFile.Open(systematicDirectory + systematic[1] + 
                                           "/Pt_broad_" + variable + ".root", "READ")]
        graphSys     = [fileSystematic[0].Get(graphName), 
                        fileSystematic[1].Get(graphName)]
        SysValues = [np.ndarray(nPoints, dtype = float, buffer = graphSys[0].GetY()),
                     np.ndarray(nPoints, dtype = float, buffer = graphSys[1].GetY())]
        sysErrorArray += np.square(np.maximum(np.absolute(nomValues-SysValues[0]), 
                                              np.absolute(nomValues-SysValues[1])))/3

        # print("Target: " + target + " Number: " + str(numberPion) + " Systematic: ", end ="")
        # print(systematic)
        # print(sysErrorArray)
        fileSystematic[0].Close()
        fileSystematic[1].Close()
    
    return np.sqrt(sysErrorArray)


def SystematicArray(target, numberPion, systematic, variable):


    fileSystematic = [ROOT.TFile.Open(systematicDirectory + systematic[0] + "/Pt_broad_" + variable + ".root", 
                                     "READ"),
                      ROOT.TFile.Open(systematicDirectory + systematic[1] + "/Pt_broad_" + variable + ".root", 
                                      "READ")]
    fileNominal    = ROOT.TFile.Open(inputDirectory + "Pt_broad_" + variable + ".root", "READ")

    graphNameNom = "PtBroad_" + variable + "_" + target + "_" + str(numberPion)
    graphNom     = fileNominal.Get(graphNameNom)

    NSys = 2
    if systematic[0] == systematic[1]:
        NSys = 1 

    graphNameSys = "PtBroad_" + variable + "_" + target + "_" + str(numberPion)
    
    SysValues = [np.repeat(0., nBins[variable]), np.repeat(0., nBins[variable])]
    
    for s in range(NSys):

        graphSys     = fileSystematic[s].Get(graphNameSys)

        # Extrac the data from the TGraph
        nPoints= graphSys.GetN()
        ySys  = np.ndarray(nPoints, dtype = float, buffer = graphSys.GetY())
        y  = np.ndarray(nPoints, dtype = float, buffer = graphNom.GetY())
        ey = np.ndarray(nPoints, dtype = float, buffer = graphNom.GetEY())


        SysValues[s] = np.absolute(y-ySys)
    
    return np.maximum(SysValues[0], SysValues[1])      

def SumSystematics(target, numberPion, systematics, variable):
   
    totSys = np.repeat(0., nBins[variable])

    for systematic in systematics: 
        
        totSys += np.square(SystematicArray(target, numberPion, systematic, variable))
        
    return np.sqrt(totSys/3) 


if variable != "FullIntegrated":
    
    print("The following results are for different bins of " + variable)
    for target in targets:

        print("This table is for " + target + " target.") 
        print("")

        broadening = [GetBroadening(target, 0), GetBroadening(target, 1)]
        statError  = [GetStatError(target, 0) , GetStatError(target, 1)]
        sysError   = [SumSystematics(target, 0, systematics, variable)  , 
                      SumSystematics(target, 1, systematics, variable)]
        totError   = [np.sqrt(np.square(statError[0]) + np.square(sysError[0])),
                      np.sqrt(np.square(statError[1]) + np.square(sysError[1]))]    


        for i in range(firstBin, lastBin):

            print("     ", end = "") 
            print(binsLabel[variable][i] + " & ", end = "") 
            print(round(broadening[0][i], decimals), end = "")
            print(" & ", end = "") 
            print(round(totError[0][i], decimals) , end = "")
            print(" & ", end = "") 
            print(round(statError[0][i], decimals) , end = "")
            print(" & ", end = "") 
            print(round(sysError[0][i], decimals) , end = "")
            print(" & ", end = "") 
            print(round(broadening[1][i], decimals) , end = "")
            print(" & ", end = "") 
            print(round(totError[1][i], decimals) , end = "")
            print(" & ", end = "") 
            print(round(statError[1][i], decimals) , end = "")
            print(" & ", end = "") 
            print(round(sysError[1][i], decimals) , end = "")
            print("\\\\ \hline")


        print("")
        print("")

else:

    print("The following results have all the kinematic variables FullIntegrated")
    print("")
    for target in targets:

        broadening = [GetBroadening(target, 1), GetBroadening(target, 2)]
        statError  = [GetStatError(target, 1) , GetStatError(target, 2)]
        sysError   = [SumSystematics(target, 1, systematics, variable)  , 
                  SumSystematics(target, 2, systematics, variable)]
        totError   = [np.sqrt(np.square(statError[0]) + np.square(sysError[0])),
                  np.sqrt(np.square(statError[1]) + np.square(sysError[1]))]    


        print("     ", end = "") 
        print(targetsNames[target] + " & ", end = "") 
        print(round(broadening[0][0], decimals), end = "")
        print(" & ", end = "") 
        print(round(totError[0][0], decimals) , end = "")
        print(" & ", end = "") 
        print(round(statError[0][0], decimals) , end = "")
        print(" & ", end = "") 
        print(round(sysError[0][0], decimals) , end = "")
        print(" & ", end = "") 
        print(round(broadening[1][0], decimals) , end = "")
        print(" & ", end = "") 
        print(round(totError[1][0], decimals) , end = "")
        print(" & ", end = "") 
        print(round(statError[1][0], decimals) , end = "")
        print(" & ", end = "") 
        print(round(sysError[1][0], decimals) , end = "")
        print("\\\\ \hline")


    print("")
    print("")









