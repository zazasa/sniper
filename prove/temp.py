
    
    def toggleAutoSave(self):
        box = self.sender()
        if (box.checkState() == QtCore.Qt.Unchecked):
            self.ui.tagBox.setEnabled(True)
            return False           
        newfilename = self.getTagFilename()
        print newfilename
        if newfilename:
            if self.clearData():    
                print "\n going on"
                self.ui.tagBox.setEnabled(False)
                self.toggleStart(False)
                self.toggleCapture(False)
                self.resetCounters()
                self.changeDataFile(newfilename)                  
                self.autoSaveMode = not self.autoSaveMode
                self.totPackNum = int(self.ui.triggerPerFileBox.text())*self.packetPerTrigger     
        else:
            self.totPackNum = -1
            self.ui.autoSaveCB.setChecked(False)
            return False
    
    def nextDataFile(self):
        self.toggleStart(False)
        newfilename = self.getTagFilename()
        if not newfilename:
            self.ui.autoSaveCB.setChecked(False)
            return False
        if self.sr.nextFile(newfilename):
            self.ui.filenameLabel.setText(newfilename) 
            self.settings["currentFile"] = newfilename     
            self.sg.tree = self.sr.tree         #reconnect graph
            self.totPackNum = int(self.ui.triggerPerFileBox.text())*self.packetPerTrigger
            self.currFileNum=0
        else:
            print "\n nextDataFile error"
            return False       
        self.toggleStart(True)
        return True
   
    
    def currFileCounter(self,status):
        if status:
            self.currFileNum+=1
        if self.currFileNum == self.totPackNum:
            print "\n ECCOCI" 
            self.nextDataFile()
            
            
            
