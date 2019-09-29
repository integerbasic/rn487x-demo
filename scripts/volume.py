#
# Simple BLE device example #2, analog control
# =============================================
#
# This client script will vary the brightness of a remote LED over a continuous range.
# The LED control signal on the BLE module is named P2_3 (pin 9 on RN4870)
#
# The service and characteristic definition for the server (BLE device):
#
#    PS,59c88760536411e7b114b2f933d5fe66
#    PC,59c889e0536411e7b114b2f933d5fe66,08,14
#
# The script for the server (BLE device):
#
#    @PW_ON
#    %0072=?FUNC1
#    ?FUNC1
#    [,2,2,$PM1,$PM2
# 
# The characteristic handle (72 in the example above) must match the handle created for the service.
#

import time
from bluetooth.ble import GATTRequester

#
# the MAC address of the BLE device.  Replace 'D8:80:39:FC:7B:F5' with the address of your device.
#
grq = GATTRequester('D8:80:39:FC:7B:F5', False)

grq.connect()
print("Waiting to connect...")
while not grq.is_connected():
    time.sleep(1)
print("Connected.")

characteristics = grq.discover_characteristics()

#
# the UUID of the service characteristic on the BLE device.
#
light_ctrl_uuid = '59c889e0-5364-11e7-b114-b2f933d5fe66'

# find the handle for the characteristic.
vh_light = None
for c12c in characteristics:
    if c12c['uuid'] == light_ctrl_uuid:
        vh_light = c12c['value_handle']
        print("Characteristic value handle is %d." % vh_light)
        break
assert(vh_light is not None)

# Use the handle to set the LED brightness to a specific intensity,
# one command every 10 microseconds.  The data sent to the characteristic
# is a UTF-8 string that describes a pair of four-byte hexadecimal numbers.
# These two numbers specify the on-off intervals of a PWM signal to the LED.
#
# The full range for each number is 65536 (2^16), but we are
# only altering one number, and only using an 8-bit range for it.
# The first number is fixed at '00ff'.
# The second number is ranging up and down like so:
#
# 0000,0010,0020...00dc,00e6,00f0,00fa,00f0,00e6,00dc...0020,0010,0000 (repeat)
print("Fading remote LED now. Press ctrl-c to stop.")
fade_in_out = range(0,255,10) + range(255,0,-10)
try:
    while True:
        for vol in fade_in_out:
            str_vol="%02x"%vol
            grq.write_by_handle(vh_light, '00ff,00' + str_vol)
            time.sleep(.01)
except KeyboardInterrupt:
    grq.write_by_handle(vh_light, '00ff,0000')
    print("\nDisconnecting...")
    grq.disconnect()
    print("Done.")


