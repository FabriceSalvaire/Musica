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

class Coordinate:

    ##############################################

    def __init__(self, *args, **kwargs):

        number_of_args = len(args)
        if number_of_args == 1:
            obj = args[0]
            self.x = obj.x
            self.y = obj.y
        elif number_of_args == 2:
            self.x = args[0]
            self.y = args[1]
        elif 'x' in kwargs:
            self.x = kwargs['x']
            self.y = kwargs['y']
        elif 'clone' in kwargs:
            obj = kwargs['clone']
            self.x = obj.x
            self.y = obj.y
        else:
            raise ValueError("Invalid parameters")

    ##############################################

    def __str__(self):
        return '({},{})'.format(self.x, self.y)

####################################################################################################

class PolarCoordinate:

    ##############################################

    def __init__(self, *args, **kwargs):

        number_of_args = len(args)
        if number_of_args == 1:
            obj = args[0]
            self.a = obj.a
            self.r = obj.r
        elif number_of_args == 2:
            self.a = args[0]
            self.r = args[1]
        elif 'a' in kwargs:
            self.a = kwargs['a']
            self.r = kwargs['r']
        elif 'clone' in kwargs:
            obj = kwargs['clone']
            self.a = obj.a
            self.r = obj.r
        else:
            raise ValueError("Invalid parameters")

    ##############################################

    def __str__(self):
        return '({}:{})'.format(self.a, self.r)

####################################################################################################

class TikzFigure(Environment):

    __option_map__ = {
        'linewidth': 'line width',
    }

    ##############################################

    def __init__(self, packages_options=(), options=''):

        super().__init__('tikzpicture', options)

        self.packages.add(Package('tikz', *packages_options))

    ##############################################

    # @staticmethod
    # def _format_coordinate(obj):

    #     if hasattr(obj, 'x'):
    #         return '({},{})'.format(obj.x, obj.y)
    #     elif isinstance(obj, dict):
    #         if 'x' in obj:
    #             return '({},{})'.format(obj['x'], obj['y'])
    #         elif 'r' in obj:
    #             return '({}:{})'.format(obj['a'], obj['r'])
    #         else:
    #             raise ValueError('Invalid coordinate')
    #     elif isinstance(obj, str):
    #         return obj

    ##############################################

    @staticmethod
    def _ensure_coordinate(obj):

        if hasattr(obj, 'x') or 'x' in obj:
            return Coordinate(obj)
        elif hasattr(obj, 'a') or 'a' in obj:
            return PolarCoordinate(obj)
        else:
            raise ValueError("Invalid coordinate {}".format(obj))

    ##############################################

    @classmethod
    def _translate_option(cls, option):
        return cls.__option_map__.get(option, option)

    ##############################################

    @classmethod
    def _format_options_dict(cls, kwargs):

        if kwargs:
            comma_list = ', '.join(['{}={}'.format(cls._translate_option(key), value)
                                    for key, value in kwargs.items()
                                    if value is not None])
            return '[' + comma_list + ']'
        else:
            return ''

    ##############################################

    @classmethod
    def _format_options(cls, **kwargs):

        return cls._format_options_dict(kwargs)

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

    def path(self, path, **kwargs):

        # close = False
        # draw
        # fill
        # linewidth

        points = [str(self._ensure_coordinate(point)) for point in path]

        command = 'draw'
        args = self._format_options(**kwargs)
        args += ' ' + ' -- '.join(points)
        if kwargs.get('close', False) or kwargs.get('fill', False):
            args += ' -- cycle'
        self.append_command(command, args)

        # if fill is None:
        #     command = 'draw'
        #     args = ''
        # else:
        #     if filldraw:
        #         command = 'filldraw'
        #         args = self._format_options(fill=fill, filldraw=filldraw)
        #     else:
        #         command = 'fill'
        #         args = '[{}]'.format(fill)

    ##############################################

    def line(self, _from, to, **kwargs):

        self.path((_from, to), **kwargs)

    ##############################################

    def text(self, coordinate, text, **kwargs):

        # anchor
        # rotate

        coordinate = self._ensure_coordinate(coordinate)
        args = self._format_options(**kwargs)
        self.append_command('node', args + self.format(r' at «0» {«1»}', coordinate, self.to_tex(text)))
