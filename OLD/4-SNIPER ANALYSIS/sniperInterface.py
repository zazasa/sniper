from socket import *
from threading import Thread,Lock
from select import select
import sys,time
import itertools #for cycle iterator



class CommandPacket():    
    def __init__(self,header = [0x0],address = [0x0], data = [0x0] , footer = [0x0], RW = "r"  ):
        self.size = 8 #number of words (2 bytes)
        self.indexes = { "data" : 4, "header" : 0, "footer" : 6, "address" : 3 , "RW" : 2 }
        self.fwords = [0x0 for i in range(self.size)] #zerofill packet
        self.UDPSock = socket(AF_INET,SOCK_DGRAM)

        self.setHeader(header)
        self.setAddress(address)
        self.setData(data)
        self.setFooter(footer)
        self.setRWFlag(RW)
        

    def setHeader(self,header):#error handling
        for i in range(len(header)):
            self.fwords[self.indexes["header"] + i] = header[i] 
    def setFooter(self,footer):
        for i in range(len(footer)):
            self.fwords[self.indexes["footer"] + i] = footer[i]        
    def setAddress(self,address):
        for i in range(len(address)):
            self.fwords[self.indexes["address"] + i] = address[i]
    def setData(self,data):
        for i in range(len(data)):
            self.fwords[self.indexes["data"] + i] = data[i]
    def setRWFlag(self,RW):
        if RW == "w":
            self.fwords[self.indexes["RW"]] = (self.fwords[self.indexes["RW"]] & 0x3fff) | 0x4000
        elif RW =="r":
            self.fwords[self.indexes["RW"]] = (self.fwords[self.indexes["RW"]] & 0x3fff)

    def getPacketData(self):        
        return str.join("",[str("%04x") %row for row in self.fwords]).decode('hex')



class Listener():
    
    eventPacket,responsePacket,unknownPacket = range(3)     
    
    def __init__(self,UDPSock): 
        self.dataMutex = Lock()         #lock on data buffer (self.eventList)
        self.respMutex = Lock()         #lock on response data (self.responseList)
        
        self.eventList = []
        self.responseList = []
        
        self.buffer = ""                #single packet buffer
        self.interfaces = [UDPSock]       # [UDPSock,TCPSock]       
        self.packetCase = { self.eventPacket : self.receiveEventPacket,
                            self.responsePacket : self.receiveResponsePacket,
                            self.unknownPacket : self.uknownPacketError    
                            }

        self.buffering = False
        self.maxEventBuffer = 999999999
        self.autoStopNum = 0
        self.autoStop = False

    def start(self):
        self.listening = True
        self.receiverThread = Thread(target = self.receive)
        self.receiverThread.daemon = True ##kill thread when main is killed
        self.receiverThread.start()
        
    def stop(self):
        self.listening = False
            
    def receive(self):
        while self.listening:
            inputReady,outputReady,exceptReady = select(self.interfaces,[],[])
            for s in inputReady:
                if s == self.interfaces[0]:
                    self.buffer = self.readUDP(20,True)
                    self.packetCase[self.getPacketType()]()
                else:
                    print "\n FURTHER INTERFACE SUPPORT NOT IMPLEMENTED YET"
        return  #dont remove :for thread handling

    def getPacketType(self):
