#!/usr/bin/env python
# Salvatore Zaza
# Created 2013
# Based on; Justin Vandenbroucke calibrateTF.py, Created Apr 30 2013
# Calibrate transfer function, as follows:
# Loop over Vped settings.
# For each take a run.
# NOTE: configure ev board before starting this script
# NOTE: read 16 block per event


from sInterface import *
from sROOT import *
from sCONST import *
import time
from datetime import datetime

def getTimeTag():
        return datetime.now().strftime("%y%m%d%H%M")





if __name__ == "__main__":
    localIP = ("0.0.0.0",8106)
    boardIP = ("192.168.0.173",8105)  
    fileTag = "vPedScale"+"_"
    dataFolder = "../../../DATA/"

    calibFolder = os.path.join(dataFolder,CALIBSUBFOLDER)
    oldDataFolder = os.path.join(dataFolder,CALIBOLDSUBFOLDER)
    calibParamFolder = os.path.join(dataFolder,CALIBFILESUBFOLDER)
    calibFileTag = CALIBFILETAG
    dp = DECROUND                #decimal point for around
    csvFields = CSVFIELDS 
    gROOT.ProcessLine(CHSTRUCT); 

  
    firstColumn = 0
    lastColumn = 0
    eventsPerRun = 100
    numChannels = 16
    sleepTime = 5       
    minVped = 100
    maxVped = 2600
    stepVped = 100
    trigger = "sw"



    si = SniperInterface()                  #create interface object
    si.connect(localIP,boardIP)                #create socket
    #si.setTimeout(2)                        #set response timeout, hardcoded 2 s as default
    si.setStopEventNum(eventsPerRun*numChannels)
    si.start()


    sr = SniperROOT("T5DATA","Target 5 Calibration Data")   #create ROOT interface object
    sr.setSource(si.popEvent)                                #connect data fetch with board interface
    sr.setMaxPacket(numChannels*eventsPerRun)
    sr.setFolder(dataFolder)                                #set folder for root files
    sr.setDelay(0)                                          #sleep time after any packet stored in ttree                                                  


    packetNumber = 0
    packetPerEvent = numChannels
    vPedList = range(minVped,maxVped,stepVped)
    ts = "\n"+time.ctime()+"\n"
    sys.stdout.write(ts)
    for vPed in vPedList:
        

        sys.stdout.write("\n###### Set Vped to %d counts and enable external trigger ######\n" %vPed)
        si.setVpedValue(vPed)

        filename = fileTag+getTimeTag()+"_vped_"+str(vPed)+".root"
        sr.open()                               #create ROOT enviroment and data files

        row = 0
        column = 0
        for column in range(firstColumn,lastColumn+2,2):

            
            value = 0x200 + (2**3*column)
            si.writeRegister(0x11,value)  
            #print hex(value),si.readStatus() 
            #continue     
            sys.stdout.write("\nStart buffering of %d events for vped value %d and column value %d \n" %(eventsPerRun,vPed,column))

            sys.stdout.write("Waiting %d sec for settings to settle.\n" %sleepTime)
            time.sleep(sleepTime)
            

            if trigger == "sw":
                si.setStopEventNum(eventsPerRun*numChannels)
                si.enableTrigger("sw")
                si.startBuffering()
                for i in range(eventsPerRun):
                    si.sendSoftwareTrigger()
                    time.sleep(0.0001)
                si.stopBuffering()

            elif trigger == "ex":
                si.enableTrigger("ex")
                si.setStopEventNum(eventsPerRun*numChannels)
                si.startBuffering()
                while si.buffering.isSet():
                    sys.stdout.write("\r Num packet received: %d" %(si.getEventNumber()))
                    time.sleep(0.01)
            else:
                sys.stdout.write("Bad trigger choice\n")
                continue
            si.enableTrigger("sw") #to avoid overflow while storing in root file

            sys.stdout.write("\nTotal event in buffer: %d\n" %si.getEventNumber())

            sr.updateStatus(si.readStatus())
            sys.stdout.write("Start writing ROOT file\n")

            sr.start()                          #start store events in ROOT tree and wait for finish
       
            while si.getEventNumber() > 0 :  
                sys.stdout.write("\r Num packet stored: %d" %(sr.getPacketNumber()))
                time.sleep(0.01)
            sr.stop()
            sys.stdout.write("\rTotal packet stored: %d\n" %sr.getPacketNumber())

        sr.changeFile(calibFolder+filename)
        sr.close()
        sys.stdout.write("###### Finished %d of %d vPed values. ######\n"%(vPedList.index(vPed)+1,len(vPedList)))



    si.join()
    ts = "\n"+time.ctime()+"\n"
    sys.stdout.write(ts)

