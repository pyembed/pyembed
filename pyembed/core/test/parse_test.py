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

from hamcrest import assert_that, contains_string, equal_to, none
import pytest

from pyembed.core import parse

pytestmark = pytest.mark.parametrize(('format', 'function'), [
    ('json', parse.parse_oembed_json),
    ('xml', parse.parse_oembed_xml)
])


def test_should_parse_type(format, function):
    assert_that(get_response(format, function).type, equal_to('link'))


def test_should_parse_version(format, function):
    assert_that(get_response(format, function).version, equal_to('1.0'))


def test_should_parse_title(format, function):
    assert_that(get_response(format, function).title, equal_to('Lots of Bees'))


def test_should_parse_author_name(format, function):
    assert_that(get_response(
        format, function).author_name, equal_to('Ian Bees'))


def test_should_parse_author_url(format, function):
    assert_that(get_response(format, function).author_url, equal_to(
        'http://www.example.com/ianbees/'))


def test_should_parse_provider_name(format, function):
    assert_that(get_response(
        format, function).provider_name, equal_to('Example'))


def test_should_parse_provider_url(format, function):
    assert_that(get_response(format, function).provider_url, equal_to(
        'http://www.example.com/'))


def test_should_parse_cache_age(format, function):
    assert_that(get_response(format, function).cache_age, equal_to(3600))


def test_should_parse_thumbnail_url(format, function):
    assert_that(get_response(format, function).thumbnail_url, equal_to(
        'http://www.example.com/bees/thumb.jpg'))


def test_should_parse_thumbnail_width(format, function):
    assert_that(get_response(format, function).thumbnail_width, equal_to(360))


def test_should_parse_thumbnail_height(format, function):
    assert_that(get_response(format, function).thumbnail_height, equal_to(240))


def test_should_parse_url_from_photo(format, function):
    assert_that(get_response(format, function, 'photo').url, equal_to(
        'http://www.example.com/bees.jpg'))


def test_should_parse_width_from_photo(format, function):
    assert_that(get_response(format, function, 'photo').width, equal_to(600))


def test_should_parse_height_from_photo(format, function):
    assert_that(get_response(format, function, 'photo').height, equal_to(400))


def test_should_parse_html_from_video(format, function):
    assert_that(get_response(format, function, 'video').html,
                contains_string('http://www.example.com/bees.mpg'))


def test_should_parse_width_from_video(format, function):
    assert_that(get_response(format, function, 'video').width, equal_to(600))


def test_should_parse_height_from_video(format, function):
    assert_that(get_response(format, function, 'video').height, equal_to(400))


def test_should_parse_html_from_rich(format, function):
    assert_that(get_response(
        format, function, 'rich').html, contains_string('Bees!'))


def test_should_parse_width_from_rich(format, function):
    assert_that(get_response(format, function, 'rich').width, equal_to(600))


def test_should_parse_height_from_rich(format, function):
    assert_that(get_response(format, function, 'rich').height, equal_to(400))


def test_should_get_none_for_missing_element(format, function):
    assert_that(get_response(format, function, 'minimal').title, none())


def test_should_raise_error_for_unknown_type(format, function):
    with pytest.raises(parse.PyEmbedParseError):
        get_response(format, function, 'unknown')


def get_response(format, function, fixture='link'):
    filename = 'pyembed/core/test/fixtures/parse/%s.%s' % (fixture, format)
    return function(open(filename).read())
