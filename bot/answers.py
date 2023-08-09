'''
File with all buttons and keyboards for bot
'''

# Matkup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, \
InlineKeyboardButton, InlineKeyboardMarkup


# Messages
STARTMSG = "Привет, я - бот, созданный @MIKHAN_GO для помощи в доставке еды внутри СУНЦ МГУ.\n\
Зарегистрируйся, и я расскажу, как это работает😁"
TELEPHONE = "Для начала отправь мне свой номер телефона в формате 8XXXXXXXXXX"
ROOM = "Отлично! Теперь отправь мне номер в комнаты, в которой ты проживаешь"
ENDREG = "Вы успешно зарегистрировались!"
PROFILE = "*Твой профиль*\n\n*Никнейм:*  {nick}\n*Номер:*  \
{number}\n*Номер комнаты:*  {room}"
EDITNUMBER = "Введи новый номер телефона в формате 8XXXXXXXXXX"
EDITROOM = "Введи новый номер комнаты"
PROFILEEDITED = "Ваш профиль успешно изменен"

BADREQUESTREG = "Ты уже зарегистрирован(-а)!"
DOESNTREG = "Ты еще не зарегистрирован(-а)! Напиши мне /start, чтобы это исправить;)"
BADREQUEST = "Я не понимаю😢"
PHONEWRONG = "Неправильный формат ввода!"

# Callbacks
CALLBACKNUMBER = 'changenumber'
CALLBACKROOM = 'changeroom'

# Buttons

PROFILEBTN = "Мой профиль"
CHANGEROOMBTN = "Изменить комнату"
CHANGENUMBERBTN = "Изменить номер"

MY_PROFILE = KeyboardButton(PROFILEBTN)

EDIT_ROOM = InlineKeyboardButton(CHANGEROOMBTN, callback_data=CALLBACKROOM)
EDIT_NUMBER = InlineKeyboardButton(CHANGENUMBERBTN, callback_data=CALLBACKNUMBER)


# Markups
BASEMARKUP = ReplyKeyboardMarkup(resize_keyboard=True)
BASEMARKUP.add(MY_PROFILE)

PROFILEMARKUP = InlineKeyboardMarkup(row_width=1)
PROFILEMARKUP.add(EDIT_ROOM, EDIT_NUMBER)


callbacks = {
    "CALLBACKNUMBER" : CALLBACKNUMBER,
    "CALLBACKROOM" : CALLBACKROOM,
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
    "BADREQUEST" : BADREQUEST,
    "BADREQUESTREG" : BADREQUESTREG,
    "DOESNTREG" : DOESNTREG,
    "PHONEWRONG" : PHONEWRONG,
}

markups = {
    "BASEMARKUP" : BASEMARKUP,
    "PROFILEMARKUP" : PROFILEMARKUP,
    "EMPTYINL" : InlineKeyboardMarkup(),
}

buttons = {
    "PROFILEBTN" : PROFILEBTN,
    "CHANGEROOMBTN" : CHANGEROOMBTN,
    "CHANGENUMBERBTN" : CHANGENUMBERBTN,
}

ansmsg = {
    "answers" : answers,
    "markups" : markups,
}
