import logging
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"

def generate_title(text, title_type):
    return title_type * len(text)

def method_ref_name(service_name, method_name):
    return "service_%s_%s" % (service_name, method_name)

def render_docs(filename, tokens):
    logging.info(TEMPLATE_DIR)
    file_loader = FileSystemLoader(str(TEMPLATE_DIR))
    env = Environment(loader=file_loader)

    env.globals['title'] = generate_title
    env.globals['method_ref_name'] = method_ref_name

    template = env.get_template(filename)

    return template.render(**tokens)
    