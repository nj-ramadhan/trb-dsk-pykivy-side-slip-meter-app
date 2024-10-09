import win32com.client

wmi = win32com.client.GetObject ("winmgmts:")
for usb in wmi.InstancesOf ("Win32_USBHub"):
    print(usb.DeviceID)



import usb.core
from usb.backend import libusb1
import libusb_package

backend = libusb1.get_backend(find_library=libusb_package.find_library)

vendor_id = 0x04F2
product_id = 0xB6A8

dev = usb.core.find(
            idVendor=vendor_id,
            idProduct=product_id,
            backend=backend,
        )

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
# dev.set_configuration()

# get an endpoint instance
# cfg = dev.get_active_configuration()
# intf = cfg[(0,0)]

# ep = usb.util.find_descriptor(
#     intf,
#     # match the first OUT endpoint
#     custom_match = lambda e: 
#         usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

# assert ep is not None

# write the data
# ep.write('test')

print(dev)

# import usb.core
# import usb.util


# dev = usb.core.find(idVendor=0x04F2, idProduct=0xB6A8)

# while True:
#     ret = dev.read(0x81, 0x40)
#     print(ret)