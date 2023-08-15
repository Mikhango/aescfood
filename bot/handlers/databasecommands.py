"""Database commands"""

from telebot import TeleBot
from telebot.types import Message


def getusersdb(message: Message, bot: TeleBot, users):
    """
    This function gets all users in db
    """

    allusers = users.getusers()

    for user in allusers:
        msg = ''
        for param in user:
            if len(str(param)) > 50:
                msg += str(param)[:50]
            else:
                msg += str(param)
            msg += ' '
        bot.send_message(message.chat.id, msg)

def delusrdb(message: Message, bot: TeleBot, users):
    """This function gets all users in db"""

    usrid = int(message.text.split()[1])

    if users.checkuser(usrid):
        users.deluser(usrid)

    bot.send_message(message.chat.id, "Deleted")
