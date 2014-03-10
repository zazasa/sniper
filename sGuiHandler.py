import sys,os,time,pickle
from sCONST import *
from PyQt4 import QtCore, QtGui
from CSVTableModel import *

class SniperGuiHandler():
 
   
    def initGui(self):

#GUI INIT SETTINGS
        self.setWindowTitle(self.progName+" "+self.progVer)
                  
        self.dataFieldList = FIELDLIST   
             
        self.loadSettings()
        
        self.uiConfig() 

        self.loadT5ConfigFile(False)

        self.updateStatusTable()        

#GUI INIT SETTINGS METHODS
    def loadSettings(self):   

        if not self.loadSettingsFile():
            self.firstConfig()
        
        self.ui.localIPBox.setText(self.settings["localIP"][0])
        
        self.ui.localPortBox.setText(str(self.settings["localIP"][1]))
        self.ui.targetIPBox.setText(self.settings["targetIP"][0])
        
        self.ui.targetPortBox.setText(str(self.settings["targetIP"][1]))
        self.ui.tagBox.setText(self.settings["fileTag"])
        self.ui.triggerPerFileBox.setText(str(self.settings["triggerPerFile"]))
        self.ui.numTriggerBox.setText(str(self.settings["maxTriggerNumber"]))
        self.ui.cFileLabel.setText(self.settings["calibFile"])
        
        if not ("currentFolder" in self.settings) or (not os.path.isdir(self.settings["currentFolder"])):    
            self.settings["currentFolder"]=""
        self.autoStopValue = self.settings["maxTriggerNumber"]*self.packetPerTrigger



    def firstConfig(self):
        self.settings["targetIP"] = ("192.168.0.173",8105)
        self.settings["localIP"] = ("0.0.0.0",8106)
        self.settings["t5cfgfile"] = "t5configfast.csv"
        self.settings["triggerType"] = "None"
        self.settings["currentFolder"] = ""
        self.settings["fileTag"] = "run"
        self.settings["triggerPerFile"] = 10
        self.settings["maxTriggerNumber"] = 1
        self.settings["statusList"] = []
        self.settings["calibFile"] = ""


    def loadSettingsFile(self):
        try:
            f = open(self.cfgFile,"rb")
            self.settings = pickle.load(f)
            f.close()
            return True
        except BaseException,error:
            self.logManager("Errore lettura file di configurazione. First config loaded.","both",True)
            return False    

#GUI CLOSE EVENT
    def closeEvent(self,event):
        self.updateUi = False
        self.saveSettings()
        if self.sg:
            self.sg.close()
        if self.sr:
            self.sr.writeTree() #dont like this
            self.sr.close()
        if self.si:
            self.si.join()
        #QtGui.qApp.closeAllWindows() #doesnt works
        #gApplication.Terminate()   #doesnt works
        #gSystem.ProcessEvents()    #doesnt works
        #gSystem.Exit(True)  #avoid root crash but it exit immediatly 
        event.accept()

#GUI UPDATE METHOD                   
    def uiUpdate(self):
        self.readStatus()
        self.updateMonitor()

    def readStatus(self):
        self.bufferSize = self.si.getEventNumber()
        self.buffering = self.si.buffering.isSet()
        self.fileSize = self.sr.getPacketNumber()
        self.rootFileName = self.sr.getFilename()

    def updateMonitor(self):
        self.ui.numEventsLCD.display(self.bufferSize)
        self.ui.currFileLCD.display(self.fileSize)
        self.toggleCapture(self.buffering,True)
        self.ui.filenameLabel.setText(self.rootFileName)



#AUTOSAVE SETTINGS IF CHANGED           
    def settingsChanged(self):
        self.settings["localIP"] = ( self.ui.localIPBox.text(),int(self.ui.localPortBox.text()))
        self.settings["targetIP"] = ( self.ui.targetIPBox.text(),int(self.ui.targetPortBox.text()))
        self.saveSettings()
          
    def saveSettings(self):
        try:        
            f = open(self.cfgFile,"wb")
            pickle.dump(self.settings,f)
            f.close()
        except BaseException,error:
            self.logManager(" Errore scrittura file di configurazione: %s" %error,"both",True)
            return False    


