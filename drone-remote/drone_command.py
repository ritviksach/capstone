#!/usr/bin/env python
from __future__ import division
import threading
import sys
import time
import socket

class CommandThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        self.FPS = 35
        self.data = bytearray(18)
        self.baseValues()
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 0)
        self.s.settimeout(1)
        
        self.stopFlag = threading.Event()
        
        try:
            self.s.connect(("192.168.10.1", 2001))
        except Exception, e:
            if ("%s"%e).find("timed out") == 0:
                print "[Socket Connection Timeout] (Re)Connect to Walkera WiFi network..."
            else:
                print e
            sys.stdout.flush()
            self.s = None
            return
        
        self.s.setblocking(0)
        print "****** Connected to Drone, Thread Initialized ******"
        sys.stdout.flush()
        
    def baseValues(self):
        self.switch    = 0x61    # 97
        self.throttle  = 0x02bc  # 700
        self.elev      = 0x044c  # 1100
        self.aile      = 0x044c  # 1100
        self.rotation  = 0x044c  # 1100
        
        self.updateData()
    
    def getBaseValues(self):
        self.baseValues()
        return (self.throttle, self.rotation, self.elev, self.aile)
    
    def updateData(self):
        self.data[0]  = self.switch;
        self.data[1]  = self.throttle >> 8
        self.data[2]  = self.throttle & 0xff
        self.data[3]  = self.rotation >> 8 # yaw
        self.data[4]  = self.rotation & 0xff
        self.data[5]  = self.elev >> 8 #pitch
        self.data[6]  = self.elev & 0xff
        self.data[7]  = self.aile >> 8 # roll
        self.data[8]  = self.aile & 0xff
        self.data[9]  = self.aile >> 8
        self.data[10] = self.aile & 0xff
        self.data[11] = self.throttle >> 8
        self.data[12] = self.throttle & 0xff
        self.data[13] = self.rotation >> 8
        self.data[14] = self.rotation & 0xff
        self.data[15] = self.elev >> 8
        self.data[16] = self.elev & 0xff
        self.data[17] = sum(self.data[0:17]) & 0xff #checksum
        
    def setControlValues(self, throttle=0.0, rotation=0.0, elev=0.0, aile=0.0):
        self.throttle   = (int((1 - throttle) * ((0x05dc-0x02bf)>>1)) + 0x02bf)
        self.rotation   = (int((1 - rotation) * ((0x0640-0x025b)>>1)) + 0x025b)
        self.elev       = (int((1 - elev)   * ((0x0640-0x025b)>>1)) + 0x025b)
        self.aile       = (int((1 - aile)  * ((0x0640-0x025b)>>1)) + 0x025b)
        
    def run(self):
        self.baseValues()
        
        if self.s is not None:
            self.s.send(self.data)
        
        while not self.stopFlag.is_set():
            self.updateData()
            self.s.send(self.data)
            time.sleep( 1.0 / self.FPS )
            
        print "****** Stopping control thread ******"
        sys.stdout.flush()
        
        self.baseValues()
        self.s.send(self.data)
        time.sleep(0.03)
        self.s.close()
        
    def shutdown(self):
        self.stopFlag.set()
        
    def sleep(self):
        pass
    def wake(self):
        pass
    def reset(self):
        pass