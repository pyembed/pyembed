from rembed import REmbedError
from . import response

from bs4 import BeautifulSoup
import json

RESPONSE_CLASSES = {'photo': response.OEmbedPhotoResponse,
                    'video': response.OEmbedVideoResponse,
                    'link': response.OEmbedLinkResponse,
                    'rich': response.OEmbedRichResponse}


class REmbedParseError(REmbedError):

    """Thrown if there is an error parsing an OEmbed response."""


def parse_oembed(format, response):
    """Parses an OEmbed response.

    :param format: format of the response.  One of 'json', 'xml'.
    :param response: the OEmbed response, in the given format.
    :returns: an REmbedResponse for the given response.
    :raises REmbedParseError: if there is an error parsing the response.
    """
    return PARSE_FUNCTIONS[format](response)


def parse_oembed_json(response):
    """Parses a JSON OEmbed response.

    :param response: the OEmbed response, as JSON.
    :returns: an REmbedResponse for the given JSON.
    :raises REmbedParseError: if there is an error parsing the response.
    """
    value_function = __value_function_json(json.loads(response))
    return __construct_response(value_function)


def parse_oembed_xml(response):
    """Parses an XML OEmbed response.

    :param response: the OEmbed response, as XML.
    :returns: an REmbedResponse for the given XML.
    :raises REmbedParseError: if there is an error parsing the response.
    """
    soup = BeautifulSoup(response)
    value_function = __value_function_xml(soup.oembed)
    return __construct_response(value_function)


def __value_function_json(value_dict):
    def value_function(field):
        if field in value_dict:
            return value_dict[field]
        else:
            return None

    return value_function


def __value_function_xml(oembed):
    def value_function(field):
        element = oembed.find(field)
        if element:
            try:
                return int(element.text)
            except ValueError:
                return element.text
        else:
            return None

    return value_function


def __construct_response(value_function):
    type = value_function('type')
    if type not in RESPONSE_CLASSES:
        raise REmbedParseError('Unknown type: %s', type)

    return RESPONSE_CLASSES[type](value_function)

PARSE_FUNCTIONS = {'json': parse_oembed_json,
                   'xml': parse_oembed_xml}
