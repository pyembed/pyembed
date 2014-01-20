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

import requests
from bs4 import BeautifulSoup

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


def get_oembed_url(url, format=None, max_width=None, max_height=None):
    """Retrieves the OEmbed URL for a given resource.

    :param url: resource URL.
    :param format: if supplied, restricts the format to use for OEmbed.  If
                   None, then the first URL found will be used.  One of
                   'json', 'xml'.
    :param max_width: (optional) the maximum width of the embedded resource.
    :param max_height: (optional) the maximum height of the embedded resource.

    :returns: OEmbed URL for the resource.
    :raises PyEmbedDiscoveryError: if there is an error getting the OEmbed URL.
    """
    media_type = __get_type(format)

    response = requests.get(url)

    if not response.ok:
        raise PyEmbedDiscoveryError(
            'Failed to get %s (status code %s)' % (url, response.status_code))

    soup = BeautifulSoup(response.text)
    link = soup.find('link', type=media_type, href=True)

    if not link:
        raise PyEmbedDiscoveryError('Could not find OEmbed URL for %s' % url)

    discovered_url = __format_url(url, link['href'], max_width, max_height)

    return (FORMATS[link['type']], discovered_url)


def __get_type(format):
    if not format:
        return list(MEDIA_TYPES.values())
    elif format in MEDIA_TYPES:
        return MEDIA_TYPES[format]

    raise PyEmbedDiscoveryError(
        'Invalid format %s specified (must be json or xml)' % format)


def __format_url(content_url, embed_url, max_width=None, max_height=None):
    url = urljoin(content_url, embed_url)
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qsl(query_string)

    if max_width is not None:
        query_params.append(('maxwidth', max_width))

    if max_height:
        query_params.append(('maxheight', max_height))

    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))
