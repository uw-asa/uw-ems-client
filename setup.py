from setuptools import setup, find_packages
setup(
    name='ems_client',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Django',
        'lxml',
        'suds',
        'UW-RestClients',
    ],
    license='Apache License, Version 2.0',
    description='',
    long_description='README.md',
)