#SOME GUI HANDLING METHODS
    def checkAllChannels(self):
        for box in self.ui.graphBox.findChildren(QtGui.QCheckBox):
            if "CH" in box.text():
                box.setChecked(True)

    def uncheckAllChannels(self):
        for box in self.ui.graphBox.findChildren(QtGui.QCheckBox):
            if "CH" in box.text():
                box.setChecked(False)

    def resetCounters(self):
        self.packetNumber=0

#COMPLEMENT UI DESIGNER GENERATED METHOD WITH CUSTOM SETTINGS
    def uiConfig(self):     
        ##triggerbutton configuration 
        menu = QtGui.QMenu()
        menu.addAction('Software',lambda: self.setTrigger('Software'))
        menu.addAction('External',lambda: self.setTrigger('External'))        
        menu.addAction('Both',lambda: self.setTrigger('Both'))
        self.ui.triggerButton.setText(self.settings["triggerType"])   
        self.ui.triggerButton.setMenu(menu)
        
        menu = QtGui.QMenu()
        for field in self.dataFieldList:
            item = menu.addAction(field)
            receiver = lambda value=field: self.setX(value)
            self.connect(item, QtCore.SIGNAL('triggered()'), receiver)
            menu.addAction(item)       
        self.ui.xButton.setMenu(menu)
        self.ui.xButton.setText(self.dataFieldList[-4])

        
        menu = QtGui.QMenu() 
        for field in self.dataFieldList:
            item = menu.addAction(field)
            receiver = lambda value=field: self.setY(value)
            self.connect(item, QtCore.SIGNAL('triggered()'), receiver)
            menu.addAction(item)
        self.ui.yButton.setMenu(menu) 
        self.ui.yButton.setText(self.dataFieldList[-3]) 

        self.ui.configViewModel = CSVTableModel()                                              #model for configview table.
#        self.ui.configView.setModel(self.ui.configViewModel)       
        self.ui.configView.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.ui.configView.verticalHeader().hide()

        self.ui.statusTable.itemChanged.connect(self.statusTableChanged)
        #self.ui.statusTable.setHorizontalHeaderLabels(["DESCRIPTION","ADDRESS","VALUE"])

        self.ui.connectButton.clicked.connect(self.openConnection)                              #Connect and disconnect button
        self.ui.disconnectButton.clicked.connect(self.closeConnection)
        self.ui.loadCfgButton.clicked.connect(lambda: self.loadT5ConfigFile(True))
        self.ui.saveCfgButton.clicked.connect(self.saveT5ConfigFile)
        self.ui.clearButton.clicked.connect(self.clearT5ConfigTable)
        self.ui.removeButton.clicked.connect(self.removeSelection)
        self.ui.chFileButton.clicked.connect(self.changeDataFile)
        self.ui.startButton.clicked.connect(self.toggleStart)
        self.ui.startButton.setStyleSheet('QPushButton {color: red}')
        self.ui.captureButton.clicked.connect(self.toggleCapture)
        self.ui.captureButton.setStyleSheet('QPushButton {color: red}')
        self.ui.browseButton.clicked.connect(self.rootBrowser)
        self.ui.allONButton.clicked.connect(self.checkAllChannels)
        self.ui.allOFFButton.clicked.connect(self.uncheckAllChannels)
        self.ui.chDirButton.clicked.connect(self.changeDir)
        self.ui.clearDataButton.clicked.connect(lambda: self.clearData(True))
        self.ui.clearBufferButton.clicked.connect(self.clearBuffer)
        self.ui.cFileButton.clicked.connect(self.selectCalibFile)

        
        self.ui.addStatButton.clicked.connect(self.addStatusTable)
        self.ui.removeStatButton.clicked.connect(self.removeStatusTable)
        self.ui.updateStatusButton.clicked.connect(self.updateStatus)

        self.ui.addButton.clicked.connect(self.addNewRow)
        self.ui.sendButton.clicked.connect(lambda: self.sendConfig(self.ui.configViewModel.getData()))
    
        self.ui.drawButton.clicked.connect(self.sgDraw)
        self.ui.sendTriggerButton.clicked.connect(self.sendTrigger)
        
        self.ui.localIPBox.editingFinished.connect(self.settingsChanged)
        self.ui.localPortBox.editingFinished.connect(self.settingsChanged)
        self.ui.targetIPBox.editingFinished.connect(self.settingsChanged)
        self.ui.targetPortBox.editingFinished.connect(self.settingsChanged)
        
        self.ui.triggerPerFileBox.editingFinished.connect(self.triggerPerFileChanged)
        self.ui.tagBox.editingFinished.connect(self.tagBoxChanged)
        self.ui.numTriggerBox.editingFinished.connect(self.numTriggerChanged)
        
        self.ui.triggerPerFileBox.setValidator(QtGui.QIntValidator(0, 999999))
        self.ui.numTriggerBox.setValidator(QtGui.QIntValidator(0, 999999))
        
        self.ui.controlTab.setEnabled(False)
        self.ui.dataTab.setEnabled(False)
        self.ui.statusTab.setEnabled(False)
        self.ui.tabWidget.setCurrentIndex(0)
        
