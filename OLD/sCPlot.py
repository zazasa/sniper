#!/usr/bin/env python
# Salvatore Zaza
# Created 2013
from ROOT import *
import csv
import numpy as np




if __name__ == "__main__":
    dataFolder = "../../../DATA/"
    calibFolder = os.path.join(dataFolder,CALIBSUBFOLDER)
    oldDataFolder = os.path.join(dataFolder,CALIBOLDSUBFOLDER)
    calibParamFolder = os.path.join(dataFolder,CALIBFILESUBFOLDER)
    calibFileTag = CALIBFILETAG
    dp = DECROUND                #decimal point for around
    csvFields = CSVFIELDS 
    gROOT.ProcessLine(CHSTRUCT);

    cParamFile = "cParam_vped_1700.csv"
    rawFile = "calibRun_1311071504_vped_1700.root"

    colors = {
        "CH0":kRed,
        "CH1":kRed-7,
        "CH2":kMagenta+2,
        "CH3":kBlue+1,
        "CH4":kAzure+7,
        "CH5":kCyan,
        "CH6":kTeal-7,
        "CH7":kTeal+9,
        "CH8":kSpring-8,
        "CH9":kYellow+2,
        "CH10":kOrange-3,
        "CH11":kOrange,
        "CH12":kOrange+7,
        "CH13":kGray+2,
        "CH14":kBlack,
        "CH15":kPink+10, }

    paramF = cParamFolder+cParamFile
    rawF = rawFolder + rawFile
#buffer file
    with open(paramF,"r") as f:
        cfi =  csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)    #calibration file index
        cBuffer = [row for row in cfi]                      #calibration data buffer

#FIRST 
    chID = "CH0"
    blockID = "511"
    drawString = chID+".value>>h1"
    drawOpt = chID+".blockID == "+blockID
    tf = TFile(rawF)
    tree = tf.Get("T5DATA")

    #h1 = TH1F("h1",chID+" distribution of blockID :%d"%blockID)
    tree.Draw(drawString,drawOpt,"goff")
    h1 = gROOT.FindObject("h1")
    h1.SetTitle("Channel : "+chID+" distribution of blockID %s"%blockID)
    


    """
    cellNum = 1
    column = csvFields.index("mean #%d" %cellNum)    
    values = [row[column] for row in cBuffer if row[0] == chID ]
   
    h1 = TH1F("h1",chID+" distribution of cell num:%d"%cellNum,100,min(values),max(values))
    for x in values:
        h1.Fill(x)
    """

#SECOND
    #chID = "CH0"
    mg2 = TMultiGraph()
    mg2.SetTitle("One line per BlockID for %s" %chID)
    bl = np.linspace(0,511,511)
    for blockID in bl:
        blockID = int(blockID)
        f = csvFields.index("mean #1")
        l = csvFields.index("mean #32")
        values = [row[f:l+1] for row in cBuffer if row[0] == chID and row[1] == blockID and row[2] == 0]
        values = np.squeeze(np.array(values))
        
        x = np.linspace(1,32,32)
        g3 = TGraph(len(x),x,values)
        g3.SetMarkerStyle(7)
        mg2.Add(g3,"lp")
        
        
    


    """    
    meanPerCell = []
    x = np.linspace(1,32,32)
    for cellNum in x:
        cellNum = int(cellNum)
        column = csvFields.index("mean #%d" %cellNum)
        values = [row[column] for row in cBuffer if row[0] == chID ]
        meanPerCell.append(np.around(np.mean(values),3))

    meanPerCell = np.array(meanPerCell)
    g1 = TGraph(len(x), x,meanPerCell)
    g1.SetTitle(chID+" mean per cell")
    g1.SetMarkerStyle(7)
    """

#THIRD
    #chID = "CH0"
    mg1 = TMultiGraph()
    mg1.SetTitle("Mean over 32 cells per blockID per channel (one channel per color)")
    for chNum in range(16):
        chID = "CH"+str(chNum)

        x = np.linspace(0,511,511)
        meanPerBlock = []
        for blockID in x:
            blockID = int(blockID)
            f = csvFields.index("mean #1")
            l = csvFields.index("mean #32")
            values = [row[f:l+1] for row in cBuffer if row[0] == chID and row[1] == blockID and row[2] == 0][0]
            meanPerBlock.append(np.around(np.mean(values),3))
            
        


        meanPerBlock = np.array(meanPerBlock)
        g2 = TGraph(len(x), x,meanPerBlock)
        g2.SetTitle(chID)
        g2.SetMarkerStyle(7)
        g2.SetMarkerColor(colors[chID])
        g2.SetLineColor(colors[chID])

        mg1.Add(g2,"lp")

    
        
   

#DRAW
    tc = TCanvas()
    tc.Divide(1,3)
    tc.cd(1)
    gPad.SetGridx(True)
    gPad.SetGridy(True)
    h1.Draw()

    
    tc.cd(2)
    gPad.SetGridx(True)
    gPad.SetGridy(True)
    mg2.Draw("a")

    tc.cd(3)
    gPad.SetGridx(True)
    gPad.SetGridy(True)
    mg1.Draw("a")
    gPad.BuildLegend()



    
    cmd = raw_input("\nEnter Command: ")

    
