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

import math

import numpy as np

from IntervalArithmetic import Interval2D, IntervalInt2D

####################################################################################################

from .MathFunctions import sign, trignometric_clamp #, is_in_trignometric_range
from .Primitive import Primitive2D

####################################################################################################

class VectorAbc(Primitive2D):

    __data_type__ = None

    ##############################################

    def __init__(self, array_size, v_size):

        # Fixme: v_size versus homogeneous

        self._array = np.zeros(array_size, dtype=self.__data_type__)
        self._v = self._array[:v_size] # view

    ##############################################

    def clone(self):

        """ Return a copy of self """

        return self.__class__(self)

    ##############################################

    @property
    def array(self):
        return self._array

    @property
    def v(self):
        return self._v

    # @v.setter
    # def v(self, value):
    #     self._v = value

    @property
    def x(self):
        return self.__data_type__(self._array[0])

    @property
    def y(self):
        return self.__data_type__(self._array[1])

    @x.setter
    def x(self, x):
        self._array[0] = x

    @y.setter
    def y(self, y):
        self._array[1] = y

    ##############################################

    def __repr__(self):

        return self.__class__.__name__ + str(self._array)

    ##############################################

    def __len__(self):

        return NotImplementedError

    ##############################################

    def __iter__(self):

        return iter(self._array)

    ##############################################

    def __getitem__(self, a_slice):

        return self._array[a_slice]

    ##############################################

    def __setitem__(self, index, value):

        self._array[index] = value

    ##############################################

    def to_numpy(self):

        return np.array(self._array, dtype=self.__data_type__)

    ##############################################

    def to_int_list(self):

        return [int(x) for x in self]

    ##############################################

    def __nonzero__(self):

        return bool(self._array.any())

    ##############################################

    def __eq__(v1, v2):

        """ self == other """

        return np.array_equal(v1._array, v2.array)

    ##############################################

    def transform(self, transformation):

        array = np.matmul(transformation.array, np.transpose(self._array))
        return self.__class__(array)

####################################################################################################

class VectorArithmeticMixin:

    ##############################################

    def __add__(self, other):

        """ Return a new vector equal to the addition of self and other """

        return self.__class__(self._v + other.v)

    ##############################################

    def __iadd__(self, other):

        """ Add other to self """

        self._v += other.v

        return self

    ##############################################

    def __sub__(self, other):

        """ Return a new vector """

        return self.__class__(self._v - other.v)

    ##############################################

    def __isub__(self, other):

        """ Return a new vector equal to the subtraction of self and other """

        self._v -= other.v

        return self

    ##############################################

    def __pos__(self):

        """ Return a new vector equal to self """

        return self.__class__(self._v)

    ##############################################

    def __neg__(self):

        """ Return a new vector equal to the negation of self """

        return self.__class__(-self._v)

    ##############################################

    def __abs__(self):

        """ Return a new vector equal to abs of self """

        return self.__class__(np.abs(self._v))

    ##############################################

    def __mul__(self, scale):

        """ Return a new vector equal to the self scaled by scale """

        return self.__class__(scale * self._v)

    ##############################################

    def __imul__(self, scale):

        """ Scale self by scale """

        self._v *= scale

        return self

    ##############################################

    def magnitude_square(self):

        """ Return the square of the magnitude of the vector """

        return np.dot(self._v, self._v)

    ##############################################

    def normal(self):

        """ Return a new vector equal to self rotated of 90 degree in the counter clockwise
        direction
        """

        xp = -self._v[1]
        yp =  self._v[0]

        return self.__class__((xp, yp))

    ##############################################

    def anti_normal(self):

        """ Return a new vector equal to self rotated of 90 degree in the clockwise direction
        """

        xp =  self._v[1]
        yp = -self._v[0]

        return self.__class__((xp, yp))

    ##############################################

    def parity(self):

        """ Return a new vector equal to self rotated of 180 degree
        """

        # parity
        xp = -self._v[0]
        yp = -self._v[1]

        return self.__class__((xp, yp))

    ##############################################

    def dot(self, other):

        """ Return the dot product of self with other """

        return self.__data_type__(np.dot(self._v, other.v))

    ##############################################

    def cross(self, other):

        """ Return the cross product of self with other """

        return self.__data_type__(np.cross(self._v, other.v))

