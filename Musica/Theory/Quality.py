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


"""Classes for representing interval qualities.
"""

####################################################################################################

__all__ = [
    'IntervalQualities',
    ]

####################################################################################################

from Musica.Locale import translate

####################################################################################################

class IntervalQuality:

    ##############################################

    def __init__(self, name, short):

        self._name = name
        self._short = short

    ##############################################

    def __repr__(self):
        return '{0.__class__.__name__} {0._name}'.format(self)

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def short(self):
        return self._short

    ##############################################

    def locale_name(self, language):
        return translate(self._name, language)

    ##############################################

    def format(self, degree):
        return '{0._short}{1}'.format(self, degree)

####################################################################################################

class Multiple:

    ##############################################

    def __init__(self, name, value):

        self._name = name
        self._value = value

    ##############################################

    def __repr__(self):
        return '{0.__class__.__name__} {0._name}'.format(self)

    ##############################################

    @property
    def name(self):
        return self._name

    # @property
    # def value(self):
    #     return self._value

    def __int__(self):
        return self._value

    ##############################################

    def locale_name(self, language):
        return translate(self._name, language)

    ##############################################

    def __lt__(self, other):
        return self._value < int(other)

####################################################################################################

class IntervalQualitiesSingleton:

    __qualities__ = (
        IntervalQuality('perfect',    'P'),
        IntervalQuality('minor',      'm'),
        IntervalQuality('major',      'M'),
        IntervalQuality('augmented',  'A'),
        IntervalQuality('diminished', 'd'),
    )

    __quality_to_short__ = {quality.name:quality for quality in __qualities__}
    __short_to_quality__ = {quality.short:quality for quality in __qualities__}

    __map__ = dict(__quality_to_short__)
    __map__.update(__short_to_quality__)

    ##############################################

    def __init__(self):

        # Faster than _getattr__
        for key, value in self.__map__.items():
            setattr(self, key, value)

    ##############################################

    @classmethod
    def __getitem__(cls, i):
        return cls.__map__[i]

    @classmethod
    def from_name(cls, quality):
        return cls.__quality_to_short__[quality]

    @classmethod
    def from_short(cls, short):
        return cls.__short_to_quality__[short]

####################################################################################################

IntervalQualities = IntervalQualitiesSingleton()

####################################################################################################

class MultiplesSingleton:

    __multiples__ = [None] + [Multiple(name, i)
                              for i, name in enumerate((
                                      '',          # 1
                                      'doubly',    # 2
                                      'triply',    # 3
                                      'quadruply', # 4
                              ))]
    __multiple_map__ = {multiple.name:multiple
                        for multiple in __multiples__ if multiple is not None}

    __map__ = {int(multiple):multiple for multiple in __multiple_map__.values()}
    __map__.update(__multiple_map__)
    __map__[0] = None

    ##############################################

    @classmethod
    def __getitem__(cls, i):
        return cls.__map__[i]

    @classmethod
    def from_value(cls, value):
        return cls.__multiples__[value]

    @classmethod
    def from_name(cls, name):
        return cls.__multiple_map__[name]

####################################################################################################

Multiples = MultiplesSingleton()
