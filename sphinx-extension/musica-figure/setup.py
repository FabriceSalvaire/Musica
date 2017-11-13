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

from setuptools import setup, find_packages

####################################################################################################

setup(
    name='sphinxcontrib-musica',
    version='0.1',
    author='Fabrice Salvaire',
    author_email='fabrice.salvaire@orange.fr',
    description='Sphinx mudica extension',
    license='GPLv3',
    keywords= 'sphinx extension musica',
    url='https://musica.fabrice-salvaire.fr',
    long_description='',
    zip_safe=False,
    packages=find_packages(),
    namespace_packages=['sphinxcontrib'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    install_requires=[
        'Sphinx>=0.6',
    ],
)