#        print self.buffer.encode("hex")
        if self.buffer.encode("hex")[0:8] == "12345678" :
            return self.responsePacket
        elif len(self.buffer) == 20 :
            return self.eventPacket
        else:
            return  self.unknownPacket       

    def uknownPacketError(self):  #uknowns packet type
        sys.stderr.write("RECEIVER ERROR: UNKNOWN PACKET TYPE %s\n" %self.readUDP().encode("hex"))
        self.stopBuffering()

    def receiveResponsePacket(self):
        self.respMutex.acquire()
        self.responseList.append(self.readUDP(16))
        self.respMutex.release()
        

    def receiveEventPacket(self):  
        length = int(self.buffer.encode("hex")[0:2],16)*8 
        data = self.readUDP(length)
        if self.buffering:
            self.dataMutex.acquire()
            if len(self.eventList) > self.maxEventBuffer:
                self.eventList = []
            self.eventList.append(data)
            if self.autoStop and (len(self.eventList) == self.autoStopNum):
                sys.stdout.write("Auto stop buffering\n")
                self.stopBuffering()
            self.dataMutex.release()            
        self.packetReceived(self.buffering)     
      
    def readUDP(self,nByte = 20,peek = False):##error handling     
        data,ip = self.interfaces[0].recvfrom(nByte,peek * MSG_PEEK)
        return data

    def getData(self):
        self.dataMutex.acquire()
        if len(self.eventList)> 0:
            data = self.eventList.pop(0)           
        else:
            data = "EOD"        #no data

        self.dataMutex.release()
        return data 
            
    def getResponse(self):
        self.respMutex.acquire()
        if len(self.responseList)> 0:            
            resp = self.responseList.pop(0)
        else:
            resp =  "EOR"        #no response
        self.respMutex.release()
        return resp
        
    def packetReceived(self,status):
        return status
    
    def startBuffering(self):
        self.buffering = True
        
    def stopBuffering(self):
        self.buffering = False
        
    def clearBuffer(self):
        self.dataMutex.acquire()        
        self.eventList = []      
        self.dataMutex.release()
        
    def getEventNumber(self):
        self.dataMutex.acquire()
        eventNum =  len(self.eventList) 
        self.dataMutex.release()    
        return eventNum 
    
    def setAutoStop(self,status,num):
        self.autoStopNum = num
        self.autoStop = status

class SniperInterface():
    receiver = False
    UDPSock = False
    def __init__(self): 
        self.timeout = 1 #seconds
        

    def open(self,localIP,boardIP):
        self.localIP = localIP
        self.boardIP = boardIP 
        self.UDPSock = socket(AF_INET,SOCK_DGRAM)
        self.UDPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #for ip already used problem
        self.UDPSock.bind(self.localIP)
        self.receiver = Listener(self.UDPSock)

        self.getData = self.receiver.getData
        self.clearBuffer = self.receiver.clearBuffer


        self.startBuffering = self.receiver.startBuffering
        self.stopBuffering = self.receiver.stopBuffering
        self.getEventNumber = self.receiver.getEventNumber
        self.setAutoStop = self.receiver.setAutoStop

        self.receiver.start()
        