####################################################################################################

class VectorIntMixin:

    __data_type__ = np.int

    ##############################################

    def bounding_box(self):

        x, y = self.x, self.y
        return IntervalInt2D((x, x) , (y, y))

####################################################################################################

class VectorFloatMixin:

    __data_type__ = np.float

    ##############################################

    def bounding_box(self):

        x, y = self.x, self.y
        return Interval2D((x, x) , (y, y))

    ##############################################

    def almost_equal(v1, v2, rtol=1e-05, atol=1e-08, equal_nan=False):

        """ self ~= other """

        return np.allclose(tuple(v1), tuple(v2), rtol, atol, equal_nan)

    ##############################################

    def __truediv__(self, scale):

        """ Return a new vector equal to the self dvivided by scale """

        return self.__class__(self._v / scale)

    ##############################################

    def __itruediv__(self, scale):

        """ Scale self by 1/scale """

        self._v /= scale

        return self

    ##############################################

    def normalise(self):

        """ Normalise the vector """

        self._v /= self.magnitude()

    ##############################################

    def magnitude(self):

        """ Return the magnitude of the vector """

        return math.sqrt(self.magnitude_square())

    ##############################################

    def orientation(self):

        """ Return the orientation in degree """

        #
        # 2 | 1
        # - + -
        # 4 | 3
        #
        #       | 1    | 2         | 3    | 4         |
        # x     | +    | -         | +    | -         |
        # y     | +    | +         | -    | -         |
        # tan   | +    | -         | -    | +         |
        # atan  | +    | -         | -    | +         |
        # theta | atan | atan + pi | atan | atan - pi |
        #

        if not bool(self):
            raise NameError("Null Vector")
        if self.x == 0:
            return math.copysign(90, self.y)
        elif self.y == 0:
            return 0 if self.x >= 0 else 180
        else:
            orientation = math.degrees(math.atan(self.tan()))
            if self.x < 0:
                if self.y > 0:
                    orientation += 180
                else:
                    orientation -= 180
            return orientation

    ##############################################

    def rotate(self, angle, counter_clockwise=True):

        """ Return a new vector equal to self rotated of angle degree in the counter clockwise
        direction
        """

        radians = math.radians(angle)
        if not counter_clockwise:
            radians = -radians
        c = math.cos(radians)
        s = math.sin(radians)

        # Fixme: np matrice
        xp = c * self._v[0] -s * self._v[1]
        yp = s * self._v[0] +c * self._v[1]

        return self.__class__((xp, yp))

    ##############################################

    def tan(self):

        """ Return the tangent """

        # RuntimeWarning: divide by zero encountered in double_scalars
        return self.y / self.x

    ##############################################

    def inverse_tan(self):

        """ Return the inverse tangent """

        return self.x / self.y

    ##############################################

    def is_parallel(self, other):

        """ Self is parallel with other """

        return round(self.cross(other), 7) == 0

    ##############################################

    def is_orthogonal(self, other):

        """ Self is orthogonal with other """

        return round(self.dot(other), 7) == 0

    ##############################################

    def cos_with(self, direction):

        """ Return the cosinus of self with direction """

        cos = direction.dot(self) / (direction.magnitude() * self.magnitude())

        return trignometric_clamp(cos)

    ##############################################

    def projection_on(self, direction):

        """ Return the projection of self on direction """

        return direction.dot(self) / direction.magnitude()

    ##############################################

    def sin_with(self, direction):

        """ Return the sinus of self with other """

        # turn from direction to self
        sin = direction.cross(self) / (direction.magnitude() * self.magnitude())

        return trignometric_clamp(sin)

    ##############################################

    def deviation_with(self, direction):

        """ Return the deviation of self with other """

        return direction.cross(self) / direction.magnitude()

    ##############################################

    def orientation_with(self, direction):

        # Fixme: check all cases
        # -> angle_with

        """ Return the angle of self on direction """

        angle = math.acos(self.cos_with(direction))
        angle_sign = sign(self.sin_with(direction))

        return angle_sign * math.degrees(angle)

