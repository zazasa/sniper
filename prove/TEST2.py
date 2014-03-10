#!/usr/bin/env python
# Justin Vandenbroucke
# Created Mar 29 2013
# Configure TARGET 5 evaluation board for data taking.

# Import modules
import target
import sys
import numpy as np
import time


from sniperInterface import *
from sniperROOT import *
from ROOT import *

exe
localIP = ("0.0.0.0",8106)
boardIP = ("192.168.0.173",8105)  
filename = "/home/salvo/Scrivania/DEV-PROJ/Target/DATA/20130919/run100.root"


si = SniperInterface(localIP,boardIP)
si.open()
si.setTimeout(2)


sr = SniperROOT(filename,"T5DATA","Target 5 Data")
sr.setSource(si.getData)
sr.setDelay(0.001)
sr.start()

sr.tree.SetMarkerStyle(20)
