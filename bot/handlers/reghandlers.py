"""
This file contain functions that will register user
"""

from telebot import TeleBot
from telebot.types import Message


STARTMSG = "Привет, я - бот, созданный @MIKHAN_GO для помощи в доставке еды внутри СУНЦ МГУ.\n\
Зарегистрируйся, и я расскажу, как это работает😁"
TELEPHONE = "Для начала отправь мне свой номер телефона"
ROOM = "Отлично! Теперь отправь мне номер в комнаты, в которой ты проживаешь"
END = "Вы успешно зарегистрировались!"
BADREQUEST = "Ты уже зарегистрирован(-а)!"


def start(message : Message, bot : TeleBot, users):
    """This function answer on a /start command"""

    try:
        users.setnametable("users")
        users.adddata([message.chat.id, -1, "", "", 0], message.chat.id, "id")
    except ValueError:
        bot.send_message(message.chat.id, BADREQUEST)
        return

    bot.send_message(message.chat.id, STARTMSG)
    bot.send_message(message.chat.id, TELEPHONE)
    bot.register_next_step_handler(message=message, callback=getnumber, bot=bot, users=users)

def getnumber(message : Message, bot : TeleBot, users):
    """This function gets number of user"""

    try:
        users.setnametable("users")
        users.editdata(message.chat.id, "id", message.text, "number")
    except ValueError:
        bot.send_message(message.chat.id, BADREQUEST)
        return

    bot.send_message(message.chat.id, ROOM)
    bot.register_next_step_handler(message=message, callback=getroom, bot=bot, users=users)

def getroom(message : Message, bot : TeleBot, users):
    """This function gets user's room number"""

    try:
        users.setnametable("users")
        users.editdata(message.chat.id, "id", message.text, "room")
    except ValueError:
        bot.send_message(message.chat.id, BADREQUEST)
        return

    bot.send_message(message.chat.id, END)
