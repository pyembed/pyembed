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

import pytest

from pyembed.core import discovery


def test_should_find_oembed_urls():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/simple/123')
    assert list(result) == [
        'http://example.com/simple/oembed?url=http%3A%2F%2Fexample.com%2Fsimple%2F123&format=json',
        'http://example.com/simple/oembed?url=http%3A%2F%2Fexample.com%2Fsimple%2F123&format=xml'
    ]


def test_should_find_oembed_urls_for_json():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/simple/123', 'json')
    assert list(result) == \
        ['http://example.com/simple/oembed?url=http%3A%2F%2Fexample.com%2Fsimple%2F123&format=json']


def test_should_find_oembed_urls_for_xml():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/simple/123', 'xml')
    assert list(result) == \
        ['http://example.com/simple/oembed?url=http%3A%2F%2Fexample.com%2Fsimple%2F123&format=xml']


def test_should_not_find_oembed_urls_for_unknown_url():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/rubbish/123')
    assert list(result) == []


def test_should_find_oembed_urls_when_only_json_allowed():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/json/123')
    assert list(result) == \
        ['http://example.com/json/oembed?url=http%3A%2F%2Fexample.com%2Fjson%2F123&format=json']


def test_should_find_oembed_urls_for_json_when_only_json_allowed():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/json/123', 'json')
    assert list(result) == \
        ['http://example.com/json/oembed?url=http%3A%2F%2Fexample.com%2Fjson%2F123&format=json']


def test_should_not_find_oembed_urls_for_xml_when_only_json_allowed():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/json/123', 'xml')
    assert list(result) == []


def test_should_find_oembed_urls_when_only_xml_allowed():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/xml/123')
    assert list(result) == \
        ['http://example.com/xml/oembed?url=http%3A%2F%2Fexample.com%2Fxml%2F123&format=xml']


def test_should_find_oembed_urls_for_xml_when_only_xml_allowed():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/xml/123', 'xml')
    assert list(result) == \
        ['http://example.com/xml/oembed?url=http%3A%2F%2Fexample.com%2Fxml%2F123&format=xml']


def test_should_not_find_oembed_urls_for_json_when_only_xml_allowed():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/xml/123', 'json')
    assert list(result) == []


def test_should_find_oembed_urls_when_split_by_format():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/split/123')

    assert list(result) == [
        'http://example.com/split_xml/oembed?url=http%3A%2F%2Fexample.com%2Fsplit%2F123&format=xml',
        'http://example.com/split_json/oembed?url=http%3A%2F%2Fexample.com%2Fsplit%2F123&format=json'
    ]


def test_should_find_oembed_urls_for_json_when_split_by_format():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/split/123', 'json')
    assert list(result) == [
        'http://example.com/split_json/oembed?url=http%3A%2F%2Fexample.com%2Fsplit%2F123&format=json'
    ]


def test_should_find_oembed_urls_for_xml_when_split_by_format():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/split/123', 'xml')
    assert list(result) == \
        ['http://example.com/split_xml/oembed?url=http%3A%2F%2Fexample.com%2Fsplit%2F123&format=xml']


def test_should_find_oembed_urls_when_format_in_endpoint():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/format/123')
    assert list(result) == [
        'http://example.com/format/oembed.json?url=http%3A%2F%2Fexample.com%2Fformat%2F123&format=json',
        'http://example.com/format/oembed.xml?url=http%3A%2F%2Fexample.com%2Fformat%2F123&format=xml'
    ]


def test_should_find_oembed_urls_for_json_when_format_in_endpoint():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/format/123', 'json')
    assert list(result) == \
        ['http://example.com/format/oembed.json?url=http%3A%2F%2Fexample.com%2Fformat%2F123&format=json']


def test_should_find_oembed_urls_for_xml_when_format_in_endpoint():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/format/123', 'xml')
    assert list(result) == \
        ['http://example.com/format/oembed.xml?url=http%3A%2F%2Fexample.com%2Fformat%2F123&format=xml']


def test_should_find_oembed_urls_for_subdomain_wildcard_without_subdomain():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://example.com/sub/123')
    assert list(result) == [
        'http://example.com/sub/oembed?url=http%3A%2F%2Fexample.com%2Fsub%2F123&format=json',
        'http://example.com/sub/oembed?url=http%3A%2F%2Fexample.com%2Fsub%2F123&format=xml'
    ]


def test_should_find_oembed_urls_for_subdomain_wildcard_with_subdomain():
    discoverer = discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/valid.json')
    result = discoverer.get_oembed_urls('http://www.example.com/sub/123')
    assert list(result) == [
        'http://example.com/sub/oembed?url=http%3A%2F%2Fwww.example.com%2Fsub%2F123&format=json',
        'http://example.com/sub/oembed?url=http%3A%2F%2Fwww.example.com%2Fsub%2F123&format=xml'
    ]


def test_should_not_find_oembed_urls_for_bad_format():
    with pytest.raises(discovery.PyEmbedDiscoveryError):
        discoverer = discovery.FileDiscoverer(
            'pyembed/core/test/fixtures/static_discovery/valid.json')
        next(discoverer.get_oembed_urls('http://example.com/simple/123', 'yaml'))


def test_should_cope_with_no_endpoint():
    discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/no_endpoint.json')


def test_should_throw_if_no_schemes():
    discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/no_schemes.json')


def test_should_throw_if_empty_schemes():
    discovery.FileDiscoverer(
        'pyembed/core/test/fixtures/static_discovery/empty_schemes.json')
