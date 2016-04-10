# -*- coding: utf-8 -*-

from business_connect import settings
from business_connect.validators import validate_toLength, validate_message, validate_toChannel, validate_eventType

import requests
import json


# https://developers.line.me/businessconnect/api-reference#getting_message_content
def get_message_content(message_id):
    endpoint = '%s/message/%s/content' % (settings.API_URL_BOT, message_id, )
    headers = {'X-Line-ChannelToken': settings.CHANNEL_ACCESS_TOKEN}

    res = requests.get(endpoint, headers=headers)

    status_message = ''
    if res.status_code != 200:
        status_message = res.json().get('statusMessage', '')

    result = res.text
    return {'status_code': res.status_code, 'result': result, 'status_message': status_message}


# https://developers.line.me/businessconnect/api-reference#getting_message_content_preview
def get_previews_of_message_content(message_id):
    endpoint = '%s/message/%s/content/preview' % (settings.API_URL_BOT, message_id, )
    headers = {'X-Line-ChannelToken': settings.CHANNEL_ACCESS_TOKEN}

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

    endpoint = settings.API_URL_PROFILES
    headers = {'X-Line-ChannelToken': settings.CHANNEL_ACCESS_TOKEN}
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

    endpoint = settings.API_URL_EVENTS
    headers = {'Content-Type': 'application/json; charset=UTF-8', 'X-Line-ChannelToken': settings.CHANNEL_ACCESS_TOKEN}

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
