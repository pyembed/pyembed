class OEmbedResponse(object):

    """Base representation of an OEmbed response.  Each response type is
       represented by a different subclass.
    """
    def __init__(self, value_function):
        """Constructor.

        :param value_function: function that takes a single string parameter,
        and returns the value of the field with that name from an OEmbed
        response (or None, if the field is not present).
        """
        for field in self.fields():
            self.__set_attr_from_dict(value_function, field)

    def __set_attr_from_dict(self, value_function, field):
        self.__dict__[field] = value_function(field)

    def fields(self):
        """Returns the list of field names applicable for this response.

        On this base class, this is the list of fields common to all response
        types.  Subclasses can override this to add in type-specific fields.

        :returns: list of field names applicable for this response.
        """
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

    def embed(self, content_url):
        """Generate an HTML representation of this response.

        :param content_url: URL of the resource being embedded.
        """
        raise NotImplementedError(
            'No embed method for type %s' % type(self).__name__)

    def __setattr__(self, *args):
        raise TypeError('Responses are immutable')


class OEmbedPhotoResponse(OEmbedResponse):

    """Represents an OEmbed photo response."""
    def fields(self):
        return super(OEmbedPhotoResponse, self).fields() + \
            ['url', 'width', 'height']

    def embed(self, content_url):
        return '<img src="%s" width="%s" height="%s" />' % \
            (self.url, self.width, self.height)


class OEmbedVideoResponse(OEmbedResponse):

    """Represents an OEmbed video response."""
    def fields(self):
        return super(OEmbedVideoResponse, self).fields() + \
            ['html', 'width', 'height']

    def embed(self, content_url):
        return self.html


class OEmbedLinkResponse(OEmbedResponse):

    """Represents an OEmbed link response."""
    def embed(self, content_url):
        return '<a href="%s">%s</a>' % (content_url, self.title)


class OEmbedRichResponse(OEmbedResponse):

    """Represents an OEmbed rich response."""
    def fields(self):
        return super(OEmbedRichResponse, self).fields() + \
            ['html', 'width', 'height']

    def embed(self, content_url):
        return self.html
