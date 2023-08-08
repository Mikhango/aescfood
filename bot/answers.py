'''
File with all buttons and keyboards for bot
'''

# Matkup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


# Messages
STARTMSG = "Привет, я - бот, созданный @MIKHAN_GO для помощи в доставке еды внутри СУНЦ МГУ.\n\
Зарегистрируйся, и я расскажу, как это работает😁"
TELEPHONE = "Для начала отправь мне свой номер телефона в формате 8XXXXXXXXXX"
ROOM = "Отлично! Теперь отправь мне номер в комнаты, в которой ты проживаешь"
END = "Вы успешно зарегистрировались!"

BADREQUESTREG = "Ты уже зарегистрирован(-а)!"
DOESNTREG = "Ты еще не зарегистрирован(-а)!"
BADREQUEST = "Я не понимаю😢"
PHONEWRONG = "Введи телефон в нужном формате"
ROOMWRONG = "Введи комнату в нужном формате"

# Buttons
MY_PROFILE = KeyboardButton("Мой профиль")


# Markups
BASEMARKUP = ReplyKeyboardMarkup(resize_keyboard=True)
BASEMARKUP.add(MY_PROFILE)

buttons = {
    "STARTMSG" : STARTMSG,
    "TELEPHONE" : TELEPHONE,
    "ROOM" : ROOM,
    "END" : END,
    "BADREQUEST" : BADREQUEST,
    "BADREQUESTREG" : BADREQUESTREG,
    "DOESNTREG" : DOESNTREG,
    "PHONEWRONG" : PHONEWRONG,
    "ROOMWRONG" : ROOMWRONG,
}

markups = {
    "BASEMARKUP" : BASEMARKUP,
}

ansmsg = {
    "buttons" : buttons,
    "markups" : markups,
}
