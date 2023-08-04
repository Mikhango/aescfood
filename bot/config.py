'''
This file gets token from txt
'''

TOKEN = None

with open("token.txt", encoding="utf-8") as t:
    TOKEN = t.read().strip()
