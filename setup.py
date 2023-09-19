
from setuptools import setup, find_packages

setup(
    name='bbapipix',
    version='0.4',
    packages=find_packages(),
    package_data={'bbapipix': ['server_certs/*.cer']},
    install_requires=[
        'pyOpenSSL == 23.2.0',
        'requests == 2.31.0',
    ],
)
