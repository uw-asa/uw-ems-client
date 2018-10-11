from setuptools import find_packages, setup

setup(
    name='ems_client',
    version='0.1',
    description='EMS client',
    packages=find_packages(),
    install_requires=[
        'commonconf>=0.6',
        'lxml',
        'python-dateutil',
        'suds-community',
        'UW-RestClients-Core',
    ],
    license='Apache License, Version 2.0',
    test_suite='runtests.runtests',
)
