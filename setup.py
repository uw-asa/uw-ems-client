from setuptools import setup, find_packages
setup(
    name='ems_client',
    version='0.1',
    description='EMS client for Django',
    packages=find_packages(),
    install_requires=[
        'Django',
        'lxml',
        'python-dateutil',
        'suds-community',
    ],
    license='Apache License, Version 2.0',
    test_suite='runtests.runtests',
)
