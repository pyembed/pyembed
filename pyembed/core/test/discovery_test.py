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

from pyembed.core import discovery

from hamcrest import assert_that, equal_to
from mock import patch, Mock
import pytest


def test_should_find_oembed_url_using_json_by_default():
    expected_url = 'http://example.com/oembed?format=json'
    assert_that(get_oembed_url(),
                equal_to(('json', expected_url)))


def test_should_find_oembed_url_using_json_when_specified():
    expected_url = 'http://example.com/oembed?format=json'
    assert_that(get_oembed_url(format='json'),
                equal_to(('json', expected_url)))


def test_should_find_oembed_url_using_xml_when_specified():
    expected_url = 'http://example.com/oembed?format=xml'
    assert_that(get_oembed_url(format='xml'),
                equal_to(('xml', expected_url)))


def test_should_return_xml_if_json_not_present():
    expected_url = 'http://example.com/oembed?format=xml'
    assert_that(get_oembed_url(fixture='no_json_oembed.html'),
                equal_to(('xml', expected_url)))


def test_should_add_max_width_when_query_string_present():
    expected_url = 'http://example.com/oembed?format=json&maxwidth=100'
    assert_that(get_oembed_url(max_width=100),
                equal_to(('json', expected_url)))


def test_should_add_max_height_when_query_string_present():
    expected_url = 'http://example.com/oembed?format=json&maxheight=200'
    assert_that(get_oembed_url(max_height=200),
                equal_to(('json', expected_url)))


def test_should_add_max_width_and_height_when_query_string_present():
    expected_url = \
        'http://example.com/oembed?format=json&maxwidth=100&maxheight=200'
    assert_that(get_oembed_url(max_width=100, max_height=200),
                equal_to(('json', expected_url)))


def test_should_add_max_width_when_no_query_string_present():
    expected_url = 'http://example.com/oembed?maxwidth=100'
    assert_that(
        get_oembed_url(fixture='no_query_string.html', max_width=100),
        equal_to(('json', expected_url)))


def test_should_add_max_height_when_no_query_string_present():
    expected_url = 'http://example.com/oembed?maxheight=200'
    assert_that(
        get_oembed_url(fixture='no_query_string.html', max_height=200),
        equal_to(('json', expected_url)))


def test_should_add_max_width_and_height_when_no_query_string_present():
    expected_url = 'http://example.com/oembed?maxwidth=100&maxheight=200'
    assert_that(
        get_oembed_url(
            fixture='no_query_string.html', max_width=100, max_height=200),
        equal_to(('json', expected_url)))


def test_should_find_oembed_url_using_json_with_relative_url():
    expected_url = 'http://example.com/oembed?format=json'
    assert_that(get_oembed_url(fixture='relative_url.html', format='json'),
                equal_to(('json', expected_url)))


def test_should_find_oembed_url_using_xml_with_relative_url():
    expected_url = 'http://example.com/oembed?format=xml'
    assert_that(get_oembed_url(fixture='relative_url.html', format='xml'),
                equal_to(('xml', expected_url)))


def test_should_throw_error_if_href_not_present():
    with pytest.raises(discovery.PyEmbedDiscoveryError):
        get_oembed_url(fixture='json_oembed_no_href.html')


def test_should_throw_error_for_invalid_html():
    with pytest.raises(discovery.PyEmbedDiscoveryError):
        get_oembed_url(fixture='invalid.html')


def test_should_throw_error_when_invalid_format_specified():
    with pytest.raises(discovery.PyEmbedDiscoveryError):
        get_oembed_url(format='txt')


def test_should_throw_error_on_error_response():
    with pytest.raises(discovery.PyEmbedDiscoveryError):
        get_oembed_url(ok=False)


def get_oembed_url(fixture='valid_oembed.html',
                   format=None,
                   max_width=None,
                   max_height=None,
                   ok=True):
    with patch('requests.get') as mock_get:
        response = Mock()
        response.ok = ok
        response.text = open(
            'pyembed/core/test/fixtures/discovery/' + fixture).read()
        mock_get.return_value = response

        result = discovery.AutoDiscoverer().get_oembed_url(
            'http://example.com', format, max_width, max_height)

        mock_get.assert_called_with('http://example.com')
        return result
