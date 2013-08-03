from rembed import consumer

from hamcrest import assert_that, contains_string


def test_should_get_correct_embedding():
    embedding = consumer.embed(
        'https://twitter.com/BarackObama/status/266031293945503744')
    assert_that(embedding, contains_string('Four more years.'))


def test_should_embed_with_maximum_height():
    embedding = consumer.embed(
        'http://www.youtube.com/watch?v=9bZkp7q19f0', max_height=100)
    assert_that(embedding, contains_string('height="100"'))
