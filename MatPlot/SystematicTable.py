import ROOT
import numpy as np
from include import inputDirectory, outputDirectory, systematicDirectory

nPion = 2

dicSysName = {    "DZLow"      : "$\Delta Z$ Cut",
                  "DZHigh"     : "$\Delta Z$ Cut",
                  "50Bins"     : "Number of bins",
                  "70Bins"     : "Number of bins",
                  "VC_RD"      : "Vertex identification",
                  "VC_HH"      : "Vertex identification",
                  "Normal"     : "BG Subtraction",
                  "Cutoff"     : "BG Subtraction", 
                  "TOFHigh"    : "Pion Identification",
                  "TOFLow"     : "Pion Identification", 
                  "LimitHigh"  : "Limit Acc",
                  "LimitLow"   : "Limit Acc", 
                  "NAccept0"   : "$N^i_{a=t}$",
                  "NAccept2"   : "N_Accept",
                  "NAcceptRec" : "N_Accept",
                  "CT"         : "Closure Test",
                  "RC"         : "Rad. Corrections",
                 }


targets = ["C", "Fe", "Pb"]

systematics = [["TOFLow", "TOFHigh"], ["VC_RD",  "VC_HH"], ["DZLow",  "DZHigh"], 
               ["Normal", "Cutoff"], ["50Bins", "70Bins"], ["NAccept0", "NAccept2"], 
               ["LimitLow", "LimitHigh"], ["CT", "CT"], ["RC", "RCInter"]]

firstBin = 2
lastBin = 7


def FindMax(values, firstBin, lastBin):

    max = -1000
    for i in range(firstBin, lastBin):
        
        if values[i] > max:
            max = values[i]

    return round(max, 2)  


def FindMin(values, firstBin, lastBin):

    min = 1000
    for i in range(firstBin, lastBin):
        
        if values[i] < min:
            min = values[i]

    return round(min, 2)
 

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
        nPointsSys = graphSys.GetN()
        xSys  = np.ndarray(nPointsSys, dtype = float, buffer = graphSys.GetX())
        ySys  = np.ndarray(nPointsSys, dtype = float, buffer = graphSys.GetY())
        nPointsNom = graphNom.GetN()
        y  = np.ndarray(nPointsNom, dtype = float, buffer = graphNom.GetY())
        ey = np.ndarray(nPointsNom, dtype = float, buffer = graphNom.GetEY())

        ySys[0] = 1
        y[0] = 1

        SysValues[s] = np.absolute((y-ySys)/y)*100
    
    return np.maximum(SysValues[0], SysValues[1])      


def TotalSytematic(target, systematics, firstBin, lastBin):

    totalSys = np.array([0, 0, 0, 0])

    for systematic in systematics:

        totalSys[0] += np.square(FindMin(SystematicArray(target, 0, systematic), firstBin, 
                                         lastBin))
        totalSys[1] += np.square(FindMax(SystematicArray(target, 0, systematic), firstBin, 
                                         lastBin))
        totalSys[2] += np.square(FindMin(SystematicArray(target, 1, systematic), firstBin, 
                                         lastBin))
        totalSys[3] += np.square(FindMax(SystematicArray(target, 1, systematic), firstBin, 
                                         lastBin))

    return np.sqrt(totalSys/3)


def PrintTableRow(target, systematic, firstBin, lastBin):

    print("     ", end = "") 
    print(dicSysName[systematic[0]] + " & ", end = "") 
    print(FindMin(SystematicArray(target, 0, systematic), firstBin, lastBin), end = "")
    print("\% & ", end = "") 
    print(FindMax(SystematicArray(target, 0, systematic), firstBin, lastBin), end = "")
    print("\%  & ", end = "") 
    print(FindMin(SystematicArray(target, 1, systematic), firstBin, lastBin), end = "")
    print("\%  & ", end = "") 
    print(FindMax(SystematicArray(target, 1, systematic), firstBin, lastBin), end = "")
    print("\% \\\\ \hline")



# End Function definition Section

for target in targets:

    print("This table is for " + target + " target.") 
    print("")

    
    for systematic in systematics:

        PrintTableRow(target, systematic, firstBin, lastBin)
    
    total = TotalSytematic(target, systematics, firstBin, lastBin)
    print("     Total & ", end = "")
    print(round(total[0], 2), end = "")
    print(" \% & ", end ="")
    print(round(total[1], 2), end = "")
    print(" \% & ", end ="")
    print(round(total[2], 2), end = "")
    print(" \% & ", end ="")
    print(round(total[3], 2), end = "")
    print("\% \\\\ \hline")

    print("")
    print("")











