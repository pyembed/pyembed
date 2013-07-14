import requests
from bs4 import BeautifulSoup

class REmbedError(Exception):
    pass

class REmbedConsumer:
    def get_oembed_url(self, url, format='json'):
        type = self.get_type(format)

        response = requests.get(url)

        if not response.ok:
            raise REmbedError('Failed to get %s (status code %s)' % (url, response.status_codes))

        soup = BeautifulSoup(requests.get(url).text)
        link = soup.find('link', type = type, href = True)

        return link['href'] if link else None

    def get_type(self, format):        
        if format == 'json':
            return 'application/json+oembed'
        elif format == 'xml':
            return 'text/xml+oembed'

        raise REmbedError('Invalid format %s specified (must be json or xml)' % format)