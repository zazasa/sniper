#!/usr/bin/env python
# Salvatore Zaza
# Created 2013

from ROOT import *
from sCONST import *




if __name__ == "__main__":
    gROOT.ProcessLine(CHSTRUCT);
    dataF = "/home/salvo/Scrivania/Tesi/DATA/run_131111142833_1.root"
    chID = "CH0"

    tc = TCanvas("tc","sPlot")
    tc.Divide(1,2)
    pad = tc.FindObject("tc_1")
    cpad = tc.FindObject("tc_2")
    

    drawStr = chID+".value:"+chID+".seqTime>>h1"
    cdrawStr = chID+".cvalue:"+chID+".seqTime>>h2"
    cutStr = chID+".seqTime < 512"

    tf = TFile(dataF)
    tree = tf.Get("T5DATA") 

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
