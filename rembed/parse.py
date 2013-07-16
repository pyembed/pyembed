from response import *

import json

RESPONSE_CLASSES = {'photo' : OEmbedPhotoResponse}

def parse_oembed_json(value):
    dict = json.loads(value)
    
    response_class = RESPONSE_CLASSES[dict['type']]
    return response_class(dict)