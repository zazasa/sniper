#!/usr/bin/env python
from socket import *
import threading,time

#t5board register values, regnum:value
reg =   {}

def sendRegValue(ip,data):
    addr = data[3][2:].zfill(2)
    print "\n" , addr
    fword = ['1234','5678','0000','0000','0000','0000','0000','0000']
    fword[4]=reg[addr][:4]
    fword[5]=reg[addr][4:]
    data = str.join("",fword).decode('hex')
    UDPSock.sendto(data, ip)

    print "\nSent message" , ip,reg[addr],fword,data

def sendResponsePacket(ip):
    fword = ['1234','5678','0000','0000','0000','0000','0000','0000']
    data = str.join("",fword).decode('hex')
    UDPSock.sendto(data, ip)

def sendError(ip):
    fword = ['1234','5678','0000','0000','0000','0000','EEEE','0000']
    data = str.join("",fword).decode('hex')
    UDPSock.sendto(data, ip)
    print "\nSEND ERROR"

def writeRegister(ip,data):
    addr = data[3][2:].zfill(2)
    if addr in reg :
        value = data[4]+data[5]
        reg[addr]=value
        sendResponsePacket(ip)
        print "\nWrite Register", addr,value
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
    print rwFlag
    if (rwFlag == "00"): #read request
        sendRegValue(ip,data)
    elif (rwFlag == "01"): #write request
        writeRegister(ip,data)
    else:
        print "\nError msgParsing"

          
def listener(num,ip):
    print "\nSTART LISTENER"
    while 1:
        data,ip = UDPSock.recvfrom(buf)
        data = [data[i:i+2].encode('hex') for i in range(0, len(data), 2)] #hexify and split
    
        print "\nReceived message ", data, ip

        msgParsing(data,ip)

    




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
    print cmd
    if cmd == "reg" :
     print "\nRegister Value" , reg



UDPSock.close()

