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
# codes from SimpleMorphoMath - A simple mathematical morphology library.
#
####################################################################################################

""" This module implements Morphological 1D Operators.
"""

# Fixme: in-place ? f() ->

####################################################################################################

import numpy as np

####################################################################################################

def even(n):
    """ Test if *n* is even """
    return n & 1 == 0

def odd(n):
    """ Test if *n* is odd """
    return n & 1 == 1

####################################################################################################

class Domain(object):

    """ This class implements a functional 1D domain defined by the range [inf, sup].

    The size of the domain defined by ``sup - inf +1`` is given by the function :func:`len`.

    To test if ``x`` is in the domain, use::

      x in domain

    """

    ##############################################

    def __init__(self, inf, sup):

        self.inf = inf
        self.sup = sup

    ##############################################

    def __len__(self):

        """ Return the size of the domain. """

        return self.sup - self.inf +1

    ##############################################

    def range(self):

        """ Return the list of values in the domain. """

        return range(self.inf, self.sup +1)

    ##############################################

    def forward_iterator(self):

        """ Return a forward iterator over the domain. """

        return range(self.inf, self.sup +1)

    ##############################################

    def backward_iterator(self):

        """ Return a backward iterator over the domain. """

        return range(self.sup, self.inf -1, -1)

    ##############################################

    def __contains__(self, x):

        """ Test if *x* is in the domain. """

        return self.inf <= x <= self.sup

####################################################################################################

class StructuringElement(object):

    """ This class implements a structuring element.

    The parameter *offsets* is an iterable that contains the offsets of the pixels on of the
    structuring element.

    The neighbor set :math:`N_G^+` and :math:`N_G^-` is defined in the article: Morphological
    Grayscale Reconstruction in Image Analysis: Applications and Efficient Algorithms, Luc Vincent,
    IEEE Transactions on image processing, Vol. 2, No. 2, April 1993.
    """

    # Fixme: this code is only true for symetrical structuring element.
    #   implements reference location

    ##############################################

    def __init__(self, offsets):

        self.offsets = offsets

    ##############################################

    def __len__(self):

        return len(self.offsets)

    ##############################################

    def half_length(self):

        return int((len(self.offsets)-1)/2)

    ##############################################

    def __iter__(self):

        return iter(self.offsets)

    ##############################################

    def iterator_plus(self):

        """ Iterate over the offset up to the reference location. """

        # Fixme: check definition

        return iter(self.offsets[:self.half_length()+1])

    ##############################################

    def iterator_minus(self):

        """ Iterate over the offset from the reference location. """

        return iter(self.offsets[-self.half_length()-1:])

####################################################################################################

class BallStructuringElement(StructuringElement):

    """ This class implements a ball structuring element.

    The domain of the structuring element is [-radius, radius].
    """

    ##############################################

    def __init__(self, radius):

        super(BallStructuringElement, self).__init__(range(-radius, radius+1))

####################################################################################################

#: Unit ball structuring element.
unit_ball = BallStructuringElement(1)

####################################################################################################

class StructuringElementIterator(object):

    """ This class implements a structuring element iterator.

    The parameter *structuring_element* defines the structuring element and the parameter *domain*
    defines the domain of the lattice.
    """

    ##############################################

    def __init__(self, structuring_element, domain):

        self.domain = domain
        self.structuring_element = structuring_element

    ##############################################

    def iterate_at(self, location, sub_domain=None):

        """ Iterate over the structuring element positioned at a location.

        The parameter *sub_domain* is used to restrict the domain of the structuring element, set to
        '+' to restrict to the positive domain and to '-' for the negative domain, respectively.
        """

        if sub_domain is None:
            iterator = self.structuring_element
        elif sub_domain == '+':
            iterator = self.structuring_element.iterator_plus()
        elif sub_domain == '-':
            iterator = self.structuring_element.iterator_minus()
        else:
            raise ValueError('Wrong sub_domain')

        for offset in iterator:
            l = location + offset
            if l in self.domain:
                yield l
            else:
                continue

