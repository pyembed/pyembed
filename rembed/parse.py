from response import OEmbedResponse

import json

def parse_oembed_json(value):
    return OEmbedResponse(json.loads(value))