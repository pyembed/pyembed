from rembed import discovery, parse, REmbedError

import requests

class REmbedConsumerError(REmbedError):
    '''Thrown if there is an error discovering an OEmbed URL.'''

def get_oembed_response(url):
    (discovered_format, oembed_url) = discovery.get_oembed_url(url)
    response = requests.get(oembed_url)

    if not response.ok:
        raise REmbedConsumerError('Failed to get %s (status code %s)' % (url, response.status_code))

    return parse.parse_oembed(discovered_format, response.text)

def embed(url):
    return get_oembed_response(url).embed()