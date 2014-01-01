# The MIT License(MIT)

# Copyright (c) 2013-2014 Matt Thomson

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pyembed.core import PyEmbedError

from os import path
from pkg_resources import resource_string
from pystache import Renderer


def render_response(content_url, response, template_dir=None):
    """Renders a response using a template.

    :param content_url: the content URL.
    :param response: the response to render.
    :param template_dir: (optional) path to the directory containing the
    Mustache templates to use for rendering.  If this is not supplied, a
    default template will be used.
    :returns: an HTML representation of the resource.
    """

    file_name = '%s.mustache' % response.type

    if template_dir:
        template = __load_template_from_file(template_dir, file_name)
    else:
        template = resource_string(__name__, 'templates/%s' % file_name)

    return Renderer().render(template, response, {'content_url': content_url})


def __load_template_from_file(template_dir, file_name):
    template_path = path.join(template_dir, file_name)

    with open(template_path) as template_file:
        return template_file.read()
