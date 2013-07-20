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

    def embed(self):
        raise NotImplementedError('No embed method for type %s' % type(self).__name__)

    def __setattr__(self, *args):
        raise TypeError('Responses are immutable')

class OEmbedPhotoResponse(OEmbedResponse):
    def fields(self):
        return super(OEmbedPhotoResponse, self).fields() + ['url', 'width', 'height']

    def embed(self):
        return '<img src="%s" width="%s" height="%s" />' % (self.url, self.width, self.height)

class OEmbedVideoResponse(OEmbedResponse):
    def fields(self):
        return super(OEmbedVideoResponse, self).fields() + ['html', 'width', 'height']

    def embed(self):
        return self.html

class OEmbedLinkResponse(OEmbedResponse):
    pass

class OEmbedRichResponse(OEmbedResponse):
    def fields(self):
        return super(OEmbedRichResponse, self).fields() + ['html', 'width', 'height']

    def embed(self):
        return self.html