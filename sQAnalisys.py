#!/usr/bin/env python
# Salvatore Zaza
# Created 2013
from ROOT import *
from PyQt4 import QtCore, QtGui
from sCONST import *
from sQAGui import Ui_MainWindow
import sys,os,time
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
        "CH15":kPink+10,
        "bg" :kBlue+3,
        "s-bg":kTeal+3  }


    xField = "seqTime"
    yField = "cvalue"
    dataFolder = "/home/salvo/Scrivania/Tesi/DATA"
    dataFieldList = FIELDLIST
    tree = False
    tc = False

    numBlocks = 16
    winWidth = numBlocks * samplePerBlock    #seqTime window width
    winIndex = 1   #actual window displayed
    winMax = 1  #max window number
    winNum = 1  #number of window to plot
    chanList = []
    hList = {}
    gList = {}
    rBuffer = {}
    x=[]
    y=[]
    n=0
    numBins = 100
    source = "s-bg" #source data for measure

    gDrawOptions = "p"
    lineStyle = 1
    markerStyle = 20
    bglineStyle = 5
    bgMarkerStyle = 1
    sbglineStyle = 5
    sbgMarkerStyle = 1
    smoothColor = kBlack

    fitSigma = 1
    peakSigma = 2
    bgInt = 10  #spectrum.backgroun iterations
    sWidth = 5  #smooth window width
    trunc = 0
    fitNumPoint = 1000

    mFrom = 0
    mTo = 0
    gFrom = 0
    gTo = 0
    nPeaks = 0
    params = []
    xPeaks = []
    yPeaks = []
    hValues = []

    mHist = False

###########################################################################
###UI CONFIG

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
            receiver = lambda value=field: self.setY(value)
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
        self.ui.meanButton.clicked.connect(lambda: self.measure("mean"))
        self.ui.bgButton.clicked.connect(self.showBg)
        self.ui.sbgButton.clicked.connect(self.showSBG)
        self.ui.smoothButton.clicked.connect(self.showSmooth)
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

        self.ui.showMarkCB_1.stateChanged.connect(self.toggleMarkers)
        self.ui.showLineCB_1.stateChanged.connect(self.toggleLine)
        self.ui.showLegendCB_1.stateChanged.connect(self.toggleLegend1)


        self.ui.mFromBox.valueChanged.connect(self.setMfrom)
        self.ui.mToBox.valueChanged.connect(self.setMto)
        self.ui.numBinBox.valueChanged.connect(self.setNumBins)
        self.ui.sWidthBox.valueChanged.connect(self.setsWidth)
        self.ui.fSigmaBox.valueChanged.connect(self.setfSigma)
        self.ui.pSigmaBox.valueChanged.connect(self.setpSigma)

        self.ui.source.editingFinished.connect(self.setSource)
###########################################################################



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

    def chanCheckBox(self):        
        box = self.sender()
        text = str(box.text())
        if (box.checkState() == QtCore.Qt.Checked) :
            self.chanList.append(text)
            self.chanList = list(set(self.chanList))
        if (box.checkState() == QtCore.Qt.Unchecked):
            self.chanList.remove(str(box.text()))
        #self.draw()


    def loadFile(self):
        filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open File',self.dataFolder,"*.root *.txt"))
        if filename == "":
            return False
        self.filename = filename
        fn,ext = os.path.splitext(self.filename)
        self.setWindowTitle(os.path.basename(self.filename))
        self.tc = False
        self.rBuffer = {}

        if ext == ".root" :
            self.ui.groupBox.setEnabled(True)
            self.getNumBlocks()
            pass
        else:
            self.ui.groupBox.setEnabled(False)
            self.readOFile(self.filename)
            pass

#########################################################################################   
###OSCILLOSCOPE FILE READER
    def readOFile(self,filename):
        pass
