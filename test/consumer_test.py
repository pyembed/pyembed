from rembed import *

from hamcrest import *
from mock import patch
import pytest
import requests

def test_should_find_oembed_url_using_json_by_default():
    with patch('requests.get') as mock_get:
    	mock_get.return_value = open('test/fixtures/valid_oembed.html').read()

        consumer = REmbedConsumer()
        oembed_url = consumer.get_oembed_url('http://example.com')

        assert_that(oembed_url, equal_to('http://example.com/oembed?format=json'))