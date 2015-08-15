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

from mock import patch, Mock
import pytest

from pyembed.core import discovery
import json


def test_should_find_oembed_urls():
    response = Mock()
    response.ok = True

    with open('pyembed/core/test/fixtures/static_discovery/valid.json') as f:
        response.json.return_value = json.load(f)

    with patch('requests.get') as mock_get:
        mock_get.return_value = response

        discoverer = discovery.UrlDiscoverer('http://example.com/providers.json')
        result = discoverer.get_oembed_urls('http://example.com/simple/123')
        assert set(result) == {
            'http://example.com/simple/oembed?url=http%3A%2F%2Fexample.com%2Fsimple%2F123&format=xml',
            'http://example.com/simple/oembed?url=http%3A%2F%2Fexample.com%2Fsimple%2F123&format=json'
        }

        mock_get.assert_called_with('http://example.com/providers.json')


def test_should_raise_if_error_reading_url():
    response = Mock()
    response.ok = False
    response.status_code = 404

    with patch('requests.get') as mock_get, \
        pytest.raises(discovery.PyEmbedDiscoveryError):
        mock_get.return_value = response

        discovery.UrlDiscoverer('http://example.com/providers.json')
