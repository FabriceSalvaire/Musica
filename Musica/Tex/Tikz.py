####################################################################################################
#
# Musica - A Music Theory Package for Python
# Copyright (C) 2017 Fabrice Salvaire
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

from .Environment import Environment
from .Package import Package

####################################################################################################

class TikzFigure(Environment):

    ##############################################

    def __init__(self, packages_options=(), options=''):

        super().__init__('tikzpicture', options)

        self.packages.add(Package('tikz', *packages_options))

    ##############################################

    @staticmethod
    def _format_coordinate(kwargs):

        if isinstance(kwargs, dict):
            if 'x' in kwargs:
                return '{},{}'.format(kwargs['x'], kwargs['y'])
            elif 'r' in kwargs:
                return '{}:{}'.format(kwargs['a'], kwargs['r'])
            else:
                raise ValueError('Invalid coordinate')
        elif isinstance(kwargs, str):
            return kwargs

    ##############################################

    def use_library(self, name):

        # \usetikzlibrary{}
        self.packages['tikz'].set_option(name)

    ##############################################

    def append_command(self, command):

        self.append(command + ';')

    ##############################################

    def coordinate(self, name, **kwargs):

        coordinate = self._format_coordinate(kwargs)
        self.append_command(self.format(r'\coordinate («0») at («1»)', name, coordinate))

    ##############################################

    def line(self, _from, to):

        _from = self._format_coordinate(_from)
        to = self._format_coordinate(to)
        self.append_command(self.format(r'\draw («0») -- («1»)', _from, to))

    ##############################################

    def node(self, coordinate, text):

        coordinate = self._format_coordinate(coordinate)
        self.append_command(self.format(r'\node at («0») {«1»}', coordinate, text))
