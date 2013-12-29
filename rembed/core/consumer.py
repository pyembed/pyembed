from rembed.core import discovery, parse, render, REmbedError

import requests


class REmbedConsumerError(REmbedError):

    """Thrown if there is an error discovering an OEmbed URL."""


def embed(url, max_width=None, max_height=None, template_dir=None):
    """Returns an HTML representation of a resource, given a URL.  This can be
       directly embedded in a web page.

    :param url: the content URL.
    :param max_width: (optional) the maximum width of the embedded resource.
    :param max_height: (optional) the maximum height of the embedded resource.
    :param template_dir: (optional) path to the directory containing the
    Mustache templates to use for rendering.
    :returns: an HTML representation of the resource.
    :raises REmbedError: if there is an error fetching the response.
    """
    response = get_oembed_response(url, max_width, max_height)
    return render.render_response(url, response, template_dir)


def get_oembed_response(url, max_width=None, max_height=None):
    """Fetches an OEmbed response for a given content URL.

    :param url: the content URL.
    :param max_width: (optional) the maximum width of the embedded resource.
    :param max_height: (optional) the maximum height of the embedded resource.
    :returns: an REmbedResponse, representing the resource to embed.
    :raises REmbedError: if there is an error fetching the response.
    """

    (discovered_format, oembed_url) = discovery.get_oembed_url(
        url, max_width=max_width, max_height=max_height)
    response = requests.get(oembed_url)

    if not response.ok:
        raise REmbedConsumerError('Failed to get %s (status code %s)' % (
            url, response.status_code))

    return parse.parse_oembed(discovered_format, response.text)