#########################################################################################        
    def getNumBlocks(self):
        ch = chID_t()
        tf = TFile(self.filename)
        tree = tf.Get(TREENAME)
        branch = tree.GetBranch("CH0")
        branch.SetAddress(ch)
        branch.GetEntry(10)
        self.numBlocks = ch.numBlocks
        self.winWidth = self.numBlocks * samplePerBlock   #seqTime window width



    def bufferize(self,chID):
        self.rBuffer[chID] = {self.xField:[],self.yField:[]}
        ch = chID_t()
        tf = TFile(self.filename)
        tree = tf.Get(TREENAME)
        branch = tree.GetBranch(chID)
        self.nEntries = branch.GetEntries()
        branch.SetAddress(ch)
        for i in range(self.nEntries):
            branch.GetEntry(i)
            self.rBuffer[chID][self.xField].append(getattr(ch,self.xField))
            self.rBuffer[chID][self.yField].append(getattr(ch,self.yField))
        self.winMax = self.nEntries / self.winWidth
        

    def getData(self,chID,stMin,stMax):
        if not chID in self.rBuffer:
            self.bufferize(chID)
        iMin = self.rBuffer[chID][self.xField].index(stMin)
        iMax = self.rBuffer[chID][self.xField].index(stMax) + 1
        self.x = self.rBuffer[chID][self.xField][iMin:iMax]
        self.y = self.rBuffer[chID][self.yField][iMin:iMax]
        self.n = len(self.x)

    """
    def hFill(self):#not used
        xFrom = ((self.winIndex - 1) * self.winWidth) + 1
        xTo = xFrom + self.winWidth - 1 - self.trunc
        n = self.winWidth - self.trunc
        for chID in self.chanList:
            color = self.colors[chID]
            self.getData(chID,xFrom,xTo)
            self.hList[chID] = TH1F(chID,chID,n,1,n)
            self.hList[chID].SetLineColor(color)
            self.hList[chID].SetMarkerColor(color)
            self.hList[chID].SetMarkerStyle(self.markerStyle)
            for i in range(n):
                self.hList[chID].SetBinContent(i,self.y[i])
            if self.axisIndex == "": self.axisIndex = chID
            print "AXIS\n",self.hList[chID].GetMaximum(),self.hList[self.axisIndex].GetMaximum()
            if self.hList[chID].GetMaximum() > self.hList[self.axisIndex].GetMaximum():
                self.axisIndex = chID

    def hDraw(self):#not used
        print "hDRAW\n"
        xFrom = self.winIndex * self.winWidth
        xTo = xFrom + (self.winWidth*self.winNum)
        n = self.winWidth
        for chID in self.chanList:
            color = self.colors[chID]
            self.getData(chID,xFrom,xTo)
            h = TH1F(chID,chID,n,1,n)
            h.SetLineColor(color)
            h.SetMarkerColor(color)
            h.SetMarkerStyle(self.markerStyle)
            for i in range(n):
                h.SetBinContent(i,self.y[i])
            #self.h = h
            if h.GetMaximum() > self.pad1.GetUymax():
                print "AXIS\n", h.GetMaximum(), self.pad1.GetUymax()
                h.DrawCopy("AXIS")
            h.DrawCopy("same")
    """

    def gFill(self):
        xFrom = ((self.winIndex - 1) * self.winWidth) + 1
        xTo = xFrom + (self.winWidth*self.winNum) - 1 - self.trunc
        n = self.winWidth - self.trunc
        for chID in self.chanList:
            color = self.colors[chID]
            self.getData(chID,xFrom,xTo)
            self.gList[chID] = TGraph()
            self.gList[chID].SetName(chID)
            self.gList[chID].SetTitle(chID)
            self.gList[chID].SetLineColor(color)
            self.gList[chID].SetMarkerColor(color)
            self.gList[chID].SetMarkerStyle(self.markerStyle)
            for i in range(self.n):
                self.gList[chID].SetPoint(i,i%n,self.y[i])

    def gStyle(self):
        return
        pad = self.pad1
        mg = self.mg
        
        pad.SetLeftMargin(0.065)
        pad.SetRightMargin(0.12)
        pad.SetTopMargin(0.15)
        pad.SetBottomMargin(0.10)

        leg = pad.BuildLegend(0.9,1.0,0.99,0.004,"")
        leg.SetFillColor(kWhite)
        leg.SetTextSize(0.08)
        leg.SetTextFont(82)
        leg.SetTextAlign(22)
        pl = leg.GetListOfPrimitives()
        n = leg.GetNRows()
        for i in range(n):
            pl[i].SetOption("p")

        pad.Modified()
        pad.Update()
        mg.GetXaxis().SetLabelSize(0.1)
        mg.GetXaxis().SetRangeUser(0,127)
        mg.GetYaxis().SetLabelSize(0.1)
        t = pad.GetPrimitive("title")
        t.SetTextSize(0.13)
        t.SetX1NDC(0.07)
        t.SetY1NDC(0.89)
        pad.Modified()
        pad.Update()

    def mStyle(self):
        return
        pad = self.pad2
        hist = self.mHist
        pad.SetLeftMargin(0.065)
        pad.SetTopMargin(0.15)
        pad.SetBottomMargin(0.10)
        pad.SetRightMargin(0.27)

        hist.GetXaxis().SetLabelSize(0.1)
        hist.GetYaxis().SetLabelSize(0.1)
        t = pad.GetPrimitive("title")
        t.SetTextSize(0.13)
        t.SetX1NDC(0.07)
        t.SetY1NDC(0.89)
        hist.SetLineWidth(2)

        pst = pad.GetPrimitive("stats")
        pst.SetTextSize(0.1)
        pst.SetTextFont(82)
        #lsl = pst.GetListOfLines()
        #st = pst.GetTitle()
        #pst.SetTitleTextFont(102)
        #lsl.Remove(st)
        #gStyle.SetOptStat("emr")
        pst.SetX1NDC(0.75)
        pst.SetY1NDC(0.85)
        pst.SetX2NDC(0.99)
        pst.SetY2NDC(0.10)
        #lt = st.GetListOfLines()

        pad.Update()
        pad.Modified()


    def mSBG(self):#source-bg histogram
        chID = self.chanList[0]
        x = self.rBuffer[chID][self.xField]
        source = np.array(self.rBuffer[chID][self.yField])
        bg = np.array(self.rBuffer["bg"][self.yField])
        y = source-bg
        self.rBuffer["s-bg"] = {self.xField: x,self.yField:y}
        print "fillsbgHist finished\n"
        return True


    def  mSmooth(self): #smooth histogram     
        self.smSource = []
        for i in range(self.mHist.GetNbinsX()):
            self.smSource.append(self.mHist.GetBinContent(i))
         
        self.smSource = np.array(self.smSource,dtype = np.float32)
        self.s.SmoothMarkov(self.smSource,len(self.smSource),self.sWidth)
        self.mAxis = self.mHist.GetXaxis()
        xmin = self.mAxis.GetXmin()
        xmax = self.mAxis.GetXmax()
        nbins = int(self.mAxis.GetNbins())

        self.smHist = TH1F("smooth","smooth",nbins,xmin,xmax)
        for i in range(len(self.smSource)):
            self.smHist.SetBinContent(i,self.smSource[i])


    def showSmooth(self):
        self.mSmooth()
        self.mHist = self.smHist
        self.pad2.cd()
        self.mHist.Draw()
        self.update()


    def fillsHist(self):#source histogram
        chID = self.chanList[0]
        self.getData(chID,1,self.nEntries)
        n = self.n
        self.sHist = TH1F(chID,chID,n,1,n)
        for i in range(n):
            self.sHist.SetBinContent(i,self.y[i])

    def mBackground(self):
        self.fillsHist()
        bg = self.s.Background(self.sHist,self.bgInt)
        self.bg = bg
        n = int(bg.GetEntries())
        self.rBuffer["bg"] = {self.xField:[],self.yField:[]}
        
        for i in range(1,n+1):
            y = bg.GetBinContent(i)
            #x = bg.GetBinCenter(i)
            x = i
            self.rBuffer["bg"][self.xField].append(x)
            self.rBuffer["bg"][self.yField].append(y)
        print "mBackground finished\n"
        

    def fillmHist(self,f,chID):
        self.mHist = ""
        fCase = {   "sum"   : lambda l: [sum(l)],
                    "max"   : lambda l: [max(l)],
                    "mean"  : lambda l: [np.mean(l)],
                    "hist"  : lambda l: l,
                }
        #chID = self.chanList[0]
        self.getData(chID,1,self.nEntries)
        n = self.n

        self.x = np.array(range(1,self.winWidth+1)*self.winMax)*1.
        indexes = sorted(sum([np.where(self.x==value)[0].tolist() for value in range(self.mFrom,self.mTo+1)],[]))
        groupby = self.mTo-self.mFrom+1
        indexes = [indexes[i:i+groupby] for i in range(0,len(indexes)+1,groupby)]
        while [] in indexes:
            indexes.remove([])

        self.hValues = []
        for row in indexes:
            values = [self.y[i] for i in row]
            self.hValues.extend(fCase[f](values)) 

        self.mHist = TH1F(chID,chID,self.numBins,min(self.hValues),max(self.hValues))
        for y in self.hValues: 
                self.mHist.Fill(y)


    def measure(self,f,chID = ""):
        if chID == "": chID = self.source
        print chID
        self.fillmHist(f,chID)
        self.pad2.cd()
        self.mHist.Draw()
        self.update()


    def fitFunction(self,x,par):
        result = 0
        for i in range(0,3*self.nPeaks,3):
            norm = par[i]
            mean = par[i+1]
            sigma = par[i+2]
            result+=norm*TMath.Gaus(x[0],mean,sigma)
            #print x[0],norm,mean,sigma,norm*TMath.Gaus(x[0],mean,sigma),result
            #time.sleep(0.1)
        return result

    def getParams(self):
        self.params = []
        self.yPeaks = []
        self.xPeaks = []

        #self.yPeaks = []
        #self.params = []
        #fline = TF1("fline","pol1",0,1000)
        #self.h1.Fit("fline","qn")
        #self.params.extend([fline.GetParameter(0),fline.GetParameter(1)])      #linear backgroun computing

        binw = self.mHist.GetBinWidth(1)
        print binw
        self.nPeaks = self.s.Search(self.mHist,self.peakSigma)
        self.xPeaks = self.s.GetPositionX()
        xp = [self.xPeaks[i] for i in range(self.nPeaks)]
        self.xmin = min(xp)-(4*self.fitSigma*binw)
        self.xmax = max(xp)+(4*self.fitSigma*binw) 

        for i in range(self.nPeaks):
            xp = self.xPeaks[i]
            bin = self.mHist.GetXaxis().FindBin(xp)
            yp = self.mHist.GetBinContent(bin)
            sigma = self.fitSigma
            self.yPeaks.append(yp)
            self.params.extend([yp,xp,sigma])
        return True

    def fitHist(self):
        self.fit = ""
        self.getParams()
        params = np.array(self.params)
        self.fit = TF1("fit",self.fitFunction,self.xmin,self.xmax,len(params))
        self.fit.SetParameters(params)
        self.fit.SetNpx(self.fitNumPoint)
        self.mHist.Fit(self.fit,"R")
        self.update()

        npar = self.fit.GetNpar()
        par = self.fit.GetParameters()
        epar = self.fit.GetParErrors()

        parToTex(npar,par,epar)




    def draw(self,persistent = False):
        print "DRAW\n"
        self.gFill() 
        if not self.tc:
            self.tc = TCanvas()
            self.tc.Divide(1,2)
            self.pad1 = self.tc.cd(1)
            self.pad2 = self.tc.cd(2)
        self.mg = TMultiGraph()
        self.mg.SetTitle("T5 Data (ADC counts per cell)")
        self.pad1.Clear()
        self.pad1.cd()
        for chID in self.chanList:
            print self.gDrawOptions
            self.mg.Add(self.gList[chID],self.gDrawOptions)
        self.mg.Draw("a")
        self.update()



    def update(self):
        self.gStyle()
        if self.mHist: self.mStyle()
        self.tc.Update()
        self.tc.Modified()
        self.pad1.Update()
        self.pad1.Modified()
        self.pad2.Update()
        self.pad2.Modified()


    def prevWin(self):
        print "prevWin\n"
        if self.winIndex > 1 :
            self.winIndex-=1
            self.draw()
    def nextWin(self):
        print "nextWin\n"
        if self.winIndex < self.winMax:
            self.winIndex+=1
            self.draw()
        
            
    def showBg(self):
        if not "bg" in self.rBuffer:
            self.mBackground()
        if "bg" in self.chanList:
            self.chanList.remove("bg")
        else:
            self.chanList.append("bg")
            self.chanList = list(set(self.chanList))
        self.draw()

    def showSBG(self):
        if not "s-bg" in self.rBuffer:
            self.mSBG()
        if "s-bg" in self.chanList:
            self.chanList.remove("s-bg")
        else:
            self.chanList.append("s-bg")
            self.chanList = list(set(self.chanList))
        self.draw()

    def toggleOptions(self,opt):
        if opt in self.gDrawOptions:
            self.gDrawOptions = self.gDrawOptions.replace(opt,"")
        else:
            self.gDrawOptions += opt

    def toggleMarkers(self):
        self.toggleOptions("p")
    def toggleLine(self):
        self.toggleOptions("l")

    def toggleLegend1(self):
        self.showLegend[0] = ~self.showLegend[0]
        self.update()


    def setX(self,field):
        self.xField = field
        self.ui.xButton_1.setText(field)
    def setY(self,field):
        self.yField = field
        self.ui.yButton_1.setText(field) 
    def setMfrom(self,value):
        self.mFrom = value
    def setMto(self,value):
        self.mTo = value


    def allIn(self):
        self.winIndex = 1
        self.winNum = self.winMax
        self.draw()
        self.winNum = 1

        
    def setNumBins(self,value):
        self.numBins = value

    def setsWidth(self,value):
        self.sWidth = value

    def setfSigma(self,value):
        self.fitSigma = value

    def setpSigma(self,value):
        self.peakSigma = value


    def setBgInt(self,value):
        self.bgInt = value


    def setSource(self):
        box =  self.sender()
        self.source = str(box.text())

            

                


