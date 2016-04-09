# -*- coding: utf-8 -*-
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
    if len(to) > 150:
        raise ValueError('target user is up to 150. You passed %d users' % (len(to), ))

    try:
        validate_toChannel(to_channel)
        validate_eventType(event_type)
    except ValueError, e:
        raise e

    if content.get('contentType') != 1:
        raise ValueError('Acceptable contentType is "1" only')

    if content.get('toType') not in [1, 2, 3]:
        raise ValueError('Acceptable toType is 1, 2 or 3')

    if len(content.get('text')) > 1025:
        raise ValueError('Acceptable text is up to 1024 characters')

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

def validate_toChannel(to_channel):
    if to_channel != '1383378250':
        raise ValueError('Acceptable toChannel is "1383378250" only')

def validate_eventType(event_type):
    if event_type != '138311608800106203':
        raise ValueError('Acceptable eventType is "138311608800106203" only')
