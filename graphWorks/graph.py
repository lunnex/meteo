import sqlite3
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def corrStr(s):
    s = s.replace('"', '')
    s = s.replace('(', '')
    s = s.replace(')', '')
    s = s.replace(',', '')
    s = s.replace("'", '')
    s = s.replace("[", '')
    s = s.replace("]", '')
    return s

def getPicCD(year, month, day):
    connection = sqlite3.connect(os.path.abspath("meteo.db"))
    #print(os.path.abspath("meteo.db"))
    cursor = connection.cursor()
    masfloat = []
    masdaynum = []
    x = []
    y = []

    cursor.execute('select carbon_dioxide from data where day = (?) and month = (?) and year = (?)', [day, month, year])
    s = str(cursor.fetchall())
    s = corrStr(s)
    masstr = (s.split(' '))

    cursor.execute('select hour*3600+minute*60+second from data where day = (?) and month = (?) and year = (?)', [day, month, year])
    daynum = str(cursor.fetchall())
    daynum = corrStr(daynum)
    masdaynum = (daynum.split(' '))

    for i in range (0, len(masstr)):
        masfloat.insert(i,float(masstr[i]))
        y.insert(i, int (masdaynum[i]))
        
    for i in range (1, len(masstr)):
        masdaynum[0] = 0
        x.insert(i, int (masdaynum[i]))

    field = plt.figure()
    ax = plt.subplot()
    ax.plot(y, masfloat, color = "red")
    #plt.show()
    plt.savefig('pic')


def getPicTemp(year, month, day):
    connection = sqlite3.connect(os.path.abspath("meteo.db"))
    #print(os.path.abspath("meteo.db"))
    cursor = connection.cursor()
    masfloat = []
    masdaynum = []
    x = []
    y = []

    cursor.execute('select temperature from data where day = (?) and month = (?) and year = (?)', [day, month, year])
    s = str(cursor.fetchall())
    s = corrStr(s)
    masstr = (s.split(' '))

    cursor.execute('select hour*3600+minute*60+second from data where day = (?) and month = (?) and year = (?)',
                   [day, month, year])
    daynum = str(cursor.fetchall())
    daynum = corrStr(daynum)
    masdaynum = (daynum.split(' '))

    for i in range(0, len(masstr)):
        masfloat.insert(i, float(masstr[i]))
        y.insert(i, int(masdaynum[i]))

    for i in range(1, len(masstr)):
        masdaynum[0] = 0
        x.insert(i, int(masdaynum[i]))

    field = plt.figure()
    ax = plt.subplot()
    ax.plot(y, masfloat, color = "green")
    # plt.show()
    plt.savefig('pic')


def getPicHum(year, month, day):
    connection = sqlite3.connect(os.path.abspath("meteo.db"))
    #print(os.path.abspath("meteo.db"))
    cursor = connection.cursor()
    masfloat = []
    masdaynum = []
    x = []
    y = []

    cursor.execute('select humidity from data where day = (?) and month = (?) and year = (?)', [day, month, year])
    s = str(cursor.fetchall())
    s = corrStr(s)
    masstr = (s.split(' '))

    cursor.execute('select hour*3600+minute*60+second from data where day = (?) and month = (?) and year = (?)',
                   [day, month, year])
    daynum = str(cursor.fetchall())
    daynum = corrStr(daynum)
    masdaynum = (daynum.split(' '))

    for i in range(0, len(masstr)):
        masfloat.insert(i, float(masstr[i]))
        y.insert(i, int(masdaynum[i]))

    for i in range(1, len(masstr)):
        masdaynum[0] = 0
        x.insert(i, int(masdaynum[i]))

    field = plt.figure()
    ax = plt.subplot()
    ax.plot(y, masfloat, color = "blue")
    # plt.show()
    plt.savefig('pic')


def getPicPres(year, month, day):
    connection = sqlite3.connect(os.path.abspath("meteo.db"))
    #print(os.path.abspath("meteo.db"))
    cursor = connection.cursor()
    masfloat = []
    masdaynum = []
    x = []
    y = []

    cursor.execute('select pressure from data where day = (?) and month = (?) and year = (?)', [day, month, year])
    s = str(cursor.fetchall())
    s = corrStr(s)
    masstr = (s.split(' '))

    cursor.execute('select hour*3600+minute*60+second from data where day = (?) and month = (?) and year = (?)',
                   [day, month, year])
    daynum = str(cursor.fetchall())
    daynum = corrStr(daynum)
    masdaynum = (daynum.split(' '))

    for i in range(0, len(masstr)):
        masfloat.insert(i, float(masstr[i]))
        y.insert(i, int(masdaynum[i]))

    for i in range(1, len(masstr)):
        masdaynum[0] = 0
        x.insert(i, int(masdaynum[i]))

    field = plt.figure()
    ax = plt.subplot()
    ax.plot(y, masfloat, color = "yellow")
    # plt.show()
    plt.savefig('pic')