####################################################################################################

class Vector2DBase(VectorAbc):

    ##############################################

    def __init__(self, *args):

        """
        Example of usage::

          Vector(1, 3)
          Vector((1, 3))
          Vector([1, 3])
          Vector(iterable)
          Vector(vector)

        """

        array = self._check_arguments(args)
        super().__init__(2, 2)
        self._v[...] = array[:2]

    ##############################################

    def _check_arguments(self, args):

        size = len(args)
        if size == 1:
            array = args[0] # iterable, vector
        elif size == 2:
            array = args # (x, y)
        else:
            raise ValueError("More than 2 arguments where given")

        # if not (np.iterable(array) and len(array) == 2):
        #     raise ValueError("Argument must be iterable and of length 2")

        return array

    ##############################################

    def __len__(self):

        return 2

    ##############################################

    def transform(self, transformation):

        if transformation.size == 2:
            return super().transform(transformation)
        elif transformation.size == 3:
            return HomogeneousVector2D(self).transform(transformation)
        else:
            raise ValueError("Incompatible size")

####################################################################################################

class Vector2DInt(VectorIntMixin, VectorArithmeticMixin, Vector2DBase):
    pass

####################################################################################################

class Vector2D(VectorFloatMixin, VectorArithmeticMixin, Vector2DBase):

    """ 2D Vector """

    ##############################################

    @classmethod
    def from_angle(cls, angle):

        """ Create the unitary vector (cos(angle), sin(angle)).  The *angle* is in degree. """

        rad = math.radians(angle)

        return cls((math.cos(rad), math.sin(rad)))

    ##############################################

    @classmethod
    def middle(cls, p0, p1):

        """ Return the middle point. """

        return cls(p0 + p1) * .5

    ##############################################

    def rint(self):

        return Vector2DInt(np.rint(self._v))

    ##############################################

    def to_normalised(self):

        """ Return a normalised vector """

        return NormalisedVector2D(self._v / self.magnitude())

####################################################################################################

class NormalisedVector2D(VectorAbc):

    """ 2D Normalised Vector """

    ##############################################

    def __init__(self, array):

        VectorAbc.__init__(self, 2, 2)
        self._v[...] = array

        #! if self.magnitude() != 1.:
        #!     raise ValueError("Magnitude != 1")

        # if not (is_in_trignometric_range(self.x) and
        #         is_in_trignometric_range(self.y)):
        #     raise ValueError("Values must be in trignometric range")

    ##############################################

    def __mul__(self, scale):

        """ Return a new vector equal to the self scaled by scale """

        return Vector2D(scale * self._v)

####################################################################################################

class HomogeneousVector2D(VectorAbc):

    """ 2D Homogeneous Coordinate Vector """

    __data_type__ = float

    ##############################################

    def __init__(self, *args):

        array = self._check_arguments(args)

        VectorAbc.__init__(self, 3, 2)

        if len(array) == 2:
            self._v[...] = array
            self.w = 1
        else:
            self._array[...] = array[:3]

    ##############################################

    def _check_arguments(self, args):

        size = len(args)
        if size == 1:
            array = args[0] # iterable, vector
        elif 2 <= size <= 3:
            array = args
        else:
            raise ValueError("More than 3 arguments where given")

        return array

    ##############################################

    def to_vector(self):

        return Vector2D(self._v)

    ##############################################

    @property
    def w(self):
        return self._array[2]

    @w.setter
    def w(self, value):
        self._array[2] = value

    ##############################################

    def __len__(self):

        return 3
