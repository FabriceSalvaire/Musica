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

# (2cm,-5mm+2pt)
# \fill [red] ($(a) + 1/3*(1cm,0)$) circle (2pt);
#
# \draw[red] (0,0) -- ([xshift=3pt] 1,1);
# \draw[red] (1,0) -- +([shift=(135:5pt)] 30:2cm);
#
# \draw (0,0) -- ++(1,0) -- ++(0,1) -- ++(-1,0) -- cycle; % relative coordinate
# \draw (0,0) -- +(1,0) -- +(1,1) -- +(0,1) -- cycle; % don't update coordinate
#
# \tikz \draw (0,0) -- (1,1) -- ([turn]-45:1cm) -- ([turn]-30:1cm);
#
# \draw (0,0) --(2,0) (0,1) --(2,1); % mode to operation
#
# \draw[rounded corners]
# \draw[rounded corners=10pt] (0,0) -- (0pt,25pt) -- (40pt,25pt);
#
# \draw (1,0) circle [radius=1.5];
# \fill (1,0) circle [x radius=1cm, y radius=5mm, rotate=30];
#
# \draw svg {M 0 0 L 20 20 h 10 a 10 10 0 0 0 -20 0};
# https://www.w3.org/TR/SVG/paths.html#PathData
# M/m x y | move to absolute/relative
# Z/z     | close
# L/l x y | lineto absolute/relative
# H/h x   | horizontal absolute/relative
# V/v x   | vertical absolute/relative
# curve
#
# \draw     = \path[draw].
# \fill     = \path[fill].
# \filldraw = \path[fill,draw].

####################################################################################################

from .Environment import Environment
from .Package import Package

####################################################################################################

def _format_number(x):
    if isinstance(x, (str, int)):
        return str(x)
    else:
        return '{:.2f}'.format(x)

####################################################################################################

class NameCoordinate:

    ##############################################

    def __init__(self, obj):

        if isinstance(obj, str):
            self.name = obj
        elif hasattr(obj, 'name'):
            self.name = obj.name
        else:
            raise ValueError("Invalid parameters")

    ##############################################

    def __str__(self):
        return '({})'.format(self.name)

####################################################################################################

class Coordinate:

    ##############################################

    def __init__(self, *args, **kwargs):

        if not args:
            if 'x' in kwargs:
                self._set_from_dict(kwargs)
            elif 'clone' in kwargs:
                self._set_from_obj(kwargs['clone'])
        else:
            number_of_args = len(args)
            if number_of_args == 1:
                obj = args[0]
                if isinstance(obj, dict):
                    self._set_from_dict(obj)
                else:
                    self._set_from_obj(obj)
            elif number_of_args == 2:
                self._set_from_tuple(args)
            else:
                raise ValueError("Invalid parameters")

    ##############################################

    def _set_from_tuple(self, obj):

        self.x = obj[0]
        self.y = obj[1]

    ##############################################

    def _set_from_dict(self, obj):

        self.x = obj['x']
        self.y = obj['y']

    ##############################################

    def _set_from_obj(self, obj):

        self.x = obj.x
        self.y = obj.y

    ##############################################

    def __str__(self):
        return '({},{})'.format(_format_number(self.x), _format_number(self.y))

####################################################################################################

class PolarCoordinate:

    ##############################################

    def __init__(self, *args, **kwargs):

        if not args:
            if 'a' in kwargs: # only differ here
                self._set_from_dict(kwargs)
            elif 'clone' in kwargs:
                self._set_from_obj(kwargs['clone'])
        else:
            number_of_args = len(args)
            if number_of_args == 1:
                obj = args[0]
                if isinstance(obj, dict):
                    self._set_from_dict(obj)
                else:
                    self._set_from_obj(obj)
            elif number_of_args == 2:
                self._set_from_tuple(args)
            else:
                raise ValueError("Invalid parameters")

    ##############################################

    def _set_from_tuple(self, obj):

        self.a = obj[0]
        self.r = obj[1]

    ##############################################

    def _set_from_dict(self, obj):

        self.a = obj['a']
        self.r = obj['r']

    ##############################################

    def _set_from_obj(self, obj):

        self.a = obj.a
        self.r = obj.r

    ##############################################

    def __str__(self):
        return '({}:{})'.format(_format_number(self.a), _format_number(self.r))

