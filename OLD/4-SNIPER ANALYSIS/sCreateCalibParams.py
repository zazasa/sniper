#!/usr/bin/env python
# Salvatore Zaza
# Created 2013


import ROOT as r
import numpy as np
import os,sys,csv
from sniperCOST import *

def wannaChange():
    return True


def scanRawFile():
    tf = r.TFile(dataFolder+dataFile)
    tree = tf.Get("T5DATA")
    data = []
    ListOfBranches = tree.GetListOfBranches()
    for branch in ListOfBranches:
        chID = branch.GetName()
        print chID

        ch = r.chID_t()
        pyData = {}
        calibData = []


        branch.SetAddress(ch)
        n = branch.GetEntries()

        for i in range(n):
            branch.GetEntry(i)
            pyData.setdefault((int(ch.blockID),int(ch.sablockID)),list()).append(int(ch.value))
            #print ch.blockID,ch.sablockID
            #print ch.blockID,ch.numBlocksDigitized,ch.numBlocks,ch.currentSampleOffset

        for (blockID,sablockID) in pyData:
            #print blockID,sablockID
            values = np.array(pyData[(blockID,sablockID)])
            entriesPerBlock = len(values)


            if not entriesPerBlock%samplePerBlock == 0:
                sys.stderr.write("Error entries per block number\n")
                return False
            
            M = np.matrix(np.array_split(values,(values.shape[0])/samplePerBlock)).transpose()
            meanPerCell = []
            stdPerCell = []
           
            for cell in M:
                meanPerCell.append(np.around(cell.mean(),dp))
                stdPerCell.append(np.around(cell.std(),dp))

            calibData = [chID,blockID,sablockID,entriesPerBlock,dataFile] + meanPerCell + stdPerCell
            indexes = [cBuffer.index(row) for row in cBuffer if row[0]== chID and row[1] == blockID and row[2] == sablockID]
            if not indexes:
                cBuffer.append(calibData)
            elif len(indexes) > 1 :
                sys.stderr.write("Error, multiple key entry in csv file with (chID,blockID) : (%s,%d)\n" %(chID,blockID))
                return False
            elif wannaChange() :
                cBuffer[indexes[0]] = calibData
    tf.Close()
    tree = ""


if __name__ == "__main__":
    dataFolder = "../../DATA/calibrationData/RAWDATA/"
    #dataFile = "calibRun_1310151923_vped_1700.root"
    calibParamFolder = "../../DATA/calibrationData/PARAMS"
    calibFileTag = "cParam"
    #calibParamFile = "calibrationParameters_vped_1700.csv"
    samplePerBlock = 32
    dp = 3                #decimal point for around
    saBlockNum = 2          #sampling array block number
    csvFields = ["chID","blockID","sablockID","entriesPerBlock","dataFile"] + ["mean #%d" %d for d in range(1,samplePerBlock+1)] + ["std #%d" %d for d in range(1,samplePerBlock+1)] 
    
    r.gROOT.ProcessLine(CHSTRUCT);
    


    

    fList = os.listdir(dataFolder)
    fList.sort()   
    for dataFile in fList:
        fn,ext = os.path.splitext(dataFile)
        if not (ext == ".root"):
            continue
        info = fn.split("_")
        calibParamFile = calibFileTag+"_vped_"+info[3]+".csv"
        #print calibParamFile
        
        sys.stdout.write("Processing file : %s\n" %dataFile)

        calibData = []
        cBuffer = []
        cFilename = os.path.join(calibParamFolder,calibParamFile) #calibration file name
        if os.path.isfile(cFilename):
            with open(cFilename,"r") as f:
                cfi =  csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)    #calibration file index
                cBuffer = [row for row in cfi]
        else:
            cBuffer.append(csvFields)
        
        scanRawFile()

        with open(cFilename,"wb") as f:
            cfi = csv.writer(f,quoting=csv.QUOTE_NONNUMERIC)
            for row in cBuffer:
                cfi.writerow(row)   

            

    
        
        
