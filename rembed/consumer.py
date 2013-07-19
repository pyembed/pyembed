from rembed import discovery, parse

import requests

def get_oembed_response(url):
    (discovered_format, oembed_url) = discovery.get_oembed_url(url)
    response = requests.get(oembed_url)
    return parse.parse_oembed(discovered_format, response.text)