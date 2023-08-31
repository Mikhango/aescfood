"""Cancel action handler"""

from telebot import TeleBot
from telebot.types import Message


def cancel_action(message: Message, bot: TeleBot, answers, markups):
    """
    This function answer on any requests, that weren't accepted
    by other functions
    """

    bot.send_message(message.chat.id, answers.CANCELACTION,
                     reply_markup=markups.BASEMARKUP)
    bot.delete_state(message.from_user.id, message.chat.id)