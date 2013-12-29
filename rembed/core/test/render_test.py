from rembed.core import render, response

from hamcrest import assert_that, equal_to
from mock import Mock
import pytest


def test_should_render_response_using_custom_template():
    response = Mock()
    response.title = 'Bees'
    response.author_name = 'Ian Bees'
    response.type = 'video'

    result = render.render_response(
        'http://example.com', response, 'rembed/core/test/fixtures/render')

    assert_that(result, equal_to('Bees by Ian Bees from http://example.com'))


def test_should_raise_error_on_missing_template():
    response = Mock()
    response.title = 'Bees'
    response.author_name = 'Ian Bees'
    response.type = 'invalid'

    with pytest.raises(IOError):
        render.render_response(
            'http://example.com', response, 'rembed/core/test/fixtures/render')


def test_should_embed_photo():
    values = {'type': 'photo',
              'version': '1.0',
              'url': 'http://example.com/bees.jpg',
              'width': 300,
              'height': 200}

    oembed_response = response.OEmbedPhotoResponse(
        create_value_function(values))
    assert_that(render.render_response('http://example.com', oembed_response),
                equal_to('<img src="http://example.com/bees.jpg" ' +
                         'width="300" height="200" />'))


def test_should_embed_video():
    embedding = '<iframe src="http://www.example.com/bees.mpg"></iframe>'
    values = {'type': 'video',
              'version': '1.0',
              'html': embedding}

    oembed_response = response.OEmbedVideoResponse(
        create_value_function(values))
    assert_that(render.render_response('http://example.com', oembed_response),
                equal_to(embedding))


def test_should_embed_rich():
    embedding = '<h1>Bees!</h1>'
    values = {'type': 'rich',
              'version': '1.0',
              'html': embedding}

    oembed_response = response.OEmbedRichResponse(
        create_value_function(values))
    assert_that(render.render_response('http://example.com', oembed_response),
                equal_to(embedding))


def test_should_embed_link():
    values = {'type': 'link',
              'title': 'Bees!'}

    oembed_response = response.OEmbedLinkResponse(
        create_value_function(values))
    assert_that(render.render_response('http://example.com', oembed_response),
                equal_to('<a href="http://example.com">Bees!</a>'))


def create_value_function(values):
    return lambda field: values[field] if field in values else None
