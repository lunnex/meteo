import serial
import os
import sqlite3
import datetime
import time
import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

def getDBpath():
    return (os.path.abspath('meteo.db'))

def getCarboneDioxide():
    with serial.Serial ("/dev/ttyAMA0", 9600, timeout = 2) as ser:
        send = bytearray([0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x79])
        ser.write(send)
        takestr = ser.read(9)
        #print (int((takestr[2]*256+takestr[3])))
        return int((takestr[2]*256+takestr[3]))

def getBMEInfo():
   data = bme280.sample(bus, address, calibration_params)
   return data

    
def putDataIntoDB():
    connection = sqlite3.connect(getDBpath())
    cursor = connection.cursor()
    data = getBMEInfo()
    
    now = datetime.datetime.now()
    
    cursor.execute(f'insert into data (year, month, day, hour, minute, second, carbon_dioxide, temperature, humidity, pressure) values (?,?,?,?,?,?,?,?,?,?)',\
    (now.year, now.month, now.day, now.hour, now.minute, now.second, getCarboneDioxide(), round(data.temperature, 2), round(data.humidity, 2), round(data.pressure, 2)))
    connection.commit()
    connection.close()

def insideHome():
    while True:
        try:
            putDataIntoDB()
        except Exception as exception:
            print (exception)
        time.sleep(10)
