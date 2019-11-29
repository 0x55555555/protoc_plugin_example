import collections
import logging
import typing

import jinja2

from .generated_item import GeneratedItem
from .template_utils import render_docs

Method = collections.namedtuple("Method", [ "name", "input_type", "output_type", "client_streaming", "server_streaming" ])

def service_key(service_name):
    return "service_%s" % service_name

def generate_service(
        generated_items: typing.Dict[str,GeneratedItem],
        file,
        service,
        source_code_info):
    key = service_key(service.name)

    for code_info in source_code_info.location:
        item = file
        logging.info(help(item))
        for i in code_info.path:
            item = item.GetField(i)
        linked_item = file.GetField

    tokens = {
        'name': service.name,
        'methods': [
            Method(m.name, m.input_type, m.output_type, m.client_streaming, m.server_streaming) for m in service.method
        ],
    }

    generated_items[key] = GeneratedItem(key, render_docs("service.template", tokens))