import collections
import logging
import typing

import jinja2

from .generated_item import GeneratedItem
from .template_utils import render_docs

Method = collections.namedtuple("Method", [ "name", "input_type", "output_type", "client_streaming", "server_streaming", "docs" ])

def service_key(service_name):
    return "service_%s" % service_name

def generate_service(
        generated_items: typing.Dict[str,GeneratedItem],
        service,
        comment_strcucture):
    key = service_key(service.name)

    logging.info(comment_strcucture.members)

    def docs_for(method, comment_strcucture):
        method = comment_strcucture.members.get(method.name, None)
        if not method:
            return []
        return method

    tokens = {
        'name': service.name,
        'methods': [
            Method(m.name, m.input_type, m.output_type, m.client_streaming, m.server_streaming, docs_for(m, comment_strcucture)) for m in service.method
        ],
    }

    generated_items[key] = GeneratedItem(key, render_docs("service.template", tokens))