from __future__ import division
from Tkinter import *
from PIL import Image, ImageTk
import tkMessageBox
import multiprocessing
import Queue
import datetime
import cv2
import imutils
import os
from xinput import XInputJoystick
from drone_command import CommandThread
from drone_video   import VideoThread
from drone_flight_presets import FlightModePresets as FMP
from gps import GPS
from ADSB.ADSB_lib import ADSB_SDR_Thread, ADSB_MSG
import threading


class ControllerGUI(threading.Thread):
    def __init__(self, master, interface):
        threading.Thread.__init__(self)
        self.master = master
        master.title("Controller for Walkera drones")
        self.setWindowSize(350, 600)
        
        self.GPS = GPS(0, 0, 1) # lat, lng, caution distance in metres
        self.SDR_RECV = ADSB_SDR_Thread("recv", interface)
        self.SDR_SEND = ADSB_SDR_Thread("send", interface)
        self.flightModePresets = FMP()
        self.commander = None
        self.video = None
        self.flightMode = None
        
        self.evadingObject = None # Signifies whether performing evasive movements or not
        
        self.throttleVal = IntVar()
        self.rotationVal = IntVar()
        self.elevVal = IntVar()
        self.aileVal = IntVar()
        self.statusVar = StringVar()
        
        self.statusVar.set("STATUS: Disconnected")
        
        main_panel = PanedWindow(self.master)
        main_panel.pack(fill=BOTH, expand=1)

        statusStrLabel = Label(main_panel, textvariable= self.statusVar)
        statusStrLabel.pack()
        
        self.addScales(main_panel)
        
        buttonFrame = Frame(main_panel)
        buttonFrame.pack()
        
        self.connectButton = Button(buttonFrame, text="Connect", command=self.connectDrone, fg="green")
        self.disconnectButton = Button(buttonFrame, text="Disconnect", command=self.disconnectDrone, fg="red", state=DISABLED)
        
        self.connectButton.pack(side = LEFT)
        self.disconnectButton.pack(side = LEFT)
        
        presetFrame = Frame(main_panel)
        presetFrame.pack()
                
        self.videoImage = Label(presetFrame, width=352, height=288)
        self.videoImage.pack(side=BOTTOM, padx=10, pady=10)
        
    def createThreads(self):
        self.video = VideoThread(self.videoImage)
        self.commander = CommandThread()
        
    def destroyThreads(self):
        self.video = None
        self.commander = None
        
    def connectDrone(self):
        self.createThreads()
        
        self.statusVar.set("STATUS: Connected")
        self.connectButton['state'] = DISABLED
        self.disconnectButton['state'] = ACTIVE
        
        self.video.start()
        self.commander.start()
        
    def disconnectDrone(self):
        if self.video is not None:
            self.video.shutdown()
        
        if self.commander is not None:
            self.commander.shutdown()
        
        self.statusVar.set("STATUS: Disconnected")
        self.disconnectButton['state'] = DISABLED
        self.connectButton['state'] = ACTIVE
        
        self.destroyThreads()
        
    def hoverDrone(self):
        self.statusVar.set("Status: Hovering, connected")
        
    def setWindowSize(self, x, y):
        self.master.geometry('{}x{}'.format(x, y))


    def addScales(self, parent):
        self.throttle_scale = self.addScale(parent, "Throttle", self.throttleVal, HORIZONTAL, 700, 1500)
        self.rotation_scale = self.addScale(parent, "Rotation", self.rotationVal, HORIZONTAL, 600, 1600)

        self.elev_scale = self.addScale(parent, "Elevation", self.elevVal, HORIZONTAL, 600, 1600)
        self.aile_scale = self.addScale(parent, "Aile", self.aileVal, HORIZONTAL, 600, 1600)
        
    
    def addScale(self, parent, scale_label, scale_variable, orientation, range_from, range_to):
        newScale = Scale(parent, 
                         label=scale_label, 
                         variable=scale_variable, 
                         orient=orientation, 
                         from_=range_from, 
                         to_=range_to,
                         length=350)
        newScale.pack(anchor=CENTER)

        return newScale
    
    def listenController(self, root, joystick):
        joystick.dispatch_events() # for buttons
        current_state = joystick.get_translated_state()
        
        # If any flight mode is activated
        # Apply preset values over current values
        if self.flightMode is not None:
            current_state = self.applyFlightMode(self.flightMode, current_state)
        
        # Get all nearby valid ADS-B messages/locations
        '''
            COLLISION AVOIDANCE SYSTEM
        '''
        objectLocations = self.SDR_RECV.getPositionStream() # Returns a list of tuples of lat lng altitude timestamp [(lat1, lng1..), (lat2, lng2..)...]
        for objectLocation in objectLocations:
            lat, lng, icao, altitude, timestamp = objectLocation
            
            isAlert = self.GPS.alert(lat, lng)
            
            if isAlert and not self.evadingObject:
                self.flightModePresets.reset()
                print "*** Collision detection activated, taking over controls! ***"
                sys.stdout.flush()
                self.evadingObject = icao
                current_state = self.applyFlightMode("evasiveManeuver", current_state, None)
            elif isAlert and self.evadingObject == icao:
                current_state = self.applyFlightMode("evasiveManeuver", current_state, None) # Stay in evasive mode
            elif self.evadingObject == icao and not isAlert:
                print "*** Collision avoided! Slowly giving control back ***"
                current_state = self.applyFlightMode("evasiveManeuver", current_state, "stop", self.resetEvading)
            
        
        self.updateScales(current_state) # Updates GUI
        # Send updated values to drone!
        if self.commander is not None:
            self.updateDrone(current_state)
            
        # Target FPS for input = 40, 1000 / 40 == 25
        root.after(25, self.listenController, root, joystick)
        
    def updateDrone(self, current_state):
        scaledThrottle, scaledRotation, scaledElev, scaledAile = self.scaleValues(current_state)

        throttle = self.scale(current_state["r_thumb_y"], [-0.50, 0.50], [-1, 1])
        # Throttle is reversed i.e. pulling it down should be the lowest value
        throttle = 0 - throttle
        self.commander.setControlValues(
            throttle,
            self.scale(current_state["r_thumb_x"], [-0.50, 0.50], [-1, 1]),
            self.scale(current_state["l_thumb_y"], [-0.50, 0.50], [-1, 1]),
            self.scale(current_state["l_thumb_x"], [-0.50, 0.50], [-1, 1])
        )
    
    def applyFlightMode(self, flightMode, current_state):
        throttle, rotation, elev, aile = self.flightModePresets.getValues(flightMode)
        if throttle is not None:
            current_state["r_thumb_y"] = self.scale(throttle, [700, 1500], [-0.50, 0.50])
        if rotation is not None:
            current_state["r_thumb_x"] = self.scale(rotation, [600, 1600], [-0.50, 0.50])
        if elev is not None:
            current_state["l_thumb_y"] = self.scale(elev, [600, 1600], [-0.50, 0.50])
        if aile is not None:
            current_state["l_thumb_x"] = self.scale(aile, [600, 1600], [-0.50, 0.50])

        return current_state
    
    def updateScales(self, state):
        scaledThrottle, scaledRotation, scaledElev, scaledAile = self.scaleValues(state)
        
        self.throttle_scale.set(scaledThrottle)
        self.rotation_scale.set(scaledRotation)
        self.elev_scale.set(scaledElev)
        self.aile_scale.set(scaledAile)
        
    def scaleValues(self, state):
        throttle, rotation, elev, aile = state["r_thumb_y"], state["r_thumb_x"], state["l_thumb_y"], state["l_thumb_x"] 
        if throttle == 1:
            throttle = 0
        if rotation == 1:
            rotation = 0
        if elev == 1:
            elev = 0
        if aile == 1:
            aile = 0
            
        scaledThrottle = self.scale(throttle, [-0.50, 0.50], [700, 1500])
        scaledRotation = self.scale(rotation, [-0.50, 0.50], [600, 1600])
        scaledElev = self.scale(elev, [-0.50, 0.50], [600, 1600])
        scaledAile = self.scale(aile, [-0.50, 0.50], [600, 1600])
        
        return scaledThrottle, scaledRotation, scaledElev, scaledAile
    
    def scale(self, val, src, dst):
        """
        Scale the given value from the scale of src to the scale of dst.
        """
        return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]
    
    def toggleFlightMode(self, mode):
        # Reset cycle values if applying any preset!
        self.flightModePresets.reset()
        
        if mode == self.flightMode:
            self.flightMode = None
            self.statusVar.set("STATUS: CONNECTED")
        else:
            self.statusVar.set("STATUS: " + mode + " mode")
            self.flightMode = mode
    
    def resetEvading(self):
        self.evadingObject = False