#!/usr/bin/env python
# Salvatore Zaza
# Created 2013

from ROOT import *
from sniperCOST import *
import itertools as it
import csv,sys,os
import numpy as np


def getValuesFromFile((chID,blockID,sablockID)):
    indexes = [cBuffer.index(row) for row in cBuffer if row[0]== chID and row[1] == blockID and row[2] == sablockID]
    if not indexes:
        return False
    elif len(indexes) > 1 :
        sys.stderr.write("Error, multiple key entry in csv file with (chID,blockID) : (%s,%d)\n" %(chID,blockID))
        return False
    key = (chID,blockID,sablockID)
    valuesList = cBuffer[indexes[0]][-64:-32]
    stdList = cBuffer[indexes[0]][-32:]
    pvalue[key] = it.cycle(valuesList)
    pstd[key] = it.cycle(stdList)
    return True
    
    



if __name__ == "__main__":
    gROOT.ProcessLine(CHSTRUCT);
    dp = 3                #decimal point for around
    dataFolder = "../../DATA/"
    cdataFolder = "../../DATA/CALIBRATED/"
    rawDataFolder = "../../DATA/CALIBRATED/RAW/"

    cParamFolder = "../../DATA/calibrationData/PARAMS/"

    #cdataFile = "run_131016142807_1_c.root"
    #dataFile = "run_131016142807_1.root"
    cParamFile = "cParam_vped_1700.csv"
    #dataFile = sys.argv[1]
    #cParamFile = sys.argv[2]


    nfkList = [] #not found keys
    fList = os.listdir(dataFolder)
    fList.sort()   
    for dataFile in fList:
        fn,ext = os.path.splitext(dataFile)
        if not (ext == ".root"):
            continue


        fn,ext = os.path.splitext(dataFile)
        cdataFile = fn+"c.root"

        print cdataFile

        dataF = dataFolder+dataFile
        cdataF = cdataFolder+cdataFile
        paramF = cParamFolder+cParamFile
        rdataF = rawDataFolder+dataFile
        
        with open(paramF,"r") as f:
            cfi =  csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)    #calibration file index
            cBuffer = [row for row in cfi]                      #calibration data buffer


        pvalue = {}             #calib param eg. {("CH0",438): [iter list of values]
        pstd = {}               #calib param eg. {("CH0",438): [iter list of std]
        ch = chID_t()           #channel struct
        applyCalib = False

        dataTF = TFile(dataF)
        tree = dataTF.Get("T5DATA")
        cdataTF = TFile(cdataF,"recreate")
        ctree = TTree("T5DATA","Target 5 Data with calibration")
        
        bl = tree.GetListOfBranches()
        for branch in bl:

            chID = branch.GetName()
            branch.SetAddress(ch)
            n = branch.GetEntries()

            cbranch = ctree.Branch(chID,ch,CHBRANCH)      #create branch in new file
            print chID
            for i in range(n):
                branch.GetEntry(i)

                applyCalib = True
                key = (chID,ch.blockID,ch.sablockID)
                if key not in pvalue:
                    if not getValuesFromFile(key):
                        if key not in nfkList:
                            nfkList.append(key)
                        applyCalib = False

                if applyCalib:
                    corr = float(pvalue[key].next())
                    std = float(pstd[key].next())
                    ch.cvalue = np.around(ch.value - corr,dp)
                    ch.cstd = std
                cbranch.Fill()
                #print chID,ch.blockID,ch.seqTime,ch.sablockID,ch.value,corr,std,ch.value-corr,key

            

        ctree.SetEntries(-1)
        ctree.Write("",5)  #5 = kOverwrite option
        dataTF.Close() 
        cdataTF.Close() 
        os.rename(dataF,rdataF)
       
        if len(nfkList) > 0 :
            print "not found keys list: "
            for k in nfkList:
                print k





     



