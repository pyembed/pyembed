from rembed import REmbedError

import requests
from bs4 import BeautifulSoup

MEDIA_TYPES = {
    'json' : 'application/json+oembed',
    'xml' : 'text/xml+oembed'
}

FORMATS = {v: k for k, v in MEDIA_TYPES.items()}

class REmbedDiscoveryError(REmbedError):
    """Thrown if there is an error discovering an OEmbed URL."""

def get_oembed_url(url, format=None):
    """Retrieves the OEmbed URL for a given resource.

    :param url: resource URL.
    :param format: if supplied, restricts the format to use for OEmbed.  If 
                   None, then the first URL found will be used.  One of 
                   'json', 'xml'.
    :returns: OEmbed URL for the resource.
    :raises REmbedDiscoveryError: if there is an error getting the OEmbed URL.
    """
    type = __get_type(format)

    response = requests.get(url)

    if not response.ok:
        raise REmbedDiscoveryError('Failed to get %s (status code %s)' % (url, response.status_code))

    soup = BeautifulSoup(response.text)
    link = soup.find('link', type = type, href = True)

    if not link:
        raise REmbedDiscoveryError('Could not find OEmbed URL for %s' % url)

    return (FORMATS[link['type']], link['href'])

def __get_type(format): 
    if not format:
        return MEDIA_TYPES.values()
    elif MEDIA_TYPES.has_key(format):
        return MEDIA_TYPES[format]

    raise REmbedDiscoveryError('Invalid format %s specified (must be json or xml)' % format)