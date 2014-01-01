from pyembed.core import response

from hamcrest import assert_that, equal_to
import pytest


def test_should_load_from_dictionary():
    values = {'type': 'link', 'version': '1.0'}
    oembed_response = response.OEmbedResponse(create_value_function(values))

    assert_that(oembed_response.type, equal_to('link'))


def test_response_should_be_immutable():
    values = {'type': 'link', 'version': '1.0'}
    oembed_response = response.OEmbedResponse(create_value_function(values))

    with pytest.raises(TypeError):
        oembed_response.type = 'photo'


def create_value_function(values):
    return lambda field: values[field] if field in values else None
