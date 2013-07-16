from rembed import response

from hamcrest import *
import pytest

def test_should_load_from_dictionary():
    dict = {'title' : 'Bees'}
    oembed_response = response.OEmbedResponse(dict)

    assert_that(oembed_response.title, equal_to('Bees'))

def test_response_should_be_immutable():
    dict = {'title' : 'Bees'}
    oembed_response = response.OEmbedResponse(dict)

    with pytest.raises(TypeError):
        oembed_response.title = 'Wasps'