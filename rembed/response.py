class OEmbedResponse(object):
    def __init__(self, dict):
        map(lambda field: self.__set_attr_from_dict(dict, field), self.fields())

    def __set_attr_from_dict(self, dict, field):
        if dict.has_key(field):
            self.__dict__[field] = dict[field]

    def fields(self):
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

    def __setattr__(self, *args):
        raise TypeError("can't modify immutable instance")

class OEmbedPhotoResponse(OEmbedResponse):
    def fields(self):
        return super(OEmbedPhotoResponse, self).fields() + ['url', 'width', 'height']