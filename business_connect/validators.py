# -*- coding: utf-8 -*-

SEND_MESSAGE_CHANNEL = '1383378250'
SEND_LINK_MESSAGE_CHANNEL = '1341301715'
SEND_MULTIPLE_MESSAGE_CHANNEL = SEND_MESSAGE_CHANNEL
SEND_RICH_MESSAGE_CHANNEL = SEND_MESSAGE_CHANNEL
SEND_MESSAGE_EVENT_TYPE = '138311608800106203'
SEND_LINK_MESSAGE_EVENT_TYPE = '137299299800026303'
SEND_MULTIPLE_MESSAGE_EVENT = '140177271400161403'
SEND_RICH_MESSAGE_EVENT = SEND_MESSAGE_EVENT_TYPE


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
            raise ValueError('Acceptable eventType is "%s" only' % (SEND_MULTIPLE_MESSAGE_CHANNEL, ))
    elif api_name == 'send_link_messages':
        if event_type == SEND_LINK_MESSAGE_EVENT_TYPE:
            return
        else:
            raise ValueError('Acceptable eventType is "%s" only' % (SEND_LINK_MESSAGE_EVENT_TYPE, ))
    else:
        raise ValueError('unknown api_name: %s' % (api_name, ))
