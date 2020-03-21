# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
from pathlib import Path
import re

# Get current version
version = '0.1.0'
version_input_path = Path('./setup/version.txt')
if version_input_path.exists():
    with open(version_input_path, 'r') as f:
        version_input = f.readline().rstrip()

    if re.match('\\d+\\.\\d+\\.\\d+', version_input):
        version = version_input

# Load doc
with open('README.md') as f:
    readme = f.read()

setup(
    name='cronotrack',
    version=version,
    description='CLI App to track time',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='salpreh',
    author_email='salva.perez46@gmail.com',
    url='https://github.com/salpreh/tablat',
    license='MIT License',
    packages=find_packages(exclude=('test', 'assets', 'dev_test', 'doc'))
)