####################################################################################################

class Function(object):

    """ This class implements a 1D function.

    The parameters *values* is an iterable that define the initial values of the function.

    The function domain is set to [0, len(values) -1].
    """

    # Fixme: already defined
    unit_ball = BallStructuringElement(1)

    ##############################################

    def __init__(self, values):

        self.values = np.array(values, dtype=np.int)
        self.domain = Domain(inf=0, sup=self.values.size -1)

    ##############################################

    def clone(self):

        """ Return a copy of the function. """

        return self.__class__(self)

    ##############################################

    def clone_zeros(self):

        """ Return a function defined on the same domain with values set to zero. """

        return self.__class__(self._zeros())

    ##############################################

    def _zeros(self):

        """ return a Numpy zero array of the same size than the function domain. """

        return np.zeros(len(self), dtype=np.uint)

    ##############################################

    def __len__(self):

        """ Return the size of the function domain. """

        return self.values.size

    ##############################################

    def __getitem__(self, i):

        """ Return the function value at *i*. """

        return self.values[i]

    ##############################################

    def __setitem__(self, i, value):

        """ Set the function value at *i*. """

        self.values[i] = value

    ##############################################

    def add(self, obj):

        """ Add a function. """

        self.values += obj
        return self

    ##############################################

    def __add__(a, b):

        """ Return sum of *a* with *b*. """

        return a.clone().add(b)

    ##############################################

    def __iadd__(self, obj):

        """ Add a function. """

        return self.add(obj)

    ##############################################

    def subtract(self, obj):

        """ Subtract a function.

        Negative values are set to zero.
        """

        self.values -= obj
        self.values[np.where(self.values < 0)] = 0
        return self

    ##############################################

    def __sub__(a, b):

        """ Return the subtraction of *a* with *b*. """

        return a.clone().subtract(b)

    ##############################################

    def __isub__(self, obj):

        """ Subtract a function. """

        return self.subtract(obj)

    ##############################################

    def __eq__(self, other):

        """ Test if the functions are equal. """

        if other is None: # Fixme: why ?
            return False
        else:
            return (self.values == other.values).all()

    ##############################################

    def min(self):

        """ Return the inf of the function. """

        # Fixme: inf ?

        return self.values.min()

    ##############################################

    def max(self):

        """ Return the sup of the function. """

        # Fixme: sup ?

        return self.values.max()

    ##############################################

    def _rank_filter(self, structuring_element, rank_operator):

        """ This method implements a rank filter.

        The function is modified in-place.
        """

        structuring_element_iterator = StructuringElementIterator(structuring_element, self.domain)

        new_values = self.clone_zeros() # so as to use: new_values[i]
        for i in self.domain.forward_iterator():
            new_values[i] = rank_operator([self[j] for j in structuring_element_iterator.iterate_at(i)])
        self.values = new_values.values

    ##############################################

    def erode(self, structuring_element):

        """ Perform an erosion. """

        self._rank_filter(structuring_element, rank_operator=min)
        return self

    ##############################################

    def dilate(self, structuring_element):

        """ Perform a dilation. """

        self._rank_filter(structuring_element, rank_operator=max)
        return self

    ##############################################

    def open(self, structuring_element):

        """ Perform an opening. """

        self.erode(structuring_element)
        self.dilate(structuring_element)
        return self

    ##############################################

    def close(self, structuring_element):

        """ Perform an closing. """

        self.dilate(structuring_element)
        self.erode(structuring_element)
        return self

    ##############################################

    def top_hat(self, structuring_element):

        """ Perform an top-hat. """

        self -= self.clone().open(structuring_element)
        return self

    ##############################################

    def translate(self, offset, padd_inf=True):

        """ Translate the function.

        If the parameter *padd_inf* is set to True then the padding value is set to zero else to the
        sup of the function.
        """

        new_values = self._zeros()

        if offset == 0:
            new_values[...] = self.values[...]
        else:
            if padd_inf:
                padd_value = 0
            else:
                padd_value = self.max()

            if offset < 0:
                new_values[offset:] = padd_value
                new_values[:offset] = self.values[-offset:]
            elif offset > 0:
                new_values[offset:] = self.values[:-offset]
                new_values[:offset] = padd_value

        self.values = new_values

        return self

    ##############################################

    def _pointwise_rank(self, other, rank_operator):

        """ This method implements a point-wise rank filter.

        The function is modified in-place.
         """

        for i in self.domain.forward_iterator():
            self[i] = rank_operator(self[i], other[i])
        return self

    ##############################################

    def pointwise_max(self, other):

        """ Perform the point-wise max of the function with another function. """

        return self._pointwise_rank(other, max)

    ##############################################

    def pointwise_min(self, other):

        """ Perform the point-wise min of the function with another function. """

        return self._pointwise_rank(other, min)

    ##############################################

    def geodesic_reconstruction(self, marker):

        """ Perform a geodesic reconstruction. """

        mask = self
        prev_reconstruction = None
        reconstruction = marker.clone()

        while not reconstruction == prev_reconstruction:
            prev_reconstruction = reconstruction.clone()
            reconstruction.dilate(self.unit_ball).pointwise_min(mask)

        return reconstruction

    ##############################################

    def h_dome(self, level):

        """ Perform an H-dome operation. """

        if level <= 0:
            raise ValueError('level must be > 0')

        marker = self.clone().subtract(level)
        reconstruction = self.geodesic_reconstruction(marker)
        h_dome = self.clone().subtract(reconstruction)

        return h_dome

    ##############################################

    def _rank_filter_vhgw(self, radius, rank_operator):

        """ This method implements a rank filter using the Van Herk & Gill-Werman algorithm.

        This algorithm comes from C. Clienti, M. Bilodeau, and S. Beucher, An Efficient Hardware
        Architecture without Line Memories for Morphological Image Processing.  In Proceedings of
        ACIVS. 2008, 147-156.
        """

        domain_size = len(self) # len(self.domain)
        domain_sup = domain_size -1 # self.domain.sup

        size = 2*radius +1
        padding_size = size - (domain_sup % size) -1

        domain_sup_plus_padding_size = domain_size + padding_size

        forward = self.clone_zeros() # _zeros()
        for i in self.domain.forward_iterator():
            if i % size == 0:
                # Start new window
                forward[i] = self[i]
            else:
                # Propagate forward
                forward[i] = rank_operator(forward[i-1], self[i])

        backward = self.clone_zeros() # _zeros()
        for i in self.domain.backward_iterator():
            if i == self.domain.sup or (i+1) % size == 0:
                # Start new window
                backward[i] = self[i]
            else:
                # Propagate backward
                backward[i] = rank_operator(backward[i+1], self[i])

        for i in self.domain.forward_iterator():

            i_plus_radius  = i + radius
            i_minus_radius = i - radius

            if i_minus_radius < 0:
                # We are at right of the domain
                self[i] = forward[i_plus_radius]

            elif i_plus_radius >= domain_size:
                # We are at left of the domain
                if i_plus_radius < domain_sup_plus_padding_size:
                    # We are in the padding area
                    self[i] = rank_operator(forward[domain_sup], backward[i_minus_radius])
                else:
                    # We are out
                    self[i] = backward[i_minus_radius]

            else:
                # Normal way, we are in the domain
                self[i] = rank_operator(forward[i_plus_radius], backward[i_minus_radius])

        return self

    ##############################################

    def dilate_vhgw(self, radius):

        """ Perform a dilation using the WHGW algorithm. """

        return self._rank_filter_vhgw(radius, rank_operator=max)

    ##############################################

    def erode_vhgw(self, radius):

        """ Perform an erosion using the WHGW algorithm. """

        return self._rank_filter_vhgw(radius, rank_operator=min)
