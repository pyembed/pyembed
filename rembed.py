import requests
from bs4 import BeautifulSoup

class REmbedConsumer:
	def get_oembed_url(self, url):
		soup = BeautifulSoup(requests.get(url))
		return soup.link['href']