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

class IntervalQualities:

    __quality_to_short__ = {
        'perfect':    'P',
        'minor':      'm',
        'major':      'M',
        'augmented':  'A',
        'diminished': 'd',
    }

    __short_to_quality__ = {value:key for key, value in __quality_to_short__.items()}

    __multiple__ =  (
        None,        # 0
        '',          # 1
        'doubly',    # 2
        'triply',    # 3
        'quadruply', # 4
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
