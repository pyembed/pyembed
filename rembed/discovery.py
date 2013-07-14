import requests
from bs4 import BeautifulSoup

class REmbedDiscoveryError(Exception):
    '''Thrown if there is an error discovering an OEmbed URL'''

def get_oembed_url(url, format='json'):
    type = get_type(format)

    response = requests.get(url)

    if not response.ok:
        raise REmbedDiscoveryError('Failed to get %s (status code %s)' % (url, response.status_codes))

    soup = BeautifulSoup(requests.get(url).text)
    link = soup.find('link', type = type, href = True)

    return link['href'] if link else None

def get_type(format):        
    if format == 'json':
        return 'application/json+oembed'
    elif format == 'xml':
        return 'text/xml+oembed'

    raise REmbedDiscoveryError('Invalid format %s specified (must be json or xml)' % format)