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

from .Buffer import TexContent

####################################################################################################

class Environment(TexContent):

    ##############################################

    def __init__(self, name, options=''):

        super().__init__()

        self._name = name
        self._options = options

    ##############################################

    def format_begin(self):

        if self._options:
            options = '[' + self._options + ']'
        else:
            options = ''

        return r'\begin{%s}%s' % (self._name, options)

    ##############################################

    def _content_to_string(self):

        source = self.format_begin() + '\n'
        source += super().to_string('content')
        source += r'\end{%s}' % (self._name) + '\n'

        return source

    ##############################################

    def to_string(self, context):

        if context == 'content':
            return self._content_to_string()
        else:
            return super().to_string(context)

####################################################################################################

class Center(Environment):
    def __init__(self):
        Environment.__init__(self, 'center')
