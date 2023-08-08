"""
This file contain functions that will register user
"""

from telebot import TeleBot
from telebot.types import Message


def start(message : Message, bot : TeleBot, users, ansmsg):
    """This function answer on a /start command"""

    try:
        users.adduser([message.chat.id, -1, "", "", 0], message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, ansmsg['buttons']['BADREQUESTREG'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
        return

    bot.send_message(message.chat.id, ansmsg['buttons']['STARTMSG'])
    bot.send_message(message.chat.id, ansmsg['buttons']['TELEPHONE'])
    bot.register_next_step_handler(message=message, callback=getnumber, bot=bot, users=users,
                                   ansmsg = ansmsg)

def getnumber(message : Message, bot : TeleBot, users, ansmsg):
    """This function gets number of user"""

    try:
        if not message.text.isdigit():
            bot.send_message(message.chat.id, ansmsg['buttons']['PHONEWRONG'])
            bot.register_next_step_handler(message=message, callback=getnumber, bot=bot,
                                           users=users, ansmsg=ansmsg)
            return
        users.edituser("number", int(message.text), message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, ansmsg['buttons']['BADREQUESTREG'])
        return

    bot.send_message(message.chat.id, ansmsg['buttons']['ROOM'])
    bot.register_next_step_handler(message=message, callback=getroom, bot=bot, users=users,
                                   ansmsg=ansmsg)

def getroom(message : Message, bot : TeleBot, users, ansmsg):
    """This function gets user's room number"""

    try:
        if not message.text.isdigit():
            bot.send_message(message.chat.id, ansmsg['buttons']['ROOMWRONG'])
            bot.register_next_step_handler(message=message, callback=getroom, bot=bot, users=users,
                                           ansmsg=ansmsg)
            return
        users.edituser("room", message.text, message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, ansmsg['buttons']['BADREQUESTREG'])
        return

    bot.send_message(message.chat.id, ansmsg['buttons']['END'],
                     reply_markup=ansmsg['markups']['BASEMARKUP'])
