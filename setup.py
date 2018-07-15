import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ASCIITreeLog",
    version = "0.1.1",
    description = "Show tree graph in terminal with time series.",
    long_description=read('Readme.md'),
    url = "https://github.com/mhlemonh/ASCIITreeLog",
    packages=find_packages(exclude=['test']),
)