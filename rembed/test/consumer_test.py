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
        response.ok = True
        response.text = 'hello, world'
        mock_get.return_value = response

        parsed = Mock()
        mock_parse.return_value = parsed

        assert_that(consumer.get_oembed_response('http://example.com/'), equal_to(parsed))

        mock_get_url.assert_called_with('http://example.com/', max_width = None, max_height = None)
        mock_get.assert_called_with('http://example.com/oembed?format=json')
        mock_parse.assert_called_with('json', 'hello, world')

def test_should_discover_and_get_oembed_url_with_max_width_and_height():
    with patch('rembed.discovery.get_oembed_url') as mock_get_url, \
         patch('rembed.parse.parse_oembed') as mock_parse, \
         patch('requests.get') as mock_get:

        mock_get_url.return_value = ('json', 'http://example.com/oembed?format=json&maxwidth=100&maxheight=200')

        response = Mock()
        response.ok = True
        response.text = 'hello, world'
        mock_get.return_value = response

        parsed = Mock()
        mock_parse.return_value = parsed

        assert_that(consumer.get_oembed_response('http://example.com/', 100, 200), equal_to(parsed))

        mock_get_url.assert_called_with('http://example.com/', max_width = 100, max_height = 200)
        mock_get.assert_called_with('http://example.com/oembed?format=json&maxwidth=100&maxheight=200')
        mock_parse.assert_called_with('json', 'hello, world')

def test_should_raise_error_on_request_error():
    with patch('rembed.discovery.get_oembed_url') as mock_get_url, \
         patch('requests.get') as mock_get, \
         pytest.raises(consumer.REmbedConsumerError):

        mock_get_url.return_value = ('json', 'http://example.com/oembed?format=json')

        response = Mock()
        response.ok = False
        response.text = 'hello, world'
        mock_get.return_value = response

        consumer.get_oembed_response('http://example.com/')

def test_should_embed():
    with patch('rembed.consumer.get_oembed_response') as mock_get_response:
        response = Mock()
        response.embed = lambda embed_url : '<h1>hello</h1>'
        mock_get_response.return_value = response

        assert_that(consumer.embed('http://example.com/'), equal_to('<h1>hello</h1>'))

        mock_get_response.assert_called_with('http://example.com/', None, None)

def test_should_embed_with_max_width_and_height():
    with patch('rembed.consumer.get_oembed_response') as mock_get_response:
        response = Mock()
        response.embed = lambda embed_url : '<h1>hello</h1>'
        mock_get_response.return_value = response

        assert_that(consumer.embed('http://example.com/', 100, 200), equal_to('<h1>hello</h1>'))

        mock_get_response.assert_called_with('http://example.com/', 100, 200)