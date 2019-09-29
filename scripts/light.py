#
# Simple BLE device example #1, digital control
# =============================================
#
# This client script will flash a remote LED on and off.
# The LED control signal on the BLE module is named P1_2 (pin 13 on RN4870, pin 3 on the RN4871)
#
# The service and characteristic definition for the server (BLE device):
#
#    PS,59c88760536411e7b114b2f933d5fe66
#    PC,59c889e0536411e7b114b2f933d5fe66,08,01
#
# The script for the server (BLE device):
#
#    @CONN
#    |O,08,%0072
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
# the UUID of the service on the BLE device.
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

# use the handle to command the LED on and off, at a one-second interval
print("Flashing remote LED now. Press ctrl-c to stop.")
try:
    while True:
        grq.write_by_handle(vh_light, str(bytearray([8])))
        time.sleep(1)
        grq.write_by_handle(vh_light, str(bytearray([0])))
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDisconnecting...")
    grq.disconnect()
    print("Done.")


