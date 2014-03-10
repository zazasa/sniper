#!/usr/bin/env python
# Salvatore Zaza
# Created 2013
from ROOT import *
from PyQt4 import QtCore, QtGui
from sniperCOST import *
from sGPlotGui import Ui_MainWindow
import sys

class sGPlot(QtGui.QMainWindow):

    colors = {
        "CH0":kRed,
        "CH1":kRed-7,
        "CH2":kMagenta+2,
        "CH3":kBlue+1,
        "CH4":kAzure+7,
        "CH5":kCyan,
        "CH6":kTeal-7,
        "CH7":kTeal+9,
        "CH8":kSpring-8,
        "CH9":kYellow+2,
        "CH10":kOrange-3,
        "CH11":kOrange,
        "CH12":kOrange+7,
        "CH13":kGray+2,
        "CH14":kBlack,
        "CH15":kPink+10, }

    graphList = []
    graphs = [{},{}]

    xField = ["seqTime","seqTime"]
    yField = ["value","cvalue"]

    dataFolder = "../../DATA/CALIBRATED"
    dataFieldList = FIELDLIST
    drawOptions = ["p","p"]
    x=[]
    y=[]
    n=0
    tree = False
    tc = False
    showLegend = [False,False]
    title = ["T5 RAW DATA","T5 CALIBRATED DATA"]

    def __init__(self,parent=None):   
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 
        
        self.uiConfig()


    def checkAllChannels(self):
        for box in self.ui.chanBox.findChildren(QtGui.QCheckBox):
            if "CH" in box.text():
                box.setChecked(True)

    def uncheckAllChannels(self):
        for box in self.ui.chanBox.findChildren(QtGui.QCheckBox):
            if "CH" in box.text():
                box.setChecked(False)

    def loadFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File',self.dataFolder,"*.root")
        if filename == "":
            return False
        self.tf = TFile(str(filename))
        self.tree = self.tf.Get("T5DATA")
        self.draw()

    def draw(self):
        if not self.tc:     
            self.tc = TCanvas()
            self.tc.Divide(1,2)
            self.pad = [self.tc.FindObject("c1_1"),self.tc.FindObject("c1_2")]
            self.mg = [TMultiGraph(),TMultiGraph()]
            self.tc.cd(1)        
            self.mg[0].Draw("a")
            self.tc.cd(2)        
            self.mg[1].Draw("a")
            self.pad[0].SetGridx(True)
            self.pad[1].SetGridx(True)
            self.pad[0].SetGridy(True)
            self.pad[1].SetGridy(True)
        self.updateGraph(0)
        self.updateGraph(1)

    def createLegend(self,padNm): 
        if self.showLegend[padNm]:
            legend = self.pad[padNm].GetPrimitive("TPave")
            if legend:
                legend.Delete()
            self.pad[padNm].BuildLegend()
            legend = self.pad[padNm].GetPrimitive("TPave")
            legend.SetTextFont(62)
            legend.SetTextSize(0.028)
        else:
            legend = self.pad[padNm].GetPrimitive("TPave")
            if legend:
                legend.Delete()

    def update(self):
        if self.tc:
            self.mg[0].SetTitle(self.title[0])
            self.mg[1].SetTitle(self.title[1])
            self.createLegend(0)
            self.createLegend(1)
            self.pad[0].Modified()
            self.pad[1].Modified()
            self.pad[0].Update()
            self.pad[1].Update()

    def chanCheckBox(self):        
        box = self.sender()
        if (box.checkState() == QtCore.Qt.Checked) :
            self.addGraph(str(box.text()))
        if (box.checkState() == QtCore.Qt.Unchecked):
            self.removeGraph(str(box.text()))

    def getTreeData(self,xField,yField,chID):
        if self.tree:
            xField = chID+"."+xField
            yField = chID+"."+yField
            self.tree.Draw(xField+":"+yField,"","goff")
            self.x = self.tree.GetVal(0)
            self.y = self.tree.GetVal(1)
            self.n = self.tree.GetEntries()


    def createGraph(self,padNum,grID):
        self.getTreeData(self.xField[padNum],self.yField[padNum],grID)
        if self.n > 0:
            self.graphs[padNum][grID] = TGraph(self.n,self.x,self.y)
            self.graphs[padNum][grID].SetMarkerStyle(7)
            self.graphs[padNum][grID].SetLineColor(self.colors[grID])
            self.graphs[padNum][grID].SetMarkerColor(self.colors[grID])
            self.graphs[padNum][grID].SetName(grID) 
            self.graphs[padNum][grID].SetTitle(grID)    
            return True
        return False


    def addGraph(self,grID):
        if grID not in self.graphList:     
            self.graphList.append(grID)            
            if self.createGraph(0,grID):
                self.mg[0].Add(self.graphs[0][grID],self.drawOptions[0])
            if self.createGraph(1,grID):
                self.mg[1].Add(self.graphs[1][grID],self.drawOptions[0])
            self.update()

    def removeGraph(self,grID):
        if grID in self.graphList:
            self.graphList.remove(grID)
        if grID in self.graphs[0]:
            self.mg[0].RecursiveRemove(self.graphs[0][grID])
            del self.graphs[0][grID]
        if grID in self.graphs[1]:
            self.mg[1].RecursiveRemove(self.graphs[1][grID])
            del self.graphs[1][grID]
        if self.tc:
            self.update()

    def updateGraph(self,padNum):       
        for grID in self.graphList:
            if grID in self.graphs[padNum]:
                self.mg[padNum].RecursiveRemove(self.graphs[padNum][grID])
            if self.createGraph(padNum,grID):
                self.mg[padNum].Add(self.graphs[padNum][grID],self.drawOptions[padNum])
            self.update() 

    def toggleOptions(self,opt,padNum):
        if opt in self.drawOptions[padNum]:
            self.drawOptions[padNum] = self.drawOptions[padNum].replace(opt,"")
        else:
            self.drawOptions[padNum] += opt
        self.updateGraph(padNum)

    def toggleMarkers1(self):
        self.toggleOptions("p",0)
    def toggleLine1(self):
        self.toggleOptions("l",0)
    def toggleMarkers2(self):
        self.toggleOptions("p",1)
    def toggleLine2(self):
        self.toggleOptions("l",1)
    def toggleLegend1(self):
        self.showLegend[0] = ~self.showLegend[0]
        self.update()
    def toggleLegend2(self):
        self.showLegend[1] = ~self.showLegend[1]
        self.update()

    def setX1(self,field):
        self.xField[0] = field
        self.ui.xButton_1.setText(field)
        self.updateGraph(0)
    def setX2(self,field):
        self.xField[1] = field
        self.ui.xButton_2.setText(field)
        self.updateGraph(1)
    def setY1(self,field):
        self.yField[0] = field
        self.ui.yButton_1.setText(field) 
        self.updateGraph(0) 
    def setY2(self,field):
        self.yField[1] = field
        self.ui.yButton_2.setText(field)
        self.updateGraph(1)

    def setTitle1(self):
        value = str(self.ui.title1.text())
        self.title[0] = value

    def setTitle2(self):
        value = str(self.ui.title2.text())
        self.title[1] = value

    def uiConfig(self):  
        self.ui.allONButton.clicked.connect(self.checkAllChannels)
        self.ui.allOFFButton.clicked.connect(self.uncheckAllChannels)

        menu = QtGui.QMenu()
        for field in self.dataFieldList:
            item = menu.addAction(field)
            receiver = lambda value=field: self.setX1(value)
            self.connect(item, QtCore.SIGNAL('triggered()'), receiver)
            menu.addAction(item)       
        self.ui.xButton_1.setMenu(menu)
        self.ui.xButton_1.setText(self.dataFieldList[-4])
        
        menu = QtGui.QMenu()
        for field in self.dataFieldList:
            item = menu.addAction(field)
            receiver = lambda value=field: self.setX2(value)
            self.connect(item, QtCore.SIGNAL('triggered()'), receiver)
            menu.addAction(item)
        self.ui.xButton_2.setMenu(menu)
        self.ui.xButton_2.setText(self.dataFieldList[-4])
        
        menu = QtGui.QMenu() 
        for field in self.dataFieldList:
            item = menu.addAction(field)
            receiver = lambda value=field: self.setY1(value)
            self.connect(item, QtCore.SIGNAL('triggered()'), receiver)
            menu.addAction(item)
        self.ui.yButton_1.setMenu(menu) 
        self.ui.yButton_1.setText(self.dataFieldList[-3]) 
        
        menu = QtGui.QMenu() 
        for field in self.dataFieldList:
            item = menu.addAction(field)
            receiver = lambda value=field: self.setY2(value)
            self.connect(item, QtCore.SIGNAL('triggered()'), receiver)
            menu.addAction(item)
        self.ui.yButton_2.setMenu(menu) 
        self.ui.yButton_2.setText(self.dataFieldList[-2]) 
    
        self.ui.loadButton.clicked.connect(self.loadFile)
        self.ui.drawButton.clicked.connect(self.draw)

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

        self.ui.showMarkCB_1.stateChanged.connect(self.toggleMarkers1)
        self.ui.showLineCB_1.stateChanged.connect(self.toggleLine1)
        self.ui.showLegendCB_1.stateChanged.connect(self.toggleLegend1)
        self.ui.showMarkCB_2.stateChanged.connect(self.toggleMarkers2)
        self.ui.showLineCB_2.stateChanged.connect(self.toggleLine2)
        self.ui.showLegendCB_2.stateChanged.connect(self.toggleLegend2)

        self.ui.title1.editingFinished.connect(self.setTitle1)
        self.ui.title2.editingFinished.connect(self.setTitle2)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)    

    #gEnv.SetValue("Gui.Backend","qt")
    #gEnv.SetValue("Gui.Factory","qt")
    #gEnv.SaveLevel(kEnvLocal)
    gSystem.Load("qtcint")     
    
    myapp = sGPlot()    
    myapp.show()
    sys.exit(app.exec_())
