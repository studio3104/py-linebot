# -*- coding: utf-8 -*-

from business_connect import event

import responses
import pytest


@responses.activate
def test_get_message_content(mocking):
    response = event.get_message_content(mocking['message_id'])
    assert 'status_code' in response
    assert 'result' in response
    assert 'status_message' in response
    assert response['status_code'] == 200


@responses.activate
def test_get_previews_of_message_content(mocking):
    response = event.get_previews_of_message_content(mocking['message_id'])
    assert 'status_code' in response
    assert 'result' in response
    assert 'status_message' in response
    assert response['status_code'] == 200


@responses.activate
def test_get_user_profile_information(mocking):
    response = event.get_user_profile_information(mocking['mids'])
    assert 'status_code' in response
    assert 'result' in response
    assert 'status_message' in response
    assert response['status_code'] == 200


@responses.activate
def test_send_messages(mocking):
    # they are fixed values, ref: https://developers.line.me/businessconnect/api-reference#sending_message
    to_channel = '1383378250'
    event_type = '138311608800106203'
    response = event.send_messages(
        [mocking['mids'], ], to_channel, event_type,
        {
            'contentType': 1,
            'toType': 1,
            'text': 'Hello, World!'
        }
    )
    assert 'status_code' in response
    assert 'result' in response
    assert 'status_message' in response
    assert response['status_code'] == 200

@responses.activate
def test_send_link_messages(mocking):
    to_channel = '1341301715'
    event_type = '137299299800026303'
    response = event.send_link_messages(
        [mocking['mids'], ], to_channel, event_type,
        {
            "content": {
               "templateId": "template_id_3",
               "previewUrl": "http://example.com/images/brown.png",
               "textParams": {
                    "text_param": "Brown"
               },
               "subTextParams": {
                    "subtext_param": "Cony"
               },
               "altTextParams": {
                    "alttext_param": "Help!"
               },
               "linkTextParams": {
                    "lt_p": "Happy"
               },
               "aLinkUriParams": {
                    "alu_p": "foo"
               },
               "iLinkUriParams": {
                    "ilu_p": "bar"
               },
               "linkUriParams": {
                    "lu_p": "baz"
               }
            }
        }
    )
    assert 'status_code' in response
    assert 'result' in response
    assert 'status_message' in response
    assert response['status_code'] == 200

@responses.activate
def test_send_multiple_messages(mocking):
    to_channel = '1383378250'
    event_type = '140177271400161403'
    response = event.send_multiple_messages(
        [mocking['mids'], ], to_channel, event_type,
        {
            "content": {
                "messageNotified": 0,
                "messages": [
                    {
                        "contentType": 1,
                        "text": "First message"
                    },
                    {
                        "contentType": 2,
                        "originalContentUrl": "http://original/content/url",
                        "previewImageUrl": "http://preview/image/url",
                    }
                ]
            }
        }
    )
    assert 'status_code' in response
    assert 'result' in response
    assert 'status_message' in response
    assert response['status_code'] == 200

@responses.activate
def test_send_rich_messages(mocking):
    to_channel = '1383378250'
    event_type = '138311608800106203'
    response = event.send_rich_content_messages(
        [mocking['mids'], ], to_channel, event_type,
        {
            "content": {
                "contentType": 12,
                "toType": 1,
                "contentMetadata": {
                    "DOWNLOAD_URL": "http://example.com/bot/images/12345",
                    "SPEC_REV": "1",
                    "ALT_TEXT": "Please visit our homepage and the item page you wish.",
                    "MARKUP_JSON": "{\"canvas\":{...},\"images\":{...},\"actions\":{},\"scenes\":{...}}"
                }
            }
        }
    )
    assert 'status_code' in response
    assert 'result' in response
    assert 'status_message' in response
    assert response['status_code'] == 200

def test_validate_toChannel():
    test_data = [ # correct data
            {'api_name':'send_messages', 'to_channel': '1383378250'},
            {'api_name':'send_link_messages', 'to_channel': '1341301715'},
            {'api_name':'send_multiple_messages', 'to_channel': '1383378250'},
            {'api_name':'send_rich_content_messages', 'to_channel': '1383378250'},
            # {'api_name':'', 'to_channel': ''},
            ]
    for d in test_data:
        event.validate_toChannel(d['api_name'], d['to_channel'])

    test_data = [ # correct data
            {'api_name':'send_messages', 'to_channel': '1383378251'},
            {'api_name':'send_link_messages', 'to_channel': '1341301716'},
            {'api_name':'send_multiple_messages', 'to_channel': '1383378251'},
            {'api_name':'send_rich_content_messages', 'to_channel': '1383378251'},
            # {'api_name':'', 'to_channel': ''},
            ]
    with pytest.raises(ValueError):
        for d in test_data:
            event.validate_toChannel(d['api_name'], d['to_channel'])

def test_validate_eventType():
    test_data = [ # correct data
            {'api_name':'send_messages', 'event_type': '138311608800106203'},
            {'api_name':'send_link_messages', 'event_type': '137299299800026303'},
            {'api_name':'send_multiple_messages', 'event_type': '140177271400161403'},
            {'api_name':'send_rich_content_messages', 'event_type': '138311608800106203'},
            # {'event_type': '', 'event_name':''},
            ]
    for d in test_data:
        event.validate_eventType(d['api_name'], d['event_type'])

    test_data = [ # invalid data
            {'api_name':'send_messages', 'event_type': '138311608800106204'},
            {'api_name':'send_link_messages', 'event_type': '137299299800026304'},
            {'api_name':'send_multiple_messages', 'event_type': '140177271400161404'},
            {'api_name':'send_rich_content_messages', 'event_type': '138311608800106204'},
            # {'event_type': '', 'event_name':''},
            ]
    with pytest.raises(ValueError):
        for d in test_data:
            event.validate_eventType(d['api_name'], d['event_type'])
