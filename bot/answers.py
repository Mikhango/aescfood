'''
File with all buttons and keyboards for bot
'''

# Matkup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, \
InlineKeyboardButton, InlineKeyboardMarkup


# Format functions
def buttonformcourierstatus(text):
    """Format courier change status button"""

    return InlineKeyboardButton(COURIERCHSTBTN.format(status=text),
                                callback_data=CALLBACKCOURIERCHST)


# Messages
STARTMSG = "Привет, я - бот, созданный @MIKHAN_GO для помощи в доставке еды внутри СУНЦ МГУ.\n\
Зарегистрируйся, и я расскажу, как это работает😁"
TELEPHONE = "Для начала отправь мне свой номер телефона в формате 8XXXXXXXXXX"
ROOM = "Отлично! Теперь отправь мне номер комнаты, в которой ты проживаешь"
ENDREG = "Ты успешно зарегистрировался(-ась)!"

PROFILE = "*Твой профиль*\n\n*Имя:*  {nick}\n*Номер:*  \
{number}\n*Номер комнаты:*  {room}"
EDITNUMBER = "Введи новый номер телефона в формате 8XXXXXXXXXX"
EDITROOM = "Введи новый номер комнаты"
PROFILEEDITED = "Твой профиль успешно изменен"

COURIERPROFILE = "*Твой карьерный профиль*\n\n*Имя:*  {nick}\n*Заказ от:* {minrub} ₽\n\
*Всего заработано:*  {coins} ₽\n*Текущий статус:*  {currstatus}"
COURIERREG = "Ты еще не зарегистрирован(-а) как курьер. Если хочешь начать брать заказы, \
зарегистрируйся по конпке ниже."
COURIERREGSUCCESS = "Вы успешно зарегистрировались как курьер!"
COURIERBUSY = "Занят"
COURIERFREE = "Свободен"
COURIERMINPRICE = "Введи минимальную цену, от которой ты берешь заказы\nНе более 10000"

ORDERS = "Мои заказы"

BADREQUESTREG = "Ты уже зарегистрирован(-а)!"
DOESNTREG = "Ты еще не зарегистрирован(-а)! Напиши мне /start, чтобы это исправить;)"
BADREQUEST = "Я не понимаю😢"
PHONEWRONG = "Неправильный формат ввода!"
ROOMWRONG = "Неправильный формат ввода!"
UNCORRECTPRICE = "Неправильный формат цены!"

# Callbacks
CALLBACKNUMBER = 'changenumber'
CALLBACKROOM = 'changeroom'

CALLBACKCOURIERREG = 'courierreg'
CALLBACKCOURIERCHST = 'courierchst'
CALLBACKCOURIERPRICE = 'courierprice'

# Buttons

PROFILEBTN = "Мой профиль"
COURIERBTN = "Карьера курьера"

COURIERSTARTBTN = "Зарегистрироваться"
COURIERCHSTBTN = "Изменить статус на: {status}"
CHANGECOURIERPRICEBTN = "Изменить минимальную цену заказа"

CHANGEROOMBTN = "Изменить комнату"
CHANGENUMBERBTN = "Изменить номер"


MY_PROFILE = KeyboardButton(PROFILEBTN)
COURIER = KeyboardButton(COURIERBTN)
MYORDERS = KeyboardButton(ORDERS)

EDIT_ROOM = InlineKeyboardButton(CHANGEROOMBTN, callback_data=CALLBACKROOM)
EDIT_NUMBER = InlineKeyboardButton(CHANGENUMBERBTN, callback_data=CALLBACKNUMBER)

COURIER_START = InlineKeyboardButton(COURIERSTARTBTN, callback_data=CALLBACKCOURIERREG)
CHANGECOURIERPRICE = InlineKeyboardButton(CHANGECOURIERPRICEBTN, callback_data=CALLBACKCOURIERPRICE)

# Markups
BASEMARKUP = ReplyKeyboardMarkup(resize_keyboard=True)
BASEMARKUP.add(MY_PROFILE, COURIER, ORDERS)

PROFILEMARKUP = InlineKeyboardMarkup(row_width=1)
PROFILEMARKUP.add(EDIT_ROOM, EDIT_NUMBER)

COURIERREGMARKUP = InlineKeyboardMarkup(row_width=1)
COURIERREGMARKUP.add(COURIER_START)

COURIERSTATMARKUP = InlineKeyboardMarkup(row_width=1)
COURIERSTATMARKUP.add(COURIER_START)

COURIERBUSYMARKUP = InlineKeyboardMarkup(row_width=1)
COURIERBUSYMARKUP.add(buttonformcourierstatus(COURIERBUSY), CHANGECOURIERPRICE)

COURIERFREEMARKUP = InlineKeyboardMarkup(row_width=1)
COURIERFREEMARKUP.add(buttonformcourierstatus(COURIERFREE), CHANGECOURIERPRICE)

callbacks = {
    "CALLBACKNUMBER" : CALLBACKNUMBER,
    "CALLBACKROOM" : CALLBACKROOM,
    "CALLBACKCOURIERREG" : CALLBACKCOURIERREG,
    "CALLBACKCOURIERCHST" : CALLBACKCOURIERCHST,
    "CALLBACKCOURIERPRICE" : CALLBACKCOURIERPRICE,
}

answers = {
    "STARTMSG" : STARTMSG,
    "TELEPHONE" : TELEPHONE,
    "ROOM" : ROOM,
    "ENDREG" : ENDREG,
    "PROFILE" : PROFILE,
    "EDITNUMBER" : EDITNUMBER,
    "EDITROOM" : EDITROOM,
    "PROFILEEDITED" : PROFILEEDITED,
    "COURIERREGSUCCESS" : COURIERREGSUCCESS,
    "COURIERREG" : COURIERREG,
    "COURIERPROFILE" : COURIERPROFILE,
    "COURIERBUSY" : COURIERBUSY,
    "COURIERFREE" : COURIERFREE,
    "COURIERMINPRICE" : COURIERMINPRICE,

    "BADREQUEST" : BADREQUEST,
    "BADREQUESTREG" : BADREQUESTREG,
    "DOESNTREG" : DOESNTREG,
    "PHONEWRONG" : PHONEWRONG,
    "ROOMWRONG" : ROOMWRONG,
    "UNCORRECTPRICE" : UNCORRECTPRICE,
}

markups = {
    "BASEMARKUP" : BASEMARKUP,
    "PROFILEMARKUP" : PROFILEMARKUP,
    "COURIERREGMARKUP" : COURIERREGMARKUP,
    "COURIERSTATMARKUP" : COURIERSTATMARKUP,
    "COURIERFREEMARKUP" : COURIERFREEMARKUP,
    "COURIERBUSYMARKUP" : COURIERBUSYMARKUP,
    "EMPTYINL" : InlineKeyboardMarkup(row_width=1),
}

buttons = {
    "PROFILEBTN" : PROFILEBTN,
    "COURIERBTN" : COURIERBTN,
}

ansmsg = {
    "answers" : answers,
    "markups" : markups,
}
