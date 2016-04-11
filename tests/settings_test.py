# -*- coding: utf-8 -*-

from linebot.settings import API_URL_EVENTS, API_URL_PROFILES, API_URL_BOT


def test_default_urls():
    assert API_URL_EVENTS == 'https://api.line.me/v1/events'
    assert API_URL_PROFILES == 'https://api.line.me/v1/profiles'
    assert API_URL_BOT == 'https://api.line.me/v1/bot'
