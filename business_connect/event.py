# -*- coding: utf-8 -*-

from business_connect.validators import validate_toLength, validate_message, validate_toChannel, validate_eventType

import os
import requests
import json

API_URL_EVENTS = 'https://api.line.me/v1/events'
API_URL_PROFILES = 'https://api.line.me/v1/profiles'
API_URL_BOT = 'https://api.line.me/v1/bot'

CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')

if CHANNEL_SECRET is None or CHANNEL_SECRET == '' or CHANNEL_ACCESS_TOKEN is None or CHANNEL_ACCESS_TOKEN == '':
    raise ValueError('Environment variable CHANNEL_SECRET and CHANNEL_ACCESS_TOKEN not defined.')


# https://developers.line.me/businessconnect/api-reference#getting_message_content
def get_message_content(message_id):
    endpoint = '%s/message/%s/content' % (API_URL_BOT, message_id, )
    headers = {'X-Line-ChannelToken': CHANNEL_ACCESS_TOKEN}

    res = requests.get(endpoint, headers=headers)

    status_message = ''
    if res.status_code != 200:
        status_message = res.json().get('statusMessage', '')

    result = res.text
    return {'status_code': res.status_code, 'result': result, 'status_message': status_message}


# https://developers.line.me/businessconnect/api-reference#getting_message_content_preview
def get_previews_of_message_content(message_id):
    endpoint = '%s/message/%s/content/preview' % (API_URL_BOT, message_id, )
    headers = {'X-Line-ChannelToken': CHANNEL_ACCESS_TOKEN}

    res = requests.get(endpoint, headers=headers)

    status_message = ''
    if res.status_code != 200:
        status_message = res.json().get('statusMessage', '')

    result = res.text
    return {'status_code': res.status_code, 'result': result, 'status_message': status_message}


# https://developers.line.me/businessconnect/api-reference#getting_user_profile_information
# Lists the MIDs of the users whose information is to be retrieved, separated by commas.
def get_user_profile_information(mids):
    if mids == '':
        raise ValueError('mids must not be empty')

    endpoint = API_URL_PROFILES
    headers = {'X-Line-ChannelToken': CHANNEL_ACCESS_TOKEN}
    payload = {'mids': mids}

    res = requests.get(endpoint, headers=headers, params=payload)

    status_message = ''
    result = ''
    if res.status_code != 200:
        status_message = res.json().get('statusMessage', '')

    result = res.text
    return {'status_code': res.status_code, 'result': result, 'status_message': status_message}


# https://developers.line.me/businessconnect/api-reference#sending_message
def send_messages(to, to_channel, event_type, content):
    try:
        validate_message(content)
    except ValueError, e:
        raise e

    return _post('send_messages', to, to_channel, event_type, content)


# https://developers.line.me/businessconnect/api-reference#sending_link_message
def send_link_messages(to, to_channel, event_type, content):
    return _post('send_link_messages', to, to_channel, event_type, content)


# https://developers.line.me/businessconnect/api-reference#sending_multiple_messages
def send_multiple_messages(to, to_channel, event_type, content):
    return _post('send_multiple_messages', to, to_channel, event_type, content)


# https://developers.line.me/businessconnect/api-reference#sending_rich_content_message
def send_rich_content_messages(to, to_channel, event_type, content):
    return _post('send_rich_content_messages', to, to_channel, event_type, content)


def _post(api_name, to, to_channel, event_type, content):
    try:
        validate_toLength(to)
        validate_toChannel(api_name, to_channel)
        validate_eventType(api_name, event_type)
    except ValueError, e:
        raise e

    endpoint = API_URL_EVENTS
    headers = {'Content-Type': 'application/json; charset=UTF-8', 'X-Line-ChannelToken': CHANNEL_ACCESS_TOKEN}

    data = json.dumps({
        'to': to,
        'toChannel': to_channel,
        'eventType': event_type,
        'content': content
        })

    res = requests.post(endpoint, data=data, headers=headers)

    status_message = ''
    if res.status_code != 200:
        status_message = res.json().get('statusMessage', '')

    result = res.text
    return {'status_code': res.status_code, 'result': result, 'status_message': status_message}
