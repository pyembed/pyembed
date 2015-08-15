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

from pyembed.core import parse


pytestmark = pytest.mark.parametrize(('oembed_format', 'function'), [
    ('json', parse.parse_oembed_json),
    ('xml', parse.parse_oembed_xml)
])


def test_should_parse_type(oembed_format, function):
    assert get_response(oembed_format, function).type == 'link'


def test_should_parse_version(oembed_format, function):
    assert get_response(oembed_format, function).version == '1.0'


def test_should_parse_title(oembed_format, function):
    assert get_response(oembed_format, function).title == 'Lots of Bees'


def test_should_parse_author_name(oembed_format, function):
    assert get_response(oembed_format, function).author_name == 'Ian Bees'


def test_should_parse_author_url(oembed_format, function):
    assert get_response(oembed_format, function).author_url == 'http://www.example.com/ianbees/'


def test_should_parse_provider_name(oembed_format, function):
    assert get_response(oembed_format, function).provider_name == 'Example'


def test_should_parse_provider_url(oembed_format, function):
    assert get_response(oembed_format, function).provider_url == 'http://www.example.com/'


def test_should_parse_cache_age(oembed_format, function):
    assert get_response(oembed_format, function).cache_age == 3600


def test_should_parse_thumbnail_url(oembed_format, function):
    assert get_response(oembed_format, function).thumbnail_url == 'http://www.example.com/bees/thumb.jpg'


def test_should_parse_thumbnail_width(oembed_format, function):
    assert get_response(oembed_format, function).thumbnail_width == 360


def test_should_parse_thumbnail_height(oembed_format, function):
    assert get_response(oembed_format, function).thumbnail_height == 240


def test_should_parse_url_from_photo(oembed_format, function):
    assert get_response(oembed_format, function, 'photo').url == 'http://www.example.com/bees.jpg'


def test_should_parse_width_from_photo(oembed_format, function):
    assert get_response(oembed_format, function, 'photo').width == 600


def test_should_parse_height_from_photo(oembed_format, function):
    assert get_response(oembed_format, function, 'photo').height == 400


def test_should_parse_html_from_video(oembed_format, function):
    assert 'http://www.example.com/bees.mpg' in get_response(oembed_format, function, 'video').html


def test_should_parse_width_from_video(oembed_format, function):
    assert get_response(oembed_format, function, 'video').width == 600


def test_should_parse_height_from_video(oembed_format, function):
    assert get_response(oembed_format, function, 'video').height == 400


def test_should_parse_html_from_rich(oembed_format, function):
    assert 'Bees!' in get_response(oembed_format, function, 'rich').html


def test_should_parse_width_from_rich(oembed_format, function):
    assert get_response(oembed_format, function, 'rich').width == 600


def test_should_parse_height_from_rich(oembed_format, function):
    assert get_response(oembed_format, function, 'rich').height == 400


def test_should_get_none_for_missing_element(oembed_format, function):
    assert not get_response(oembed_format, function, 'minimal').title


def test_should_raise_error_for_unknown_type(oembed_format, function):
    with pytest.raises(parse.PyEmbedParseError):
        get_response(oembed_format, function, 'unknown')


def test_should_select_parse_function(oembed_format, function):
    filename = 'pyembed/core/test/fixtures/parse/link.%s' % oembed_format
    content_type = {'json': 'application/json', 'xml': 'text/xml'}.get(oembed_format)

    assert parse.parse_oembed(open(filename).read(), content_type).title == 'Lots of Bees'


def test_should_raise_on_invalid_format(oembed_format, function):
    filename = 'pyembed/core/test/fixtures/parse/link.%s' % oembed_format
    content_type = {'json': 'text/json', 'xml': 'application/xml'}.get(oembed_format)

    with pytest.raises(parse.PyEmbedParseError):
        parse.parse_oembed(open(filename).read(), content_type)


def get_response(oembed_format, function, fixture='link'):
    filename = 'pyembed/core/test/fixtures/parse/%s.%s' % (fixture, oembed_format)
    return function(open(filename).read())
