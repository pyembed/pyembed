from rembed import consumer, discovery, parse

from hamcrest import *
from mock import *
import pytest
import requests

def test_should_discover_and_get_oembed_url():
    with patch('rembed.discovery.get_oembed_url') as mock_get_url, \
         patch('rembed.parse.parse_oembed') as mock_parse, \
         patch('requests.get') as mock_get:

        mock_get_url.return_value = ('json', 'http://example.com/oembed?format=json')

        response = Mock()
        response.text = 'hello, world'
        mock_get.return_value = response

        parsed = Mock()
        mock_parse.return_value = parsed

        assert_that(consumer.get_oembed_response('http://example.com/'), equal_to(parsed))

        mock_get_url.assert_called_with('http://example.com/')
        mock_get.assert_called_with('http://example.com/oembed?format=json')
        mock_parse.assert_called_with('json', 'hello, world')