#CHECHBOXES        
        self.ui.ch0.stateChanged.connect(self.chanCheckBox)
        self.ui.ch1.stateChanged.connect(self.chanCheckBox)
        self.ui.ch2.stateChanged.connect(self.chanCheckBox)
        self.ui.ch3.stateChanged.connect(self.chanCheckBox)
        self.ui.ch4.stateChanged.connect(self.chanCheckBox)
        self.ui.ch5.stateChanged.connect(self.chanCheckBox)
        self.ui.ch6.stateChanged.connect(self.chanCheckBox)
        self.ui.ch7.stateChanged.connect(self.chanCheckBox)
        self.ui.ch8.stateChanged.connect(self.chanCheckBox)
        self.ui.ch9.stateChanged.connect(self.chanCheckBox)
        self.ui.ch10.stateChanged.connect(self.chanCheckBox)
        self.ui.ch11.stateChanged.connect(self.chanCheckBox)        
        self.ui.ch12.stateChanged.connect(self.chanCheckBox)
        self.ui.ch13.stateChanged.connect(self.chanCheckBox)
        self.ui.ch14.stateChanged.connect(self.chanCheckBox)
        self.ui.ch15.stateChanged.connect(self.chanCheckBox) 
        
        self.ui.showMarkCB.stateChanged.connect(self.toggleMarkers)
        self.ui.showLineCB.stateChanged.connect(self.toggleLine)
        self.ui.showLegendCB.stateChanged.connect(self.toggleLegend)
        self.ui.autoSaveCB.stateChanged.connect(self.toggleAutoSave)
        self.ui.calibCB.stateChanged.connect(self.toggleCalibration)



#STATUS TABLE 
    def addStatusTable(self):        
        table = self.ui.statusTable
        table.blockSignals(True)
        row = table.rowCount()
        table.insertRow(row)
        table.blockSignals(False)
        return row

    def removeStatusTable(self):
        table = self.ui.statusTable
        if table.selectedItems():
            row = table.selectedItems()[0].row()
            table.removeRow(row)
            self.statusTableChanged()


    def statusTableChanged(self):        
        table = self.ui.statusTable
        self.settings["statusList"] = []
        for row in range(table.rowCount()):          
            if table.item(row,0): descr = str(table.item(row,0).text())
            else: descr = ""
            if table.item(row,1): address = str(table.item(row,1).text())
            else: address = ""
            self.settings["statusList"].append((descr,address))   

    def updateStatusTable(self):      
        table = self.ui.statusTable
        table.blockSignals(True)

        for item in self.settings["statusList"]:
            row = self.addStatusTable()
            value = QtGui.QTableWidgetItem("") #readregister
            value.setFlags(value.flags() ^ QtCore.Qt.ItemIsEditable)    #not editable
            table.setItem(row, 2, value)
            descr = item[0]
            address = item[1]   
            table.setItem(row, 0, QtGui.QTableWidgetItem(descr))
            table.setItem(row, 1, QtGui.QTableWidgetItem(address))
        table.blockSignals(False)



    def updateStatus(self):
        table = self.ui.statusTable
        table.blockSignals(True)
        for row in range(table.rowCount()):
            if table.item(row,0): descr = str(table.item(row,0).text())
            else: descr = ""
            if table.item(row,1): address = str(table.item(row,1).text())
            else: address = ""
            if not(address == ""):
                value = "0x"+self.si.readRegister(int(address,16))
                valuehex = QtGui.QTableWidgetItem(value)
                valuedec = QtGui.QTableWidgetItem(str(eval(value)))
                valuebin = QtGui.QTableWidgetItem("0b"+bin(eval(value))[2:].zfill(32))
                
                valuehex.setFlags(valuehex.flags() ^ QtCore.Qt.ItemIsEditable)
                valuedec.setFlags(valuedec.flags() ^ QtCore.Qt.ItemIsEditable)
                valuebin.setFlags(valuebin.flags() ^ QtCore.Qt.ItemIsEditable)

                table.setItem(row, 2, valuehex)
                table.setItem(row, 3, valuedec)
                table.setItem(row, 4, valuebin)
                
        table.blockSignals(False)
            
            
                   
