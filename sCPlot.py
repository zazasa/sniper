#!/usr/bin/env python
# Salvatore Zaza
# Created 2013
from ROOT import *
import csv,sys,os
import numpy as np
import itertools as it



if __name__ == "__main__":
    dataFolder = ""
    chID = "CH0"

    paramF = "../../../DATA/calibrationData/CFILE/cParams_vped_2000.csv"
    #rawFile = "calibRun_1311071504_vped_1700.root"

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

    colors2 = it.cycle([colors[key] for key in colors])

#buffer file
    with open(paramF,"r") as f:
        cfi =  csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)    #calibration file index
        cBuffer = [row for row in cfi]                      #calibration data buffer
    headers = cBuffer[0]
    cBuffer = cBuffer[1:]
    bIndex = headers.index("blockID")
    cIndex = headers.index("chID")
    f = headers.index("mean #1")
    l = headers.index("mean #32")
    f2 = headers.index("std #1")
    l2 = headers.index("std #32")

    tc = TCanvas()
    tc.Divide(1,3)

#FIRST

    mg = TMultiGraph()
    mg.SetTitle("Cell noise value. One line per BlockID for %s (16 blockIDs total)" %chID)
    bl = sorted([int(row[bIndex]) for row in cBuffer if row[cIndex] == chID])

    for blockID in bl:

        values = [row[f:l+1] for row in cBuffer if row[cIndex] == chID and row[bIndex] == blockID]
        values = np.squeeze(np.array(values))
             
        x = np.linspace(1,len(values),len(values))
        g = TGraph(len(x),x,values)
        g.SetMarkerStyle(20)
#        g.SetMarkerSize(0.7)
        g.SetLineWidth(2)
        g.SetTitle("blockID "+str(blockID))
        col = colors2.next()
        g.SetLineColor(col)
        g.SetMarkerColor(col)
        mg.Add(g,"lp")


    pad = tc.cd(1)
    pad.SetLeftMargin(0.05)
    pad.SetRightMargin(0.22)
    pad.SetTopMargin(0.15)
    pad.SetBottomMargin(0.09)
    mg.Draw("ALP")
    leg = gPad.BuildLegend(0.8,1.0,0.99,0.004,"")
    leg.SetFillColor(kWhite)
    leg.SetTextSize(0.08)
    leg.SetTextFont(82)
    leg.SetTextAlign(11)
    pl = leg.GetListOfPrimitives()
    n = leg.GetNRows()
    for i in range(n):
        pl[i].SetOption("lp")
    pad.Modified()
    pad.Update()
    mg.GetXaxis().SetLabelSize(0.1)
    mg.GetXaxis().SetRangeUser(1,32)
    mg.GetYaxis().SetLabelSize(0.1)
    t = pad.GetPrimitive("title")
    t.SetTextSize(0.13)
    t.SetX1NDC(0.12)
    t.SetY1NDC(0.89)
    pad.Modified()
    pad.Update()



#SECOND
    #chID = "CH0"
    mg2 = TMultiGraph()
    mg2.SetTitle("Cell noise STD. One line per BlockID for %s (16 blockIDs total)" %chID)
    bl = sorted([int(row[bIndex]) for row in cBuffer if row[cIndex] == chID])

    for blockID in bl:

        values = [row[f2:l2+1] for row in cBuffer if row[cIndex] == chID and row[bIndex] == blockID]
        values = np.squeeze(np.array(values))
             
        x = np.linspace(1,len(values),len(values))
        g2 = TGraph(len(x),x,values)
        g2.SetMarkerStyle(20)
#        g2.SetMarkerSize(0.7)
        g2.SetLineWidth(2)
        g2.SetTitle("blockID "+str(blockID))
        col = colors2.next()
        g2.SetLineColor(col)
        g2.SetMarkerColor(col)
        mg2.Add(g2,"lp")


    pad = tc.cd(2)
    pad.SetLeftMargin(0.05)
    pad.SetRightMargin(0.22)
    pad.SetTopMargin(0.15)
    pad.SetBottomMargin(0.09)
    mg2.Draw("ALP")
    leg = gPad.BuildLegend(0.8,1.0,0.99,0.004,"")
    leg.SetFillColor(kWhite)
    leg.SetTextSize(0.08)
    leg.SetTextFont(82)
    leg.SetTextAlign(11)
    pl = leg.GetListOfPrimitives()
    n = leg.GetNRows()
    for i in range(n):
        pl[i].SetOption("lp")
    pad.Modified()
    pad.Update()
    mg2.GetXaxis().SetLabelSize(0.1)
    mg2.GetXaxis().SetRangeUser(1,32)
    mg2.GetYaxis().SetLabelSize(0.1)
    t = pad.GetPrimitive("title")
    t.SetTextSize(0.13)
    t.SetX1NDC(0.12)
    t.SetY1NDC(0.89)
    pad.Modified()
    pad.Update()
    
        


#THIRD
    mg3 = TMultiGraph()
#    mg3.SetTitle("Mean over 32 cells per blockID per channel (one channel per color, 16 blockIDs per channel)")
    mg3.SetTitle("Mean over 32 cells per blockID per channel (16 blockIDs per channel)")
    for chNum in range(16):
        chID = "CH"+str(chNum)
        meanPerBlock = []
        for blockID in bl:
            values = [row[f:l+1] for row in cBuffer if row[0] == chID and row[1] == blockID]
            values = np.squeeze(np.array(values))
            meanPerBlock.append(np.around(np.mean(values),3))

            
        

        x = np.linspace(1,len(bl),len(bl))
        meanPerBlock = np.array(meanPerBlock)
        g3 = TGraph(len(x), x,meanPerBlock)
        g3.SetTitle(chID)
        g3.SetMarkerStyle(20)
#        g3.SetMarkerSize(0.7)
        g3.SetLineWidth(2)
        g3.SetMarkerColor(colors[chID])
        g3.SetLineColor(colors[chID])
        mg3.Add(g3,"lp")


    pad = tc.cd(3)
    pad.SetLeftMargin(0.05)
    pad.SetRightMargin(0.22)
    pad.SetTopMargin(0.15)
    pad.SetBottomMargin(0.09)
    mg3.Draw("ALP")

    leg = gPad.BuildLegend(0.8,1.0,0.99,0.004,"")
    leg.SetFillColor(kWhite)
    leg.SetTextSize(0.08)
    leg.SetTextFont(82)
    leg.SetTextAlign(11)
    pl = leg.GetListOfPrimitives()
    n = leg.GetNRows()
    for i in range(n):
        pl[i].SetOption("lp")
    pad.Modified()
    pad.Update()
    mg3.GetXaxis().SetLabelSize(0.1)
    mg3.GetXaxis().SetRangeUser(1,16)
    mg3.GetYaxis().SetLabelSize(0.1)
    t = pad.GetPrimitive("title")
    t.SetTextSize(0.13)
    t.SetX1NDC(0.12)
    t.SetY1NDC(0.89)
    pad.Modified()
    pad.Update()

    tc.Update()

    
