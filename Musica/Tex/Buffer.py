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

import copy

from .Package import Packages

####################################################################################################

class Buffer:

    LINE_BREAK = r'\\'

    ##############################################

    def __init__(self):

        self._content = []
        self.clear()

    ##############################################

    def __iter__(self):

        return iter(self._content)

    ##############################################

    def to_string(self, context):

        source = ''
        for item in self._content:
            if isinstance(item, str):
                source += item
            else:
                source += item.to_string(context)

        return source

    ##############################################

    def clear(self):

        self._content.clear()

    ##############################################

    def append(self, data, deepcopy=False, newline=True):

        if isinstance(data, list):
            for item in data:
                self._append(item, deepcopy)
        else:
            self._append(data, deepcopy)
        if newline:
            self._append('\n')

        return self

    ##############################################

    def _append(self, data, deepcopy=False):

        if deepcopy:
            data = copy.deepcopy(data)
        # if isinstance(data, str) or isinstance(data, Buffer):
        self._content.append(data)

####################################################################################################

class BasicCommandMixin:

    ##############################################

    @staticmethod
    def to_tex(x):

        x = str(x)
        x = x.replace('♭', r'$\flat$')
        x = x.replace('♯', r'$\sharp$')

        return x

    ##############################################

    @staticmethod
    def format(pattern, *args, **kwargs):

        pattern = pattern.replace('{', '{{')
        pattern = pattern.replace('}', '}}')
        pattern = pattern.replace('«', '{')
        pattern = pattern.replace('»', '}')
        return pattern.format(*args, **kwargs)

    ##############################################

    def define(self, name, value, unit=''):

        value = str(value) + unit
        self.append(self.format(r'\def\«»{«»}', name, value))

    ##############################################

    def new_command(self, name, number_of_parameters, code):

        self.append(self.format(r'\newcommand{\«»}[«»]{«»}', name, number_of_parameters, code))

    ##############################################

    def set_main_font(self, name):

        self.append(self.format(r'\setmainfont[Ligatures=TeX]{«»}', name))

    ##############################################

    def font_size(self, font_size, base_line_skip=None):

        if base_line_skip is None:
            base_line_skip = 1.2 * font_size

        self.append(self.format(r'\fontsize{«»}{«:.2f»}', font_size, base_line_skip))

    ##############################################

    def centerline(self, content):

        self.append(self.format(r'\centerline{«»}', content))

####################################################################################################

class ContentCommandMixin:

    ##############################################

    def page_style(self, style):

        self.append(r'\pagestyle{%s}' % style)

    ##############################################

    def empty_page_style(self):

        self.page_style('empty')

    ##############################################

    def new_page(self):

        self.append(r'\newpage')

####################################################################################################

class PreambuleBuffer(Buffer, BasicCommandMixin):
    pass

####################################################################################################

class TexContent(BasicCommandMixin, ContentCommandMixin):

    #######################################

    def __init__(self):

        self._packages = Packages()
        self._preambule = PreambuleBuffer()
        self._content = Buffer()

    ##############################################

    @property
    def packages(self):
        return self._packages

    @property
    def preambule(self):
        return self._preambule

    @property
    def content(self):
        return self._content

    ##############################################

    def collect_packages(self):

        packages = self._packages.clone()
        for item in self._content:
            if isinstance(item, TexContent):
                packages.merge(item.collect_packages())
        return packages

    ##############################################

    def collect_preambule(self):

        source = ''
        for item in self._content:
            if isinstance(item, TexContent):
                source += item.to_string('preambule')
        return source

    ##############################################

    def to_string(self, context):

        if context not in ('preambule', 'content'):
            raise ValueError("Invalid context {}".format(context))

        if context == 'preambule':
            obj = self._preambule
        else:
            obj = self._content

        return obj.to_string(context)

    ##############################################

    def append_preambule(self, data, deepcopy=False, newline=True):

        self._preambule.append(data, deepcopy, newline)

    ##############################################

    def append(self, data, deepcopy=False, newline=True):

        self._content.append(data, deepcopy, newline)
