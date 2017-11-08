from drone_command import CommandThread
import sys
from xinput import XInputJoystick
import time

# l_thumb_x -> aile
# l_thumb_y -> elev
# r_thumb_x -> rotation
# r_thumb_y -> throttle

if __name__ == '__main__':
    controller = CommandThread()
    joystick = XInputJoystick(0)
    
    
    
    @joystick.event
    def on_button(button, pressed):
        print('button', button, pressed)
        controller.shutdown()

    left_speed = 0
    right_speed = 0

    @joystick.event
    def on_axis(axis, value):
        updateVals = False
        if   axis == "r_thumb_y":
            joystick.throttle = value
            updateVals = True
        elif axis == "r_thumb_x":
            joystick.rotation = value
            updateVals = True
        elif axis == "l_thumb_y":
            joystick.elev = value
            updateVals = True
        elif axis == "l_thumb_x":
            joystick.aile = value
            updateVals = True
            
        if updateVals:
            controller.setControlValues(joystick.throttle, joystick.rotation, joystick.elev, joystick.aile)
        
        left_speed = 0
        right_speed = 0

        print('axis', axis, value)
        if axis == "left_trigger":
            left_speed = value
        elif axis == "right_trigger":
            right_speed = value
        joystick.set_vibration(left_speed, right_speed)

    controller.start()
    while True:
        joystick.dispatch_events()
        time.sleep(.01)
    