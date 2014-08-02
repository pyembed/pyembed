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

from hamcrest import assert_that, equal_to
from mock import patch, Mock
import pytest

from pyembed.core import consumer


def test_should_discover_and_get_oembed_url():
    with patch('requests.get') as mock_get, \
            patch('pyembed.core.parse.parse_oembed') as mock_parse:
        result = __set_up_mocks(mock_get, mock_parse)

        assert_that(consumer.get_oembed_response(
            'http://example.com/oembed'), equal_to(result))

        mock_get.assert_called_with('http://example.com/oembed')
        mock_parse.assert_called_with('hello, world', 'application/json')


def test_should_discover_and_get_oembed_url_for_xml():
    with patch('requests.get') as mock_get, \
            patch('pyembed.core.parse.parse_oembed') as mock_parse:
        result = __set_up_mocks(mock_get, mock_parse, 'text/xml')

        assert_that(consumer.get_oembed_response(
            'http://example.com/oembed'), equal_to(result))

        mock_get.assert_called_with('http://example.com/oembed')
        mock_parse.assert_called_with('hello, world', 'text/xml')


def test_should_discover_and_get_oembed_url_with_charset():
    with patch('requests.get') as mock_get, \
            patch('pyembed.core.parse.parse_oembed') as mock_parse:
        result = __set_up_mocks(
            mock_get, mock_parse, 'application/json;charset=utf-8')

        assert_that(consumer.get_oembed_response(
            'http://example.com/oembed'), equal_to(result))

        mock_get.assert_called_with('http://example.com/oembed')
        mock_parse.assert_called_with('hello, world', 'application/json')


def test_should_add_max_width():
    with patch('requests.get') as mock_get, \
            patch('pyembed.core.parse.parse_oembed') as mock_parse:
        result = __set_up_mocks(mock_get, mock_parse)

        assert_that(consumer.get_oembed_response(
            'http://example.com/oembed', max_width=100), equal_to(result))

        mock_get.assert_called_with('http://example.com/oembed?maxwidth=100')
        mock_parse.assert_called_with('hello, world', 'application/json')


def test_should_add_max_height():
    with patch('requests.get') as mock_get, \
            patch('pyembed.core.parse.parse_oembed') as mock_parse:
        result = __set_up_mocks(mock_get, mock_parse)

        assert_that(consumer.get_oembed_response(
            'http://example.com/oembed', max_height=200), equal_to(result))

        mock_get.assert_called_with('http://example.com/oembed?maxheight=200')
        mock_parse.assert_called_with('hello, world', 'application/json')


def test_should_add_max_width_and_height():
    with patch('requests.get') as mock_get, \
            patch('pyembed.core.parse.parse_oembed') as mock_parse:
        result = __set_up_mocks(mock_get, mock_parse)

        assert_that(consumer.get_oembed_response(
            'http://example.com/oembed', max_width=100, max_height=200), equal_to(result))

        mock_get.assert_called_with(
            'http://example.com/oembed?maxwidth=100&maxheight=200')
        mock_parse.assert_called_with('hello, world', 'application/json')


def test_should_add_max_width_when_query_string_present():
    with patch('requests.get') as mock_get, \
            patch('pyembed.core.parse.parse_oembed') as mock_parse:
        result = __set_up_mocks(mock_get, mock_parse)

        assert_that(consumer.get_oembed_response(
            'http://example.com/oembed?format=json', max_width=100), equal_to(result))

        mock_get.assert_called_with(
            'http://example.com/oembed?format=json&maxwidth=100')
        mock_parse.assert_called_with('hello, world', 'application/json')


def test_should_add_max_height_when_query_string_present():
    with patch('requests.get') as mock_get, \
            patch('pyembed.core.parse.parse_oembed') as mock_parse:
        result = __set_up_mocks(mock_get, mock_parse)

        assert_that(consumer.get_oembed_response(
            'http://example.com/oembed?format=json', max_height=200), equal_to(result))

        mock_get.assert_called_with(
            'http://example.com/oembed?format=json&maxheight=200')
        mock_parse.assert_called_with('hello, world', 'application/json')


def test_should_add_max_width_and_height_when_query_string_present():
    with patch('requests.get') as mock_get, \
            patch('pyembed.core.parse.parse_oembed') as mock_parse:
        result = __set_up_mocks(mock_get, mock_parse)

        assert_that(consumer.get_oembed_response(
            'http://example.com/oembed?format=json', max_width=100, max_height=200), equal_to(result))

        mock_get.assert_called_with(
            'http://example.com/oembed?format=json&maxwidth=100&maxheight=200')
        mock_parse.assert_called_with('hello, world', 'application/json')


def test_should_raise_error_on_request_error():
    with patch('requests.get') as mock_get, \
            pytest.raises(consumer.PyEmbedConsumerError):
        response = Mock()
        response.ok = False
        response.text = 'hello, world'
        mock_get.return_value = response

        consumer.get_oembed_response('http://example.com/oembed')


def __set_up_mocks(mock_get, mock_parse, content_type='application/json'):
    response = Mock()
    response.ok = True
    response.text = 'hello, world'
    response.headers = {'content-type': content_type}

    mock_get.return_value = response

    parsed = Mock()
    mock_parse.return_value = parsed
    return parsed
