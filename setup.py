
from setuptools import setup, find_packages

setup(
    name='bbapipix',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyOpenSSL == 23.2.0',
        'requests == 2.31.0',
    ],
)
