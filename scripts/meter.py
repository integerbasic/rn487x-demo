#
# Simple BLE device example #3, analog input
# =============================================
#
# This client script will read an analog signal collected by the remote device.
# The signal on the BLE module is named P1_2 (pin 13 on RN4870, pin 3 on the RN4871)
#
# The service and characteristic definition for the server (BLE device):
#
#    PS,59c88760536411e7b114b2f933d5fe66
#    PC,59c889e0536411e7b114b2f933d5fe66,02,02
#
# The script for the server (BLE device):
#
#    @CONN
#    SM,2,0010
#    @DISCON
#    SM,2,0000
#    @TMR2
#    $VAR1=@,2
#    SHW,0072,$VAR1
#    SM,2,0010
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
sample_uuid = '59c889e0-5364-11e7-b114-b2f933d5fe66'

# find the handle for the characteristic.
vh_sample = None
for c12c in characteristics:
    if c12c['uuid'] == sample_uuid:
        vh_sample = c12c['value_handle']
        print("Characteristic value handle is %d." % vh_sample)
        break
assert(vh_sample is not None)

# use the handle to read the signal value, at a one-second interval
print("Press ctrl-c to stop.")
try:
    while True:
        data = grq.read_by_handle(vh_sample)[0]
        print("bytes received:",)
        for b in data:
            print(hex(ord(b)),)
        print("")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDisconnecting...")
    grq.disconnect()
    print("Done.")


