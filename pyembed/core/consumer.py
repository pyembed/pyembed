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

from pyembed.core import discovery, parse
from pyembed.core.error import PyEmbedError

import requests


class PyEmbedConsumerError(PyEmbedError):

    """Thrown if there is an error discovering an OEmbed URL."""


def get_oembed_response(url, max_width=None, max_height=None):
    """Fetches an OEmbed response for a given content URL.

    :param url: the content URL.
    :param max_width: (optional) the maximum width of the embedded resource.
    :param max_height: (optional) the maximum height of the embedded resource.
    :returns: an PyEmbedResponse, representing the resource to embed.
    :raises PyEmbedError: if there is an error fetching the response.
    """

    (discovered_format, oembed_url) = discovery.get_oembed_url(
        url, max_width=max_width, max_height=max_height)
    response = requests.get(oembed_url)

    if not response.ok:
        raise PyEmbedConsumerError('Failed to get %s (status code %s)' % (
            url, response.status_code))

    return parse.parse_oembed(discovered_format, response.text)
