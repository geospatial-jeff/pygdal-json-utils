from setuptools import setup, find_packages


with open('./requirements.txt') as reqs:
    requirements = [line.rstrip() for line in reqs]

setup(
    name='gdaljson-utils',
    version='0.1',
    description='GDAL Utilities for use with gdaljson',
    author='Jeff Albrecht',
    author_email='geospatialjeff@gmail.com',
    packages=find_packages(),
    install_requires = requirements
)