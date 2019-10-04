#
# Simple BLE device example #1, digital input
# =============================================
#
# This client script will report when a remote switch is opened or closed.
# The switch is connected to a pin on the BLE module.
# The pin on the BLE module is named P1_2 (pin 13 on RN4870, pin 3 on the RN4871)
#
# The service and characteristic definition for the server (BLE device):
#
#    PS,59c88760536411e7b114b2f933d5fe66
#    PC,59c889e0536411e7b114b2f933d5fe66,10,01
#
# The script for the server (BLE device):
#
#    @PW_ON
#    SW,0A,09
#    @PIO1H
#    SHW,0072,01
#    @PIO1L
#    SHW,0072,00
#
# The characteristic handle (72 in the example above) must match the handle created for the service.
#

import time
from bluetooth.ble import GATTRequester

#
# Derive our own requester with one addition; a custom notification method.
#
class MyRequester(GATTRequester):
    def on_notification(self, handle, data):
        print("- notification on handle: {}\n".format(handle))
        for b in data:
            print(hex(ord(b)),)
        print("")

#
# the MAC address of the BLE device.  Replace 'D8:80:39:FC:7B:F5' with the address of your device.
#
grq = MyRequester('D8:80:39:FC:7B:F5', False)

grq.connect()
print("Waiting to connect...")
while not grq.is_connected():
    time.sleep(1)
print("Connected.")

characteristics = grq.discover_characteristics()

#
# the UUID of the service characteristic on the BLE device.
#
switch_uuid = '59c889e0-5364-11e7-b114-b2f933d5fe66'

# find the handle for the characteristic.
vh_switch = None
for c12c in characteristics:
    if c12c['uuid'] == switch_uuid:
        vh_switch = c12c['value_handle']
        print("Characteristic value handle is %d." % vh_switch)
        break
assert(vh_switch is not None)

print("Enabling notifications...")
# The characteristic properties are used to activate notifications.
# The characteristic property handle is one greater than
# the characteristic value handle.
ph_switch = vh_switch + 1
grq.write_by_handle(ph_switch, str(bytearray([01, 00])))

# Just sleep.  Notifications are handled above in 'on_notification'.
print("Waiting for notifications now. Press ctrl-c to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDisconnecting...")
    grq.disconnect()
    print("Done.")


