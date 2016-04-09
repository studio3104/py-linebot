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

def test_validate_toChannel():
    to_channel = '1383378250'
    event.validate_toChannel(to_channel)

    to_channel = '1383378251'
    with pytest.raises(ValueError):
        event.validate_toChannel(to_channel)

def test_validate_eventType():
    event_type = '138311608800106203'
    event.validate_eventType(event_type)

    event_type = '138311608800106204'
    with pytest.raises(ValueError):
        event.validate_eventType(event_type)
