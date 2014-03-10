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
from sniperGraph import *
from ROOT import *

localIP = ("0.0.0.0",8106)
boardIP = ("192.168.0.173",8105)  
filename = ".tempRun.root"


si = SniperInterface()
si.open(localIP,boardIP)
si.setTimeout(2)


sr = SniperROOT("T5DATA","Target 5 Data")
sr.setSource(si.getData)
sr.setDelay(0.001)
sr.open()
sr.start()

sg = SniperGraph()
sg.tree = sr.tree     #connect tree with graph
sg.xField = "seqTime"
sg.yField = "value"
sg.draw()



