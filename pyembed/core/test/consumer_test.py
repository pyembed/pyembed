# The MIT License(MIT)

# Copyright (c) 2013-2014 Matt Thomson

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pyembed.core import consumer

from hamcrest import assert_that, equal_to
from mock import patch, Mock

import pytest


def test_should_discover_and_get_oembed_url():
    with patch('pyembed.core.discovery.get_oembed_url') as mock_get_url, \
        patch('pyembed.core.parse.parse_oembed') as mock_parse, \
            patch('requests.get') as mock_get:

        mock_get_url.return_value = (
            'json', 'http://example.com/oembed?format=json')

        response = Mock()
        response.ok = True
        response.text = 'hello, world'
        mock_get.return_value = response

        parsed = Mock()
        mock_parse.return_value = parsed

        assert_that(consumer.get_oembed_response(
            'http://example.com/'), equal_to(parsed))

        mock_get_url.assert_called_with(
            'http://example.com/', max_width=None, max_height=None)
        mock_get.assert_called_with('http://example.com/oembed?format=json')
        mock_parse.assert_called_with('json', 'hello, world')


def test_should_discover_and_get_oembed_url_with_max_width_and_height():
    with patch('pyembed.core.discovery.get_oembed_url') as mock_get_url, \
        patch('pyembed.core.parse.parse_oembed') as mock_parse, \
            patch('requests.get') as mock_get:

        mock_get_url.return_value = (
            'json',
            'http://example.com/oembed?format=json&maxwidth=100&maxheight=200')

        response = Mock()
        response.ok = True
        response.text = 'hello, world'
        mock_get.return_value = response

        parsed = Mock()
        mock_parse.return_value = parsed

        assert_that(consumer.get_oembed_response(
            'http://example.com/', 100, 200), equal_to(parsed))

        mock_get_url.assert_called_with(
            'http://example.com/', max_width=100, max_height=200)
        mock_get.assert_called_with(
            'http://example.com/oembed?format=json&maxwidth=100&maxheight=200')
        mock_parse.assert_called_with('json', 'hello, world')


def test_should_raise_error_on_request_error():
    with patch('pyembed.core.discovery.get_oembed_url') as mock_get_url, \
        patch('requests.get') as mock_get, \
            pytest.raises(consumer.PyEmbedConsumerError):

        mock_get_url.return_value = (
            'json', 'http://example.com/oembed?format=json')

        response = Mock()
        response.ok = False
        response.text = 'hello, world'
        mock_get.return_value = response

        consumer.get_oembed_response('http://example.com/')


def test_should_embed():
    with patch('pyembed.core.consumer.get_oembed_response') as mock_get:
        response = Mock()
        response.type = 'rich'
        response.html = '<h1>hello</h1>'

        mock_get.return_value = response

        result = consumer.embed('http://example.com/')
        assert_that(result, equal_to('<h1>hello</h1>'))

        mock_get.assert_called_with('http://example.com/', None, None)


def test_should_embed_with_max_width_and_height():
    with patch('pyembed.core.consumer.get_oembed_response') as mock_get:
        response = Mock()
        response.type = 'rich'
        response.html = '<h1>hello</h1>'

        mock_get.return_value = response

        result = consumer.embed('http://example.com/', 100, 200)
        assert_that(result, equal_to('<h1>hello</h1>'))

        mock_get.assert_called_with('http://example.com/', 100, 200)


def test_should_embed_with_custom_renderer():
    with patch('pyembed.core.consumer.get_oembed_response') as mock_get:
        response = Mock()
        response.type = 'rich'
        response.html = '<h1>hello</h1>'

        renderer = Mock()
        renderer.render = lambda content_url, response: '<h1>hi</h1>'

        mock_get.return_value = response

        result = consumer.embed('http://example.com/', 100, 200, renderer)
        assert_that(result, equal_to('<h1>hi</h1>'))

        mock_get.assert_called_with('http://example.com/', 100, 200)
