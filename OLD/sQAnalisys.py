#!/usr/bin/env python
# Salvatore Zaza
# Created 2013
from ROOT import *
from PyQt4 import QtCore, QtGui
from sCONST import *
from sQAGui import Ui_MainWindow
import sys,os
import numpy as np

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
    yField = ["cvalue","cvalue"]


    dataFolder = "/home/salvo/Scrivania/Tesi/DATA/"
    dataFieldList = FIELDLIST
    drawOptions = ["p","p"]
    x=[]
    y=[]
    n=0
    tree = False
    tc = False
    showLegend = [False,False]
    title = ["T5 DATA","MEASURE"]

    numBin = 100

    numBlocks = 16
    winWidth = numBlocks * samplePerBlock    #seqTime window width
    winIndex = 1   #actual window displayed
    winMax = 1
    winNum = 1  #number of window to plot

    mFrom = 0
    mTo = 0

    nPeaks = 0
    params = []
    xPeaks = []
    yPeaks = []

    hValues = []

    data = {}
    mg = False

    smooth = True

    def __init__(self,parent=None):   
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 
        
        self.uiConfig()
        gROOT.ProcessLine(CHSTRUCT);
        self.s = TSpectrum()


    def checkAllChannels(self):
        for box in self.ui.chanBox.findChildren(QtGui.QCheckBox):
            if "CH" in box.text():
                box.setChecked(True)

    def uncheckAllChannels(self):
        for box in self.ui.chanBox.findChildren(QtGui.QCheckBox):
            if "CH" in box.text():
                box.setChecked(False)

    def loadFile(self):
        self.tc = False
        self.mg = False

        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File',self.dataFolder,"*.root *.txt")
        if filename == "":
            return False
        fn,ext = os.path.splitext(str(filename))
        if ext == ".root" :
            self.ui.groupBox.setEnabled(True)
            self.tf = TFile(str(filename))
            self.tree = self.tf.Get("T5DATA")
            nEntries = self.tree.GetEntries()
            self.numBlocks = self.readNumBlocks()
            self.winWidth = self.numBlocks * samplePerBlock
            self.winMax = nEntries / self.winWidth
            self.draw()
            
            self.setWindowTitle(os.path.basename(str(filename)))
            #self.bufferize()
        else:
            self.ui.groupBox.setEnabled(False)
            self.readOFile(filename)
            
        

    def bufferize(self):  #bufferize all file .. to valuate if usable
        ch = chID_t()
        bl = self.tree.GetListOfBranches()
        for branch in bl:
            chID = branch.GetName()
            self.data[chID] = {"x":[],"y":[]} #x,y
            branch.SetAddress(ch)
            n = branch.GetEntries()
            for i in range(n):
                branch.GetEntry(i)
                self.data[chID]["x"].append(ch.seqTime)
                self.data[chID]["y"].append(ch.cvalue)
            

    def draw(self):
        if not self.tc:     
            self.tc = TCanvas()
            self.tc.Divide(1,2)
            self.pad = [self.tc.FindObject("c1_1"),self.tc.FindObject("c1_2")]
            self.mg = [TMultiGraph(),""]
            self.tc.cd(1)        
            self.mg[0].Draw("a")
            self.pad[0].SetGridx(True)
            self.pad[0].SetGridy(True)
        self.updateGraph(0)


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
            if self.mg:
                self.mg[0].SetTitle(self.title[0])
                self.createLegend(0)
                self.pad[0].Update()
                self.pad[0].Modified()
                self.pad[1].Update()
                self.pad[1].Modified()
            else:
                pad = self.tc.cd(2)
                pad.Modified()
                pad.Update()
                self.tc.Update()
                self.tc.Modified()


    def chanCheckBox(self):        
        box = self.sender()
        if (box.checkState() == QtCore.Qt.Checked) :
            self.addGraph(str(box.text()))
        if (box.checkState() == QtCore.Qt.Unchecked):
            self.removeGraph(str(box.text()))

    def getTreeData(self,xField,yField,chID):
        sqFrom = (self.winIndex-1) * self.winWidth
        sqTo = sqFrom + (self.winWidth*self.winNum) + 1 - 100
        cutString = chID+".seqTime > "+str(sqFrom)+ " && "+chID+".seqTime < "+str(sqTo)
        if self.tree:
            xField = chID+"."+xField
            yField = chID+"."+yField
            self.tree.Draw(xField+":"+yField,cutString,"goff")
            self.y = self.tree.GetVal(1)
            self.n = self.tree.GetSelectedRows()
            self.x = np.array(range(1,self.winWidth+1)*self.winNum)*1.

        if self.smooth:
            self.smoothSource = np.ndarray((self.n,),dtype = np.float32)
            for i in range(self.n):
                self.smoothSource[i] = self.y[i]


    def createGraph(self,padNum,grID):
        self.getTreeData(self.xField[padNum],self.yField[padNum],grID)
        
        if self.n > 0:
            if self.smooth:
                self.s.SmoothMarkov(self.smoothSource,self.n,10)
                self.graphs[padNum][grID] = TGraph()
                for i in range(self.n):
                    self.graphs[padNum][grID].SetPoint(i,self.x[i],self.smoothSource[i])
            else:
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
            self.update()

    def removeGraph(self,grID):
        if grID in self.graphList:
            self.graphList.remove(grID)
        if grID in self.graphs[0]:
            self.mg[0].RecursiveRemove(self.graphs[0][grID])
            del self.graphs[0][grID]
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
    def toggleLegend1(self):
        self.showLegend[0] = ~self.showLegend[0]
        self.update()


    def setX1(self,field):
        self.xField[0] = field
        self.ui.xButton_1.setText(field)
        self.updateGraph(0)
    def setY1(self,field):
        self.yField[0] = field
        self.ui.yButton_1.setText(field) 
        self.updateGraph(0) 

    def setTitle1(self):
        value = str(self.ui.title1.text())
        self.title[0] = value

    def setTitle2(self):
        value = str(self.ui.title2.text())
        self.title[1] = value

    def setMfrom(self,value):
        self.mFrom = value
    def setMto(self,value):
        self.mTo = value

    def prevWin(self):
        if self.winIndex > 1 :
            self.winIndex-=1
            self.draw()

    def nextWin(self):
        if self.winIndex < self.winMax:
            self.winIndex+=1
            self.draw()

    def allIn(self):
        self.winIndex = 1
        self.winNum = self.winMax
        self.draw()
        self.winNum = 1

    def measure(self,f):
        fCase = {   "sum" : lambda l: [sum(l)],
                    "max" : lambda l: [max(l)],
                    "hist" : lambda l: l,
                }

        self.winIndex = 1
        self.winNum = self.winMax
        self.getTreeData(self.xField[0],self.yField[0],self.graphList[0])
        self.winNum = 1

        indexes = sorted(sum([np.where(self.x==value)[0].tolist() for value in range(self.mFrom,self.mTo+1)],[]))
        groupby = self.mTo-self.mFrom+1
        indexes = [indexes[i:i+groupby] for i in range(0,len(indexes)+1,groupby)]
        while [] in indexes:
            indexes.remove([])

        self.hValues = []
        if self.smooth:
            source = self.smoothSource
        else : 
            source = self.y
        for row in indexes:
            values = [source[i] for i in row]
            self.hValues.extend(fCase[f](values)) 
        self.drawHist()
        
    def drawHist(self):
        minH = min(self.hValues)
        maxH = max(self.hValues)
        print minH,maxH, len(self.hValues)

        self.h1 = TH1F("h1",self.title[1],self.numBin,minH,maxH)
        for y in self.hValues:
            self.h1.Fill(y)

        pad = self.tc.cd(2)        
        pad.SetGridx(True)
        pad.SetGridy(True)
        self.h1.Draw()
        pad.Modified()
        pad.Update()

        mean = self.h1.GetMean()
        rms = self.h1.GetRMS()
        self.ui.mean.setText(str(mean))
        self.ui.rms.setText(str(rms))
        print mean,rms

        
    def setNumBin(self,value):
        self.numBin = value
        

    def readNumBlocks(self):
        self.tree.Draw("CH0.numBlocks","CH0.seqTime = 1","goff")
        y = self.tree.GetVal(0)
        return int(y[0])

    def fitFunction(self,x,par):
        result = 0
        #result = par[0]+par[1]*x[0]        #linear background removal
        for i in range(0,3*self.nPeaks,3):
            norm = par[i]
            mean = par[i+1]
            sigma = par[i+2]
            result+=norm*TMath.Gaus(x[0],mean,sigma)
        #print norm,mean,sigma,result
        return result

    def getBackground(self):

        backHist = self.s.Background(self.h1)
        backFit = TF1("backFit","gaus",self.xmin,self.xmax)
        backHist.Fit("backFit")
        params = backFit.GetParameters()



    def getParams(self):
        self.xmin = self.h1.GetXaxis().GetXmin()
        self.xmax = self.h1.GetXaxis().GetXmax() 
        #self.yPeaks = []
        #self.params = []
        #fline = TF1("fline","pol1",0,1000)
        #self.h1.Fit("fline","qn")
        #self.params.extend([fline.GetParameter(0),fline.GetParameter(1)])      #linear backgroun computing


        
        self.nPeaks = self.s.Search(self.h1,1)
        self.xPeaks = self.s.GetPositionX()

        for i in range(self.nPeaks):
            xp = self.xPeaks[i]
            bin = self.h1.GetXaxis().FindBin(xp)
            yp = self.h1.GetBinContent(bin)
            sigma = 3
            self.yPeaks.append(yp)
            self.params.extend([yp,xp,sigma])
        return



        self.yPeaks = [self.h1.GetBinContent(self.h1.GetXaxis().FindBin(x)) for x in self.xPeaks]
        self.params = [[self.yPeaks[i],self.xPeaks[i],3] for i in range(self.nPeaks)]
        self.params = sum(self.params,[])
        

    def fitHist(self):
        self.x = []
        self.y = []
        self.hValues = []
        self.fit = ""
        self.xPeaks = []
        self.yPeaks = []
        self.params = []


        self.getParams()
        params = np.array(self.params)
        self.fit = TF1("fit",self.fitFunction,self.xmin,self.xmax,len(params))
        self.fit.SetParameters(params)
        self.fit.SetNpx(1000)
        self.h1.Fit(self.fit)
        self.update()


    def readOFile(self,filename):
        if os.path.isfile(filename) :
            fBuffer = []
            self.x = []
            self.y = []
            with open(filename,"r") as f:
                for line in f:
                    fBuffer.append(line.rstrip())
            for row in fBuffer[5:] :
                self.x.append(float(row.split(" ")[0]))
                self.y.append(float(row.split(" ")[1]))
            bins = np.linspace(1,len(self.x),len(self.x))
            
            self.h1 = TH1F("h1","Oscilloscope Data",len(bins),min(bins),max(bins))
            for i in range(len(bins)):
                self.h1.SetBinContent(i,self.y[i])
            self.tc = TCanvas()
            pad = self.tc.cd(2)        
            pad.SetGridx(True)
            pad.SetGridy(True)
            self.h1.Draw()
            pad.Modified()
            pad.Update()
            

                


        


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
            receiver = lambda value=field: self.setY1(value)
            self.connect(item, QtCore.SIGNAL('triggered()'), receiver)
            menu.addAction(item)
        self.ui.yButton_1.setMenu(menu) 
        self.ui.yButton_1.setText(self.dataFieldList[-2]) 

    
        self.ui.loadButton.clicked.connect(self.loadFile)
        self.ui.drawButton.clicked.connect(self.draw)
        self.ui.prevButton.clicked.connect(self.prevWin)
        self.ui.nextButton.clicked.connect(self.nextWin)
        self.ui.allButton.clicked.connect(self.allIn)
        self.ui.maxButton.clicked.connect(lambda: self.measure("max"))
        self.ui.sumButton.clicked.connect(lambda: self.measure("sum"))
        self.ui.histButton.clicked.connect(lambda: self.measure("hist"))
        self.ui.fitButton.clicked.connect(self.fitHist)




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


        #self.ui.title1.editingFinished.connect(self.setTitle1)
        #self.ui.title2.editingFinished.connect(self.setTitle2)

        self.ui.mFromBox.valueChanged.connect(self.setMfrom)
        self.ui.mToBox.valueChanged.connect(self.setMto)
        self.ui.numBinBox.valueChanged.connect(self.setNumBin)
  


if __name__ == "__main__":
        
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        app = QtGui.QApplication(sys.argv)
        myapp = sGPlot()
        myapp.graphList.append("CH0")
        myapp.loadFile()
        myapp.mFrom = 110
        myapp.mTo = 120
        myapp.numBin = 150
        #myapp.measure("sum")
        #myapp.fitHist()
        self = myapp

    else:
        app = QtGui.QApplication(sys.argv)    

        #gEnv.SetValue("Gui.Backend","qt")
        #gEnv.SetValue("Gui.Factory","qt")
        #gEnv.SaveLevel(kEnvLocal)
        gSystem.Load("qtcint")     
        
        myapp = sGPlot()    
        myapp.show()
        sys.exit(app.exec_())
