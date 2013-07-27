from rembed import discovery, parse, REmbedError

import requests

class REmbedConsumerError(REmbedError):
    """Thrown if there is an error discovering an OEmbed URL."""

def embed(url):
    """Returns an HTML representation of a resource, given a URL.  This can be
       directly embedded in a web page.

    :param url: the content URL
    :returns: an HTML representation of the resource.
    :raises REmbedError: if there is an error fetching the response.
    """
    return get_oembed_response(url).embed(url)

def get_oembed_response(url):
    """Fetches an OEmbed response for a given content URL.

    :param url: the content URL
    :returns: an REmbedResponse, representing the resource to embed.
    :raises REmbedError: if there is an error fetching the response.
    """

    (discovered_format, oembed_url) = discovery.get_oembed_url(url)
    response = requests.get(oembed_url)

    if not response.ok:
        raise REmbedConsumerError('Failed to get %s (status code %s)' % (url, response.status_code))

    return parse.parse_oembed(discovered_format, response.text)