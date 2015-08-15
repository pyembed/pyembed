# The MIT License(MIT)

# Copyright (c) 2013-2014 Matt Thomson

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import pytest

from pyembed.core import render, response


def test_should_embed_photo():
    values = {'type': 'photo',
              'version': '1.0',
              'url': 'http://example.com/bees.jpg',
              'width': 300,
              'height': 200}

    oembed_response = response.OEmbedPhotoResponse(
        create_value_function(values))
    assert render.DefaultRenderer().render('http://example.com', oembed_response) == \
        '<img src="http://example.com/bees.jpg" width="300" height="200" />'


def test_should_embed_video():
    embedding = '<iframe src="http://www.example.com/bees.mpg"></iframe>'
    values = {'type': 'video',
              'version': '1.0',
              'html': embedding}

    oembed_response = response.OEmbedVideoResponse(
        create_value_function(values))
    assert render.DefaultRenderer().render('http://example.com', oembed_response) == \
        embedding


def test_should_embed_rich():
    embedding = '<h1>Bees!</h1>'
    values = {'type': 'rich',
              'version': '1.0',
              'html': embedding}

    oembed_response = response.OEmbedRichResponse(
        create_value_function(values))
    assert render.DefaultRenderer().render('http://example.com', oembed_response) == \
        embedding


def test_should_embed_link():
    values = {'type': 'link',
              'title': 'Bees!'}

    oembed_response = response.OEmbedLinkResponse(
        create_value_function(values))
    assert render.DefaultRenderer().render('http://example.com', oembed_response) == \
        '<a href="http://example.com">Bees!</a>'


def test_must_override_render():
    with pytest.raises(NotImplementedError):
        render.PyEmbedRenderer().render('http://example.com', None)


def create_value_function(values):
    return lambda field: values[field] if field in values else None
