# -*- coding: utf-8 -*-

from __future__ import absolute_import

from urlparse import urlparse, urljoin
import os
import validators

api_base_url = urlparse('https://api.line.me/v1/')
env_api_base_url = os.getenv('API_URL_BASE')
if env_api_base_url is not None and validators.url(env_api_base_url):
    api_base_url = urlparse(env_api_base_url)

API_URL_EVENTS = urljoin(api_base_url.geturl(), 'events')
API_URL_PROFILES = urljoin(api_base_url.geturl(), 'profiles')
API_URL_BOT = urljoin(api_base_url.geturl(), 'bot')

CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')

if CHANNEL_SECRET is None or CHANNEL_SECRET == '' or CHANNEL_ACCESS_TOKEN is None or CHANNEL_ACCESS_TOKEN == '':
    raise ValueError('Environment variable CHANNEL_SECRET and CHANNEL_ACCESS_TOKEN not defined.')
