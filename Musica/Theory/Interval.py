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

class IntervalQuality:

    __quality_to_short__ = {
        'perfect':    'P',
        'minor':      'm',
        'major':      'M',
        'augmented':  'A',
        'diminished': 'd',
    }

    __short_to_quality__ = {value:key for key, value in __quality_to_short__.items()}

    __multiple__ =  (
        None,
        '',
        'doubly',
        'triply',
        )

    ##############################################

    @classmethod
    def short(cls, quality):
        return cls.__quality_to_short__[quality]

    @classmethod
    def quality(cls, short):
        return cls.__short_to_quality__[short]

    @classmethod
    def multiple(cls, i):
        return cls.__multiple__[i]

####################################################################################################

class IntervalNumber:

    ##############################################

    def __init__(self, number, name, qualities):

        self._number = number
        self._name = name
        self._qualities = qualities

    ##############################################

    @property
    def number(self):
        return self._number

    @property
    def name(self):
        return self._name

    @property
    def qualities(self):
        return self._qualities

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

    __interval_numbers__ = sorted((
        IntervalNumber(
            number=1,
            name='unison', # prime unison
            qualities='perfect',
        ),
        IntervalNumber(
            number=2,
            name='second', # seconde
            qualities=('minor', 'major'),
        ),
        IntervalNumber(
            number=3,
            name='third', # tierce
            qualities=('minor', 'major'),
        ),
        IntervalNumber(
            number=4,
            name='fourth', # quarte
            qualities='perfect',
        ),
        IntervalNumber(
            number=5,
            name='fifth', # quinte
            qualities='perfect',
        ),
        IntervalNumber(
            number=6,
            name='sixth', # sixte
            qualities=('minor', 'major'),
        ),
        IntervalNumber(
            number=7,
            name='seventh', # septième
            qualities=('minor', 'major'),
        ),
        IntervalNumber(
            number=8,
            name='octave',
            qualities='perfect',
        ),
    ))

    ##############################################

    def __getitem__(self, number):
        return self.__interval_numbers__[number -1]

IntervalNumbers = IntervalNumbersSingleton()

####################################################################################################

class MainInterval:

    ##############################################

    def __init__(self,
                 number_of_semitones,
                 name, short,
                 altered_name, altered_short,
                 frequency_ratio,
                 alternative_names=None, alternative_short=None,
    ):

        self._number_of_semitones = number_of_semitones
        self._name = name
        self._short = short
        self._altered_name = altered_name
        self._altered_short = altered_short
        self._frequency_ratio = frequency_ratio
        self._alternative_names = alternative_names
        self._alternative_short = alternative_short

        if short is not None:
            self._quality = short[0]
            self._degree = int(short[1])
        else:
            self._quality = None
            self._degree = None

    ##############################################

    @property
    def number_of_semitones(self):
        return self._number_of_semitones

    @property
    def name(self):
        return self._name

    @property
    def short(self):
        return self._short

    @property
    def quality(self):
        return self._quality

    @property
    def degree(self):
        return self._degree

    ##############################################

    def __repr__(self):
        return self._name

    ##############################################

    def __int__(self):
        return self._number_of_semitones

    def __lt__(self, other):
        return self._number_of_semitones < int(other)

####################################################################################################

class MainIntervals:

    __main_intervals__ = sorted((
        MainInterval(
            number_of_semitones=0,
            name='perfect unison', # prime unison
            short='P1',
            altered_name='diminished second',
            altered_short='d2',
            frequency_ratio='1:1',
        ),
        MainInterval(
            number_of_semitones=1,
            name='minor second', # seconde
            short='m2',
            altered_name='augmented unison',
            altered_short='A1',
            alternative_names=('semitone', 'half tone', 'half step'),
            alternative_short='S',
            frequency_ratio='16:15',
        ),
        MainInterval(
            number_of_semitones=2,
            name='major second',
            short='M2',
            altered_name='diminished third',
            altered_short='d3',
            alternative_names=('tone', 'whole tone', 'whole step'),
            alternative_short='S',
            frequency_ratio='9:8',
        ),
        MainInterval(
            number_of_semitones=3,
            name='minor third', # tierce
            short='m3',
            altered_name='augmented second',
            altered_short='A2',
            frequency_ratio='6:5',
        ),
        MainInterval(
            number_of_semitones=4,
            name='major third',
            short='M3',
            altered_name='diminished fourth',
            altered_short='d4',
            frequency_ratio='5:4',
        ),
        MainInterval(
            number_of_semitones=5,
            name='perfect fourth', # quarte
            short='P4',
            altered_name='augmented third',
            altered_short='A3',
            frequency_ratio='4:3',
        ),
        MainInterval(
            number_of_semitones=6,
            name=None,
            short=None,
            altered_name=('diminished fifth', 'augmented fourth'),
            altered_short=('d5', 'A4'),
            alternative_names='tritone',
            alternative_short='TT',
            frequency_ratio='',
        ),
        MainInterval(
            number_of_semitones=7,
            name='perfect fifth', # quinte
            short='P5',
            altered_name='diminished sixth',
            altered_short='d6',
            frequency_ratio='3:2',
        ),
        MainInterval(
            number_of_semitones=8,
            name='minor sixth', # sixte
            short='m6',
            altered_name='augmented fifth',
            altered_short='A5',
            frequency_ratio='8:5',
        ),
        MainInterval(
            number_of_semitones=9,
            name='major sixth',
            short='M6',
            altered_name='diminished seventh',
            altered_short='d7',
            frequency_ratio='5:3',
        ),
        MainInterval(
            number_of_semitones=10,
            name='minor seventh', # septième
            short='m7',
            altered_name='augmented sixth',
            altered_short='A6',
            frequency_ratio='16:9',
        ),
        MainInterval(
            number_of_semitones=11,
            name='major seventh',
            short='M7',
            altered_name='diminished octave',
            altered_short='d8',
            frequency_ratio='15:8',
        ),
        MainInterval(
            number_of_semitones=12,
            name='perfect octave',
            short='P8',
            altered_name='augmented seventh',
            altered_short='A7',
            frequency_ratio='2:1',
        ),
    ))

    __degree_to_interval__ = [None]
    for interval in __main_intervals__:
        if interval.degree is not None:
            if len(__degree_to_interval__) < interval.degree +1:
                __degree_to_interval__.append([interval])
            else:
                __degree_to_interval__[interval.degree].append(interval)

    ##############################################

    @classmethod
    def intervals_for_degree(cls, degree):
        return cls.__degree_to_interval__[degree]

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

        inf_degree = cls.__temperament__.name_to_degree(inf)
        sup_degree = cls.__temperament__.name_to_degree(sup)

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
        if number_of_semitones < 0:
            number_of_semitones += self.__temperament__.number_of_steps # or % 12

        deltas = [(number_of_semitones - interval.number_of_semitones, interval)
                  for interval in MainIntervals.intervals_for_degree(self._number)]
        alteration, closest_interval = sorted(deltas, key=lambda x: x[0])[0]

        self._number_of_semitones = number_of_semitones
        self._alteration = alteration
        self._closest_interval = closest_interval

        print(self)

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
        quality = IntervalQuality.quality(short_quality)
        multiple = IntervalQuality.multiple(abs(self._alteration))
        return ' '.join([x for x in (multiple, quality, self.degree_name) if x])


    def __str__(self):
        return self.short_name
