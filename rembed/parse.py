from rembed import REmbedError

from response import *

import json

RESPONSE_CLASSES = {'photo' : OEmbedPhotoResponse,
                    'video' : OEmbedVideoResponse,
                    'link' : OEmbedLinkResponse,
                    'rich' : OEmbedRichResponse}

class REmbedParseError(REmbedError):
    '''Thrown if there is an error parsing an OEmbed response.'''

def parse_oembed_json(value):
    dict = json.loads(value)

    type = dict['type']
    if not RESPONSE_CLASSES.has_key(type):
        raise REmbedParseError('Unknown type: %s', type)

    return RESPONSE_CLASSES[type](dict)