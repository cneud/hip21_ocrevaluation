# -*- coding: utf-8 -*-
from setuptools import setup

install_requires = open('requirements.txt').read().split('\n')

setup(
    name='hip21_ocrevaluation',
    version='1.0.0',
    description='Code for analysis of OCR evaluation results',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Konstantin Baierer, Clemens Neudecker',
    author_email='{first}.{last}@sbb.spk-berlin.de',
    url='https://github.com/cneud/hip21_ocrevaluation',
    license='Apache License 2.0',
    packages=['hip21_ocrevaluation'],
    install_requires=install_requires,
    package_data={'': ['*.json', '*.yml', '*.xml']},
    keywords=['OCR'],
    entry_points={
        'console_scripts': [
            'hip21-ocrevaluation=hip21_ocrevaluation.cli:cli',
        ]
    },
)
