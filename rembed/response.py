class OEmbedResponse():
    def __init__(self, dict):
        map(lambda field: self.__set_attr(dict, field), self.__fields())

    def __set_attr(self, dict, field):
        if dict.has_key(field):
            self.__dict__[field] = dict[field]

    def __fields(self):
        return ['type', 
                'version', 
                'title', 
                'author_name', 
                'author_url', 
                'provider_name', 
                'provider_url',
                'cache_age',
                'thumbnail_url',
                'thumbnail_width',
                'thumbnail_height']