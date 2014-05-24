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

from pyembed.core.error import PyEmbedError

from bs4 import BeautifulSoup
import functools
import re
import requests
import yaml

try:  # pragma: no cover
    from urlparse import parse_qsl, urljoin, urlsplit, urlunsplit
    from urllib import urlencode
except ImportError:  # pragma: no cover
    from urllib.parse import parse_qsl, urljoin, urlsplit, urlunsplit, urlencode

MEDIA_TYPES = {
    'json': 'application/json+oembed',
    'xml': 'text/xml+oembed'
}

FORMATS = {MEDIA_TYPES[format]: format for format in MEDIA_TYPES}


class PyEmbedDiscoveryError(PyEmbedError):

    """Thrown if there is an error discovering an OEmbed URL."""


class PyEmbedDiscoverer(object):

    """Base class for discovering OEmbed URLs."""

    def get_oembed_url(self, url, format=None):
        """Retrieves the OEmbed URL for a given resource.

        :param url: resource URL.
        :param format: if supplied, restricts the format to use for OEmbed.  If
                       None, then the first URL found will be used.  One of
                       'json', 'xml'.

        :returns: the OEmbed URL for the resource.
        :raises PyEmbedDiscoveryError: if there is an error getting the OEmbed URL.
        """
        raise NotImplementedError(
            'No get_oembed_url method for discoverer of type %s' % type(self).__name__)


class AutoDiscoverer(PyEmbedDiscoverer):

    """Discoverer that tries to automatically find the OEmbed URL within the 
    HTML page.
    """

    def get_oembed_url(self, url, format=None):
        media_type = self.__get_type(format)

        response = requests.get(url)

        if not response.ok:
            raise PyEmbedDiscoveryError(
                'Failed to get %s (status code %s)' % (url, response.status_code))

        soup = BeautifulSoup(response.text)
        link = soup.find('link', type=media_type, href=True)

        if not link:
            raise PyEmbedDiscoveryError(
                'Could not find OEmbed URL for %s' % url)

        return urljoin(url, link['href'])

    def __get_type(self, format):
        if not format:
            return list(MEDIA_TYPES.values())
        elif format in MEDIA_TYPES:
            return MEDIA_TYPES[format]

        raise PyEmbedDiscoveryError(
            'Invalid format %s specified (must be json or xml)' % format)


class StaticDiscoverer(PyEmbedDiscoverer):

    """Discoverer that uses a YAML file to discover the OEmbed URL.
    """

    def __init__(self, file):
        with open(file) as f:
            self.endpoints = [StaticDiscoveryEndpoint(e)
                              for e in yaml.load(f.read())]

    def get_oembed_url(self, url, oembed_format=None):
        if oembed_format and oembed_format not in MEDIA_TYPES:
            raise PyEmbedDiscoveryError(
                'Invalid format %s specified (must be json or xml)' % oembed_format)

        for endpoint in self.endpoints:
            if endpoint.matches(url, oembed_format):
                return endpoint.build_oembed_url(url, oembed_format)

        raise PyEmbedDiscoveryError('Did not find OEmbed URL for %s' % url)


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
        scheme, netloc, path, query_string, fragment = urlsplit(self.endpoint)
        query_params = parse_qsl(query_string)
        query_params.append(('url', content_url))

        if (oembed_format):
            query_params.append(('format', oembed_format))

        new_query_string = urlencode(query_params, doseq=True)
        return urlunsplit((scheme, netloc, path, new_query_string, fragment))

    def __extract_schemes(self, endpoint):
        result = endpoint.get('schemes')
        if not result:
            raise PyEmbedDiscoveryError(
                'Malformed discovery config (must specify schemes)')

        return result

    def __extract_endpoint(self, endpoint):
        result = endpoint.get('endpoint')
        if not result:
            raise PyEmbedDiscoveryError(
                'Malformed discovery config (must specify an endpoint)')

        return result

    def __create_matcher(self, scheme):
        regex = re.compile(scheme.replace('*', '.*'))
        return functools.partial(self.__matcher, regex)

    def __matcher(self, regex, url):
        return regex.match(url)

    def __format_matches(self, oembed_format):
        return (not oembed_format) or \
            (not self.oembed_format) or \
            (oembed_format == self.oembed_format)
