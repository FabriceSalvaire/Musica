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
    def _format_coordinate(obj):

        if hasattr(obj, 'x'):
            return '({},{})'.format(obj.x, obj.y)
        elif isinstance(obj, dict):
            if 'x' in obj:
                return '({},{})'.format(obj['x'], obj['y'])
            elif 'r' in obj:
                return '({}:{})'.format(obj['a'], obj['r'])
            else:
                raise ValueError('Invalid coordinate')
        elif isinstance(obj, str):
            return obj

    ##############################################

    @staticmethod
    def _format_options(kwargs):

        # key can have spaces

        if kwargs:
            comma_list = ', '.join(['{}={}'.format(key, value)
                                    for key, value in kwargs.items()
                                    if value is not None])
            return '[' + comma_list + ']'
        else:
            return ''

    ##############################################

    @classmethod
    def _format_options_dict(cls, **kwargs):

        return cls._format_options(kwargs)

    ##############################################

    @staticmethod
    def setup_externalisation(document):

        document.append_preambule(r'\usetikzlibrary{external}')
        document.append_preambule(r'\tikzexternalize')

    ##############################################

    def use_library(self, name):

        # self.packages['tikz'].set_option(name)
        self.append_preambule(r'\usetikzlibrary{%s}' % name)

    ##############################################

    def append_command(self, command, args):

        if not args.startswith('[') and not args.startswith(' '):
            space = ' '
        else:
            space = ''
        self.append('\\' + command + space + args + ';')

    ##############################################

    def coordinate(self, name, **kwargs):

        coordinate = self._format_coordinate(kwargs)
        self.append_command('coordinate', self.format('(«0») at «1»', name, coordinate))

    ##############################################

    def line(self, _from, to):

        _from = self._format_coordinate(_from)
        to = self._format_coordinate(to)
        self.append_command('draw', self.format(r'«0» -- «1»', _from, to))

    ##############################################

    def path(self, path, close=False, fill=None, draw=None):

        points = [self._format_coordinate(point)  for point in path]

        # if fill is None:
        #     command = 'draw'
        #     args = ''
        # else:
        #     if filldraw:
        #         command = 'filldraw'
        #         args = self._format_options_dict(fill=fill, filldraw=filldraw)
        #     else:
        #         command = 'fill'
        #         args = '[{}]'.format(fill)

        command = 'draw'
        args = self._format_options_dict(fill=fill, draw=draw)
        args += ' ' + ' -- '.join(points)
        if close:
            args += ' -- cycle'
        self.append_command(command, args)

    ##############################################

    def node(self, coordinate, text, **kwargs):

        # anchor
        # rotate

        coordinate = self._format_coordinate(coordinate)
        args = self._format_options_dict(**kwargs)
        self.append_command('node', args + self.format(r' at «0» {«1»}', coordinate, text))
