#!/usr/bin/env python
# Salvatore Zaza
# Created 2013
# Based on; Justin Vandenbroucke calibrateTF.py, Created Apr 30 2013
# Calibrate transfer function, as follows:
# Loop over Vped settings.
# For each take a run.
# NOTE: configure ev board before starting this script


from sniperInterface import *
from sniperROOT import *
import time
from datetime import datetime

def getTimeTag():
        return datetime.now().strftime("%y%m%d%H%M")





if __name__ == "__main__":
    localIP = ("0.0.0.0",8106)
    boardIP = ("192.168.0.173",8105)  
    fileTag = "calibRun_"
    dataFolder = "../../DATA/calibrationData/RAWDATA/"

    eventsPerRun = 5000
    eventTimeout = 5 #secs
    numChannels = 16
    sleepTime = 5       #see leonid mail
    minVped = 100
    maxVped = 2600
    stepVped = 100
    trigger = "ex"



    si = SniperInterface()                  #create interface object
    si.open(localIP,boardIP)                #create socket
    si.setTimeout(2)                        #set response timeout
    si.setAutoStop(True,eventsPerRun*numChannels)


    sr = SniperROOT("T5DATA","Target 5 Calibration Data")   #create ROOT interface object
    sr.setSource(si.getData)                                #connect data fetch with board interface
    sr.setMaxPacket(numChannels*eventsPerRun)
    sr.setFolder(dataFolder)                                #set folder for root files
    sr.setDelay(0)                                          #sleep time after any packet stored in ttree                                                  






    packetNumber = 0
    packetPerEvent = numChannels
    vPedList = range(minVped,maxVped,stepVped)

    vPedList = [1700]
    for vPed in vPedList:
        

        sys.stdout.write("\n###### Set Vped to %d counts and enable external trigger ######\n" %vPed)
        si.setVpedValue(vPed)
        sys.stdout.write("Waiting %d sec for Vped to settle.\n" %sleepTime)
        

        if trigger == "sw":
            si.setAutoStop(False,eventsPerRun*numChannels)
            si.enableTrigger("sw")
            time.sleep(sleepTime)
            sys.stdout.write("Start buffering of %d events for vped value %d\n" %(eventsPerRun,vPed))
            si.startBuffering()
            for i in range(eventsPerRun):
                si.sendSoftwareTrigger()
                time.sleep(0.0001)
                sys.stdout.write("\r trigger num: %d . Event Buffer: %d" %(i+1,si.getEventNumber()))
            si.stopBuffering()
        elif trigger == "ex":
            si.setAutoStop(True,eventsPerRun*numChannels)
            si.enableTrigger("ex")
            time.sleep(sleepTime)
            sys.stdout.write("Start buffering of %d events for vped value %d\n" %(eventsPerRun,vPed))
            si.startBuffering()
            while si.getEventNumber() < (packetPerEvent*eventsPerRun):
                time.sleep(0.1)
            si.enableTrigger("sw")
        else:
            sys.stdout.write("Bad trigger choice\n")
            continue

        sys.stdout.write("\n")
        eNum = si.getEventNumber()
        sys.stdout.write("Total event in buffer: %d\n" %eNum)

      

        sys.stdout.write("Start writing ROOT file\n")
        filename = fileTag+getTimeTag()+"_vped_"+str(vPed)+".root"
        sr.open()                               #create ROOT enviroment and data files
        sr.start()                          #start store events in ROOT tree and wait for finish
        pNum = 0        
        while pNum < (eNum) :  #upgrade to while enum > 0 and enum = si.GetEventNumber()
            pNum = sr.getPacketNumber()
            sys.stdout.write("\r Num packet stored: %f%%  completed" %(100*(pNum/float(eNum))))
            time.sleep(0.01)
        sr.stop()
        sys.stdout.write("Total packet stored: %d\n" %sr.getPacketNumber())
        sr.changeFile(dataFolder+filename)
        sr.close()
        sys.stdout.write("###### Finished %d of %d vPed values. ######\n"%(vPedList.index(vPed)+1,len(vPedList)))



    si.close()


