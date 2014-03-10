#!/usr/bin/env python
# Salvatore Zaza
# Created 2013


import ROOT as r
import numpy as np
import os,sys,csv
from sniperCOST import *
from sniperROOT import *

def bufferizeFile():
    for peek in iter(lambda: fi.read(16), ''):
        length = int(peek.encode("hex")[0:2],16)*8 
        data = peek+fi.read(length-16)
        eventBuffer.append(data)

        """
        data = data.encode("hex")
        data = [data[i:i+4] for i in range(0,len(data),4)]
        print data,len(data),length
        """

def getData():
    if len(eventBuffer)> 0:
        data = eventBuffer.pop(0)           
    else:
        data = "EOD"        #no data
    return data 
    


if __name__ == "__main__":
    r.gROOT.ProcessLine(CHSTRUCT);

    dataFolder = "../../DATA/BIN/"
    destFolder = "../../DATA/"
    #dataFile = "run_131022101139_2.bin"

    fList = os.listdir(dataFolder)
    fList.sort()   
    for dataFile in fList:
        fn,ext = os.path.splitext(dataFile)
        if not (ext == ".bin"):
            continue

        fn,ext = os.path.splitext(dataFile)
        destFile = fn+".root"


        eventBuffer = []


        dataF = dataFolder+dataFile
        destF = destFolder+destFile

        sys.stdout.write("Bufferize\n")
        fi = open(dataF,"rb")
        #fi.read(88*1566000)
        bufferizeFile()

        fi.close()

        eNum = len(eventBuffer) 
        sr = SniperROOT("T5DATA","Target 5 Calibration Data")   #create ROOT interface object
        sr.setSource(getData)                                #connect data fetch with board interface
        sr.setMaxPacket(eNum)
        sr.setFolder(destFolder)                                #set folder for root files
        sr.setDelay(0)                                          #sleep time after any packet stored in ttree   
        sys.stdout.write("Start writing ROOT file\n")
        
        filename = destFile
        sr.open()                               #create ROOT enviroment and data files
        sr.start()  
                               #start store events in ROOT tree and wait for finish
        pNum = 0        
        while pNum < (eNum) :
            pNum = sr.getPacketNumber()
            sys.stdout.write("\r Num packet stored: %f%%  completed" %(100*(pNum/float(eNum))))
            time.sleep(0.0001)
        sr.stop()
        sys.stdout.write("Total packet stored: %d\n" %sr.getPacketNumber())
        sr.changeFile(destFolder+filename)
        sr.close()
