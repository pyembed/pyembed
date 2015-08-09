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

from requests.exceptions import RequestException

from pyembed.core import PyEmbed
from pyembed.core.error import PyEmbedError


def test_should_embed():
    with patch('pyembed.core.consumer.get_oembed_response') as mock_get:
        discoverer = Mock()
        discoverer.get_oembed_urls.return_value = ['http://example.com/oembed?format=json']

        response = Mock()
        mock_get.return_value = response

        renderer = Mock()
        renderer.render.return_value = '<h1>hi</h1>'

        result = PyEmbed(discoverer, renderer).embed('http://example.com/')
        assert_that(result, equal_to('<h1>hi</h1>'))

        discoverer.get_oembed_urls.assert_called_with('http://example.com/')
        mock_get.assert_called_with(
            'http://example.com/oembed?format=json', max_width=None, max_height=None)
        renderer.render.assert_called_with('http://example.com/', response)


def test_should_embed_xml():
    with patch('pyembed.core.consumer.get_oembed_response') as mock_get:
        discoverer = Mock()
        discoverer.get_oembed_urls.return_value = ['http://example.com/oembed?format=xml']

        response = Mock()
        mock_get.return_value = response

        renderer = Mock()
        renderer.render.return_value = '<h1>hi</h1>'

        result = PyEmbed(discoverer, renderer).embed('http://example.com/')
        assert_that(result, equal_to('<h1>hi</h1>'))

        discoverer.get_oembed_urls.assert_called_with('http://example.com/')
        mock_get.assert_called_with(
            'http://example.com/oembed?format=xml', max_width=None, max_height=None)
        renderer.render.assert_called_with('http://example.com/', response)


def test_should_embed_with_max_width_and_height():
    with patch('pyembed.core.consumer.get_oembed_response') as mock_get:
        discoverer = Mock()
        discoverer.get_oembed_urls.return_value = ['http://example.com/oembed?format=json']

        response = Mock()
        mock_get.return_value = response

        renderer = Mock()
        renderer.render.return_value = '<h1>hi</h1>'

        result = PyEmbed(discoverer, renderer).embed(
            'http://example.com/', 100, 200)
        assert_that(result, equal_to('<h1>hi</h1>'))

        discoverer.get_oembed_urls.assert_called_with('http://example.com/')
        mock_get.assert_called_with(
            'http://example.com/oembed?format=json', max_width=100, max_height=200)
        renderer.render.assert_called_with('http://example.com/', response)


def test_should_throw_error_on_request_error():
    with pytest.raises(PyEmbedError):
        discoverer = Mock()
        discoverer.get_oembed_urls.side_effect = RequestException()

        PyEmbed(discoverer, None).embed('http://example.com/', 100, 200)
