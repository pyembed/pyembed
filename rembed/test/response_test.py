from rembed import response

from hamcrest import *
import pytest

def test_should_load_from_dictionary():
    dict = {'type' : 'link', 'version' : '1.0'}
    oembed_response = response.OEmbedResponse(dict)

    assert_that(oembed_response.type, equal_to('link'))

def test_response_should_be_immutable():
    dict = {'type' : 'link', 'version' : '1.0'}
    oembed_response = response.OEmbedResponse(dict)

    with pytest.raises(TypeError):
        oembed_response.type = 'photo'