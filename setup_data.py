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

import os
import sys
import subprocess

####################################################################################################

def merge_include(src_lines, doc_path, included_rst_files=None):
    if included_rst_files is None:
        included_rst_files = {}
    text = ''
    for line in src_lines:
        if line.startswith('.. include::'):
            include_file_name = line.split('::')[-1].strip()
            if include_file_name not in included_rst_files:
                # print "include", include_file_name
                with open(os.path.join(doc_path, include_file_name)) as f:
                    included_rst_files[include_file_name] = True
                    text += merge_include(f.readlines(), doc_path, included_rst_files)
        else:
            text += line
    return text

####################################################################################################

# Utility function to read the README file.
# Used for the long_description.
def read_readme(file_name):

    source_path = os.path.dirname(os.path.realpath(__file__))
    if os.path.basename(source_path) == 'tools':
        source_path = os.path.dirname(source_path)
    elif 'build/bdist' in source_path:
        source_path = source_path[:source_path.find('build/bdist')]
    absolut_file_name = os.path.join(source_path, file_name)
    doc_path = os.path.join(source_path, 'doc', 'sphinx', 'source')

    # Read and merge includes
    with open(absolut_file_name) as f:
        lines = f.readlines()
    text = merge_include(lines, doc_path)

    return text

####################################################################################################

if not __file__.endswith('conf.py'):
    long_description = read_readme('README.txt')
else:
    long_description = ''

####################################################################################################

setup_dict = dict(
    name='Musica-pip',
    version='0.1.0',
    author='Fabrice Salvaire',
    author_email='fabrice.salvaire@orange.fr',
    description='Musica is a free and open source computational music toolkit written in Python covering several topics from music theory, audio analysis to high quality figure generation',
    license='GPLv3',
    keywords= 'music computational theory',
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
