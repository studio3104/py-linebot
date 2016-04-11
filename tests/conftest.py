# -*- coding: utf-8 -*-

from linebot import event
from linebot import settings

import pytest
import responses


@pytest.yield_fixture
def mocking():
    params = {
        'message_id': '123456789',
        'mids': 'u0047556f2e40dba2456887320ba7c76d',
    }
    get_urls = {
        'get_message_content': '{}/message/{}/content'.format(settings.API_URL_BOT, params['message_id']),
        'get_previews_of_message_content': '{}/message/{}/content/preview'.format(settings.API_URL_BOT, params['message_id']),
        'get_user_profile_information': settings.API_URL_PROFILES,
    }
    for _, url in get_urls.iteritems():
        responses.add(responses.GET, url, status=200)

    post_urls = {
        'send_messages': settings.API_URL_EVENTS,
        'send_link_messages': settings.API_URL_EVENTS,
        'send_multiple_messages': settings.API_URL_EVENTS,
        'send_rich_content_message': settings.API_URL_EVENTS,
    }

    for _, url in post_urls.iteritems():
        responses.add(responses.POST, url, status=200)

    yield params
