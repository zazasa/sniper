#!/usr/bin/env python
import time
from sniperInterface import *
from sniperROOT import *
from ROOT import *



def calibrateTF():
    eventsPerRun = 1
    sleepTime = 5
    minVped = 106
    maxVped = 2915
    stepVped = 117
    numSettings = 0
    
    VpedList = range(minVped,maxVped,stepVped)	# 100:100:2500 mV = 106:117:2914 DAC counts (25 points spanning 2400 mV)
    sr.peek = True #display data while receiving
    
    for Vped in VpedList:
           
	    # Set Vped
	    si.setVpedValue(Vped)
	    
	    numSettings += 1
	    print "Finished setting Vped to %d counts." % (Vped)

	    # Wait for Vped to settle
	    print "Waiting %d sec for Vped to settle." % sleepTime
	    time.sleep(sleepTime)

	    # Take one run
	    si.triggerCycle(eventsPerRun)
	    print "Finished %d of %d Vped values." % (numSettings,len(VpedList))



    def plot():
        pass




if __name__ == "__main__":
    localIP = ("0.0.0.0",8106)
    boardIP = ("192.168.0.173",8105)  
    filename = "/home/salvo/Scrivania/DEV-PROJ/Target/DATA/20130919/run100.root"

    
    si = SniperInterface(localIP,boardIP)
    si.open()
    si.setTimeout(2)
#    si.enableTrigger("software")
    
    sr = SniperROOT(filename,"T5DATA","Target 5 Data")
    sr.setSource(si.getData)
    sr.setDelay(0.001)
    sr.start()

    sr.tree.SetMarkerStyle(20)

      
    f = True
    while f :
        cmd = raw_input("\nEnter Command: ")
        cmd = cmd.split(" ")
        if "quit" in cmd :
            si.close()
            sr.stop()
            f = False
            cmd = ""
        if "trigger" in cmd :
            if len(cmd) == 1:
                si.sendSoftwareTrigger()
            else :
                si.triggerCycle(int(cmd[1]))
            cmd = ""
        if "save" in cmd :
            print "\n Data stored in :", filename
            sr.writeTree()
            cmd = ""  
        if "browse" in cmd :
            tb = TBrowser()
            cmd = ""
        if "print" in cmd :
            sr.printTree()
            cmd = ""
        if "draw" in cmd :
            ch = cmd[1]
            sc = TCanvas()
            
            #sr.tree.SetMarkerColor(kBlue)
            z = sr.tree.Draw("CH1.value:CH1.seqTime>>h1","","lp")
            h= gPad.FindObject("h1")
            h.SetMarkerColor(kGreen)
            h.SetLineColor(kGreen)
            
            #time.sleep(5)
            sr.tree.SetMarkerColor(kRed)
            sr.tree.SetLineColor(kRed)
            sr.tree.Draw("CH2.value:CH2.seqTime","","same lp")    
            k = gPad.GetPrimitive("h1")
            print k
            
            
            sc.Modified()
            sc.Update()
            time.sleep(5)
            
            f = gPad.GetListOfPrimitives()
            f.Remove(k)
            sc.Modified()
            sc.Update()
            
            
            #sr.tree.Draw("CH"+ch+".value:CH"+ch+".seqTime")
            #sr.tree.Draw("value:seqTime","blockID == 400")
            cmd = ""
        if "calibrate" in cmd :
            calibrateTF()
            cmd = ""
        if "vped" in cmd :
            
            value = int(cmd[1])
            si.setVpedValue(value)
            print "\n vped ",value
            cmd = ""
        if "readreg" in cmd :

            addr = int(cmd[1],16)
            data = si.readRegister(0x10)
            print data, bin(int(data,16))[2:].zfill(32)
            cmd = ""
        if "settrig" in cmd :
            print "\n enable",cmd[1],"trigger"
            si.enableTrigger(cmd[1])
            cmd = ""
    

