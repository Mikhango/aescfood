'''
This file polls bot
'''

# Telebot
from telebot import TeleBot

# States
from telebot.storage import StateMemoryStorage
from telebot.custom_filters import StateFilter

# DataBase
from sqlitework import DataBase

# Token
from bot.config import TOKEN

# Register handlers
from bot.register_handlers import register_handlers

# Middleware class
from bot.middlewares.middlewareclasses import BotMiddleware

# Answers
from bot.answers import Answers, Markups, Callbacks

# Helpfunctions
from bot.filters.filters import Helpers

# States
from bot.states.states import States


# States memory
state_storage = StateMemoryStorage()


bot = TeleBot(TOKEN, use_class_middlewares=True, state_storage=state_storage)

bot.add_custom_filter(StateFilter(bot))

users = DataBase(__file__, "users")
users.createtable("users", [["id", "INT"], ["number", "TEXT"], ["room", "TEXT"]])
users.createtable("couriers", [["id", "INT"], ["status", "INT"],
                    ["price", "INT"], ["earned", "INT"]])
users.createtable("orders", [["id", "INT"], ["id_client", "INT"], ["name_client", "TEXT"],
                  ["id_courier", "INT"], ["name_courier", "TEXT"],
                  ["room", "TEXT"], ["price", "INT"], ["comment", "TEXT"]])

helpers = Helpers(users)
states = States()

register_handlers(bot=bot, users=users, helpers=helpers, states=states)

bot.setup_middleware(BotMiddleware(users, Answers(), Markups(), Callbacks(), helpers, states))

if __name__ == '__main__':
    bot.polling(none_stop = True, interval = 0)
