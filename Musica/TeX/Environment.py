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

from . import Buffer

####################################################################################################

class Environment(Buffer):

    #######################################

    def __init__(self, name):

        super(Environment, self).__init__()

        self._name = name

        self.begin_buffer = Buffer()
        self.end_buffer = Buffer()

    #######################################

    def set_begin(self):

        self.begin_buffer.push(r'\begin{%s}' % (self._name) + '\n')

    #######################################

    def set_end(self):

        self.end_buffer.push(r'\end{%s}' % (self._name) + '\n')

    #######################################

    def write(self, stream):

        self.set_begin()
        self.begin_buffer.write(stream)
        super(Environment, self).write(stream)
        self.set_end()
        self.end_buffer.write(stream)
