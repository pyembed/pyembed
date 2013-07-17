from rembed import response

from hamcrest import *
import pytest

def test_should_load_from_dictionary():
    oembed_response = response.OEmbedResponse(value_function)

    assert_that(oembed_response.type, equal_to('link'))

def test_response_should_be_immutable():
    oembed_response = response.OEmbedResponse(value_function)

    with pytest.raises(TypeError):
        oembed_response.type = 'photo'

def value_function(field):
    if field == 'type':
        return 'link'
    elif field == 'version':
        return '1.0'
    else:
        return None