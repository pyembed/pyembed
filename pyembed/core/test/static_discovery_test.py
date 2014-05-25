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


def test_should_find_oembed_url():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/simple/123')
    assert_that(result, equal_to(
        'http://example.com/simple/oembed?url=http%3A%2F%2Fexample.com%2Fsimple%2F123'))


def test_should_find_oembed_url_for_json():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/simple/123', 'json')
    assert_that(result, equal_to(
        'http://example.com/simple/oembed?url=http%3A%2F%2Fexample.com%2Fsimple%2F123&format=json'))


def test_should_find_oembed_url_for_xml():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/simple/123', 'xml')
    assert_that(result, equal_to(
        'http://example.com/simple/oembed?url=http%3A%2F%2Fexample.com%2Fsimple%2F123&format=xml'))


def test_should_not_find_oembed_url_for_bad_format():
    with pytest.raises(discovery.PyEmbedDiscoveryError):
        discoverer = discovery.StaticDiscoverer(
            'pyembed/core/test/fixtures/static_discovery/valid.yml')
        discoverer.get_oembed_url('http://example.com/simple/123', 'yaml')


def test_should_not_find_oembed_url_for_unknown_url():
    with pytest.raises(discovery.PyEmbedDiscoveryError):
        discoverer = discovery.StaticDiscoverer(
            'pyembed/core/test/fixtures/static_discovery/valid.yml')
        discoverer.get_oembed_url('http://example.com/rubbish/123')


def test_should_find_oembed_url_when_only_json_allowed():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/json/123')
    assert_that(result, equal_to(
        'http://example.com/json/oembed?url=http%3A%2F%2Fexample.com%2Fjson%2F123&format=json'))


def test_should_find_oembed_url_for_json_when_only_json_allowed():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/json/123', 'json')
    assert_that(result, equal_to(
        'http://example.com/json/oembed?url=http%3A%2F%2Fexample.com%2Fjson%2F123&format=json'))


def test_should_not_find_oembed_url_for_xml_when_only_json_allowed():
    with pytest.raises(discovery.PyEmbedDiscoveryError):
        discoverer = discovery.StaticDiscoverer(
            'pyembed/core/test/fixtures/static_discovery/valid.yml')
        discoverer.get_oembed_url('http://example.com/json/123', 'xml')


def test_should_find_oembed_url_when_only_xml_allowed():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/xml/123')
    assert_that(result, equal_to(
        'http://example.com/xml/oembed?url=http%3A%2F%2Fexample.com%2Fxml%2F123&format=xml'))


def test_should_find_oembed_url_for_xml_when_only_xml_allowed():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/xml/123', 'xml')
    assert_that(result, equal_to(
        'http://example.com/xml/oembed?url=http%3A%2F%2Fexample.com%2Fxml%2F123&format=xml'))


def test_should_not_find_oembed_url_for_json_when_only_xml_allowed():
    with pytest.raises(discovery.PyEmbedDiscoveryError):
        discoverer = discovery.StaticDiscoverer(
            'pyembed/core/test/fixtures/static_discovery/valid.yml')
        discoverer.get_oembed_url('http://example.com/xml/123', 'json')


def test_should_find_oembed_url_when_split_by_format():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/split/123')
    assert_that(result, equal_to(
        'http://example.com/split_json/oembed?url=http%3A%2F%2Fexample.com%2Fsplit%2F123&format=json'))


def test_should_find_oembed_url_for_json_when_split_by_format():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/split/123', 'json')
    assert_that(result, equal_to(
        'http://example.com/split_json/oembed?url=http%3A%2F%2Fexample.com%2Fsplit%2F123&format=json'))


def test_should_find_oembed_url_for_xml_when_split_by_format():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/split/123', 'xml')
    assert_that(result, equal_to(
        'http://example.com/split_xml/oembed?url=http%3A%2F%2Fexample.com%2Fsplit%2F123&format=xml'))


def test_should_find_oembed_url_when_format_in_endpoint():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/format/123')
    assert_that(result, equal_to(
        'http://example.com/format/oembed.json?url=http%3A%2F%2Fexample.com%2Fformat%2F123'))


def test_should_find_oembed_url_for_json_when_format_in_endpoint():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/format/123', 'json')
    assert_that(result, equal_to(
        'http://example.com/format/oembed.json?url=http%3A%2F%2Fexample.com%2Fformat%2F123&format=json'))


def test_should_find_oembed_url_for_xml_when_format_in_endpoint():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/format/123', 'xml')
    assert_that(result, equal_to(
        'http://example.com/format/oembed.xml?url=http%3A%2F%2Fexample.com%2Fformat%2F123&format=xml'))


def test_should_find_oembed_url_for_subdomain_wildcard_without_subdomain():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://example.com/sub/123')
    assert_that(result, equal_to(
        'http://example.com/sub/oembed?url=http%3A%2F%2Fexample.com%2Fsub%2F123'))


def test_should_find_oembed_url_for_subdomain_wildcard_with_subdomain():
    discoverer = discovery.StaticDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.yml')
    result = discoverer.get_oembed_url('http://www.example.com/sub/123')
    assert_that(result, equal_to(
        'http://example.com/sub/oembed?url=http%3A%2F%2Fwww.example.com%2Fsub%2F123'))


def test_should_throw_if_no_endpoint():
    with pytest.raises(discovery.PyEmbedDiscoveryError):
        discovery.StaticDiscoverer(
            'pyembed/core/test/fixtures/static_discovery/no_endpoint.yml')


def test_should_throw_if_no_schemes():
    with pytest.raises(discovery.PyEmbedDiscoveryError):
        discovery.StaticDiscoverer(
            'pyembed/core/test/fixtures/static_discovery/no_schemes.yml')


def test_should_throw_if_empty_schemes():
    with pytest.raises(discovery.PyEmbedDiscoveryError):
        discovery.StaticDiscoverer(
            'pyembed/core/test/fixtures/static_discovery/empty_schemes.yml')
