from escpos.printer import Usb
import win32com.client
import usb.core
from usb.backend import libusb1
import libusb_package
import numpy as np

""" Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
# wmi = win32com.client.GetObject ("winmgmts:")
# for usb in wmi.InstancesOf ("Win32_USBHub"):
#     print(usb.DeviceID)
# backend = libusb1.get_backend(find_library=libusb_package.find_library)
# # p = Usb(0x04b8, 0x0e27, 0, profile="TM-T88II")
# p = Usb(0x04b8, 0x0e27, 0)
# p.text("Hello World\n")
# p.image("logo.gif")
# p.barcode('4006381333931', 'EAN13', 64, 2, '', '')
# p.cut()


from escpos.printer import Serial

dt_no_antrian = "0001"
dt_no_reg = "12121212"
dt_no_uji = "12345678"
dt_nama = "Husna"
dt_jenis_kendaraan = "Kendaraan Bak Terbuka"
dt_slm_flag = "Lulus"
dt_slm_value = "98.99"

""" 9600 Baud, 8N1, Flow Control Enabled """
printer = Serial(devfile='COM10',
           baudrate=38400,
           bytesize=8,
           parity='N',
           stopbits=1,
           timeout=1.00,
           dsrdtr=True)

# p.text("Hello World\n")
# p.qr("You can readme from your smartphone")
# p.cut()

printer.image("asset/logo-small-print.png")
printer.textln(" \n ")
printer.textln("HASIL UJI KEBISINGAN")
printer.textln("SOUND LEVEL METER / SLM")
printer.textln("================================================================")
printer.text(f"No Antrian: {dt_no_antrian}\t")
printer.text(f"No Reg: {dt_no_reg}\t")
printer.textln(f"No Uji: {dt_no_uji}")
printer.textln("  ")
printer.text(f"Nama: {dt_nama}\t")
printer.textln(f"Jenis Kendaraan: {dt_jenis_kendaraan}")
printer.textln("  ")
printer.textln(f"Status: {dt_slm_flag}")
printer.textln(f"Nilai: {str(np.round(dt_slm_value, 2))}")
printer.textln("================================================================")
printer.cut()


