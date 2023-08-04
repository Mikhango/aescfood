'''
This file polls bot
'''

# Telebot
from telebot import TeleBot

# Token
from bot.config import TOKEN

# Register handlers
from bot.register_handlers import register_handlers

bot = TeleBot(TOKEN)

register_handlers(bot)

if __name__ == '__main__':
    bot.polling(none_stop = True, interval = 0)
