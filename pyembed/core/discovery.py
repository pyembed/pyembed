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

import functools
import re
from collections import OrderedDict

from bs4 import BeautifulSoup
from pkg_resources import resource_filename
import requests
import yaml

from pyembed.core.error import PyEmbedError


try:  # pragma: no cover
    from urlparse import parse_qsl, urljoin, urlsplit, urlunsplit
    from urllib import urlencode
except ImportError:  # pragma: no cover
    from urllib.parse import parse_qsl, urljoin, urlsplit, urlunsplit, urlencode

from itertools import product

MEDIA_TYPES = {
    'json': 'application/json+oembed',
    'xml': 'text/xml+oembed'
}

FORMATS = {MEDIA_TYPES[oembed_format]: oembed_format for oembed_format in MEDIA_TYPES}


class PyEmbedDiscoveryError(PyEmbedError):
    """Thrown if there is an error discovering an OEmbed URL."""


class PyEmbedDiscoverer(object):
    """Base class for discovering OEmbed URLs."""

    def get_oembed_url(self, url, oembed_format=None):  # pragma: no cover
        """Retrieves the OEmbed URL for a given resource.

        Deprecated - use get_oembed_urls instead.

        :param url: resource URL.
        :param oembed_format: if supplied, restricts the format to use for OEmbed.  If
                       None, then the first URL found will be used.  One of
                       'json', 'xml'.

        :returns: the OEmbed URL for the resource.
        :raises PyEmbedDiscoveryError: if there is an error getting the OEmbed URL.
        """
        urls = self.get_oembed_urls(url, oembed_format)

        if not urls:
            raise PyEmbedDiscoveryError(
                'Could not find OEmbed URL for %s' % url)

        return urls[0]

    def get_oembed_urls(self, url, oembed_format=None):
        """Retrieves the OEmbed URLs for a given resource.

        :param url: resource URL.
        :param oembed_format: if supplied, restricts the format to use for OEmbed.  If
                       None, then the first URL found will be used.  One of
                       'json', 'xml'.

        :returns: a list of OEmbed URLs for the resource.
        :raises PyEmbedDiscoveryError: if there is an error getting the OEmbed URLs.
        """
        raise NotImplementedError(
            'No get_oembed_urls method for discoverer of type %s' % type(self).__name__)


class AutoDiscoverer(PyEmbedDiscoverer):
    """Discoverer that tries to automatically find the OEmbed URL within the
    HTML page.
    """

    def get_oembed_urls(self, url, oembed_format=None):
        media_type = self.__get_type(oembed_format)

        response = requests.get(url)

        if not response.ok:
            return []

        soup = BeautifulSoup(response.text)
        links = soup.find_all('link', type=media_type, href=True)

        return [urljoin(url, link['href']) for link in links]

    @staticmethod
    def __get_type(oembed_format):
        if not oembed_format:
            return list(MEDIA_TYPES.values())
        elif oembed_format in MEDIA_TYPES:
            return MEDIA_TYPES[oembed_format]

        raise PyEmbedDiscoveryError(
            'Invalid format %s specified (must be json or xml)' % oembed_format)


class StaticDiscoverer(PyEmbedDiscoverer):
    """Discoverer that uses a YAML file to discover the OEmbed URL.
    """

    def __init__(self, config_file):
        with open(config_file) as f:
            self.endpoints = [StaticDiscoveryEndpoint(e)
                              for e in yaml.load(f.read())]

    def get_oembed_urls(self, url, oembed_format=None):
        if oembed_format and oembed_format not in MEDIA_TYPES:
            raise PyEmbedDiscoveryError(
                'Invalid format %s specified (must be json or xml)' % oembed_format)

        formats = [oembed_format] if oembed_format else MEDIA_TYPES.keys()

        return [e.build_oembed_url(url, f)
                for (e, f) in product(self.endpoints, formats)
                if e.matches(url, f)]


class StaticDiscoveryEndpoint(object):
    """Applies static discovery rules for a single endpoint.
    """

    def __init__(self, endpoint):
        self.matchers = [self.__create_matcher(s)
                         for s in self.__extract_schemes(endpoint)]
        self.endpoint = self.__extract_endpoint(endpoint)
        self.oembed_format = endpoint.get('format')

    def matches(self, url, oembed_format=None):
        if not self.__format_matches(oembed_format):
            return False

        return any((matcher(url) for matcher in self.matchers))

    def build_oembed_url(self, content_url, oembed_format=None):
        selected_format = oembed_format or self.oembed_format
        format_endpoint = self.__add_format_to_endpoint(selected_format)
        scheme, netloc, path, query_string, fragment = urlsplit(
            format_endpoint)
        query_params = parse_qsl(query_string)
        query_params.append(('url', content_url))

        if selected_format:
            query_params.append(('format', selected_format))

        new_query_string = urlencode(query_params, doseq=True)
        return urlunsplit((scheme, netloc, path, new_query_string, fragment))

    @staticmethod
    def __extract_schemes(endpoint):
        result = endpoint.get('schemes')
        if not result:
            raise PyEmbedDiscoveryError(
                'Malformed discovery config (must specify schemes)')

        return result

    @staticmethod
    def __extract_endpoint(endpoint):
        result = endpoint.get('endpoint')
        if not result:
            raise PyEmbedDiscoveryError(
                'Malformed discovery config (must specify an endpoint)')

        return result

    def __create_matcher(self, scheme_url):
        scheme, netloc, path, query_string, fragment = urlsplit(scheme_url)
        netloc_regex = re.compile(netloc.replace('*.', '.*\.?'))
        path_regex = re.compile(path.replace('*', '.*'))

        return functools.partial(self.__matcher, netloc_regex, path_regex)

    @staticmethod
    def __matcher(netloc_regex, path_regex, url):
        scheme, netloc, path, query_string, fragment = urlsplit(url)
        return netloc_regex.match(netloc) and path_regex.match(path)

    def __format_matches(self, oembed_format):
        return (not oembed_format) or \
               (not self.oembed_format) or \
               (oembed_format == self.oembed_format)

    def __add_format_to_endpoint(self, oembed_format):
        target_format = oembed_format or 'json'
        return self.endpoint.replace('{format}', target_format)


class ChainingDiscoverer(PyEmbedDiscoverer):
    """Discoverer that delegates to a sequence of other discoverers, returning
    the first valid result."""

    def __init__(self, delegates):
        self.delegates = delegates

    def get_oembed_urls(self, url, oembed_format=None):
        return list(OrderedDict.fromkeys(self.__generate(url, oembed_format)))

    def __generate(self, url, oembed_format):
        for delegate in self.delegates:
            try:
                for oembed_url in delegate.get_oembed_urls(url, oembed_format):
                    yield oembed_url
            except PyEmbedDiscoveryError:
                pass


class DefaultDiscoverer(ChainingDiscoverer):
    """Discoverer that uses auto-discovery, followed by the included config
    file."""

    def __init__(self):
        super(DefaultDiscoverer, self).__init__([
            AutoDiscoverer(),
            StaticDiscoverer(
                resource_filename(__name__, 'config/endpoints.yml'))
        ])
