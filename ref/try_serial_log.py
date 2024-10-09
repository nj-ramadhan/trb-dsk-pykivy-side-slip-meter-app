import serial
import time

ser = serial.Serial()
ser.baudrate = 115200
ser.port = "COM9"
parity=serial.PARITY_NONE,
# parity=serial.PARITY_EVEN,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS
# bytesize=serial.SEVENBITS
ser.open()

# cw = b'0xaa,0xf4'
# ser.write(serial.to_bytes(cw))
# print(cw)
# time.sleep(1)

# cw = [0xaa,0xf4]
# ser.write(serial.to_bytes(cw))
# print(cw)
# time.sleep(1)


# cw = b'\xaa\xf4'
# ser.write(serial.to_bytes(cw))
# print(cw)

# n = ser.write(b'\xaa\xf4')
# n += ser.write(bytes([2]))
# n += ser.write(bytes([3]))
# print("bytes written ", n)


# while(1):
# byte_read = []
# byte_read = ser.readline()
# print(byte_read)

# byte_read = ser.read().decode("ascii")
# byte_read = ser.read(13).hex()
byte_read = ser.read(29)
# byte_read = ser.readline()
print(byte_read)

# for i in range(7):
#     byte_read = ser.read(30)
#     hex_read = byte_read.hex()
#     byte_read = ser.readline
    
#     # ascii_read = byte_read.decode("ascii")
#     # utf8_read = byte_read.decode("utf8")
#     file = open('serial_log.txt',"a",)
#     file.write('hex:'+str(hex_read)+'\n'+'byt:'+str(byte_read)+'\n')
#     # byte_read += ser.read(1)
#     # print(byte_read.decode("utf-8"))
#     print(byte_read)

ser.close()


#0    = b'\x00\x00\x00\x00x\x00\x07\xc0\x00\x00\x80x\x00\x80x\x00\xc0\x00\x80'
#100  = b'\x00\x00\x00\x00x\x00\x07\xc0\x00\x00\x80x\x00\x80x\x00x\xc0\x00\x00'
#30.7 = b'\x00\x00\x00\x00x\x00\x07\xc0\x00\x00\x80x\x00\x80x\x00\xf8\x00\x00\xf8\x00x\x00\x00\x80\xf8\x00\x00\x00'
#30.8 = b'\x00\x00\x00\x00x\x00\x07\xc0\x00\x00\x80x\x00\x80x\x00x\xf8\x00\x00\x00\x00x\x00x\xc0\x80\xf8\x00\x00\x00'
#31.1 = b'\x00\x00\x00\x00x\x00\x07\xc0\x00\x00\x80x\x00\x80x\x00x\xf8\x00\x00\x00\x00x\x00x\xc0\x80\xf8\x00\x00\x00'
#29.9 = b'\x00\x00\x00\x00x\x00\x07\xc0\x00\x00\x80x\x00\x80x\x00\x80\x00x\xc0\x00x\xc0\x00x\x00\x80\x80x\xfc'