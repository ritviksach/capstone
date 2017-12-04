#!/usr/bin/env python

import threading
import sys
import time
import socket
import urllib2
import cv2
import imutils
import numpy as np
import datetime
from PIL import Image, ImageTk

class VideoThread(threading.Thread):
    def __init__(self, video):
        threading.Thread.__init__(self)
        self.video = video
        self.exit = threading.Event()
        self.sleeping = threading.Event()
        
        self.password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        self.baseUrl = "http://192.168.10.1:8080"
        self.videoUrl = self.baseUrl + "/?action=stream"
        
    def run(self):
        buffer = ""
        self.state = 0
        self.password_manager.add_password(None, self.baseUrl, 'admin', 'admin123')
        self.handler = urllib2.HTTPBasicAuthHandler(self.password_manager)
        self.opener = urllib2.build_opener(self.handler)
        try:
            self.opener.open(self.videoUrl)
            urllib2.install_opener(self.opener)
            self.resp = urllib2.urlopen(self.videoUrl)
        except Exception, e:
            print "Got an error opening Walkera Stream", e
            sys.stdout.flush()
            self.exit.set()
            time.sleep(0.1)
            
        while not self.exit.is_set():
            if self.sleeping.is_set():
                time.sleep(0.1)
                continue
            
            data = self.resp.read(4096)
            buffer += data
            
            while buffer.find("\n") != -1: # break on a new line
                line, buffer = buffer.split("\n", 1)
                if self.state == 0:
                    if line[0:20] == "--boundarydonotcross":
                        self.state = 1
                elif self.state == 1:
                    self.state = 2
                elif self.state == 2:
                    dataLength = int(line.split(":")[1][1:-1])
                    self.state = 3
                elif self.state == 3:
                    self.state = 4
                    sys.stdout.flush()
                else:
                    while(len(buffer) < dataLength):
                        bytesRemaining = dataLength - len(buffer)
                        data = self.resp.read(bytesRemaining)
                        buffer += data
                    self.state = 0
                    
                    try:
                        cvImg = cv2.imdecode(np.fromstring(buffer, np.uint8), cv2.IMREAD_COLOR)
                        vis = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(vis)
                        img = ImageTk.PhotoImage(img)
                    except Exception, e:
                        print Exception, e, "video issue"
                        sys.stdout.flush()
                        continue
                        
                    tstamp = datetime.datetime.now()
                    backup = self.video.image
                    try:
                        self.video.image = img
                        self.video.configure(image=img)
                    except Exception, e:
                        print Exception, e, "video issue 2"
                        self.video.image = backup
                        self.video.configure(image=backup)
                        continue
                        
    def isAwake(self):
        return not self.sleeping.is_set()

    def shutdown(self):
        self.exit.set()
      
    def sleep(self):
        self.sleeping.set()
      
    def wake(self):
        self.sleeping.clear()