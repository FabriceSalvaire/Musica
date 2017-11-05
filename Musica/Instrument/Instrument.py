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
    'InstrumentWriting',
    'InstrumentTransposition',
    'Ambitus',
    'Instrument',
]

####################################################################################################

from ..Notation.Stave import Stave
from ..Theory.Pitch import Pitch, PitchInterval
from ..Tools.Abc import Named

####################################################################################################

class InstrumentWriting(Named):

    ##############################################

    def __init__(self, name, stave, pitch_interval):

        super().__init__(name)
        self._stave = stave.clone() # can be Stave or StavePair for piano
        self._pitch_interval = PitchInterval.clone(pitch_interval)

    ##############################################

    @property
    def stave(self):
        return self._stave

    @property
    def pitch_interval(self):
        return self._pitch_interval

####################################################################################################

class InstrumentTransposition(Named):

    ##############################################

    def __init__(self, name, transposition):

        super().__init__(name)
        self.transposition = Pitch(transposition)

    ##############################################

    @property
    def transposition(self):
        return self._transposition

####################################################################################################

class Ambitus(Named):

    ##############################################

    def __init__(self, name, pitch_interval):

        super().__init__(name)
        self._pitch_interval = PitchInterval.clone(pitch_interval)

    ##############################################

    @property
    def pitch_interval(self):
        return self._pitch_interval

####################################################################################################

class Instrument(Named):

    ##############################################

    def __init__(self,
                 name,
                 family='',
                 writings=[],
                 transpositions=[],
                 ambitus=[],
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

        super().__init__(name)

        self._family = family
        self._writings = {item.name:item for item in writings}
        self._transpositxions = {item.name:item for item in transpositions}
        self._ambitus = {item.name:item for item in ambitus}

    ##############################################

    @property
    def family(self):
        return self._family

    @property
    def writings(self):
        return self._writings

    @property
    def transpositions(self):
        return self._transpositions

    @property
    def ambitus(self):
        return self._ambitus

    @property
    def lowest_note(self):
        raise NotImplementedError

    @property
    def highest_note(self):
        raise NotImplementedError
