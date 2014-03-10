import socket
import threading
import Queue
import sys
import time
from select import select




class CommandPacket():    
    def __init__(self,header = [0x0],address = [0x0], data = [0x0] , footer = [0x0], RW = "r"  ):
        self.size = 8 #number of words (2 bytes)
        self.indexes = { "data" : 4, "header" : 0, "footer" : 6, "address" : 3 , "RW" : 2 }
        self.fwords = [0x0 for i in range(self.size)] #zerofill packet
        self.UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

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


class SniperInterface(threading.Thread):

    EVENTPACKET,RESPONSEPACKET,UNKNOWNPACKET = range(3)

    def __init__(self): 
        super(SniperInterface, self).__init__()

        self.eventList = Queue.Queue()
        self.responseList = Queue.Queue()
        self.buffer = ""



        self.alive = threading.Event()
        self.connected = threading.Event()
        self.buffering = threading.Event()

        self.alive.set()

        #self.TCPSock = socket(AF_INET,SOCK_STREAM) 
        #self.TCPSock.bind(("0.0.0.0",8888))
        #self.TCPSock.listen(0)
        
      
        self.packetCase = { self.EVENTPACKET : self.receiveEventPacket,
                            self.RESPONSEPACKET : self.receiveResponsePacket,
                            self.UNKNOWNPACKET : self.receiveUknownPacket    
                            }

        self.timeout = 2 #seconds
        #self.maxEventBuffer = 1e10 #not used
        self.stopEventNum = -1        #number of entries in eventlist after which autostop buffering


    def connect(self,localIP,boardIP):
        self.localIP = localIP
        self.boardIP = boardIP    
        try:
            self.UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #for "ip already used" problem
            self.UDPSock.bind(self.localIP)
            self.connected.set()
            self.interfaces = [self.UDPSock]       # [self.UDPSock,self.TCPSock] 
        except IOError as e:
            sys.stderr.write(str(e))

    def close(self):
        if self.UDPSock:
            self.UDPSock.close()
        self.connected.clear()

   
    def startBuffering(self):
        self.buffering.set()
        
    def stopBuffering(self):
        self.buffering.clear()

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)

    def run(self):
        while self.alive.isSet():
            if self.connected.isSet():
                self.receive()
            else:
                time.sleep(0.1)


    def receive(self):
        inputReady,outputReady,exceptReady = select(self.interfaces,[],[],self.timeout)  #wait for data in interfaces list
        for s in inputReady:
            if s == self.interfaces[0]:
                self.buffer = self.readUDP(20,True)
                self.packetCase[self.getPacketType()]()
            #else : "\n FURTHER INTERFACE SUPPORT NOT IMPLEMENTED YET"
    

    def readUDP(self,nByte = 20,peek = False): ##error handling     
        data,ip = self.interfaces[0].recvfrom(nByte,peek * socket.MSG_PEEK)
        return data

    def getPacketType(self):
        if self.buffer.encode("hex")[0:8] == "12345678" :
            return self.RESPONSEPACKET
        elif len(self.buffer) == 20 :
            return self.EVENTPACKET
        else:
            return  self.UNKNOWNPACKET  

    def receiveUknownPacket(self):  #uknowns packet type
        sys.stderr.write("RECEIVER ERROR: UNKNOWN PACKET TYPE %s\n" %self.readUDP().encode("hex"))

    def receiveResponsePacket(self):
        self.responseList.put(self.readUDP(16))

    def receiveEventPacket(self):  
        length = int(self.buffer.encode("hex")[0:2],16)*8 
        data = self.readUDP(length)

        if self.buffering.isSet():
            self.eventList.put(data)
            self.stopEventNum-=1
            if (self.stopEventNum == 0) :
                self.stopBuffering()

    def readStatus(self):
        value = self.readRegister(0x11)
        value = bin(int(value,16))[2:][-10:]        #binaryze and get 10 lsb
        status = {  "bFlag"     : int(value[0],2),
                    "column"    : int(value[-9:-3],2),
                    "row"       : int(value[-3:],2)}

        return status

    def popEvent(self):
        try:
            data = self.eventList.get(True,0.1)
        except Queue.Empty as e:
            data = "EOD"
        return data

    def popResponse(self):
        try:
            resp = self.responseList.get(True,self.timeout)
            return resp
        except Queue.Empty as e:
            raise NameError("ReadResponsePacket: Timeout Error")
            


    def clearBuffer(self):
        self.eventList.queue.clear()   
        self.stopEventSize = 0   

    def getEventNumber(self):   
        return self.eventList.qsize() 

    def sendUDP(self,data): #need2 implement exceptions
            self.UDPSock.sendto(data, self.boardIP)

    def setTimeout(self,timeout): #seconds
        self.timeout = timeout

    def setStopEventNum(self, value):
        self.stopEventNum = value

    def writeRegister(self,address,value):#handle errors
        high,low = divmod(value,0x10000)
        packet = CommandPacket(header=[0x1234,0x5678],footer = [0xdead,0xbeef],RW = 'w',address = [address], data = [high,low])
        self.sendUDP(packet.getPacketData())
        return self.readResponsePacket()   

    def readRegister(self,address):
        packet = CommandPacket(header=[0x1234,0x5678],footer = [0xdead,0xbeef],RW = 'r',address = [address])
        self.sendUDP(packet.getPacketData())
        data = self.readResponsePacket()
        return data[4]+data[5]
        
    def readResponsePacket(self):#handle errors
        resp = self.popResponse()
        return [resp[i:i+2].encode('hex') for i in range(0, len(resp), 2)] #hexify and split


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

#sample usage
if __name__ == "__main__":
    localip = ("0.0.0.0",8106)
    boardip = ("192.168.0.173",8105)  

    si = SniperInterface()
    si.start()
    si.setTimeout(2)
    si.connect(localip,boardip)
    

    boardVer= si.readRegister(0x0) 
    print boardVer

    si.startBuffering()
    si.sendSoftwareTrigger()

