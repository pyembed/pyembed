class OEmbedResponse(object):
    def __init__(self, value_function):
        map(lambda field: self.__set_attr_from_dict(value_function, field), self.fields())

    def __set_attr_from_dict(self, value_function, field):
        self.__dict__[field] = value_function(field)

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

class OEmbedVideoResponse(OEmbedResponse):
    def fields(self):
        return super(OEmbedVideoResponse, self).fields() + ['html', 'width', 'height']

class OEmbedLinkResponse(OEmbedResponse):
    pass

class OEmbedRichResponse(OEmbedResponse):
    def fields(self):
        return super(OEmbedRichResponse, self).fields() + ['html', 'width', 'height']