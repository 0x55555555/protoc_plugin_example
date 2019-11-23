
import setuptools

setuptools.setup(
    name='protoc_plugin_example',
    version='0.1',
    packages=['protoc_plugin_example',],
    install_requires=[
        'protobuf >= 3.3.0',
        'grpcio-tools',
    ],
    license='BSD',
    entry_points = {
        'console_scripts': ['protoc-gen-protoc_plugin_example=protoc_plugin_example.cli:main'],
    }
)