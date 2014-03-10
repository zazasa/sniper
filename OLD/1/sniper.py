#!/usr/bin/env python
# Salvatore Zaza
# Created 2013
# Management Gui for Target 5 evaluation board.


import sys,csv,os
import target
from datetime import datetime

from PyQt4 import QtCore, QtGui
from sniperGui import Ui_MainWindow
from sniperActions import *
from CSVTableModel import *


###stderr redirection class
class OutLog:
    def __init__(self, logManager):
        self.logManager = logManager
	
    def write(self, message):
        self.logManager(message,"both",True)


class sniper(QtGui.QMainWindow,sniperActions):


    progName = "Sniper"
    progVer = "0.1"
    logFile = "sniperLog.log"
    cfgFile = ""  #not used yet
    settings = {}
    board = ""
    boardVer = ""
    boardSN = ""


    def __init__(self,parent=None):   
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)       
        self.loadSettings() 
        self.board = target.T5EvalBoard()
        self.uiConfig()
        self.loadT5ConfigFile(False)

#        sys.stderr = OutLog(self.logManager) #stderr redirection


    ###Read configuration from INI file
    def loadSettingsFile(self): #todo
        self.settings["localIP"] = "0.0.0.0"
        self.settings["localPort"] = "8106"
        self.settings["targetIP"] = "192.168.0.173"
        self.settings["targetPort"] = "8105"
        self.settings["triggerType"] = "None"
        self.settings["t5cfgfile"] = "t5configfast.csv"
        


    ###Initial settings for Connection Tab
    def loadSettings(self):
        self.loadSettingsFile()
        self.ui.localIPBox.setText(self.settings["localIP"])
        self.ui.localPortBox.setText(self.settings["localPort"])
        self.ui.targetIPBox.setText(self.settings["targetIP"])
        self.ui.targetPortBox.setText(self.settings["targetPort"])

    def checkCfgFile(self,filename):
        if filename == "": return False
        row = open(filename).readline()
        return ("SeqNum,Address,Value,Descr" in row)
                    
    
    def loadT5ConfigFile(self,ask):
        if ask:
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        else:
            filename = self.settings["t5cfgfile"]
        
        if self.checkCfgFile(filename):
            self.settings["t5cfgfile"] = filename
            self.ui.configViewModel.clearData()
            inputFile = csv.reader(open(self.settings["t5cfgfile"],'r'))
            headers = inputFile.next()
            data = [row for row in inputFile]
            self.ui.configViewModel.setHeaderData(headers)
            self.ui.configViewModel.insertRows(0,len(data),data)
            self.ui.configViewModel.insertLastRow()
            self.ui.configView.setModel(self.ui.configViewModel)   
        else:
            self.logManager("Invalid filename "+filename, "both",True)
                  
    def clearT5ConfigTable(self):
        self.ui.configViewModel.clearData()
        self.ui.configViewModel.insertLastRow()       

    def removeSelection(self):
        rows = [row.row() for row in self.ui.configView.selectionModel().selectedRows()]
        print rows, rows[0],len(rows)
        self.ui.configViewModel.removeRows(rows[0],len(rows))


    def addNewRow(self):
        rows = [row.row() for row in self.ui.configView.selectionModel().selectedRows()]
        self.ui.configViewModel.insertRows(rows[-1]+1,1,[])




    ###Custom configuration for ui elements (not qtdesigner)    
    def uiConfig(self):     
        ##triggerbutton configuration 
        menu = QtGui.QMenu()
        menu.addAction('Software',lambda: self.setTrigger(self.ui.triggerButton,'Software'))
        menu.addAction('External',lambda: self.setTrigger(self.ui.triggerButton,'External'))        
        menu.addAction('Both',lambda: self.setTrigger(self.ui.triggerButton,'Both'))
        self.ui.triggerButton.setText(self.settings["triggerType"])   
        self.ui.triggerButton.setMenu(menu)

        self.ui.configViewModel = CSVTableModel()                                              #model for configview table.
#        self.ui.configView.setModel(self.ui.configViewModel)       
        self.ui.configView.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.ui.configView.verticalHeader().hide()

        self.ui.connectButton.clicked.connect(self.openConnection)                              #Connect and disconnect button
        self.ui.disconnectButton.clicked.connect(self.closeConnection)
        self.ui.loadCfgButton.clicked.connect(lambda: self.loadT5ConfigFile(True))
        self.ui.clearButton.clicked.connect(self.clearT5ConfigTable)
        self.ui.removeButton.clicked.connect(self.removeSelection)
        self.ui.addButton.clicked.connect(self.addNewRow)
        self.ui.sendButton.clicked.connect(lambda: self.sendConfig(self.ui.configViewModel.getData()))
    


    ###Write log message in text window or log file
    def logManager(self,message,mtype,error): #mtype = log for filelog, win for editbox, both for both.        
        message = datetime.now().isoformat() + " " + message;
        if error:
            boxMessage = "<font color ='#ff0000'>"+message+"</font>"  
        else:
            boxMessage = message

        if ( mtype in ["log","both"] ):            
            try:
                f = open(self.logFile,"a")
                f.write(message + "\n")
                f.close()            
            except: 
                self.logManager("Impossibile scrivere sul file log", "win",True)
                self.ui.messageBox.append(self.logFile +  "  " + boxMessage)              
        if ( mtype in ["win","both"] ):      
            self.ui.messageBox.append(boxMessage)   


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = sniper()
    myapp.show()

    sys.exit(app.exec_())
    
