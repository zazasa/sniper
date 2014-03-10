#!/usr/bin/env python
from socket import *
import threading,time
from select import select

#t5board register values, regnum:value
reg =   {}

def sendRegValue(ip,data):
    addr = data[3][2:].zfill(2)
#    print "\n" , addr
    if addr in reg :
        fword = ['1234','5678','0000','0000','0000','0000','0000','0000']
        fword[4]=reg[addr][:4]
        fword[5]=reg[addr][4:]
        data = str.join("",fword).decode('hex')
        print "\nSend message" ,fword,data,ip
        UDPSock.sendto(data, ip)
    else:
        sendError(ip)



def sendResponsePacket(ip):
    fword = ['1234','5678','0000','0000','0000','0000','0000','0000']
    data = str.join("",fword).decode('hex')
    UDPSock.sendto(data, ip)
    print "\nSent response" ,fword,data,ip

def sendError(ip):
    fword = ['1234','5678','0000','0000','0000','0000','EEEE','0000']
    data = str.join("",fword).decode('hex')
    UDPSock.sendto(data, ip)
    print "\nSEND ERROR",fword,data,ip

def writeRegister(ip,data):
    addr = data[3][2:].zfill(2)
    if addr in reg :
        value = data[4]+data[5]
        print "\nWrite Register", addr,value
        reg[addr]=value
        sendResponsePacket(ip)
    else:
        sendError(ip)

def init():
    for i in range(45):
        reg[hex(i+1)[2:].zfill(2)]='00000000'
    reg["01"]="00000003"  #firmware version
    reg["02"]="c4000012"  #lsw of serialcode boardid 5 
    reg["03"]="3b9a7601"  #msw of serialcode boardid 5  
    reg["10"]="11111111"  #trigger control register  
    print "\nRegister Value" , reg
    

def msgParsing(data,ip):
    rwFlag = bin(int(data[2][0],16))[2:].zfill(4)[:2]
    if (rwFlag == "00"): #read request
        sendRegValue(ip,data)
    elif (rwFlag == "01"): #write request
        writeRegister(ip,data)
    else:
        print "\nError msgParsing"

          
def listener(num,ip):
    print "\nSTART LISTENER"
    while 1:
        inputready,outputready,exceptready = select([UDPSock],[],[])
        data,ip = UDPSock.recvfrom(buf)
        fword = [data[i:i+2].encode('hex') for i in range(0, len(data), 2)] #hexify and split
    
        print "\nReceived message ", fword,data, ip

        msgParsing(fword,ip)

    
def sendEvent(ip):
    print "\n SEND EVENTTYPE PACKET"       
    filename = "run.bin"
    t5FI = open(filename,"r")
    for data in iter(lambda: t5FI.read(152),""):
        UDPSock.sendto(data, ip)
    t5FI.close()




    """    
    #create data packet
    mic=CaptureMic()
    mic.start()
    time.sleep(3)
    mic.stop()
    buff = mic.getBuffer()
    packet = []
    for row in buff:
        sampleID = 0x1
        sampleValue = int((row[1]/(2**16))*(2**12)) #rescale in 12 bit 
        packet.append("%04x" %(sampleID<<12 | sampleValue))
#        print (sampleID<<12 | sampleValue)
    

    #header packet
    size = int(len(packet)/8)
    fword = ["%04x"%size,'0000','0000','0000','0000','0000','0000','0000']

    packet = fword + packet
    print packet
    data = str.join("",packet).decode('hex')
    UDPSock.sendto(data, ip)
    """




buf = 1024
ip = ("0.0.0.0",8105)
init()

UDPSock = socket(AF_INET,SOCK_DGRAM)
UDPSock.bind(ip)
#UDPSock.settimeout(0)

t = threading.Thread(target = listener, args=(ip))
t.daemon= True ## for kill thread when main is killed
t.start()
while 1:
    cmd = raw_input("\nEnter Command: ")
    if cmd == "reg" :
        cmd = ""
        print "\nRegister Value" , reg
    elif cmd == "eve" :
        cmd = ""    
        sendEvent(("0.0.0.0",8106))


UDPSock.close()

