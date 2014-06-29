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

from hamcrest import assert_that, contains_string, equal_to
import yaml

from pyembed.core import PyEmbed
from pyembed.core.discovery import StaticDiscoverer
from pyembed.core.render import PyEmbedRenderer


class DummyRenderer(PyEmbedRenderer):
    def render(self, content_url, response):
        return "%s by %s from %s" % \
               (response.title, response.author_name, content_url)


def test_should_get_correct_embedding():
    embedding = PyEmbed().embed(
        'https://twitter.com/BarackObama/status/266031293945503744')
    assert_that(embedding, contains_string('Four more years.'))


def test_should_get_another_correct_embedding():
    embedding = PyEmbed().embed(
        'http://www.flickr.com/photos/hansjuul/7899334594')
    assert_that(embedding, contains_string('.jpg'))


def test_should_embed_with_maximum_height():
    embedding = PyEmbed().embed(
        'http://www.youtube.com/watch?v=9bZkp7q19f0', max_height=200)
    assert_that(embedding, contains_string('height="200"'))


def test_should_embed_with_custom_renderer():
    embedding = PyEmbed(renderer=DummyRenderer()).embed(
        'http://www.youtube.com/watch?v=qrO4YZeyl0I')
    assert_that(embedding, equal_to(
        'Lady Gaga - Bad Romance by LadyGagaVEVO from ' +
        'http://www.youtube.com/watch?v=qrO4YZeyl0I'))


def test_should_embed_when_no_discovery():
    embedding = PyEmbed().embed(
        'http://www.rdio.com/artist/Mike_Oldfield/album/Amarok/')
    assert_that(embedding, contains_string('rd.io'))


def test_should_process_all_examples():
    config_file = 'pyembed/core/config/endpoints.yml'
    pyembed = PyEmbed(discoverer=StaticDiscoverer(config_file))

    with open(config_file) as f:
        for endpoint in yaml.load(f.read()):
            pyembed.embed(endpoint['example'])
