'''
This file contains middleware class
'''

from telebot import BaseMiddleware


class BotMiddleware(BaseMiddleware):
    '''Class for messages middlewares'''

    def __init__(self, users, ansmsg):
        self.update_sensitive = True
        self.update_types = ['message']
        self.users = users
        self.ansmsg = ansmsg

    def pre_process(self, message, data):
        '''Pre process method'''

        pass

    def post_process(self, message, data, exception=None):
        '''Post process method'''

        pass

    def pre_process_message(self, message, data):
        '''Gives users db to handlers'''

        data['users'] = self.users
        data['ansmsg'] = self.ansmsg

    def post_process_message(self, message, data, exception=None):
        '''Post process method for msg'''

        pass
