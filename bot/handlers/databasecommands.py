"""Database commands"""

from telebot import TeleBot
from telebot.types import Message


def getusersdb(message: Message, bot: TeleBot, users):
    """
    This function gets all users in db
    """

    allusers = users.getusers()

    msg = ""

    for user in allusers:
        for param in user:
            msg += str(param)
            msg += ' '
        msg += '\n'

    bot.send_message(message.chat.id, msg)

def delusrdb(message: Message, bot: TeleBot, users):
    """This function gets all users in db"""

    usrid = int(message.text.split()[1])

    if users.checkuser(usrid):
        users.deluser(usrid)

    bot.send_message(message.chat.id, "Deleted")
