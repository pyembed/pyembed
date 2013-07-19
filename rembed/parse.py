from rembed import REmbedError

from response import *

from bs4 import BeautifulSoup
import json

RESPONSE_CLASSES = {'photo' : OEmbedPhotoResponse,
                    'video' : OEmbedVideoResponse,
                    'link' : OEmbedLinkResponse,
                    'rich' : OEmbedRichResponse}

class REmbedParseError(REmbedError):
    '''Thrown if there is an error parsing an OEmbed response.'''

def parse_oembed(format, response):
    return PARSE_FUNCTIONS[format](response)

def parse_oembed_json(response):
    value_function = __value_function_json(json.loads(response))
    return __construct_response(value_function)

def parse_oembed_xml(response):
    soup = BeautifulSoup(response)
    value_function = __value_function_xml(soup.oembed)
    return __construct_response(value_function)

def __value_function_json(value_dict):
    def value_function(field):
        if value_dict.has_key(field):
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
    if not RESPONSE_CLASSES.has_key(type):
        raise REmbedParseError('Unknown type: %s', type)

    return RESPONSE_CLASSES[type](value_function)

PARSE_FUNCTIONS = {'json' : parse_oembed_json,
                   'xml' : parse_oembed_xml}