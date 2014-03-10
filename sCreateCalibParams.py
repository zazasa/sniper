#!/usr/bin/env python
# Salvatore Zaza
# Created 2013


from ROOT import *
import numpy as np
import os,sys,csv
from sCONST import *

def wannaChange():
    return True


def scanRawFile():
    tf = TFile(calibFolder+dataFile)
    tree = tf.Get("T5DATA")
    data = []
    ListOfBranches = tree.GetListOfBranches()
    for branch in ListOfBranches:
        chID = branch.GetName()
        print chID

        ch = chID_t()
        pyData = {}
        calibData = []


        branch.SetAddress(ch)
        n = branch.GetEntries()

        for i in range(n):
            branch.GetEntry(i)
            pyData.setdefault(int(ch.blockID),list()).append(int(ch.value))
            #print ch.blockID
            #print ch.blockID,ch.numBlocksDigitized,ch.numBlocks,ch.currentSampleOffset

        for blockID in pyData:
            #print blockID
            values = np.array(pyData[blockID])
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

            calibData = [chID,blockID,entriesPerBlock,dataFile] + meanPerCell + stdPerCell
            indexes = [cBuffer.index(row) for row in cBuffer if row[0]== chID and row[1] == blockID]
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
    dataFolder = "../../../DATA/"

    calibFolder = os.path.join(dataFolder,CALIBSUBFOLDER)
    oldDataFolder = os.path.join(dataFolder,CALIBOLDSUBFOLDER)
    calibParamFolder = os.path.join(dataFolder,CALIBFILESUBFOLDER)
    calibFileTag = CALIBFILETAG
    dp = DECROUND                #decimal point for around
    csvFields = CSVFIELDS 
    gROOT.ProcessLine(CHSTRUCT);
    


    

    fList = os.listdir(calibFolder)
    fList.sort()   
    for dataFile in fList:
        fn,ext = os.path.splitext(dataFile)
        if (ext == ".root"):
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

        if (ext in [".root",".bin"]):
            print ("move raw file in %s" %os.path.join(oldDataFolder,dataFile))
            os.rename(os.path.join(calibFolder,dataFile),os.path.join(oldDataFolder,dataFile)) #move file in old folder

        
            

    
        
        
