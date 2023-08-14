"""
This file contain functions that will get user profile
"""

from telebot import TeleBot
from telebot.types import Message, CallbackQuery


def mainprofile(message : Message, bot : TeleBot, users, answers, markups):
    """Main profile menu"""

    user = ()

    try:
        user = users.getuser(message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, answers.BADREQUEST,
                    reply_markup=markups.BASEMARKUP)
        return

    bot.send_message(message.chat.id, answers.PROFILE.format(
        nick=message.from_user.first_name, number=user[1], room=user[2]),
                    reply_markup=markups.PROFILEMARKUP, parse_mode='Markdown')

class Profile:
    """Profile handlers"""

    def myprofile(self, message : Message, bot : TeleBot, users, answers, markups):
        """This function gets user profile"""

        mainprofile(message, bot, users, answers, markups)

    def changenumber(self, callback_data: CallbackQuery, bot : TeleBot, answers, markups, states):
        """This function allows user to change his number"""

        bot.edit_message_text(answers.EDITNUMBER,
                            callback_data.from_user.id, callback_data.message.message_id,
                            reply_markup=markups.EMPTYINL)
        bot.set_state(callback_data.from_user.id, states.updnumber, callback_data.message.chat.id)


    def changeroom(self, callback_data: CallbackQuery, bot : TeleBot, answers, markups, states):
        """This function allows user to change his room number"""

        bot.edit_message_text(answers.EDITROOM,
                            callback_data.from_user.id, callback_data.message.message_id,
                            reply_markup=markups.EMPTYINL)
        bot.set_state(callback_data.from_user.id, states.updroom, callback_data.message.chat.id)

    def enterroom(self, message : Message, bot : TeleBot, users, answers, markups):
        """This function edits user room"""

        try:
            users.edituserroom(message.chat.id, message.text)
        except ValueError:
            bot.send_message(message.chat.id, answers.BADREQUEST,
                        reply_markup=markups.BASEMARKUP)
            return

        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, answers.PROFILEEDITED,
                        reply_markup=markups.BASEMARKUP)
        mainprofile(message, bot, users, answers, markups)

    def errorupdroom(self, message : Message, bot : TeleBot, users, answers, markups):
        """Updating room error"""

        bot.send_message(message.chat.id, answers.ROOMWRONG)
        bot.delete_state(message.from_user.id, message.chat.id)
        mainprofile(message, bot, users, answers, markups)

    def enternumber(self, message : Message, bot : TeleBot, users, answers, markups):
        """This function edits user number"""

        try:
            users.editusernumber(message.chat.id, message.text)
        except ValueError:
            bot.send_message(message.chat.id, answers.BADREQUEST,
                        reply_markup=markups.BASEMARKUP)
            return

        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, answers.PROFILEEDITED,
                        reply_markup=markups.BASEMARKUP)
        mainprofile(message, bot, users, answers, markups)

    def errorupdnumber(self, message : Message, bot : TeleBot, users, answers, markups):
        """Updating phone error"""

        bot.send_message(message.chat.id, answers.PHONEWRONG)
        bot.delete_state(message.from_user.id, message.chat.id)
        mainprofile(message, bot, users, answers, markups)
