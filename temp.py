import serial
def getCarboneDioxide():
    with serial.Serial ("/dev/ttyAMA0", 9600, timeout = 2) as ser:
        send = bytearray([0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x79])
        ser.write(send)
        takestr = ser.read(9)
        print (takestr)
        return int((takestr[2]*256+takestr[3]))
print(getCarboneDioxide())