#CALIBRATION FILE
    def selectCalibFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File',self.settings["currentFolder"], '*.csv')
        if not filename == "":
            self.sr.setCalibFile(filename)
            self.settings["calibFile"] = filename
            self.ui.cFileLabel.setText(filename)





#T5 BOARD CONFIG FILE 
    def loadT5ConfigFile(self,ask):
        if ask:
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        else:
            filename = self.settings["t5cfgfile"]
        
        if self.checkCfgFile(filename):
            self.settings["t5cfgfile"] = str(filename)
            self.ui.configFileLabel.setText(filename)
            self.ui.configViewModel.clearData()
            inputFile = csv.reader(open(self.settings["t5cfgfile"],'r'))
            headers = inputFile.next()
            data = [row for row in inputFile]
            self.ui.configViewModel.setHeaderData(headers)
            self.ui.configViewModel.insertRows(0,len(data),data)
            self.ui.configViewModel.insertLastRow()
            self.ui.configView.setModel(self.ui.configViewModel)  
            self.copyConfigFile() 
        else:
            self.logManager("Invalid filename "+filename, "both",True)
                    
    def saveT5ConfigFile(self):       
        try:       
            filename = open(QtGui.QFileDialog.getSaveFileName(self, 'Save File',".csv"),"w") 
        except:
            self.logManager(" Errore scrittura file di configurazione board.","both",True)
            return False   
        csvfile = csv.writer(filename)
        headers = self.ui.configViewModel.getHeaders()
        csvfile.writerow(headers)
        data = self.ui.configViewModel.getData()
        for row in data:
            csvfile.writerow(row)
        self.settings["t5cfgfile"] = str(filename.name)
        self.ui.configFileLabel.setText(filename.name)
        filename.close()

    def checkCfgFile(self,filename):
        if filename == "": return False
        row = open(filename).readline()
        return ("SeqNum,Address,Value,Descr" in row)

#T5 CONFIG TABLE HANDLING METHODS                  
    def clearT5ConfigTable(self):
        self.ui.configViewModel.clearData()
        self.ui.configViewModel.insertLastRow()       

    def removeSelection(self):
        rows = [row.row() for row in self.ui.configView.selectionModel().selectedRows()]
        if len(rows)>0:
            self.ui.configViewModel.removeRows(rows[0],len(rows))

    def addNewRow(self):
        rows = [row.row() for row in self.ui.configView.selectionModel().selectedRows()]
        if len(rows)>0:
            self.ui.configViewModel.insertRows(rows[-1]+1,1,[])

    def sendConfig(self,data):
        data = sorted(data,key= lambda data: int(data[0])) #sort data for seqNum
        for row in data:
            try :
                self.si.writeRegister(eval(row[1]),eval(row[2]))
            except BaseException,error:
                self.logManager("sendConfig Error %s" %error,"both",True)
        self.logManager("Config updated","both",False)
        self.readBoardInitStatus()
        self.copyConfigFile()
        self.sr.updateStatus(self.si.readStatus())

