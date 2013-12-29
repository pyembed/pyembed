from os import path
from pkg_resources import resource_string
from pystache import Renderer


def render_response(content_url, response, template_dir=None):
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
