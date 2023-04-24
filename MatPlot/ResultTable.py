import ROOT
import numpy as np
from include import inputDirectory, outputDirectory, systematicDirectory


targets = ["C", "Fe", "Pb"]
binsLabel = ["0.0 - 0.1" ,"0.1 - 0.2" ,"0.2 - 0.3" ,"0.3 - 0.4" ,"0.4 - 0.5",
             "0.5 - 0.6" ,"0.6 - 0.8" ,"0.8 - 1.0"]

systematics = [["TOFLow", "TOFHigh"], ["VC_RD",  "VC_HH"], ["DZLow",  "DZHigh"], 
               ["Normal", "Cutoff"], ["50Bins", "70Bins"], ["NAccept0", "NAccept2"], 
               ["LimitLow", "LimitHigh"], ["CT", "CT"], ["RC", "RC"]]

firstBin = 1
lastBin = 8

decimals = 4

def GetBroadening(target, numberPion):

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")
    graphName = "PtBroad_Zh_" + target + "_" + str(numberPion)
    graph     = file.Get(graphName)
    nPoints = graph.GetN()

    return np.ndarray(nPoints, dtype = float, buffer = graph.GetY())


def GetStatError(target, numberPion):

    file = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")
    graphName = "PtBroad_Zh_" + target + "_" + str(numberPion)
    graph     = file.Get(graphName)
    nPoints = graph.GetN()

    return np.ndarray(nPoints, dtype = float, buffer = graph.GetEY())

def GetSysError(target, numberPion):

    fileNominal = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")
    graphName   = "PtBroad_Zh_" + target + "_" + str(numberPion)
    graphNom    = fileNominal.Get(graphName)
    nPoints = graphNom.GetN()
    nomValues  = np.ndarray(nPoints, dtype = float, buffer = graphNom.GetY())
    errorValues  = np.ndarray(nPoints, dtype = float, buffer = graphNom.GetEY())
    fileNominal.Close()
 
    sysErrorArray = np.repeat(0., 8)
    
    for systematic in systematics:

        fileSystematic = [ROOT.TFile.Open(systematicDirectory + systematic[0] + 
                                          "/Pt_broad_Zh.root", "READ"),
                           ROOT.TFile.Open(systematicDirectory + systematic[1] + 
                                           "/Pt_broad_Zh.root", "READ")]
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


def SystematicArray(target, numberPion, systematic):


    fileSystematic = [ROOT.TFile.Open(systematicDirectory + systematic[0] + "/Pt_broad_Zh.root", 
                                     "READ"),
                      ROOT.TFile.Open(systematicDirectory + systematic[1] + "/Pt_broad_Zh.root", 
                                      "READ")]
    fileNominal    = ROOT.TFile.Open(inputDirectory + "Pt_broad_Zh.root", "READ")

    graphNameNom = "PtBroad_Zh_" + target + "_" + str(numberPion)
    graphNom     = fileNominal.Get(graphNameNom)

    NSys = 2
    if systematic[0] == systematic[1]:
        NSys = 1 

    graphNameSys = "PtBroad_Zh_" + target + "_" + str(numberPion)
    
    SysValues = [np.repeat(0., 8), np.repeat(0., 8)]
    
    for s in range(NSys):

        graphSys     = fileSystematic[s].Get(graphNameSys)

        # Extrac the data from the TGraph
        nPoints= graphSys.GetN()
        ySys  = np.ndarray(nPoints, dtype = float, buffer = graphSys.GetY())
        y  = np.ndarray(nPoints, dtype = float, buffer = graphNom.GetY())
        ey = np.ndarray(nPoints, dtype = float, buffer = graphNom.GetEY())


        SysValues[s] = y-ySys
    
    return np.maximum(SysValues[0], SysValues[1])      

def SumSystematics(target, numberPion, systematics):
   
    totSys = np.repeat(0., 8)

    for systematic in systematics: 
        
        totSys += np.square(SystematicArray(target, numberPion, systematic))
        
    return np.sqrt(totSys/3) 


for target in targets:

    print("This table is for " + target + " target.") 
    print("")

   
    broadening = [GetBroadening(target, 0), GetBroadening(target, 1)]
    statError  = [GetStatError(target, 0) , GetStatError(target, 1)]
    # sysError   = [GetSysError(target, 0)  , GetSysError(target, 1)]
    sysError   = [SumSystematics(target, 0, systematics)  , SumSystematics(target, 1, systematics)]
    totError   = [np.sqrt(np.square(statError[0]) + np.square(sysError[0])),
                  np.sqrt(np.square(statError[1]) + np.square(sysError[1]))]    
    

    for i in range(firstBin, lastBin):

        print("     ", end = "") 
        print(binsLabel[i] + " & ", end = "") 
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