####################################################################################################

class TikzFigure(Environment):

    __option_map__ = {
        'linewidth': 'line width',
    }

    ##############################################

    def __init__(self, packages_options=(), options=''):

        super().__init__('tikzpicture', options)

        self.packages.add(Package('xcolor', 'rgb'))
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

        if isinstance(obj, str) or hasattr(obj, 'name'):
           return NameCoordinate(obj)
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
    def _format_option(cls, key, value):

        key = cls._translate_option(key)

        if value is None or value is False:
            return None
        if value is True:
            return key
        else:
            return '{}={}'.format(key, value)

    ##############################################

    @classmethod
    def _format_options_dict(cls, kwargs):

        if kwargs:
            formated_options = [cls._format_option(key, value) for key, value in kwargs.items()]
            comma_list = ', '.join([x for x in formated_options if x])
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

    @staticmethod
    def format_number(x):
        return _format_number(x)

    ##############################################

    def append_command(self, command, args):

        if not args.startswith('[') and not args.startswith(' '):
            space = ' '
        else:
            space = ''
        self.append('\\' + command + space + args + ';')

    ##############################################

    def coordinate(self, name, *args, **kwargs):

        if not args:
            coordinate = self._ensure_coordinate(kwargs)
        elif len(args) == 1:
            coordinate = self._ensure_coordinate(args[0])
        else:
            raise ValueError("Invalid coordinate")

        self.append_command('coordinate', self.format('(«0») at «1»', name, coordinate))

    ##############################################

    def circle(self, point, radius, **kwargs):

        point = self._ensure_coordinate(point)

        command = 'path'
        args = self._format_options(**kwargs)
        args += ' {} circle '.format(point) + self._format_options(radius=radius)
        self.append_command(command, args)

    ##############################################

    def draw_circle(self, point, radius, **kwargs):
        self.circle(point, radius, draw=True, **kwargs)

    ##############################################

    def ellipse(self, point, x_radius, y_radius, **kwargs):

        point = self._ensure_coordinate(point)

        command = 'path'
        args = self._format_options(**kwargs)
        args += ' {} ellipse '.format(point) + self._format_options(x_radius=x_radius, y_radius=y_radius)
        self.append_command(command, args)

    ##############################################

    def rectangle(self, point0, point1, **kwargs):

        # draw fill

        point0 = self._ensure_coordinate(point0)
        point1 = self._ensure_coordinate(point1)

        command = 'path'
        args = self._format_options(**kwargs)
        args += ' {} rectangle {}'.format(point0, point1)
        self.append_command(command, args)

    ##############################################

    def draw_rectangle(self, point0, point1, **kwargs):
        self.rectangle(point0, point1, draw=True, **kwargs)

    ##############################################

    def path(self, path, **kwargs):

        # close = False
        # draw
        # fill
        # linewidth

        points = [str(self._ensure_coordinate(point)) for point in path]

        command = 'path'
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
        self.path((_from, to), draw=True, **kwargs)

    ##############################################

    def text(self, coordinate, text, **kwargs):

        # anchor
        # rotate

        coordinate = self._ensure_coordinate(coordinate)
        args = self._format_options(**kwargs)
        self.append_command('node', args + self.format(r' at «0» {«1»}', coordinate, self.to_tex(text)))

    ##############################################

    def add_license(self):

        import datetime
        now = datetime.datetime.now()
        year = now.year

        self.packages.add(Package('ccicons'))
        coordinate = 'current bounding box.south east'

        icons = ('Logo', 'Attribution', 'NonCommercial', 'ShareAlike')
        text = r'\hspace{.2ex}'.join([r'\cc' + x for x in icons])
        text += r'\hspace{.5ex}'
        text += 'Musica Toolkit {}'.format(year)
        self.text(coordinate, text, anchor='north east')
