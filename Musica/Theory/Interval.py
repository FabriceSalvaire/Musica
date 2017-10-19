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
    ]

####################################################################################################

from .Temperament import ET12

####################################################################################################

class Interval:

    #! Assume a Twelve-tone equal temperament
    __temperament__ = ET12

    ##############################################

    @staticmethod
    def number_from_note(inf, sup):

        """Return interval number between *inf* and *sup*"""

        inf_degree = self.__temperament__.name_to_degree(inf)
        sup_degree = self.__temperament__.name_to_degree(sup)

        delta = sup_degree - inf_degree
        if delta > 0:
            delta += 1
        elif delta < 0:
            delta += self.__temperament__.number_of_names
        # else: delta = 0 # unison or octave

        return delta

    ##############################################

    def __init__(self, inf, sup):

        self._inf = inf
        self._sup = sup
