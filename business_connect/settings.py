# -*- coding: utf-8 -*-

import os

API_URL_EVENTS = 'https://api.line.me/v1/events'
API_URL_PROFILES = 'https://api.line.me/v1/profiles'
API_URL_BOT = 'https://api.line.me/v1/bot'

CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')

if CHANNEL_SECRET is None or CHANNEL_SECRET == '' or CHANNEL_ACCESS_TOKEN is None or CHANNEL_ACCESS_TOKEN == '':
    raise ValueError('Environment variable CHANNEL_SECRET and CHANNEL_ACCESS_TOKEN not defined.')
