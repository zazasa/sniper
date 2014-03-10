from ROOT import *
import sys


class SniperGraph():
    xField = ""
    yField = ""
    tree = ""
    graph = {} #list of TGraph object {"ch1": TGrap(), ...}
    tc = False     #root canvas
    tb = False     #root browser
    mg = False      #root multigraph
    graphID = [] #which channel is enabled to draw

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
            
    x = []
    y = []
    n = 0
    drawOptions = "p"
    
    def __init__(self):
        self.mg = TMultiGraph()
        self.showLegend = False

        
    def close(self):
        if self.tc:
            self.tc.Close()
        if self.tb:
            self.tb.Close()
        self.mg = ""
        self.graph = {}
        self.tree = ""

    
    def setSource(self,source):
        self.source = source
        
    def setX(self,value):
        self.xField = value
        self.updateGraph()
        
    def setY(self,value):
        self.yField = value
        self.updateGraph()


    def updateGraph(self):        
        for grID in self.graphID:
            if grID in self.graph:
                self.mg.RecursiveRemove(self.graph[grID])
            if self.createGraph(grID):
                self.mg.Add(self.graph[grID],self.drawOptions)
            self.update() 


    def addGraph(self,grID):
        if grID not in self.graphID:     
            self.graphID.append(grID)               
            if self.createGraph(grID):
                self.mg.Add(self.graph[grID],self.drawOptions)
        if self.tc:
            self.update()
            
    def removeGraph(self,grID):
        if grID in self.graphID:
            self.graphID.remove(grID)
        if grID in self.graph:
            self.mg.RecursiveRemove(self.graph[grID])
            del self.graph[grID]
        if self.tc:
            self.update()
          
    def getTreeData(self,chID):
        self.tree = self.source()       #connect to sr object
        xField = chID+"."+self.xField
        yField = chID+"."+self.yField
        self.tree.Draw(xField+":"+yField,"","goff")
        self.x = self.tree.GetVal(0)
        self.y = self.tree.GetVal(1)
        self.n = self.tree.GetEntries()
        self.tree = ""                  #disconnect to sr object
    
    def createGraph(self,grID):
        self.getTreeData(grID)
        if self.n > 0:
            self.graph[grID] = TGraph(self.n,self.x,self.y)
            self.graph[grID].SetMarkerStyle(7)
            self.graph[grID].SetLineColor(self.colors[grID])
            self.graph[grID].SetMarkerColor(self.colors[grID])
            self.graph[grID].SetName(grID) 
            self.graph[grID].SetTitle(grID)         
            return True
        return False

    def createLegend(self): 
        if self.showLegend:
            legend = self.tc.GetPrimitive("TPave")
            if legend:
                legend.Delete()
            self.tc.BuildLegend()
            legend = self.tc.GetPrimitive("TPave")
            legend.SetTextFont(62)
            legend.SetTextSize(0.028)
        else:
            legend = self.tc.GetPrimitive("TPave")
            if legend:
                legend.Delete()

         
        
    def update(self):
        if self.tc:
            self.createLegend()
            self.tc.Modified()
            self.tc.Update()
      
        
        
    def draw(self): 
        if not self.tc:     
            self.tc = TCanvas()
            self.mg.Draw("a")        
            self.update()
        self.updateGraph()

    def toggleOptions(self,opt):
        if opt in self.drawOptions:
            self.drawOptions = self.drawOptions.replace(opt,"")
        else:
            self.drawOptions += opt
        self.updateGraph()

    def toggleLegend(self):
        self.showLegend = ~self.showLegend
        self.update()
        
        

    def clearData(self):    #maybe useless
        self.tc = False
        self.tb = False
        self.graph = {}
        self.graphID = []
        self.mg = TMultiGraph()
        sys.stdout.write("Graph data cleared\n")

        
        
        
    def browse(self):
        if not self.tb:
            self.tb = TBrowser() 
        
        
        
        

