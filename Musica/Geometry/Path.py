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

from .Primitive import Primitive2D
from .Vector import Vector2D

####################################################################################################

class Polyline(Primitive2D):

    #######################################

    def __init__(self, *args):

        """ Construct a :class:`Polyline` along points. """

        if len(args) == 1:
            self._points = [Vector2D(point) for point in args[0]]
        else:
            self._points = [Vector2D(point) for point in args]

    ##############################################

    def clone(self):

        return self.__class__(self._points)

    ##############################################

    def __repr__(self):

        return "{0.__class__.__name__} {0._points}".format(self)

    ##############################################

    def transform(self, transformation):

        points = transformation * self._points
        return self.__class__(points)

    ##############################################

    def __iter__(self):
        return iter(self._points)

    def __len__(self):
        return len(self._points)

    def __getitem__(self, _slice):
        return self._points[_slice]
