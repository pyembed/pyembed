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


def test_should_find_oembed_urls():
    expected_urls = [
        'http://example.com/oembed?format=json',
        'http://example.com/oembed?format=xml'
    ]

    assert get_oembed_urls() == expected_urls


def test_should_find_oembed_urls_using_json_when_specified():
    expected_url = 'http://example.com/oembed?format=json'
    assert get_oembed_urls(oembed_format='json') == [expected_url]


def test_should_find_oembed_urls_using_xml_when_specified():
    expected_url = 'http://example.com/oembed?format=xml'
    assert get_oembed_urls(oembed_format='xml') == [expected_url]


def test_should_return_xml_if_json_not_present():
    expected_url = 'http://example.com/oembed?format=xml'
    assert get_oembed_urls(fixture='no_json_oembed.html') == [expected_url]


def test_should_find_oembed_urls_using_json_with_relative_url():
    expected_url = 'http://example.com/oembed?format=json'
    assert get_oembed_urls(fixture='relative_url.html', oembed_format='json') == [expected_url]


def test_should_find_oembed_urls_using_xml_with_relative_url():
    expected_url = 'http://example.com/oembed?format=xml'
    assert get_oembed_urls(fixture='relative_url.html', oembed_format='xml') == [expected_url]


def test_should_return_empty_if_href_not_present():
    assert get_oembed_urls(fixture='json_oembed_no_href.html') == []


def test_should_return_empty_for_invalid_html():
    assert get_oembed_urls(fixture='invalid.html') == []


def test_should_return_empty_on_error_response():
    assert get_oembed_urls(ok=False) == []


def test_should_throw_error_when_invalid_oembed_format_specified():
    with pytest.raises(discovery.PyEmbedDiscoveryError):
        get_oembed_urls(oembed_format='txt')


def get_oembed_urls(fixture='valid_oembed.html',
                   oembed_format=None,
                   ok=True):
    with patch('requests.get') as mock_get:
        response = Mock()
        response.ok = ok
        response.text = open(
            'pyembed/core/test/fixtures/auto_discovery/' + fixture).read()
        mock_get.return_value = response

        result = list(discovery.AutoDiscoverer().get_oembed_urls(
            'http://example.com', oembed_format))

        mock_get.assert_called_with('http://example.com')
        return result
