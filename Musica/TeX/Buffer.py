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

####################################################################################################

class Buffer(object):

    #######################################

    def __init__(self):

        self._content = list()
        self.clear()

    #######################################

    def clear(self):

        del self._content[:]

    #######################################

    def push(self, data, deepcopy=False):

        if isinstance(data, list):
            for item in data:
                self.push_internal(item, deepcopy)
        else:
            self.push_internal(data, deepcopy)

        return self

    #######################################

    def push_internal(self, data, deepcopy=False):

        if deepcopy:
            data = copy.deepcopy(data)
        if isinstance(data, (str, unicode)) or isinstance(data, Buffer):
            self._content.append(data)

    #######################################

    def write(self, stream):

        for item in self._content:
            if isinstance(item, Buffer):
                item.write(stream)
            else:
                stream.write(item)
