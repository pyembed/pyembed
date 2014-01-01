from pyembed.core import consumer

from hamcrest import assert_that, contains_string, equal_to


def test_should_get_correct_embedding():
    embedding = consumer.embed(
        'https://twitter.com/BarackObama/status/266031293945503744')
    assert_that(embedding, contains_string('Four more years.'))


def test_should_embed_with_maximum_height():
    embedding = consumer.embed(
        'http://www.youtube.com/watch?v=9bZkp7q19f0', max_height=200)
    assert_that(embedding, contains_string('height="200"'))


def test_should_embed_with_custom_template():
    embedding = consumer.embed(
        'http://www.youtube.com/watch?v=qrO4YZeyl0I',
        template_dir='pyembed/core/test/fixtures/render')
    assert_that(embedding, equal_to(
        'Lady Gaga - Bad Romance by LadyGagaVEVO from ' +
        'http://www.youtube.com/watch?v=qrO4YZeyl0I'))