#        self.TCPSock = socket(AF_INET,SOCK_STREAM) 
#        self.TCPSock.bind(("0.0.0.0",8888))
#        self.TCPSock.listen(0)

    def close(self):
        if self.receiver:
            self.receiver.stop() 
        if self.UDPSock:    
            self.UDPSock.close()     
        
    def sendUDP(self,data): #need2 implement exceptions
            self.UDPSock.sendto(data, self.boardIP)

    def setTimeout(self,timeout): #seconds
        self.timeout = timeout

    def writeRegister(self,address,value):#handle errors
        high,low = divmod(value,0x10000)
        packet = CommandPacket(header=[0x1234,0x5678],footer = [0xdead,0xbeef],RW = 'w',address = [address], data = [high,low])
        self.sendUDP(packet.getPacketData())
        return self.readResponsePacket()   
        ##manage packet errors
    
    def readRegister(self,address):
        packet = CommandPacket(header=[0x1234,0x5678],footer = [0xdead,0xbeef],RW = 'r',address = [address])
        self.sendUDP(packet.getPacketData())
        data = self.readResponsePacket()
        return data[4]+data[5]
        ##manage packet errors and data 


    def readResponsePacket(self):#handle errors
        endTime = time.time() + self.timeout
        toc = time.time()
        while toc < endTime:
            toc = time.time()
            time.sleep(0.000000001)           #i dont know why it needed
            resp = self.receiver.getResponse()
            if not resp == "EOR":
                return [resp[i:i+2].encode('hex') for i in range(0, len(resp), 2)] #hexify and split
        raise NameError("ReadResponsePacket: Timeout Error")
        #sys.exit(0)             
            

    def sendSoftwareTrigger(self):#error handling
        try:
            data = self.readRegister(0x10)
            value = int(data,16)        #string to binary
            value = value & 0xffff7fff  #set bit 15 = 0
            value = value | 2**31       #set bit 31 = 1  
            self.writeRegister(0x10,value)
            
            data = self.readRegister(0x10)
            value = int(data,16)        #string to binary
            value = value & 0x7fff7fff  #set bit 15,31 = 0
            self.writeRegister(0x10,value) 
        except BaseException,error:
                sys.stderr.write("Send Software Trigger error: %s\n"%error)
                return False
        return True
        
            
            

    

    def setVpedValue(self,vped):
        if (vped > 2**12):
            print "\n setVpedValue Error : vpped must be less than 4096"
            return
        else:
            self.writeRegister(0x15,vped & 0x0FFF)


    def enableTrigger(self,trigger):    #sw,ex,both
        try:
            data = self.readRegister(0x10)
            value = int(data,16)
      
            if trigger == "ex":
                value = self.setBit(value,15,0)  
                value = self.setBit(value,5,0)  #disable software
                value = self.setBit(value,4,1) 
                
            if trigger == "sw":
                value = self.setBit(value,15,0)  
                value = self.setBit(value,4,0)  #disable external
                value = self.setBit(value,5,1)  
                
            if trigger == "both":
                value = self.setBit(value,15,0)  
                value = self.setBit(value,4,1)  
                value = self.setBit(value,5,1)  
                    
            return self.writeRegister(0x10,value)
        except BaseException,error:
            sys.stderr.write("Send Software Trigger error: %s\n"%error)
            return False
        return True
        
    def connectEventListChanged(self,dest):
        self.receiver.eventListChanged = dest
        
    def connectPacketReceived(self,dest):
        self.receiver.packetReceived = dest             
        
    def setBit(self,var,bitNum,value):
        bitNum = -1*(bitNum+1)
        var = bin(var)[2:].zfill(32)
        var = [bit for bit in var ]
        var[bitNum] = str(value)
        var = "".join(var)
        return int(var,2)

    def getBit(self,var,bitNum):
        bitNum = -1*(bitNum+1)
        var = bin(var)[2:].zfill(32)
        var = [bit for bit in var ]
        return int(var[bitNum],2)
        
        
    def getTriggerStatus(self):
        data = self.readRegister(0x10)
        data = int(data,16)
        sw = self.getBit(data,5)
        ex = self.getBit(data,4)
        if ex and sw:
            return "Both"
        if ex:
            return "External"
        if sw:
            return "Software"
        return "None"

    def getEventNumber(self):
        return 0

    def getNumChannels(self):
        pass

        
        
        
        
        
# Sample usage:
if __name__ == "__main__":

    localip = ("0.0.0.0",8106)
    boardip = ("192.168.0.173",8105)  

    
    si = SniperInterface(localip,boardip)   
    si.setTimeout(5)
    si.open()
#    c = CommandPacket(header = [0x1234,0x5678],footer= [0xdead,0xbeef], RW = "r" , address = [0x20], data = [0x1111,0x1111])
#    si.sendUDP(c.getPacketData())

#    print si.writeRegister(0x1f,0x22222222)
#    print si.writeRegister(0xff,0x11111111)
#    print si.readRegister(0x03)
#    print si.readRegister(0xff)

    si.sendSoftwareTrigger()

    f = True
    while f :
        cmd = raw_input("\nEnter Command: ")
        if cmd == "quit" :
            si.close()
            f = False

    

