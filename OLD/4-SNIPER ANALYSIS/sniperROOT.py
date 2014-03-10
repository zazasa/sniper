import sys,os,time,itertools
from datetime import datetime
from threading import Thread,Lock
from ROOT import *
from sniperCOST import *



class SniperROOT():
    def __init__(self,TName,TDescription):
        self.TName = TName
        self.TDescription = TDescription
        gROOT.ProcessLine(CHSTRUCT);  

        self.T5CONST()
        
        self.receiving = False      
        self.delay = 0      #in receive method
        self.maxPacket = 0
        self.fileTag = "run"
        self.tempFileName = ".tempRun"
        self.folder = ""
        self.autoSave = False
        

        self.TFilename = ""
        self.BFilename = ""

        self.fileIndex = 0
        
       

    def T5CONST(self):
        self.numColumns = 64        #see parseWordThree.m
        self.numRows = 8
        self.samplesPerBlock = 32
        self.numChannels = 16
        self.maxBlockID = self.numColumns*self.numRows
        self.saBlockNum = 2         #sampling array number of block
        #self.numBlocks = 2
        #self.numSamples = self.numBlocks * self.samplesPerBlock

    
    def open(self):
        
        self.TFilename,self.BFilename = self.getNewFilename()
        self.TFI = TFile(self.TFilename,"recreate")
        
        sys.stdout.write("Creat new root file: %s\n" %self.TFilename)

        self.BFI = open(self.BFilename,"wb")
        self.tree = TTree(self.TName,self.TDescription)

        self.channels = {}      #{0:chID_T(),  1:chID_t() ... }
        self.chSeqTime = {}     #{0:32, 1:64}
        self.tempHeaders = {}
        self.CBranches = {}        
                       
        self.packetNumber = 0

    #polling on self.source
    def receive(self):
        while self.receiving:
            self.readSource()
            time.sleep(self.delay)
        return  #dont remove :for thread handling                    
                           
                           
    def readSource(self):
        data = self.source()
        if not(data == "EOD"):
            if self.autoSave and (self.packetNumber == self.maxPacket):
                sys.stdout.write("Nextfile at packnum: %s\n" %self.packetNumber)
                self.nextFile() 

            self.dataParse(data) 
            self.packetNumber +=1

        
    def dataParse(self,data):       #parse raw t5 udp data string
        self.BFI.write(data)        #write binary data
        data = data.encode("hex")
        data = [data[i:i+4] for i in range(0,len(data),4)] #hexify and split
        self.getHeaders(data)
        self.getSamples(data[9:-3])
        
       
        
    def getHeaders(self,data):   #see readBinaryEvent.m                   
        row2 = bin(int(data[2],16))[2:].zfill(16) #to binary string
        row3 = bin(int(data[3],16))[2:].zfill(16) #to binary string
        row4 = bin(int(data[4],16))[2:].zfill(16) #to binary string
        row5 = bin(int(data[5],16))[2:].zfill(16) #to binary string
        self.tempHeaders = {
            "packetSize"    		: int(data[0][0:2],16),
            "seqNum"        		: int(data[0][2:],16),
            "timeStamp"     		: int(data[6]+data[1],16),            
            "currentSampleOffset"  	: int(row2[-5:],2),                 ###################TO RENAME!!!!!!!!!!!!1
            "column"        		: int(row2[-11:-5],2),
            "row"           		: int(row2[-14:-11],2),
            "useOffset"     		: int(row2[-15],2), 
            "readSft"       		: int(row2[-16],2), 
            "serialID"      		: int(row3[-4:],2),      
            "numBlocks"     		: int(row3[-8:-4],2) + 1,
            "triggerMask"   		: int(row3[-14:-8],2),
            "sampleOffset"  		: int(row3[:-14],2),
            "partialNumSamples"   	: int(row4[-4:],2),
            "sampleDelay"   		: int(row4[-9:-4],2),
            "staleData"     		: int(row4[-16],2),                        
            "numBlocksDigitized"   	: int(row5[-5:],2),
            "totalNumSamples" 		: int(row5[-15:5],2),
            "triggerDelay"  		: int(data[8][2:],16),
            }

            
        self.tempHeaders["blockID"] =  self.numColumns * self.tempHeaders["row"] + self.tempHeaders["column"]
        self.numBlocks = self.tempHeaders["numBlocks"]	
        self.numSamples = self.numBlocks * self.samplesPerBlock	#update numBlock and numSamples     
        
    #copy headers in root struct
    def copyTempHeaders(self,ch):
        ch.packetSize       	= self.tempHeaders["packetSize"]        
        ch.seqNum           	= self.tempHeaders["seqNum"]
        ch.timeStamp        	= self.tempHeaders["timeStamp"]
        ch.currentSampleOffset  = self.tempHeaders["currentSampleOffset"]
        ch.column           	= self.tempHeaders["column"]
        ch.row              	= self.tempHeaders["row"]
        ch.useOffset        	= self.tempHeaders["useOffset"]
        ch.readSft          	= self.tempHeaders["readSft"]
        ch.serialID         	= self.tempHeaders["serialID"]      #channel number
        ch.numBlocks        	= self.tempHeaders["numBlocks"]
        ch.triggerMask      	= self.tempHeaders["triggerMask"]
        ch.sampleOffset         = self.tempHeaders["sampleOffset"]
        ch.partialNumSamples    = self.tempHeaders["partialNumSamples"]
        ch.sampleDelay          = self.tempHeaders["sampleDelay"]
        ch.staleData            = self.tempHeaders["staleData"]
        ch.numBlocksDigitized   = self.tempHeaders["numBlocksDigitized"]
        ch.totalNumSamples      = self.tempHeaders["totalNumSamples"]
        ch.triggerDelay         = self.tempHeaders["triggerDelay"]
        ch.blockID		        = self.tempHeaders["blockID"]
        ch.sablockID            = 0
           
        

    def getSamples(self,data):
        chID = self.tempHeaders["serialID"]
        chName = "CH"+str(chID)
        if chName not in self.channels:
            self.channels[chName] = chID_t()
            self.chSeqTime[chName] = 0
            self.CBranches[chName] = self.tree.Branch(chName,self.channels[chName],CHBRANCH)  
        self.copyTempHeaders(self.channels[chName])

        for row in data:
            value = int(row[1:],16)
            self.chSeqTime[chName]+=1

            self.channels[chName].seqTime = self.chSeqTime[chName]
            self.channels[chName].value = value  
            self.channels[chName].cvalue = value
            self.channels[chName].cvalue = 0      
            self.CBranches[chName].Fill()

            
            if self.chSeqTime[chName] % self.samplesPerBlock == 0:
                self.channels[chName].row+=1
                self.channels[chName].sablockID = (self.channels[chName].sablockID + 1) % self.saBlockNum
                if (self.channels[chName].row > (self.numRows-1)):           #see leonid mail
                    self.channels[chName].row=0
                self.channels[chName].blockID = self.numColumns * self.channels[chName].row + self.channels[chName].column



        self.tree.SetEntries(self.chSeqTime[chName])

        
    #set data source for polling and read
    def setSource(self,source):
        self.source = source

    def start(self):
        self.receiving = True
        self.receiverThread = Thread(target = self.receive)
        self.receiverThread.daemon = True ##kill thread when main is killed
        self.receiverThread.start()
        self.startStopEvent(True)

    def stop(self):
        self.receiving = False
        self.writeTree()
        self.startStopEvent(False)
        self.fileIndex = 0




        
    def close(self):
        self.writeTree()
        self.TFI.Close()
        self.BFI.close()
    
    def reset(self):
        status = self.receiving
        self.stop()
        self.close()
        self.open()
        if status:
            self.start()  
        sys.stdout.write("\nRoot data cleared")



    def setDelay(self,secs):
        self.delay = secs            

    def writeTree(self):
        self.tree.Write("",5)  #5 = kOverwrite option
        self.BFI.flush()
        os.fsync(self.BFI.fileno())      #ensure to write data on disk
	        
    def printTree(self):
        self.tree.Print()	 
    
    def changeFile(self,filename):

        status = self.receiving
        self.writeTree()
        self.stop()
        self.close()     
  
        BOF,ext = os.path.splitext(filename)
        BOF = BOF+".bin"


        os.rename(self.TFilename,filename)            
        if os.path.isfile(self.BFilename):
            os.rename(self.BFilename,BOF)   

    
        self.BFilename = BOF
        self.TFilename = filename        
        try:
            self.TFI = TFile(self.TFilename,"update")
            self.BFI = open(self.BFilename,"ab")
        except BaseException,error:
            return False
        self.tree = self.TFI.Get("T5DATA")           #connect tree
        self.CBranches = {}                         #connect branches
        self.channels = {} 
        for branch in self.tree.GetListOfBranches():
            chName = branch.GetName()
            self.CBranches[chName] = branch
            self.channels[chName] = chID_t()
            branch.SetAddress(self.channels[chName])      
        if status:
            self.start()  
        sys.stdout.write("ROOT data file changed to %s\n" %self.TFilename)
        return True      
  

    def getFilename(self):
        return self.TFilename


    def getTimeTag(self):
        return datetime.now().strftime("%y%m%d%H%M%S")
    
    def getNewFilename(self):
        if self.autoSave:
            self.fileIndex+=1
            fileindex = self.fileIndex
            filetag = self.fileTag
            timetag = self.getTimeTag()+"_"+str(fileindex)
            if not filetag:
                sys.stderr.write("getNewFilename Error : Please set filetag. \n")
                return False
            tfn = os.path.join(self.folder,filetag+"_"+timetag+".root" )
            bfn = os.path.join(self.folder,filetag+"_"+timetag+".bin" )
        else:
            tfn = os.path.join(self.folder,self.tempFileName+".root" )
            bfn = os.path.join(self.folder,self.tempFileName+".bin" )
        return tfn,bfn
           
      
    def nextFile(self):
        self.close()      
        #self.TFilename,self.BFilename = self.getNewFilename()
        self.open()


    def startStopEvent(self,status):
        return status
    

    def getPacketNumber(self):
        return self.packetNumber

    def setMaxPacket(self,num):
        self.maxPacket = num
        
    def setFileTag(self,tag):
        self.fileTag = tag

    def setFolder(self,folder):
        self.folder = folder
        sys.stdout.write("Data folder changed: %s\n" %self.folder)
        if os.path.isfile(self.TFilename):
            newfile = os.path.join(self.folder,os.path.basename(self.TFilename))
            self.changeFile(newfile)
        
            
    def getTree(self):
        return self.tree

    def setAutoSave(self,value,reset = True):   
        if value:
            self.autoSave = value
            self.reset()
        else:
            self.autoSave = value
             
# Sample usage:
if __name__ == "__main__":

    sr = SniperROOT("/home/salvo/Scrivania/DEV-PROJ/Target/DATA/run23.root","T5DATA","Target 5 Data")
    t5Filename = "/home/salvo/Scrivania/DEV-PROJ/Target/DATA/run23.bin" 
    t5FI = open(t5Filename,"r")
    tb = TBrowser()
    
    for data in iter(lambda: t5FI.read(152),""):
        sr.dataParse(data)
#        time.sleep(5)
        
    sr.tree.Write()

    while 1:
        time.sleep(1)


