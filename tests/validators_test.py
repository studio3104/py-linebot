# -*- coding: utf-8 -*-

from linebot import validators

import pytest


class TestValidateToChannel:
    @pytest.mark.parametrize(('params'), [
        {'api_name': 'send_messages', 'to_channel': '1383378250'},
        {'api_name': 'send_link_messages', 'to_channel': '1341301715'},
        {'api_name': 'send_multiple_messages', 'to_channel': '1383378250'},
        {'api_name': 'send_rich_content_messages', 'to_channel': '1383378250'},
    ])
    def test_valid_validate_toChannel(self, params):
        result = validators.validate_toChannel(params['api_name'], params['to_channel'])
        assert result is None

    @pytest.mark.parametrize(('params'), [
        {'api_name': 'send_messages', 'to_channel': '1383378251'},
        {'api_name': 'send_link_messages', 'to_channel': '1341301716'},
        {'api_name': 'send_multiple_messages', 'to_channel': '1383378251'},
        {'api_name': 'send_rich_content_messages', 'to_channel': '1383378251'},
    ])
    def test_invalid_validate_toChannel(self, params):
        with pytest.raises(ValueError):
            validators.validate_toChannel(params['api_name'], params['to_channel'])


class TestValidateEventType:
    @pytest.mark.parametrize(('params'), [
        {'api_name': 'send_messages', 'event_type': '138311608800106203'},
        {'api_name': 'send_link_messages', 'event_type': '137299299800026303'},
        {'api_name': 'send_multiple_messages', 'event_type': '140177271400161403'},
        {'api_name': 'send_rich_content_messages', 'event_type': '138311608800106203'},
    ])
    def test_valid_validate_eventType(self, params):
        result = validators.validate_eventType(params['api_name'], params['event_type'])
        assert result is None

    @pytest.mark.parametrize(('params'), [
        {'api_name': 'send_messages', 'event_type': '138311608800106204'},
        {'api_name': 'send_link_messages', 'event_type': '137299299800026304'},
        {'api_name': 'send_multiple_messages', 'event_type': '140177271400161404'},
        {'api_name': 'send_rich_content_messages', 'event_type': '138311608800106204'},
    ])
    def test_invalid_validate_eventType(self, params):
        with pytest.raises(ValueError):
            validators.validate_eventType(params['api_name'], params['event_type'])
