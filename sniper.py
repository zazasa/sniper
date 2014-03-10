#!/usr/bin/env python
# Salvatore Zaza
# Created 2013
# Management Gui for Target 5 evaluation board.


import sys,os,shutil


from datetime import datetime
from threading import Thread,Lock
from PyQt4 import QtCore, QtGui
from sGui import Ui_MainWindow
from sGraph import *
from sInterface import *

from sROOT import *
from sGuiHandler import *


from ROOT import *


#LOG MANAGER
class LogManager(QtCore.QObject):
    messageSignal = QtCore.pyqtSignal(str)

    def __init__(self,destSlot,destFile):
        super(LogManager, self).__init__()
        self.messageSignal.connect(destSlot)
        self.logFile = destFile

    def __call__(self,message,mtype,isError=False):
        message = datetime.now().isoformat() + " " + str(message).strip();
        if isError:
            boxMessage = "<font color ='#ff0000'>"+message+"</font>"  
        else:
            boxMessage = message
        if mtype in ["log","both"]: 
                       
            try:
                f = open(self.logFile,"a")
                f.write(message + "\n")
                f.close()            
            except: 
                self("Impossibile scrivere sul file log", "win",True)            

        if mtype in ["win","both"]:      
            self.messageSignal.emit(boxMessage)
            #self.ui.messageBox.append(boxMessage) 
   
#Output redirection class
class OutLog:
    def __init__(self, logManager):
        self.logManager = logManager	
    def write(self, message):
        self.logManager(message,"both",False)
class ErrorLog:
    def __init__(self, logManager):
        self.logManager = logManager
    def write(self, message):
        self.logManager(message,"both",True)

    


class sniper(QtGui.QMainWindow,SniperGuiHandler):
    progName = "Sniper"
    progVer = "0.9.9"
    logFile = "sniperLog.log"
    cfgFile = "sniperCfg.cfg"
    settings = {}
    boardVer = ""
    boardSN = ""
    si = False
    sr = False
    sg = False


    def __init__(self,parent=None):   
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)    


        self.logManager = LogManager(self.ui.messageBox.append,self.logFile)
#STDOUT AND ERR REDIRECTIONS
        sys.stderr = ErrorLog(self.logManager)
        sys.stdout = OutLog(self.logManager)

#HARDCODED SETTINGS        
        self.packetPerTrigger = 16 
        
        self.initGui() #loadsetting,uiconfig,loadt5configfile

        
#COUNTER AND INDEX INIT
        self.triggerDelay = 0 #for trigger cycle method   
        self.numEventBuffer = 0
        self.fileSize = 0
        

#SNIPER BOARD INTERFACE        
        self.si = SniperInterface()   #create board interface
        self.si.start() 
        #self.si.setTimeout(2) #sec

        
#SNIPER ROOT INTERFACE
        
        self.sr = SniperROOT("T5DATA","Target 5 Data")    
        #self.sr.setDelay(0.001)
        self.sr.setFileTag(self.settings["fileTag"])
        self.sr.setFolder(self.settings["currentFolder"])
        self.sr.setCalibFile(self.settings["calibFile"])
        self.sr.startStopEvent = self.srStartStopEvent
        
        self.sr.setMaxPacket(0)
        self.sr.autoSave = False
        self.sr.open()
        

#SNIPER ROOT GRAPH HANDLING OBJECT
        
        self.sg = SniperGraph()         
        self.sg.xField = str(self.ui.xButton.text())
        self.sg.yField = str(self.ui.yButton.text())
        

#GUI UPDATE TIMER
        self.uiTimer = QtCore.QTimer()
        self.uiTimer.timeout.connect(self.uiUpdate)
        self.uiTimer.start(100) #msec

###END __init__


