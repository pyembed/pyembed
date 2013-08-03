from rembed.core import response

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


def test_response_type_must_override_embed():
    values = {'type': 'link', 'version': '1.0'}
    oembed_response = response.OEmbedResponse(create_value_function(values))

    with pytest.raises(NotImplementedError):
        oembed_response.embed('http://www.example.com')


def test_should_embed_photo():
    values = {'type': 'photo',
              'version': '1.0',
              'url': 'http://example.com/bees.jpg',
              'width': 300,
              'height': 200}

    oembed_response = response.OEmbedPhotoResponse(
        create_value_function(values))
    assert_that(oembed_response.embed('http://www.example.com'),
                equal_to('<img src="http://example.com/bees.jpg" ' +
                         'width="300" height="200" />'))


def test_should_embed_video():
    embedding = '<iframe src="http://www.example.com/bees.mpg"></iframe>'
    values = {'type': 'video',
              'version': '1.0',
              'html': embedding}

    oembed_response = response.OEmbedVideoResponse(
        create_value_function(values))
    assert_that(oembed_response.embed('http://www.example.com'),
                equal_to(embedding))


def test_should_embed_rich():
    embedding = '<h1>Bees!</h1>'
    values = {'type': 'rich',
              'version': '1.0',
              'html': embedding}

    oembed_response = response.OEmbedRichResponse(
        create_value_function(values))
    assert_that(oembed_response.embed('http://www.example.com'),
                equal_to(embedding))


def test_should_embed_link():
    values = {'type': 'link',
              'title': 'Bees!'}

    oembed_response = response.OEmbedLinkResponse(
        create_value_function(values))
    assert_that(oembed_response.embed('http://www.example.com'),
                equal_to('<a href="http://www.example.com">Bees!</a>'))


def create_value_function(values):
    return lambda field: values[field] if field in values else None
