#!/usr/bin/env python
# Salvatore Zaza
# Created 2013

from ROOT import *
from sniperCOST import *




if __name__ == "__main__":
    gROOT.ProcessLine(CHSTRUCT);
    gROOT.ProcessLine(CCHSTRUCT);
    dp = 3                #decimal point for around
    cdataFolder = "../../DATA/calibratedRun/CALIBRATED/"

    #cdataFile = sys.argv[1]
    #chID = sys.argv[2]
    #cdataF = cdataFolder+cdataFile
    cdataF = "../../DATA/CALIBRATED/run_131019124954_1_c.root"
    chID = "CH0"

    tc = TCanvas("tc","sPlot")
    tc.Divide(1,2)
    pad = tc.FindObject("tc_1")
    cpad = tc.FindObject("tc_2")
    

    drawStr = chID+".value:"+chID+".blockID>>h1"
    cdrawStr = chID+".cvalue:"+chID+".blockID>>h2"

    tf = TFile(cdataF)
    tree = tf.Get("T5DATA") 

    tc.cd(1)
    tree.Draw(drawStr,"","p")
    pad.FindObject("h1").SetTitle("T5 RAW DATA")
    pad.FindObject("Graph").SetMarkerStyle(7)
    pad.SetGridx(True)
    pad.SetGridy(True)
    pad.Modified()
    


    tc.cd(2)
    tree.Draw(cdrawStr,"","p") 
    cpad.FindObject("h2").SetTitle("T5 CALIBRATED DATA")
    cpad.FindObject("Graph").SetMarkerStyle(7)
    cpad.SetGridx(True)
    cpad.SetGridy(True)
    cpad.Modified()

    tc.Update()
    tc.Modified()


    #cmd = raw_input("\nEnter Command: ")
