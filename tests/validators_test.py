# -*- coding: utf-8 -*-

from business_connect import validators

import pytest


def test_validate_toChannel():
    test_data = [ # correct data
            {'api_name':'send_messages', 'to_channel': '1383378250'},
            {'api_name':'send_link_messages', 'to_channel': '1341301715'},
            {'api_name':'send_multiple_messages', 'to_channel': '1383378250'},
            {'api_name':'send_rich_content_messages', 'to_channel': '1383378250'},
            # {'api_name':'', 'to_channel': ''},
            ]
    for d in test_data:
        validators.validate_toChannel(d['api_name'], d['to_channel'])

    test_data = [ # correct data
            {'api_name':'send_messages', 'to_channel': '1383378251'},
            {'api_name':'send_link_messages', 'to_channel': '1341301716'},
            {'api_name':'send_multiple_messages', 'to_channel': '1383378251'},
            {'api_name':'send_rich_content_messages', 'to_channel': '1383378251'},
            # {'api_name':'', 'to_channel': ''},
            ]
    with pytest.raises(ValueError):
        for d in test_data:
            validators.validate_toChannel(d['api_name'], d['to_channel'])

def test_validate_eventType():
    test_data = [ # correct data
            {'api_name':'send_messages', 'event_type': '138311608800106203'},
            {'api_name':'send_link_messages', 'event_type': '137299299800026303'},
            {'api_name':'send_multiple_messages', 'event_type': '140177271400161403'},
            {'api_name':'send_rich_content_messages', 'event_type': '138311608800106203'},
            # {'event_type': '', 'event_name':''},
            ]
    for d in test_data:
        validators.validate_eventType(d['api_name'], d['event_type'])

    test_data = [ # invalid data
            {'api_name':'send_messages', 'event_type': '138311608800106204'},
            {'api_name':'send_link_messages', 'event_type': '137299299800026304'},
            {'api_name':'send_multiple_messages', 'event_type': '140177271400161404'},
            {'api_name':'send_rich_content_messages', 'event_type': '138311608800106204'},
            # {'event_type': '', 'event_name':''},
            ]
    with pytest.raises(ValueError):
        for d in test_data:
            validators.validate_eventType(d['api_name'], d['event_type'])
