# -*- coding: utf-8 -*-

from __future__ import absolute_import

from urlparse import urlparse, urljoin
import os

api_base_url = urlparse('https://trialbot-api.line.me/v1/events/')
API_URL_EVENTS = urljoin(api_base_url.geturl(), 'events')
API_URL_PROFILES = urljoin(api_base_url.geturl(), 'profiles')
API_URL_BOT = urljoin(api_base_url.geturl(), 'bot')

CHANNEL_ID = os.getenv('CHANNEL_ID')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
CHANNEL_MID = os.getenv('CHANNEL_MID')

for val in (CHANNEL_ID, CHANNEL_SECRET, CHANNEL_MID):
    if val is None or val == '':
        raise ValueError('CHANNEL_ID, CHANNEL_SECRET and CHANNEL_MID are required to be specified')
