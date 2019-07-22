import re
from os.path import join, dirname

from setuptools import setup, find_packages


with open(join(dirname(__file__), 'panda', '__init__.py')) as v_file:
    package_version = re.compile('.*__version__ = \'(.*?)\'', re.S)\
        .match(v_file.read()).group(1)


dependencies = [
    'restfulpy >= 3.4.0',
    'kavenegar',
    'requests',
    'oathcy',
    'sqlalchemy_media >= 0.17.1',
]


setup(
    name='panda',
    version=package_version,
    author='mohammad sheikhian',
    author_email='mohammadsheikhian70@gmail.com',
    install_requires=dependencies,
    packages=find_packages(),
    test_suite='panda.tests',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'panda = panda:panda.cli_main'
        ]
    }
)

