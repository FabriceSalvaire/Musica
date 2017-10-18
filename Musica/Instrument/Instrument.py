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

"""
"""

####################################################################################################

__all__ = [
    ]

####################################################################################################

from Music.Theory.Pitch import Pitch

####################################################################################################

class Instrument:

    ##############################################

    def __init__(self,
                 name,
                 category,
                 # lowest_note,
                 # highest_note
    ):

        # partId
        # partName
        # partAbbreviation
        # instrumentId
        # instrumentName
        # instrumentAbbreviation
        # midiProgram
        # midiChannel
        # lowestNote (a note object or a string)
        # highestNote (a note object or a string)
        # transposition (an interval object)
        # inGMPercMap (bool – if it uses the GM percussion map)
        # soundfontFn (filepath to a sound font, optional)

        self._name = name
        self._category = category
        # self._lowest_note = lowest_note
        # self._highest_note = highest_note

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    # @property
    # def lowest_note(self):
    #     return self._lowest_note

    # @property
    # def highest_note(self):
    #     return self._highest_note
