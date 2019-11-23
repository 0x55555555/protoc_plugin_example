from .parser import CodeGeneratorParser
from google.protobuf.compiler.plugin_pb2 import CodeGeneratorResponse

import json
import sys

# See https://github.com/googleapis/protoc-docs-plugin/blob/master/protoc_docs/bin/py_docstring.py
# for origins.
def main(input_file=sys.stdin, output_file=sys.stdout):
    """Parse a CodeGeneratorRequest and return a CodeGeneratorResponse."""

    # Ensure we are getting a bytestream, and writing to a bytestream.
    if hasattr(input_file, 'buffer'):
        input_file = input_file.buffer
    if hasattr(output_file, 'buffer'):
        output_file = output_file.buffer

    # Instantiate a parser.
    parser = CodeGeneratorParser.from_input_file(input_file)

    structure = parser.describe_structure()

    answer = []
    answer.append(CodeGeneratorResponse.File(
        name="pork.txt",
        content=json.dumps(structure, indent=2),
    ))
    cgr = CodeGeneratorResponse(file=answer)
    output_file.write(cgr.SerializeToString())