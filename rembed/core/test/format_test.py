from rembed.core import format

from hamcrest import assert_that, equal_to
from mock import Mock
import pytest


def test_should_format_response_using_template():
    response = Mock()
    response.title = 'Bees'
    response.author_name = 'Ian Bees'
    response.type = 'test'

    result = format.format_response(
        'http://example.com', response, 'rembed/core/test/fixtures/format')

    assert_that(result, equal_to('Bees by Ian Bees from http://example.com'))
