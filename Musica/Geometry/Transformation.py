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

from math import sin, cos, radians # degrees

import numpy as np

####################################################################################################

class Transformation:

    __dimension__ = None
    __size__ = None

    ##############################################

    @classmethod
    def Identity(cls):

        return cls(np.identity(cls.__size__))

    ##############################################

    def __init__(self, obj):

        if isinstance(obj, Transformation):
            if self.same_dimension(obj):
                array = obj.array # *._m
            else:
                raise ValueError
        elif isinstance(obj, np.ndarray):
            if obj.shape == (self.__size__, self.__size__):
                array = obj
            else:
                raise ValueError
        else:
            array = np.array((self.__size__, self.__size__))
            array[...] = obj
        self._m = np.array(array)

    ##############################################

    @property
    def dimension(self):
        return self.__dimension__

    @property
    def size(self):
        return self.__size__

    @property
    def array(self):
        return self._m

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + str(self._m)

    ##############################################

    def same_dimension(self, other):

        return self.__size__ == other.dimension

    ##############################################

    def _compose_transformation(self, transformation):

        return np.matmul(self._m, transformation.array)

    ##############################################

    def transform(self, transformation):

        array = self._compose_transformation(transformation)
        return self.__class__(array)

    #######################################

    def __mul__(self, obj):

        try:
            return obj.transform(self)
        except AttributeError:
            try:
                return [item.transform(self) for item in obj]
            except TypeError:
                raise ValueError

    #######################################

    def __imul__(self, obj):

        if isinstance(obj, Transformation):
            self._m = self._compose_transformation(obj)
        else:
            raise ValueError

        return self

####################################################################################################

class Transformation2D(Transformation):

    __dimension__ = 2
    __size__ = 2

    ##############################################

    @classmethod
    def Rotation(cls, angle):

        angle = radians(angle)
        c = cos(angle)
        s = sin(angle)

        return cls(np.array(((c, -s), (s,  c))))

    ##############################################

    @classmethod
    def Scale(cls, x_scale, y_scale):

        return cls(np.array((x_scale, 0), (0,  y_scale)))

    ##############################################

    @classmethod
    def Parity(cls):

        return cls.Scale(-1, -1)

    ##############################################

    @classmethod
    def XReflection(cls):

        return cls.Scale(-1, 1)

    ##############################################

    @classmethod
    def YReflection(cls):

        return cls.Scale(1, -1)

####################################################################################################

class AffineTransformation(Transformation):

    ##############################################

    @classmethod
    def Translation(cls, vector):

        transformation = cls.Identity()
        transformation.translation_part[...] = vector.v[...]
        return transformation

    ##############################################

    @classmethod
    def Rotation(cls, angle):

        transformation = cls.Identity()
        transformation.matrix_part[...] = Transformation2D.Rotation(angle).array
        return transformation

    ##############################################

    @classmethod
    def RotationAt(cls, center, angle):

        transformation = cls.Translation(center)
        transformation *= cls.Rotation(angle)
        transformation *= cls.Translation(-center)
        return transformation

    ##############################################

    @property
    def matrix_part(self):
        return self._m[:self.__dimension__,:self.__dimension__]

    @property
    def translation_part(self):
        return self._m[:self.__dimension__,-1]

####################################################################################################

class AffineTransformation2D(AffineTransformation):

    __dimension__ = 2
    __size__ = 3

####################################################################################################

# The matrix to rotate an angle θ about the axis defined by unit vector (l, m, n) is
# l*l*(1-c) + c   , m*l*(1-c) - n*s , n*l*(1-c) + m*s
# l*m*(1-c) + n*s , m*m*(1-c) + c   , n*m*(1-c) - l*s
# l*n*(1-c) - m*s , m*n*(1-c) + l*s , n*n*(1-c) + c
