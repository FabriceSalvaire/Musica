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

__all__ = [
    'StaveKey',
    'StaveKeys',
    'LowerBassKey',
    'BassKey',
    'LowerTrebleKey',
    'AltoKey',
    'TenorKey',
    'TrebleKey',
    'Stave',
    'StavePair',
]

####################################################################################################

from ..Theory.Pitch import Pitch

####################################################################################################

class StaveKey:

    # English note: correct word is French "clef" literally "key"
    #   pronounced \ˈklef\ in English but as clé in French (clef is legacy spelling)
    #   from Latin clavis, chiave in Italian, clave in Spanish

    __reference_pitch__ = None
    __reference_line__ = None

    ##############################################

    def __init__(self):

        self._pitch = Pitch(self.__reference_pitch__)
        self._line = self.__reference_line__ - 1

    ##############################################

    def clone(self):
        return self.__class__()

    ##############################################

    @property
    def pitch(self):
        return self._pitch

    @property
    def line(self):
        return self._line

    ##############################################

    def pitch_to_line(self, pitch):

        temperament = self._pitch.__temperament__
        delta_degree = (pitch.octave - self._pitch.octave) * temperament.number_of_natural_steps
        delta_degree += pitch.degree - self._pitch.degree
        return self._line + delta_degree / 2

    ##############################################

    def line_to_pitch(self, line):

        temperament = self._pitch.__temperament__
        delta_degree = int((line - self._line) * 2)
        delta_degree_to_ref = self._pitch.degree + delta_degree
        degree, delta_octave = temperament.fold_natural_step_number(delta_degree_to_ref, octave=True)
        octave = self._pitch.octave + delta_octave
        step_number = self._pitch.temperament.by_degree(degree).step_number
        return Pitch(step_number, octave=octave)

####################################################################################################
#
# Usual Clefs
#

class LowerBassKey(StaveKey):
    # F-clef 8va bassa
    __key_name__ = 'F8vb'
    __reference_pitch__ = 'F2' # Fa
    __reference_line__ = 4

class BassKey(StaveKey):
    # F-clef
    # passes between the two dots of the clef
    __key_name__ = 'F'
    __reference_pitch__ = 'F3' # Fa
    __reference_line__ = 4

class LowerTrebleKey(StaveKey):
    # G-clef 8va bassa
    # e.g. guitare stave
    __key_name__ = 'G8vb'
    __reference_pitch__ = 'G3' # Sol
    __reference_line__ = 2

class AltoKey(StaveKey):
    # C-clef
    # line passes through the centre of the clef
    __key_name__ = 'Alto'
    __reference_pitch__ = 'C4' # Do
    __reference_line__ = 3

class TenorKey(StaveKey):
    __key_name__ = 'Alto'
    __reference_pitch__ = 'C4' # Do
    __reference_line__ = 4

class TrebleKey(StaveKey):
    # G-clef
    # line passes through the curl of the clef
    __key_name__ = 'G'
    __reference_pitch__ = 'G4' # Sol
    __reference_line__ = 2

####################################################################################################

# Fixme: singleton ???
# Could use metaclass
StaveKeys = {cls.__key_name__:cls()
             for cls in (
                     LowerBassKey,
                     BassKey,
                     LowerTrebleKey,
                     AltoKey,
                     TenorKey,
                     TrebleKey,
             )}

####################################################################################################

# Fixme: API !!!

class NeutralKey(StaveKey):
    pass

class TablatureKey(StaveKey):
    pass

####################################################################################################
#
# Legacy Clefs
#

class FBaritoneKey(StaveKey):
    __reference_pitch__ = 'F3' # Fa
    __reference_line__ = 3

class SubBassKey(StaveKey):
    __reference_pitch__ = 'F3' # Fa
    __reference_line__ = 5

class CBaritoneKey(StaveKey):
    __reference_pitch__ = 'C4' # Do
    __reference_line__ = 5

class CMezzoSopranoKey(StaveKey):
    __reference_pitch__ = 'C4' # Do
    __reference_line__ = 2

class CSopranoKey(StaveKey):
    __reference_pitch__ = 'C4' # Do
    __reference_line__ = 1

class FrenchViolinKey(StaveKey):
    __reference_pitch__ = 'G4' # Sol
    __reference_line__ = 1

####################################################################################################

class Stave:

    __number_of_lines__ = 5

    # 5 10 ------
    # 4  8 ------
    # 3  6 ------
    # 2  4 ------
    # 1  2 ------
    # 0  0 ------

    ##############################################

    def __init__(self, key):

        self._key = key
        lower_midi = int(self._key.pitch) - 2 * self._key.line
        upper_midi = int(self._key.pitch) + 2 * (self.__number_of_lines__ - self._key.line)
        self._lower_pitch = Pitch(midi=lower_midi)
        self._upper_pitch = Pitch(midi=upper_midi)

    ##############################################

    def clone(self):
        return self.__class__(self._key)

    ##############################################

    @property
    def key(self):
        return self._key
    
    @property
    def lower_pitch(self):
        return self._lower_pitch

    @property
    def upper_pitch(self):
        return self._upper_pitch

    ##############################################

    def pitch_to_line(self, pitch):

        return self._key.pitch_to_line(pitch)

    ##############################################

    def line_to_pitch(self, line):

        return self._key.line_to_pitch(line)

####################################################################################################

class StavePair:

    ##############################################

    def __init__(self, lower_key, upper_key):

        self._lower_stave = Stave(lower_key)
        self._upper_stave = Stave(upper_key)

    ##############################################

    def clone(self):
        return self.__class__(self._lower_stave.key, self._upper_stave.key)

    ##############################################

    def pitch_to_stave(self, pitch):

        if (pitch >= self._lower_stave.lower_pitch):
            return self._upper_stave
        else:
            return self._lower_stave
