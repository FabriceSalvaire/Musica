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

"""Classes for representing interval.
"""

####################################################################################################

__all__ = [
    'Interval',
    ]

####################################################################################################

from .Temperament import ET12

####################################################################################################

class IntervalNumber:

    #! Assume a Twelve-tone equal temperament
    # __temperament__ = ET12

    ##############################################

    @staticmethod
    def qualities_for_interval_number(number):

        # Assume ET12
        #
        # Qualities are defined by a circular permutation of
        #   (P,  mM, mM, P,  P,   mM, mM)
        #
        #   (C,  D,  E,  F,  G,   A,  B)
        #   (Do, Ré, Mi, Fa, Sol, La, Si)

        if (number - 1) % 7 in (0, 3, 4):
            return ('P',)
        else:
            return ('m', 'M')

    ##############################################

    def __init__(self, number, name):

        self._number = number
        self._name = name

    ##############################################

    @property
    def number(self):
        return self._number

    @property
    def name(self):
        return self._name

    @property
    def qualities(self):
        return self.qualities_for_interval_number(self._number)

    ##############################################

    def __repr__(self):
        return self._name

    ##############################################

    def __int__(self):
        return self._number

    def __lt__(self, other):
        return self._number < int(other)

####################################################################################################

class IntervalNumbersSingleton:

    __interval_numbers__ = [
        IntervalNumber(i,  name)
        for i, name in enumerate((
                'unison',    # prime
                'second',    # seconde
                'third',     # tierce
                'fourth',    # quarte
                'fifth',     # quinte
                'sixth',     # sixte
                'seventh',   # septième
                'octave',
                'ninth',
                'tenth',
                'eleventh',
                'twelfth',   # Tritave
                'thirteenth',
                'fourteenth',
                'fifteenth', # double octave
        ))]

    ##############################################

    def __iter__(self):
        return iter(self.__interval_numbers__)

    ##############################################

    def __getitem__(self, number):
        return self.__interval_numbers__[number -1]

IntervalNumbers = IntervalNumbersSingleton()

####################################################################################################

class Interval:

    #! Assume a Twelve-tone equal temperament
    __temperament__ = ET12

    ##############################################

    @classmethod
    def number_from_note(cls, inf, sup):

        """Return interval number between *inf* and *sup*"""

        # The number of an interval is the number of letter names it encompasses or staff positions
        # it encompasses. Both lines and spaces are counted, including the positions of both notes
        # forming the interval.

        inf_degree = cls.__temperament__.by_name(inf).degree
        sup_degree = cls.__temperament__.by_name(sup).degree

        delta = sup_degree - inf_degree
        # print(inf_degree, sup_degree, delta)
        if delta > 0:
            delta += 1
        elif delta < 0:
            delta += cls.__temperament__.number_of_names + 1
        # else: delta = 0 # unison or octave

        return delta

    ##############################################

    def __init__(self, inf, sup):

        self._inf = inf
        self._sup = sup

        self._number = self.number_from_note(inf.step, sup.step)

        number_of_semitones = int(sup) - int(inf)
         # Fixme: more than one ocatve !
        if number_of_semitones < 0:
            number_of_semitones += self.__temperament__.number_of_steps # or % 12

        deltas = [(number_of_semitones - interval.number_of_semitones, interval)
                  for interval in MainIntervals.intervals_for_degree(self._number)]
        alteration, closest_interval = sorted(deltas, key=lambda x: x[0])[0]

        self._number_of_semitones = number_of_semitones
        self._alteration = alteration # augmented / diminished
        self._closest_interval = closest_interval

    ##############################################

    @property
    def inf(self):
        return self._inf

    @property
    def sup(self):
        return self._sup

    @property
    def number(self):
        return self._number

    @property
    def degree_name(self):
        return IntervalNumbers[self._number].name

    @property
    def alteration(self):
        return self._alteration

    @property
    def closest_interval(self):
        return self._closest_interval

    ##############################################

    @property
    def short_name(self):

        if self._alteration == 0:
            return self._closest_interval.short
        elif self._alteration < 0:
            short_quality = 'd'
        else:
            short_quality = 'A'
        multiple = abs(self._alteration)
        return short_quality*multiple + str(self._number)


    @property
    def full_name(self):

        if self._alteration == 0:
            return self._closest_interval.name
        elif self._alteration < 0:
            short_quality = 'd'
        else:
            short_quality = 'A'
        quality = IntervalQualities.quality(short_quality)
        multiple = IntervalQualities.multiple(abs(self._alteration))
        return ' '.join([x for x in (multiple, quality, self.degree_name) if x])


    def __str__(self):
        return self.short_name

    ##############################################

    # def inverse(self):
    #
    #     inversed_number = 9 - self._number
