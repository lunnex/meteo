from aiogram import types
from misc import dp
from misc import bot
from dbWorks import getMessage
from graphWorks import graph
import datetime
import time
import sqlite3
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import matplotlib.pyplot as plt

buttonGetInfo = KeyboardButton("Текущее состояние")
buttonGetGraph = KeyboardButton("Получить исторические данные")
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(buttonGetInfo, buttonGetGraph)

class States(StatesGroup):
    freeState = State()
    
    changeState = State()
    yearStateCD = State()
    monthStateCD = State()
    dayStateCD = State()

    yearStateTemp = State()
    monthStateTemp = State()
    dayStateTemp = State()

    yearStateHum = State()
    monthStateHum = State()
    dayStateHum = State()

    yearStatePres = State()
    monthStatePres = State()
    dayStatePres = State()
state = ["Year", "Month", "Day"]
year = "0"
month = "0"
day = "0"

@dp.message_handler(commands=['start'])
async def startCommand (message: types.Message):
    await message.answer("Для получения информации о состоянии окружающей среды внутри квартиры, нажми на кнопку", reply_markup=keyboard)

@dp.message_handler(state = '*', text="Текущее состояние")
async def cd (message: types.Message):
    lastdata = getMessage.getMeteo()
    await message.answer (str(lastdata), reply_markup=keyboard)

@dp.message_handler(state = '*', text="Получить исторические данные")
async def getHistoricDataYearCD (message: types.Message):
    buttonTemp = KeyboardButton("Температура")
    buttonHum = KeyboardButton("Влажность")
    buttonPres = KeyboardButton("Давление")
    buttonCD = KeyboardButton("Углекислый газ")
    changeKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    changeKeyboard.add(buttonTemp, buttonHum, buttonPres, buttonCD)
    await message.answer("Выбери показатель", reply_markup=changeKeyboard)


@dp.message_handler(state = '*', text="Углекислый газ")
async def getHistoricDataYearCD (message: types.Message):
    yearKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
    cursor = connection.cursor()

    cursor.execute("select distinct year from data where carbon_dioxide is not null ")
    out = cursor.fetchone()
    for i in out:
        string = str(i).replace('(', "")
        string = string.replace(',)', '')
        button = KeyboardButton(string)
        yearKeyboard.add(button)
    await message.answer ("Введи дату, на которую хочешь получить информацию. Сейчас введи год", reply_markup = yearKeyboard)
    await States.yearStateCD.set()

@dp.message_handler(state=States.yearStateCD)
async def getHistoricDataMonthCD(message: types.Message):
    global year
    year = message.text
    monthKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
    cursor = connection.cursor()
    cursor.execute("select distinct month from data where year = (?) and carbon_dioxide is not null", [year])
    out = cursor.fetchall()
    for i in out:
        string = str(i).replace('(', "")
        string = string.replace(',)','')
        button = KeyboardButton(string)
        monthKeyboard.add(button)
    await message.answer("Теперь номер месяца", reply_markup=monthKeyboard)
    await States.monthStateCD.set()

@dp.message_handler(state=States.monthStateCD)
async def getHistoricDataDayCD(message: types.Message):
    global month
    month = message.text
    dayKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    #print(year, month)
    connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
    cursor = connection.cursor()
    cursor.execute("select distinct day from data where year = (?) and month = (?) and carbon_dioxide is not null", [year,month])
    out = cursor.fetchall()
    for i in out:
        #print (str(i))
        string = str(i).replace('(', "")
        string = string.replace(',)','')
        button = KeyboardButton(string)
        dayKeyboard.insert(button)
    await message.answer("Теперь номер дня", reply_markup=dayKeyboard)
    await States.dayStateCD.set()

@dp.message_handler(state=States.dayStateCD)
async def getHistoricDataCD(message: types.Message):

    day = message.text

    graph.getPicCD(year, month, day)

    photo=open('pic.png', 'rb')
    await bot.send_photo(message.from_user.id, photo, reply_markup=keyboard)
    photo.close()
    await States.freeState.set()
#_________________________________________________________________________________________________________________________

@dp.message_handler(state = '*', text="Температура")
async def getHistoricDataYearTemp (message: types.Message):
    yearKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
    cursor = connection.cursor()

    cursor.execute("select distinct year from data where temperature is not null ")
    out = cursor.fetchone()
    for i in out:
        string = str(i).replace('(', "")
        string = string.replace(',)', '')
        button = KeyboardButton(string)
        yearKeyboard.add(button)
    await message.answer ("Введи дату, на которую хочешь получить информацию. Сейчас введи год", reply_markup = yearKeyboard)
    await States.yearStateTemp.set()

@dp.message_handler(state=States.yearStateTemp)
async def getHistoricDataMonthTemp(message: types.Message):
    global year
    year = message.text
    monthKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
    cursor = connection.cursor()
    cursor.execute("select distinct month from data where year = (?) and temperature is not null", [year])
    out = cursor.fetchall()
    for i in out:
        string = str(i).replace('(', "")
        string = string.replace(',)','')
        button = KeyboardButton(string)
        monthKeyboard.add(button)
    await message.answer("Теперь номер месяца", reply_markup=monthKeyboard)
    await States.monthStateTemp.set()

