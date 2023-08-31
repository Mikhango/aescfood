'''
This file contains middleware class
'''

from telebot import BaseMiddleware


class BotMiddleware(BaseMiddleware):
    '''Class for messages middlewares'''

    def __init__(self, users, answers, markups, callbacks, helpers, states):
        self.update_sensitive = True
        self.update_types = ['message', 'callback_query']
        self.users = users
        self.answers = answers
        self.markups = markups
        self.helpers = helpers
        self.callbacks = callbacks
        self.states = states

    def pre_process(self, message, data):
        '''Pre process method'''

        pass

    def post_process(self, message, data, exception=None):
        '''Post process method'''

        pass

    def pre_process_message(self, message, data):
        '''Gives users db to handlers'''

        data['users'] = self.users
        data['helpers'] = self.helpers
        data['states'] = self.states
        data['answers'] = self.answers
        data['callbacks'] = self.callbacks
        data['markups'] = self.markups

    def post_process_message(self, message, data, exception=None):
        '''Post process method for msg'''

        pass

    def pre_process_callback_query(self, callback_query, data):
        '''Gives dict of answers to handlers'''

        data['users'] = self.users
        data['helpers'] = self.helpers
        data['states'] = self.states
        data['answers'] = self.answers
        data['callbacks'] = self.callbacks
        data['markups'] = self.markups

    def post_process_callback_query(self, callback_query, data, exception=None):
        '''Post process method for callback'''

        pass
