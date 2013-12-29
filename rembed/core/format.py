import pystache
from os import path


def format_response(response, template_dir):
    template_path = path.join(template_dir, "%s.mustache" % response.type)

    with open(template_path) as template_file:
        template = template_file.read()
        return pystache.render(template, response)
