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

from mock import Mock

from pyembed.core import discovery


def test_should_return_both_if_valid():
    discoverer1 = Mock()
    discoverer1.get_oembed_urls.return_value = ['http://example.com/oembed1?format=json']

    discoverer2 = Mock()
    discoverer2.get_oembed_urls.return_value = [
        'http://example.com/oembed2?format=json',
        'http://example.com/oembed2?format=xml'
    ]

    discoverer = discovery.ChainingDiscoverer([discoverer1, discoverer2])

    result = discoverer.get_oembed_urls('http://example.com')
    assert list(result) == [
        'http://example.com/oembed1?format=json',
        'http://example.com/oembed2?format=json',
        'http://example.com/oembed2?format=xml'
    ]

    discoverer1.get_oembed_urls.assert_called_with('http://example.com', None)
    discoverer2.get_oembed_urls.assert_called_with('http://example.com', None)


def test_should_remove_duplicates():
    discoverer1 = Mock()
    discoverer1.get_oembed_urls.return_value = ['http://example.com/oembed?format=json']

    discoverer2 = Mock()
    discoverer2.get_oembed_urls.return_value = [
        'http://example.com/oembed?format=json',
        'http://example.com/oembed?format=xml'
    ]

    discoverer = discovery.ChainingDiscoverer([discoverer1, discoverer2])

    result = discoverer.get_oembed_urls('http://example.com')
    assert list(result) == [
        'http://example.com/oembed?format=json',
        'http://example.com/oembed?format=xml'
    ]

    discoverer1.get_oembed_urls.assert_called_with('http://example.com', None)
    discoverer2.get_oembed_urls.assert_called_with('http://example.com', None)


def test_should_continue_if_first_throws():
    discoverer1 = Mock()
    discoverer1.get_oembed_urls.side_effect = discovery.PyEmbedDiscoveryError

    discoverer2 = Mock()
    discoverer2.get_oembed_urls.return_value = ['http://example.com/oembed?format=json']

    discoverer = discovery.ChainingDiscoverer([discoverer1, discoverer2])

    result = discoverer.get_oembed_urls('http://example.com')
    assert list(result) == ['http://example.com/oembed?format=json']

    discoverer1.get_oembed_urls.assert_called_with('http://example.com', None)
    discoverer2.get_oembed_urls.assert_called_with('http://example.com', None)


def test_should_return_empty_if_all_throw():
    discoverer1 = Mock()
    discoverer1.get_oembed_urls.side_effect = discovery.PyEmbedDiscoveryError

    discoverer2 = Mock()
    discoverer2.get_oembed_urls.side_effect = discovery.PyEmbedDiscoveryError

    discoverer = discovery.ChainingDiscoverer([discoverer1, discoverer2])

    result = discoverer.get_oembed_urls('http://example.com')
    assert list(result) == []

    discoverer1.get_oembed_urls.assert_called_with('http://example.com', None)
    discoverer2.get_oembed_urls.assert_called_with('http://example.com', None)
