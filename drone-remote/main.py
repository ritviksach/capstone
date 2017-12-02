from xinput import XInputJoystick
from Tkinter import Tk
from gui import ControllerGUI
from drone_video import VideoThread
from xinput import *
import time
import sys

root = Tk()
controllerGUI = ControllerGUI(root)

joystick = XInputJoystick(0)

@joystick.event
def on_button(button, pressed):
    #print('button', button, pressed)
    # LT
    if button == 9 and pressed == 1:
        controllerGUI.connectDrone()
    # RT
    if button == 10 and pressed == 1:
        controllerGUI.disconnectDrone()
    # X
    if button == 15 and pressed == 1:
        controllerGUI.disconnectDrone()
        print "**** Exiting ****"
        time.sleep(0.5)
        sys.exit(0)
    
    # A
    if button == 13 and pressed == 1:
        controllerGUI.toggleFlightMode("hover")
        
    # B
    if button == 14 and pressed == 1:
        controllerGUI.toggleFlightMode("stable")
        
controllerGUI.listenController(root, joystick)
root.mainloop()