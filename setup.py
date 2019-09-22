#!/usr/bin/env python

from setuptools import setup, find_packages
from pkg_resources import resource_filename

with open(resource_filename("typed", "version.txt"), "r") as vf:
    version = vf.read().strip()

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='typed',
    version=version,
    author='Kavin Ruengprateepsang',
    author_email='kavinvin.vin@gmail.com',
    description="Typed Python function",
    license='AGPLv3.0+',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/kavinvin/typed',
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[
        "toolz",
        "numpy"
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 "
        "or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ]
)
