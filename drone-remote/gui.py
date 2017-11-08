from Tkinter import *
import tkMessageBox
from inputs import devices

class ControllerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Controller for Walkera drones")
        self.setWindowSize(350, 400)
        
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
        
        self.startHoverButton = Button(presetFrame, text="Start Hovering", command=self.hoverDrone, fg="blue", state=DISABLED)
        self.startHoverButton.pack(side=LEFT)
        self.stopHoverButton = Button(presetFrame, text="Stop Hovering", command=self.hoverDrone, fg="blue", state=DISABLED)
        self.stopHoverButton.pack(side=LEFT)
        
        
    def connectDrone(self):
        self.statusVar.set("STATUS: Connected")
        self.connectButton['state'] = DISABLED
        self.disconnectButton['state'] = ACTIVE
        self.startHoverButton['state'], self.stopHoverButton['state'] = ACTIVE, ACTIVE
        
    def disconnectDrone(self):
        self.statusVar.set("STATUS: Disconnected")
        self.disconnectButton['state'] = DISABLED
        self.connectButton['state'] = ACTIVE
        self.startHoverButton['state'], self.stopHoverButton['state'] = DISABLED, DISABLED
        
    def hoverDrone(self):
        self.statusVar.set("Status: Hovering, connected")
        
    def setWindowSize(self, x, y):
        self.master.geometry('{}x{}'.format(x, y))


    def addScales(self, parent):
        throttle_scale = self.addScale(parent, "Throttle", self.throttleVal, HORIZONTAL, 700, 1500)
        rotation_scale = self.addScale(parent, "Rotation", self.rotationVal, HORIZONTAL, 600, 1600)

        elev_scale = self.addScale(parent, "Elevation", self.elevVal, HORIZONTAL, 600, 1600)
        aile_scale = self.addScale(parent, "Aile", self.aileVal, HORIZONTAL, 600, 1600)
        
    
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