#SI METHODS:
#Bind socket, set target address and read first register information   
    def openConnection(self): #2do: handle herrors (socket and packet)
        message = "Binding the receive socket to port " + str(self.settings["localIP"][1]) + " of " + self.settings["localIP"][0]
        self.logManager(message,"both",False)
        message = "Connection on port " + str(self.settings["targetIP"][1]) + " of " + self.settings["targetIP"][0]
        self.logManager(message,"both",False)    

        if self.si:
            try :
            #OPEN BOARD INTERFACE
                self.si.connect(self.settings["localIP"], self.settings["targetIP"] )    
            ##reading board version and serial code from board register and handle runtimeError        
                self.boardVer= self.si.readRegister(0x0)
                self.boardSN=  self.si.readRegister(0x02)+self.si.readRegister(0x03)            
                sys.stdout.write("Running on Board (serial code %s) firmware version %s." % (self.boardSN,self.boardVer))
                self.readBoardInitStatus()
            except BaseException,error:
                sys.stderr.write("openConnecton error: %s " %error)   
                self.closeConnection()
                return False 


        #CONNECT SG AND SR
            if self.sr:
                self.sr.setSource(self.si.popEvent) 
                self.sr.updateStatus(self.si.readStatus())
            if self.sg:
                self.sg.setSource(self.sr.getTree) 
     
    #ENABLE TABS     
        self.ui.controlTab.setEnabled(True)
        self.ui.dataTab.setEnabled(True)
        self.ui.statusTab.setEnabled(True)


    def readBoardInitStatus(self):
        self.setTrigger(self.si.getTriggerStatus(),True)

    def closeConnection(self):
        if self.si:
            self.si.close()
            self.logManager("Socket closed","both",False)   
        self.ui.controlTab.setEnabled(False)
        self.ui.dataTab.setEnabled(False)
        self.ui.statusTab.setEnabled(False)
        self.logManager("Disconnected","both",False)       

    #Set Trigger mode (2do: check connection status)
    def setTrigger(self,value,init=False):
        self.ui.triggerButton.setText(value)
        if value == "Software": 
            self.ui.sendTriggerButton.setEnabled(True)
            if not init: self.si.enableTrigger("sw")
        elif value == "External":
            self.ui.sendTriggerButton.setEnabled(False)
            if not init: self.si.enableTrigger("ex")
        elif value == "Both":
	        if not init: self.si.enableTrigger("both")
                                  
    def toggleCapture(self,status,update = False):
        if status :

            self.ui.captureButton.setStyleSheet('QPushButton {color: green}')
            self.ui.captureButton.setText("ON")   
            self.ui.captureButton.setChecked(True)
            if not update: 
                self.si.setStopEventNum(self.settings["maxTriggerNumber"]*self.packetPerTrigger)
                self.si.startBuffering()
        else:
            self.ui.captureButton.blockSignals(True)
            self.ui.captureButton.setChecked(False)
            self.ui.captureButton.blockSignals(False)
            self.ui.captureButton.setStyleSheet('QPushButton {color: red}')
            self.ui.captureButton.setText("OFF")
            self.ui.captureButton.setChecked(False) 
            if not update:
                self.si.stopBuffering() 

    #TRIGGER CYCLE METHODS
    def sendTrigger(self):
        self.toggleCapture(True)
        self.triggerToSend = self.settings["maxTriggerNumber"]
        self.triggerCycleThread = Thread(target = self.triggerCycle)
        self.triggerCycleThread.daemon = True ##kill thread when main is killed
        self.triggerCycleThread.start()

    def triggerCycle(self):
        self.ui.sendTriggerButton.setEnabled(False)
        for i in range(self.triggerToSend):
            time.sleep(self.triggerDelay)
            if not self.si.sendSoftwareTrigger():
                break
        self.ui.sendTriggerButton.setEnabled(True)
   
    def clearBuffer(self):
        self.si.clearBuffer()
#END SI METHODS