def parToTex(npar,par,epar):
    par = [par[i] for i in range(npar)]
    epar = [epar[i] for i in range(npar)]
    epar = np.around(epar,2).tolist()
    par = np.around(par,2).tolist()
    values = []
    for i in range(0,npar,3):
        value = (par[i+1],abs(epar[i+1]),abs(par[i+2]),abs(epar[i+2]))
        values.append(value)

    values = sorted(values,key= lambda value: value[0])

    for value in values:
        index = values.index(value)
        line =  str(index) + " & " + str(value[0]) + " $\pm$ " + str(value[1]) + " & " + str(value[2]) + " $\pm$ " + str(value[3]) + " & "

        if index > 0:
            diff = value[0] - values[index-1][0]
            err = value[1] + values[index-1][1]
            line+= str(diff) + " $\pm$ " + str(err) + "\\\\"
        else:
            line+= "-- \T\\\\"
        print line


  


if __name__ == "__main__":
        
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        app = QtGui.QApplication(sys.argv)
        myapp = sGPlot()
        myapp.chanList.extend(["CH0"])
        myapp.loadFile()
        myapp.mFrom = 110
        myapp.mTo = 115
        myapp.numBins = 400
        myapp.draw()  
        myapp.mBackground()
        myapp.mSBG()
        myapp.measure("sum")
        myapp.mSmooth()
        myapp.showSmooth()
        #myapp.measure("max","CH0") 
        self = myapp
     



    else:
        app = QtGui.QApplication(sys.argv)    

        #gEnv.SetValue("Gui.Backend","qt")
        #gEnv.SetValue("Gui.Factory","qt")
        #gEnv.SaveLevel(kEnvLocal)
        #gSystem.Load("qtcint")     
        
        myapp = sGPlot()    
        myapp.show()
        sys.exit(app.exec_())
