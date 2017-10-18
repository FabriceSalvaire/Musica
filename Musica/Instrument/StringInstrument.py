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

class String:

    ##############################################

    def __init__(self, pitch, length):

        self._pitch = pitch
        self._length = length

    ##############################################

    @property
    def pitch(self):
        return self._pitch

    @property
    def length(self):
        return self._length

    ##############################################

    def __eq__(self, other):
        return self._pitch == other.pitch and self._length = other.length

####################################################################################################

class StringTuning:

    ##############################################

    def __init__(self, name, *pitches):

        self._name = name
        self._pitches = pitches

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def number_of_strings(self):
        return len(self._pitches)

    @property
    def pitches(self):
        return self._pitches

    ##############################################

    def __eq__(self, other):
        return self._pitches == other.pitches

    ##############################################

    def __len__(self):
        return len(self._pitches)

    ##############################################

    def __iter__(self):
        return iter(self._pitches)

    ##############################################

    def __getitem__(self, index):

        if isinstance(index, Pitch):
            string = self._pitches.find(index)
            if string == -1:
                raise IndexError()
            else:
                return string
        else:
            return self._pitches[index]

####################################################################################################

class StringInstrument(Instrument):

    # https://en.wikipedia.org/wiki/Stringed_instrument_tunings

    ##############################################

    def __init__(self,
                 name,
                 category,
                 standard_tuning):

        super().__init__(name, category)

        self._standard_tuning = standard_tuning
        self._tuning = standard_tuning

    ##############################################

    @property
    def standard_tuning(self):
        return self._standard_tuning

    @property
    def number_of_strings(self):
        return len(self._standard_tuning)

    @property
    def tuning(self):
        return self._tuning

    @tuning.setter
    def tuning(self, value):
        self._tuning = value

####################################################################################################

class GuitareTuning: # Fixme: metaclass

    standard = StringTuning(
        name='standard',
        pitches=(
            'E2', # Mi
            'A2', # La
            'D3', # Ré
            'G3', # Sol
            'B3,' # Si
            'E4', # Mi
            ),
        )

    drop_d = StringTuning(
        name='drop_d',
        pitches=(
            'D2', # Ré
            'A2', # La
            'D3', # Ré
            'G3', # Sol
            'B3,' # Si
            'E4', # Mi
            ),
        )

    # Drop D: D2 A2 D3 G3 B3 E4
    # Open D: D2 A2 D3 F#3 A3 D4
    # Open G: D2 G2 D2 G2 B3 D4
    # Open A: E2 A2 E3 A3 C#4 E4
    # Lute: E2 A2 D3 F#3 B3 E4
    # Irish: D2 A2 D3 G3 A3 D4

    # Guitar, Alto 11 strings Bb1 C2 D2 Eb2 F2 G2 C3 F3 Bb3 D4 G4
    # Guitar, Alto 13 strings A1 Bb1 C2 D2 E2 F2 G2 A2 D3 F3 A3 D4 F4
    # Guitar, Alto (Niibori) 6 strings B2 E3 A3 D4 F#4 B4
    # Guitar, 7 string
    #   Standard/Common: B1 E2 A2 D3 G3 B3 E4
    #   Van Eps: A1 E2 A2 D3 G3 B3 E4
    #   Choro: C2 E2 A2 D3 G3 B3 E4
    # Guitar, 8 string B1 E2 A2 D3 G3 B3 E4 A4
    #   [B1 D2] E2 A2 D3 G3 B3 E4
    # Guitar, 9 string E3 E2 A3 A2 D4 D3 G3 B3 E4
    #   E2  A2  D3  G4 G3 B3 B3 E4 E4
    #   F#1 B1 E2 A2 D3 G3 B3 E4 A4
    # Guitar, 10 string F#2 G#2 A#2 C2 E2 A2 D3 G3 B3 E4
    # Guitar, 12 string
    #   Standard/Common: E3 E2 A3 A2 D4 D3 G4 G3 B3 B3 E4 E4
    #   Variant: E4 E2 A3 A2 D4 D3 G4 G3 B3 B3 E4 E4
    #   All 6-string alternates may be adapted to 12-string.
    # Guitar, baritone
    #   4th lower: B1 E2 A2 D3 F#3 B3
    #   5th lower: A1 D2 G2 C3 E3 A3
    #   Octave lower: E1 A1 D2 G2 B2 E3

####################################################################################################

class Guitare(StringInstrument):

    ##############################################

    def __init__():

        super().__init__(
            name='guitare',
            category='fretted string/guitare',
            standard_tuning=GuitareTuning.standard,
        )

####################################################################################################

class BassGuitareTuning:

    standard_4_string = StringTuning(
        name='standard_4_string',
        pitches=(
            'E1', # Mi
            'A1', # La
            'D2', # Ré
            'G2', # Sol
            ),
        )

    standard_5_string = StringTuning(
        name='standard_5_string',
        pitches=(
            'B0', # Si
            'E1', # Mi
            'A1', # La
            'D2', # Ré
            'G2', # Sol
            ),
        )

    standard_5_string_tenor = StringTuning(
        name='standard_5_string_tenor',
        pitches=(
            'E1', # Mi
            'A1', # La
            'D2', # Ré
            'G2', # Sol
            'C3', # Do
            ),
        )

    standard_6_string = StringTuning(
        name='standard_6_string',
        pitches=(
            'B0', # Si
            'E1', # Mi
            'A1', # La
            'D2', # Ré
            'G2', # Sol
            'C3', # Do
            ),
        )

    # Guitar, bass
    #   Standard/Common: E1 A1 D2 G2
    #   Alternates:
    #       D1 A1 D2 G2
    #       D1 G1 C2 F2
    # Guitar, bass (5-string)
    #   Standard/Common:
    #   B0 E1 A1 D2 G2
    #   E1 A1 D2 G2 C3
    # Guitar, bass (6-string)
    #   Standard/Common: B0 E1 A1 D2 G2 C3
    #   Alternate: E1 A1 D2 G2 B2 E3
    # Guitar, bass (8-string) E2 E1 A2 A1 D3 D2 G3 G2
    # Guitar, bass (12-string) E2 E2 E1 A2 A2 A1 D3 D3 D2 G3 G3 G2
    # Guitar, octave E3 A3 D4 G4 B4 E5

####################################################################################################

# Piano A0 A#0 B0 C1 C#1 D1 D#1 E1 F1 F#1 G1 G#1 ... C#7 D7 D#7 E7 F7 F#7 G7 G#7 A7 A#7 B7 C8

# Double bass 4 strings
#    Standard/Common: E1 A1 D2 G2
#    Alternates:
#      Drop D: D1 A1 D2 G2
#      Solo Tuning: F#1 B1 E2 A2
#      With low 'C' machine: C1 A1 D2 G2
#     'C' Machine "Legion": B0 A1 D2 G2
# Double bass, 5-string
#    Standard/Common: C1 E1 A1 D2 G2
#   Alternates:
#     Modern 4th tuning: B0 E1 A1 D2 G2
