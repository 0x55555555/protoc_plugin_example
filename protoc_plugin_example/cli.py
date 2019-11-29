from .parser import CodeGeneratorParser
from google.protobuf.compiler.plugin_pb2 import CodeGeneratorResponse

import json
import logging
import sys

# See https://github.com/googleapis/protoc-docs-plugin/blob/master/protoc_docs/bin/py_docstring.py
# for origins.
def main(input_file=sys.stdin, output_file=sys.stdout):
    """Parse a CodeGeneratorRequest and return a CodeGeneratorResponse."""

    logging.basicConfig(filename='logging.log',level=logging.DEBUG)

    # Ensure we are getting a bytestream, and writing to a bytestream.
    if hasattr(input_file, 'buffer'):
        input_file = input_file.buffer
    if hasattr(output_file, 'buffer'):
        output_file = output_file.buffer

    try:
        # Instantiate a parser.
        parser = CodeGeneratorParser.from_input_file(input_file)

        docs = parser.generate_docs()
    except:
        logging.exception("Error when generating docs: ")
        raise

    answer = []
    for k,item in docs.items():
        answer.append(CodeGeneratorResponse.File(
            name=item.filename,
            content=item.content,
        ))
    cgr = CodeGeneratorResponse(file=answer)
    output_file.write(cgr.SerializeToString())
