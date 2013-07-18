from rembed import REmbedError

import requests
from bs4 import BeautifulSoup

class REmbedDiscoveryError(REmbedError):
    '''Thrown if there is an error discovering an OEmbed URL.'''

def get_oembed_url(url, format=None):
    '''Retrieves the OEmbed URL for a given resource.

    :param url: resource URL.
    :param format: if supplied, restricts the format to use for OEmbed.  If 
                   None, then the first URL found will be used.  One of 
                   'json', 'xml'.
    :returns: OEmbed URL for the resource.
    :raises REmbedDiscoveryError: if there is an error getting the OEmbed URL.
    '''
    type = __get_type(format)

    response = requests.get(url)

    if not response.ok:
        raise REmbedDiscoveryError('Failed to get %s (status code %s)' % (url, response.status_codes))

    soup = BeautifulSoup(requests.get(url).text)
    link = soup.find('link', type = type, href = True)

    return link['href'] if link else None

def __get_type(format):        
    if format == 'json':
        return 'application/json+oembed'
    elif format == 'xml':
        return 'text/xml+oembed'
    elif not format:
        return ['application/json+oembed', 'text/xml+oembed']

    raise REmbedDiscoveryError('Invalid format %s specified (must be json or xml)' % format)