import sqlite3
import os
import smbus2
import bme280

def getAbsPathOfMeteo():
    return(os.path.abspath("meteo.db"))

def getLastMeteo():
    port = 1
    address = 0x76
    bus = smbus2.SMBus(port)

    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)
    
    connection = sqlite3.connect(getAbsPathOfMeteo())
    cursor = connection.cursor()
    
    cursor.execute("select id ,hour, minute, second, carbon_dioxide from data where id >= ( select max(id) from data)")
    out = cursor.fetchone()
    msg = 'No. ' + str(out[0]) + '   ' + str(out[1]) + ':' + str(out[2]) + ':' + str(out[3]) + '   ' + str(out[4]) + ' ppm' + '\n' + str(round(data.temperature,3)) + ' °C  ' + str(round(data.pressure,3)) + ' hPa ' + str(round(data.humidity,3)) + ' %' 
    return (msg)

def getMeteo():
    connection = sqlite3.connect(getAbsPathOfMeteo())
    cursor = connection.cursor()
    
    cursor.execute('select id, year, month, day, hour, minute, second, carbon_dioxide, temperature, humidity, pressure from data where id >= ( select max(id) from data)')
    out = cursor.fetchone()
    msg = 'Номер измерения: ' + str(out[0]) + '\n' + 'Дата и время измерения: ' + str(out[1]) + "/" + str(out[2])\
    + "/" + str(out[3]) + " " + str(out[4]) + ":" + str(out[5]) + ":" + str(out[6]) + "\n" + "Содержание углекислого газа: " + str(out[7]) + "ppm" + '\n' +\
    "Температура: " + str(out[8]) + ' °C' + '\n' + "Влажность: " + str(out[9]) + ' %' +'\n' + "Давление: " + str(out[10]) + ' hPa'
    return (msg)
