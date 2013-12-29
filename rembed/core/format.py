from pystache import Renderer
from os import path


def format_response(content_url, response, template_dir):
    template_path = path.join(template_dir, "%s.mustache" % response.type)

    with open(template_path) as template_file:
        template = template_file.read()
        return Renderer().render(
            template, response, {'content_url': content_url})
