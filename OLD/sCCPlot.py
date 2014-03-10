#!/usr/bin/env python
# Salvatore Zaza
# Created 2013
from ROOT import *
import csv
import numpy as np

if __name__ == "__main__":
    cParamFile = "../../../DATA/calibrationData/CFILE/cParams_vped_1700.csv"
    rawFile = "../../../DATA/run_131108194328_42.root"

    samplePerBlock = 32
    csvFields = ["chID","blockID","entriesPerBlock","sablockID","dataFile"] + ["mean #%d" %d for d in range(1,samplePerBlock+1)] + ["std #%d" %d for d in range(1,samplePerBlock+1)] 
    fm = csvFields.index("mean #1")
    lm = csvFields.index("mean #32")+1

    chID = "CH1"

    drawStr = chID+".value:"+chID+".seqTime>>h1"
    cdrawStr = chID+".blockID:"+chID+".seqTime>>h2"
    cutStr = ""

    with open(cParamFile,"r") as f:
        cfi =  csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)    #calibration file index
        cBuffer = [row for row in cfi]                      #calibration data buffer

    
    tf = TFile(rawFile)
    tree = tf.Get("T5DATA")

    tc = TCanvas("tc","sPlot")
    tc.Divide(1,2)
    pad = tc.FindObject("tc_1")
    cpad = tc.FindObject("tc_2")


    

    cBuffer = [row for row in cBuffer if row[0] == chID]            #select only chid
    cBuffer = sorted(cBuffer, key = lambda entry: entry[1])
    even = cBuffer[::2]
    odd = cBuffer[1::2]
    cBuffer = even+odd                                              #order
    values = []

    for row in cBuffer :
        values+= row[fm:lm]

    

    x = np.linspace(0,len(values),len(values))
    values=np.array(values)


    g2 = TGraph(len(x), x,values)


    tc.cd(1)
    tree.Draw(drawStr,cutStr,"p")
    pad.FindObject("Graph").SetMarkerStyle(7)
    gPad.SetGridx(True)
    gPad.SetGridy(True)


    tc.cd(2)
    gPad.SetGridx(True)
    gPad.SetGridy(True)
    g2.Draw()

    tc.Modified()
    tc.Update()

