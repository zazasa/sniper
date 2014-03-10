#!/usr/bin/env python
# Salvatore Zaza
# Created 2013
# Create a vped reference scale:
# read 1 event for each vped value
# store these results in the same root file
# plotting value:seqtime will show the vped scale
# NOTE: configure ev board before starting this script


from sInterface import *
from sROOT import *
import time
from datetime import datetime

def getTimeTag():
        return datetime.now().strftime("%y%m%d%H%M")





if __name__ == "__main__":
    localIP = ("0.0.0.0",8106)
    boardIP = ("192.168.0.173",8105)  
    fileTag = "vpedScale_"
    dataFolder = "calibrationData/"

    eventsPerRun = 1
    eventTimeout = 5 #secs
    numChannels = 16
    sleepTime = 5
    minVped = 100
    maxVped = 2600
    stepVped = 100



    si = SniperInterface()                  #create interface object
    si.open(localIP,boardIP)                #create socket
    si.setTimeout(2)                        #set response timeout
    si.startBuffering()                     #start capture packet


    sr = SniperROOT("T5DATA","Target 5 vPed Scale Data")   #create ROOT interface object
    sr.setSource(si.getData)                                #connect data fetch with board interface
    sr.setMaxPacket(numChannels*eventsPerRun)
    sr.setFolder(dataFolder)                                #set folder for root files
    sr.setDelay(0)                                          #sleep time after any packet stored in ttree                                                  






    packetNumber = 0
    packetPerEvent = numChannels
    vPedList = range(minVped,maxVped,stepVped)

    for vPed in vPedList:
        
        si.setVpedValue(vPed)
        sys.stdout.write("Finished setting Vped to %d counts.\n" %vPed)
	    # Wait for Vped to settle
        sys.stdout.write("Waiting %d sec for Vped to settle.\n" %sleepTime)
        time.sleep(sleepTime)



                              #create ROOT enviroment and data files

        sys.stdout.write("Start sampling of %d events for vped value %d\n" %(eventsPerRun,vPed))
        for evNum in range(eventsPerRun):       #send sw trigger and wait for event buffering
            si.sendSoftwareTrigger()
            while si.getEventNumber() < (packetPerEvent):
                time.sleep(0.1)
        
        

    filename = fileTag+getTimeTag()+".root"

    sr.open() 
    sr.start()                          #start store events in ROOT tree and wait for finish
    while sr.getPacketNumber() < (packetPerEvent*eventsPerRun*len(vPedList)) :
        time.sleep(0.1)
    sr.stop()
    sys.stdout.write("Finished %d events for vPed value.\n"%eventsPerRun)

    sr.changeFile(dataFolder+filename)
    sr.close()

    si.close()


