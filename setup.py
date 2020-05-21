import os
import subprocess
from setuptools import setup, find_packages
from zadarapy import __version__

def get_git_revision():
    """Return the git revision."""
    if os.path.exists('PKG-INFO'):
        with open('PKG-INFO') as package_info:
            for key, value in (line.split(':', 1) for line in package_info):
                if key.startswith('Version'):
                    return value.strip()

    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()

setup(
    name='zadarapy',
    version=get_git_revision(),
    packages=find_packages(),
    install_requires=['configparser>=3.5.0', 'future>=0.15.2',
                      'terminaltables>=2.1.0', 'requests>=2.2.1'],
    url='https://github.com/zadarastorage/zadarapy',
    license='Apache License 2.0',
    author='Jeremy Brown',
    author_email='jeremy@zadarastorage.com',
    description='Python module and command line interface with Zadara REST '
                'APIs',
    entry_points={
        'console_scripts': ['zadarapy=zadarapy.bin.command_line:main'],
    },
    zip_safe=False,
)
