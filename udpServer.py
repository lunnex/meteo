import socket
import os
import sqlite3
import datetime
import time
from dbWorks import getMessage

UDP_IP = 'localhost'
UDP_PORT = 9000
addr = (UDP_IP, UDP_PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP) # UDP
sock.setblocking(0)
sock.bind(('', UDP_PORT))

def makeTable():
    connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
    cursor = connection.cursor()
    
    cursor.execute("create table dataOutside(id integer primary key, year integer not null, month integer not null, day integer not null, hour integer not null, minute integer not null, second not null not null, temperature real, humidity real, pressure real)")
    connection.commit()
    connection.close()

def udpGet():
    while True:
        try:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            dataStr = data.decode("utf-8")
            dataArr = dataStr.split(':')
            
            connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
            cursor = connection.cursor()
            
            now = datetime.datetime.now()
            try:
                cursor.execute(f'insert into dataOutside (year, month, day, hour, minute, second, temperature, humidity, pressure) values (?,?,?,?,?,?,?,?,?)',\
                (now.year, now.month, now.day, now.hour, now.minute, now.second, dataArr[0], dataArr[1], dataArr[2]))
                connection.commit()
                connection.close()
            except sqlite3.DatabaseError:
                makeTable()
                
        except:
            pass
#udpGet()