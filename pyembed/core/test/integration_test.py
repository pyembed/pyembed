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
import vcr

from pyembed.core import PyEmbed
from pyembed.core.render import PyEmbedRenderer


class DummyRenderer(PyEmbedRenderer):
    def render(self, content_url, response):
        return "%s by %s from %s" % \
               (response.title, response.author_name, content_url)


@vcr.use_cassette('pyembed/core/test/fixtures/cassettes/correct_embedding.yml')
def test_should_get_correct_embedding():
    embedding = PyEmbed().embed(
        'https://twitter.com/BarackObama/status/266031293945503744')
    assert 'Four more years.' in embedding


@vcr.use_cassette('pyembed/core/test/fixtures/cassettes/another_correct_embedding.yml')
def test_should_get_another_correct_embedding():
    embedding = PyEmbed().embed(
        'http://www.flickr.com/photos/hansjuul/7899334594')
    assert '.jpg' in embedding


@vcr.use_cassette('pyembed/core/test/fixtures/cassettes/maximum_height.yml')
def test_should_embed_with_maximum_height():
    embedding = PyEmbed().embed(
        'http://www.youtube.com/watch?v=9bZkp7q19f0', max_height=200)
    assert 'height="200"' in embedding


@vcr.use_cassette('pyembed/core/test/fixtures/cassettes/custom_renderer.yml')
def test_should_embed_with_custom_renderer():
    embedding = PyEmbed(renderer=DummyRenderer()).embed(
        'http://www.youtube.com/watch?v=qrO4YZeyl0I')
    assert embedding == \
        'Lady Gaga - Bad Romance by LadyGagaVEVO from ' + \
        'http://www.youtube.com/watch?v=qrO4YZeyl0I'


@vcr.use_cassette('pyembed/core/test/fixtures/cassettes/no_discovery.yml')
def test_should_embed_when_no_discovery():
    embedding = PyEmbed().embed(
        'http://www.rdio.com/artist/Mike_Oldfield/album/Amarok/')
    assert 'rd.io' in embedding


@vcr.use_cassette('pyembed/core/test/fixtures/cassettes/text_xml.yml')
def test_should_embed_when_text_xml_returned():
    embedding = PyEmbed().embed('https://soundcloud.com/coltonprovias/rush')
    assert 'soundcloud.com' in embedding
