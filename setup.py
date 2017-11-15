#! /usr/bin/env python3

####################################################################################################
#
# Musica - A Music Theory package for Python
# Copyright (C) 2017 Salvaire Fabrice
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import sys

try:
    from setuptools import setup, find_packages
    setuptools_available = True
except ImportError:
    from distutils.core import setup
    setuptools_available = False

####################################################################################################

if sys.version_info < (3,):
    print('Musica requires Python 3', file=sys.stderr)
    sys.exit(1)
if sys.version_info < (3,4):
    print('WARNING: Musica could require Python 3.4 ...', file=sys.stderr)

exec(compile(open('setup_data.py').read(), 'setup_data.py', 'exec'))

####################################################################################################

setup_dict = dict(
    name='musica-toolkit',
    version='0.1.0',
    author='Fabrice Salvaire',
    author_email='fabrice.salvaire@orange.fr',
    description='Musica is a free and open source computational music toolkit written in Python covering several topics from music theory, audio analysis to high quality figure generation',
    license='GPLv3',
    keywords= 'music computational theory computer aided musical analysis',
    url='https://musica.fabrice-salvaire.fr',
    scripts=[
        'bin/make-figure',
    ],
    packages=[ # Fixme:
        'Musica',
        'Musica.Tools',
        'Musica.Audio',
        'Musica.Theory',
        'Musica.Geometry',
        'Musica.Figure',
        'Musica.Midi',
        'Musica.Notation',
        'Musica.Locale',
        'Musica.Instrument',
        'Musica.Config',
        'Musica.MusicXML',
        'Musica.Logging',
        'Musica.Math',
        'Musica.Tex',
        'Musica.Xml',
    ],
    # package_dir = {'Musica': 'Musica'},
    package_data={
        'Musica.Config': ['logging.yml'],
        'Musica.Instrument': ['*.yml'],
        'Musica': [
            'locale/en/LC_MESSAGES/Musica.mo',
            'locale/fr/LC_MESSAGES/Musica.mo',
        ],
    },
    long_description=long_description,
    # cf. http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Education',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        ],
    install_requires=[
        'IntervalArithmetic',
        'PyYAML',
        'numpy',
        'pyxb',
    ],
)

####################################################################################################

setup(**setup_dict)
