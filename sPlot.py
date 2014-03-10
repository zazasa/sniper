#!/usr/bin/env python
# Salvatore Zaza
# Created 2013

from ROOT import *
from sCONST import *
import numpy as np



if __name__ == "__main__":
    gROOT.ProcessLine(CHSTRUCT);
    dataF = "/home/salvo/Scrivania/Tesi/DATA/RUN2/run2_131111224049_1.root"
    chID = "CH0"

    #tc = TCanvas("tc","sPlot")
    #tc.Divide(1,2)
    #pad = tc.FindObject("tc_1")
    #cpad = tc.FindObject("tc_2")
    

    drawStr = chID+".value:"+chID+".seqTime>>h1"
    cdrawStr = chID+".cvalue:"+chID+".seqTime>>h2"
    cutStr = chID+".seqTime < 512"

    tf = TFile(dataF)
    tree = tf.Get("T5DATA") 

    xField = "seqTime"
    yField = "cvalue"

    numBlock = 5
    winWidth = numBlock * samplePerBlock    #seqTime window width
    winIndex = 1   #actual window displayed
    winMax = 1
    winNum = 1  #number of window to plot
    nEntries = tree.GetEntries()
    winMax = nEntries / winWidth
    winNum = winMax
    print winMax,nEntries,winWidth

    sqFrom = (winIndex-1) * winWidth
    sqTo = sqFrom + (winWidth*winNum) + 1
    cutString = chID+".seqTime > "+str(sqFrom)+ " && "+chID+".seqTime < "+str(sqTo)
    print cutString,winWidth,winMax,winIndex
    if tree:
        xField = chID+"."+xField
        yField = chID+"."+yField
        tree.Draw(yField+":"+xField,cutString,"goff")
        #self.x = self.tree.GetVal(0)
        #self.x = np.linspace(1,self.winWidth,512)
        x = np.array(range(1,winWidth+1)*winNum)*1.
        y = tree.GetVal(1)
        n = tree.GetSelectedRows()
        #print nn,x[nn],y[nn]
        mTo = 55
        mFrom = 0
        indexes = sorted(sum([np.where(x==value)[0].tolist() for value in range(mFrom,mTo+1)],[]))
        groupby = mTo-mFrom+1
        indexes = [indexes[i:i+groupby] for i in range(0,len(indexes)+1,groupby)]
        while [] in indexes:
            indexes.remove([])


        maxValues = []
        for row in indexes:
            values = [y[i] for i in row]

            maxValues.append(sum(values)) 

        minH = min(maxValues)
        maxH = max(maxValues)

        h1 = TH1F("h1","PROVA",100,minH,maxH)
        for y in maxValues:
            h1.Fill(y)

        h1.Draw()

    """
    tc.cd(1)
    tree.Draw(drawStr,cutStr,"p")
    pad.FindObject("h1").SetTitle("T5 RAW DATA")
    pad.FindObject("Graph").SetMarkerStyle(7)
    pad.SetGridx(True)
    pad.SetGridy(True)
    pad.Modified()
    


    tc.cd(2)
    tree.Draw(cdrawStr,cutStr,"p") 
    cpad.FindObject("h2").SetTitle("T5 CALIBRATED DATA")
    cpad.FindObject("Graph").SetMarkerStyle(7)
    cpad.SetGridx(True)
    cpad.SetGridy(True)
    cpad.Modified()

    tc.Update()
    tc.Modified()
    """

    #cmd = raw_input("\nEnter Command: ")
