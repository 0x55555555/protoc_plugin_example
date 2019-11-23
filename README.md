Installing
----------

```bash
> pip install .
```

Running plugin
--------------

```bash
> protoc -I ./example_proto example_proto/example.proto --protoc_plugin_example_out=./doc
```