#SR METHODS:
    def toggleStart(self,status):
        if status :
            self.sr.start()            
        else:
            self.ui.startButton.blockSignals(True)
            self.ui.startButton.setChecked(False)
            self.ui.startButton.blockSignals(False)
            self.sr.stop()
    
    def changeDir(self):
        newFolder = str(QtGui.QFileDialog.getExistingDirectory(self,"Choose Directory",self.settings["currentFolder"]))
        sys.stdout.write(newFolder)
        if os.path.isdir(newFolder):
            self.settings["currentFolder"] = newFolder  
            self.sr.setFolder(newFolder)
            self.copyConfigFile()

    def checkDataFilename(self,filename):
        if not filename:
            return False
        filename,ext = os.path.splitext(filename)
        if filename == "" or ext != ".root":
            return False
        else:
            return True 
        

    def changeDataFile(self,filename = ""):      
        if not self.checkDataFilename(filename):           
            filename = str(QtGui.QFileDialog.getSaveFileName(self, 'Save File',os.path.join(self.settings["currentFolder"],".root"),".root"))
        if not self.checkDataFilename(filename):
            sys.stderr.write("sniper.changeDataFile error: BAD FILENAME \n")
            return False
        if self.sr.changeFile(filename):
            return True 
        else:
            sys.stderr.write("sniper.changeDataFile error: unknown\n")
            return False

    def clearData(self,reset=True):
        reply = QtGui.QMessageBox.question(self, 'Warning',"All Data will be erased", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            #self.toggleStart(False)
            #self.toggleCapture(False)
            if reset :
                self.sr.reset()
            self.resetCounters()
            #self.sg.clearData()
            #self.uncheckAllChannels()
            return True
        else:
            return False

    def toggleCalibration(self):
        box = self.sender()
        self.sr.setCalibration(box.checkState() == QtCore.Qt.Checked)

    def toggleAutoSave(self):
        self.ui.triggerPerFileBox.setEnabled(False)
        self.ui.tagBox.setEnabled(False)
        box = self.sender()
        if (box.checkState() == QtCore.Qt.Checked):
            if self.clearData(False):  
                #self.copyConfigFile()
                self.sr.setMaxPacket(self.settings["triggerPerFile"]*self.packetPerTrigger)
                self.sr.setFileTag(str(self.ui.tagBox.text()))
                self.sr.setAutoSave(True) 
        else:
            self.ui.triggerPerFileBox.setEnabled(True)
            self.ui.tagBox.setEnabled(True)
            self.toggleStart(False)
            self.sr.setAutoSave(False)

    def srStartStopEvent(self,status):
        if status :
            self.ui.startButton.setStyleSheet('QPushButton {color: green}')
            self.ui.startButton.setText("ON")            
        else:
            self.ui.startButton.setStyleSheet('QPushButton {color: red}')
            self.ui.startButton.setText("OFF")

    def triggerPerFileChanged(self):
        value = int(self.ui.triggerPerFileBox.text())
        self.settings["triggerPerFile"] = value
        self.sr.setMaxPacket(value*self.packetPerTrigger)

    def tagBoxChanged(self):
        value = str(self.ui.tagBox.text())
        self.settings["fileTag"] = value
        self.sr.setFileTag(value)

    def numTriggerChanged(self):
        value = int(self.ui.numTriggerBox.text())
        self.settings["maxTriggerNumber"] = value    


    def copyConfigFile(self):
        datatag = datetime.now().strftime("%y%m%d%H%M%S")  
        srcfile = os.path.basename(self.settings["t5cfgfile"])
        destfile,ext = os.path.splitext(srcfile)
        destfile = destfile+"_"+datatag+ext
        folder = self.settings["currentFolder"]
        destfile = os.path.join(folder,destfile)
        shutil.copy(srcfile, destfile)
        sys.stdout.write("Write config file in: %s\n"%destfile)    
#END SR METHODS


#SG METHODS:
    def setX(self,field):
        self.sg.setX(field)
        self.ui.xButton.setText(field)
        
    def setY(self,field):
        self.sg.setY(field)
        self.ui.yButton.setText(field)   
    
    def toggleMarkers(self):
            self.sg.toggleOptions("p")
            
    def toggleLine(self):
            self.sg.toggleOptions("l")

    def chanCheckBox(self):        
        box = self.sender()
        if (box.checkState() == QtCore.Qt.Checked) :
            self.sg.addGraph(str(box.text()))
        if (box.checkState() == QtCore.Qt.Unchecked):
            self.sg.removeGraph(str(box.text()))     

    def rootBrowser(self):
        self.sg.browse()

    def sgDraw(self):
        self.sg.draw() 

    def toggleLegend(self):
        self.sg.toggleLegend()

#END SG METHODS 
        




#MAIN
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)    

    #gEnv.SetValue("Gui.Backend","qt")
    #gEnv.SetValue("Gui.Factory","qt")
    #gEnv.SaveLevel(kEnvLocal)
    #gSystem.Load("qtcint")     
    
    myapp = sniper()
    myapp.show()
    sys.exit(app.exec_())
