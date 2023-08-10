'''
This file polls bot
'''

# Telebot
from telebot import TeleBot

# DataBase
from sqlitework import DataBase

# Token
from bot.config import TOKEN

# Register handlers
from bot.register_handlers import register_handlers, register_callback_handlers

# Middleware class
from bot.middlewares.middlewareclasses import BotMiddleware

# Answers
from bot.answers import ansmsg

# Helpfunctions
from bot.helpfunctions import Checkers


bot = TeleBot(TOKEN, use_class_middlewares=True)

users = DataBase(__file__, "users")
users.createtable("users", [["id", "INT"], ["number", "TEXT"], ["room", "TEXT"]])
users.createtable("couriers", [["id", "INT"], ["status", "INT"],
                    ["price", "INT"], ["earned", "INT"]])
users.createtable("orders", [["id", "INT"], ["id_client", "INT"], ["name_client", "TEXT"],
                  ["id_courier", "INT"], ["name_courier", "TEXT"],
                  ["room", "TEXT"], ["price", "INT"], ["comment", "TEXT"]])

register_handlers(bot=bot, users=users)
register_callback_handlers(bot=bot)

bot.setup_middleware(BotMiddleware(users, ansmsg, Checkers()))

if __name__ == '__main__':
    bot.polling(none_stop = True, interval = 0)
