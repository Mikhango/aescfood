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
from bot.register_handlers import register_handlers

# Middleware class
from bot.middlewares.middlewareclasses import BotMiddleware

# Answers
from bot.answers import ansmsg


bot = TeleBot(TOKEN, use_class_middlewares=True)

users = DataBase(__file__, "users")
users.createtable("users", [["id", "INT"], ["status", "INT"],
                    ["number", "TEXT"], ["room", "TEXT"], ["earned", "INT"]])
users.createtable("orders", [["id", "INT"], ["room", "TEXT"], ["price", "INT"]])

register_handlers(bot=bot, users=users)

bot.setup_middleware(BotMiddleware(users, ansmsg))

if __name__ == '__main__':
    bot.polling(none_stop = True, interval = 0)
