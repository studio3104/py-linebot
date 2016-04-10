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

SEND_MESSAGE_CHANNEL = '1383378250'
SEND_LINK_MESSAGE_CHANNEL = '1341301715'
# SEND_MULTIPLE_MESSAGE_CHANNEL = SEND_MESSAGE_CHANNEL
# SEND_RICH_MESSAGE_CHANNEL = SEND_MESSAGE_CHANNEL
SEND_MESSAGE_EVENT_TYPE = '138311608800106203'
SEND_LINK_MESSAGE_EVENT_TYPE = '137299299800026303'
SEND_MULTIPLE_MESSAGE_EVENT = '140177271400161403'
# SEND_RICH_MESSAGE_EVENT = SEND_MESSAGE_EVENT_TYPE

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

def validate_toLength(to):
    if len(to) > 150:
        raise ValueError('target user is up to 150. You passed %d users' % (len(to), ))

# Just for send_messages, cannot use send_multiple_messages
def validate_message(content):
    if 'contentType' in content:
        if content.get('contentType') not in range(1, 9):
            raise ValueError('Acceptable contentType is between 1 and 8')
    else:
        raise ValueError('Property contentType is required')

    if 'toType' in content:
        if content.get('toType') not in [1, 2, 3]:
            raise ValueError('Acceptable toType is 1, 2 or 3')
    else:
        raise ValueError('Property toType is required')

    if 'text' in content:
        if len(content.get('text')) > 1025:
            raise ValueError('Acceptable text is up to 1024 characters')
    else:
        raise ValueError('Property text is required')

def validate_toChannel(api_name, to_channel):
    if api_name in ('send_messages', 'send_multiple_messages', 'send_rich_content_messages'):
            if to_channel == SEND_MESSAGE_CHANNEL:
                return
            else:
                raise ValueError('Acceptable toChannel is "%s" only' % (SEND_MESSAGE_CHANNEL, ))
    elif api_name == 'send_link_messages':
        if to_channel == SEND_LINK_MESSAGE_CHANNEL:
            return
        else:
            raise ValueError('Acceptable toChannel is "%s" only' % (SEND_LINK_MESSAGE_CHANNEL, ))
    else:
        raise ValueError('unknown api_name: %s' % (api_name, ))

def validate_eventType(api_name, event_type):
    if api_name in ('send_messages', 'send_rich_content_messages'):
        if event_type == SEND_MESSAGE_EVENT_TYPE:
            return
        else:
            raise ValueError('Acceptable eventType is "%s" only' % (SEND_MESSAGE_EVENT_TYPE, ))
    elif api_name == 'send_link_messages':
        if event_type == SEND_LINK_MESSAGE_EVENT_TYPE:
            return
        else:
            raise ValueError('Acceptable eventType is "%s" only' % (SEND_LINK_MESSAGE_EVENT_TYPE, ))
    elif api_name == 'send_multiple_messages':
        if event_type == SEND_MULTIPLE_MESSAGE_EVENT:
            return
        else:
            raise ValueError('Acceptable eventType is "%s" only' % (send_multiple_messages, ))
    elif api_name == 'send_link_messages':
        if event_type == SEND_LINK_MESSAGE_EVENT_TYPE:
            return
        else:
            raise ValueError('Acceptable eventType is "%s" only' % (SEND_LINK_MESSAGE_EVENT_TYPE, ))
    else:
        raise ValueError('unknown api_name: %s' % (api_name, ))
