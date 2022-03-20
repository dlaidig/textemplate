# SPDX-FileCopyrightText: 2022 Daniel Laidig <daniel@laidig.info>
#
# SPDX-License-Identifier: MIT
from setuptools import setup, find_packages

setup(
    name='textemplate',

    version='0.0.1',

    description='Simple tool to render LaTeX templates from json/yaml data',

    author='Daniel Laidig',
    author_email='daniel@laidig.info',

    license='MIT',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=['numpy', 'PyYAML', 'jinja2', 'latex'],

    entry_points={
        'console_scripts': [
            'textemplate = textemplate.textemplate:main',
        ],
    },
)
