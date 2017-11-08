from inputs import devices, get_gamepad, DeviceManager
import pprint
from xinput import *

"""
Grab 1st available gamepad, logging changes to the screen.
L & R analogue triggers set the vibration motor speed.
"""
joysticks = XInputJoystick.enumerate_devices()
device_numbers = list(map(attrgetter('device_number'), joysticks))

print('found %d devices: %s' % (len(joysticks), device_numbers))

if not joysticks:
    sys.exit(0)

j = joysticks[0]
print('using %d' % j.device_number)

battery = j.get_battery_information()
print(battery)

@j.event
def on_button(button, pressed):
    print('button', button, pressed)

left_speed = 0
right_speed = 0

@j.event
def on_axis(axis, value):
    left_speed = 0
    right_speed = 0

    print('axis', axis, value)
    if axis == "left_trigger":
        left_speed = value
    elif axis == "right_trigger":
        right_speed = value
    j.set_vibration(left_speed, right_speed)

while True:
    j.dispatch_events()
    time.sleep(.01)