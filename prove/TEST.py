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

# Choose speed: 'fast' (1.0 GSa/sec) or 'slow' (0.4 GSa/sec)
speed = 'slow'
#speed = 'fast'
trigger = 'software'

# Open eval board
board = target.T5EvalBoard()
board.Open("0.0.0.0", 8106, "192.168.0.173", 8105)
board.SetTimeOut(1000) # 1 sec



board.EnableExternalTrigger(True)
board.Close()


localIP = ("0.0.0.0",8106)
boardIP = ("192.168.0.173",8105) 
si = SniperInterface(localIP,boardIP)
si.open()
si.setTimeout(10)
si.enableTrigger("ex")
si.close()
