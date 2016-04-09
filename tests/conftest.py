# -*- coding: utf-8 -*-

from business_connect import event

import pytest
import responses


@pytest.yield_fixture
def mocking():
    params = {
        'message_id': '123456789',
        'mids': 'u0047556f2e40dba2456887320ba7c76d',
    }
    get_urls = {
        'get_message_content': '{}/message/{}/content'.format(event.API_URL_BOT, params['message_id']),
        'get_previews_of_message_content': '{}/message/{}/content/preview'.format(event.API_URL_BOT, params['message_id']),
        'get_user_profile_information': event.API_URL_PROFILES,
    }
    for _, url in get_urls.iteritems():
        responses.add(responses.GET, url, status=200)

    post_urls = {
        'send_messages': event.API_URL_EVENTS,
        'send_link_messages': event.API_URL_EVENTS,
        'send_multiple_messages': event.API_URL_EVENTS,
        'send_rich_content_message': event.API_URL_EVENTS,
    }

    for _, url in post_urls.iteritems():
        responses.add(responses.POST, url, status=200)

    yield params