@dp.message_handler(state=States.monthStateTemp)
async def getHistoricDataDayTemp(message: types.Message):
    global month
    month = message.text
    dayKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    #print(year, month)
    connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
    cursor = connection.cursor()
    cursor.execute("select distinct day from data where year = (?) and month = (?) and temperature is not null", [year,month])
    out = cursor.fetchall()
    for i in out:
        #print (str(i))
        string = str(i).replace('(', "")
        string = string.replace(',)','')
        button = KeyboardButton(string)
        dayKeyboard.insert(button)
    await message.answer("Теперь номер дня", reply_markup=dayKeyboard)
    await States.dayStateTemp.set()

@dp.message_handler(state=States.dayStateTemp)
async def getHistoricDataCD(message: types.Message):

    day = message.text

    graph.getPicTemp(year, month, day)

    photo=open('pic.png', 'rb')
    await bot.send_photo(message.from_user.id, photo, reply_markup=keyboard)
    photo.close()
    await States.freeState.set()

 #__________________________________________________________________________________________________________________________

@dp.message_handler(state = '*', text="Влажность")
async def getHistoricDataYearHum (message: types.Message):
    yearKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
    cursor = connection.cursor()

    cursor.execute("select distinct year from data where humidity is not null ")
    out = cursor.fetchone()
    for i in out:
        string = str(i).replace('(', "")
        string = string.replace(',)', '')
        button = KeyboardButton(string)
        yearKeyboard.add(button)
    await message.answer ("Введи дату, на которую хочешь получить информацию. Сейчас введи год", reply_markup = yearKeyboard)
    await States.yearStateHum.set()

@dp.message_handler(state=States.yearStateHum)
async def getHistoricDataMonthHum(message: types.Message):
    global year
    year = message.text
    monthKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
    cursor = connection.cursor()
    cursor.execute("select distinct month from data where year = (?) and humidity is not null", [year])
    out = cursor.fetchall()
    for i in out:
        string = str(i).replace('(', "")
        string = string.replace(',)','')
        button = KeyboardButton(string)
        monthKeyboard.add(button)
    await message.answer("Теперь номер месяца", reply_markup=monthKeyboard)
    await States.monthStateHum.set()

@dp.message_handler(state=States.monthStateHum)
async def getHistoricDataDayHum(message: types.Message):
    global month
    month = message.text
    dayKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    #print(year, month)
    connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
    cursor = connection.cursor()
    cursor.execute("select distinct day from data where year = (?) and month = (?) and humidity is not null", [year,month])
    out = cursor.fetchall()
    for i in out:
        #print (str(i))
        string = str(i).replace('(', "")
        string = string.replace(',)','')
        button = KeyboardButton(string)
        dayKeyboard.insert(button)
    await message.answer("Теперь номер дня", reply_markup=dayKeyboard)
    await States.dayStateHum.set()

@dp.message_handler(state=States.dayStateHum)
async def getHistoricDataHum(message: types.Message):

    day = message.text

    graph.getPicHum(year, month, day)

    photo=open('pic.png', 'rb')
    await bot.send_photo(message.from_user.id, photo, reply_markup=keyboard)
    photo.close()
    await States.freeState.set()

 #____________________________________________________________________________________________________________________________

@dp.message_handler(state = '*', text="Давление")
async def getHistoricDataYearPres (message: types.Message):
    yearKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
    cursor = connection.cursor()

    cursor.execute("select distinct year from data where pressure is not null ")
    out = cursor.fetchone()
    for i in out:
        string = str(i).replace('(', "")
        string = string.replace(',)', '')
        button = KeyboardButton(string)
        yearKeyboard.add(button)
    await message.answer ("Введи дату, на которую хочешь получить информацию. Сейчас введи год", reply_markup = yearKeyboard)
    await States.yearStatePres.set()

@dp.message_handler(state=States.yearStatePres)
async def getHistoricDataMonthPres(message: types.Message):
    global year
    year = message.text
    monthKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
    cursor = connection.cursor()
    cursor.execute("select distinct month from data where year = (?) and pressure is not null", [year])
    out = cursor.fetchall()
    for i in out:
        string = str(i).replace('(', "")
        string = string.replace(',)','')
        button = KeyboardButton(string)
        monthKeyboard.add(button)
    await message.answer("Теперь номер месяца", reply_markup=monthKeyboard)
    await States.monthStatePres.set()

@dp.message_handler(state=States.monthStatePres)
async def getHistoricDataDayPres(message: types.Message):
    global month
    month = message.text
    dayKeyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    #print(year, month)
    connection = sqlite3.connect(getMessage.getAbsPathOfMeteo())
    cursor = connection.cursor()
    cursor.execute("select distinct day from data where year = (?) and month = (?) and pressure is not null", [year,month])
    out = cursor.fetchall()
    for i in out:
        #print (str(i))
        string = str(i).replace('(', "")
        string = string.replace(',)','')
        button = KeyboardButton(string)
        dayKeyboard.insert(button)
    await message.answer("Теперь номер дня", reply_markup=dayKeyboard)
    await States.dayStatePres.set()

@dp.message_handler(state=States.dayStatePres)
async def getHistoricDataPres(message: types.Message):

    day = message.text

    graph.getPicPres(year, month, day)

    photo=open('pic.png', 'rb')
    await bot.send_photo(message.from_user.id, photo, reply_markup=keyboard)
    photo.close()
    await States.freeState.set()