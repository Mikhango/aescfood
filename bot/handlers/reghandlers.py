"""
This file contain functions that will register user
"""

from telebot import TeleBot
from telebot.types import Message


class Register:
    """Class with register handlers"""

    def start(self, message : Message, bot : TeleBot, answers, states, users):
        """This function answer on a /start command"""

        if users.getuser(message.chat.id) is not None:
            bot.send_message(message.chat.id, answers.BADREQUESTREG)
            return

        bot.send_message(message.chat.id, answers.STARTMSG)
        bot.send_message(message.chat.id, answers.TELEPHONE)
        bot.set_state(message.from_user.id, states.regnumber, message.chat.id)

    def getnumber(self, message : Message, bot : TeleBot, answers, states):
        """This function gets number of user"""

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['numberu'] = message.text

        bot.send_message(message.chat.id, answers.ROOM)
        bot.set_state(message.from_user.id, states.regroom, message.chat.id)

    def errorgetnumber(self, message : Message, bot : TeleBot, answers):
        """Getting phone error"""

        bot.send_message(message.chat.id, answers.PHONEWRONG)

    def getroom(self, message : Message, bot : TeleBot, users, answers, markups):
        """This function gets user's room number"""

        try:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                users.adduser(message.chat.id, data['numberu'], message.text)
        except ValueError:
            bot.send_message(message.chat.id, answers.BADREQUESTREG)
            return

        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, answers.ENDREG,
                        reply_markup=markups.BASEMARKUP)

    def errorgetroom(self, message : Message, bot : TeleBot, answers):
        """Getting room error"""

        bot.send_message(message.chat.id, answers.ROOMWRONG)
