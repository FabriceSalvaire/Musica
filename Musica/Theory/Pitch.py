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

"""Classes for representing and manipulating pitches, pitch-space, and accidentals.

"""

####################################################################################################

__all__ = [
    'PitchStandard',
    'A440',
    'EqualTemperament',
    'ET12',
    'Accidental',
    'Pitch',
    ]

####################################################################################################

import re

####################################################################################################

class PitchStandard:

    """Class to define a pitch standard.

    Octave are numbered according SPN and step (semitone) numbers lie from 0 to 11.

    To define A440 use :code:`PitchStandard(name='A440', frequency=440, octave_number=4, step_number=9)`
    """

    def __init__(self, name, frequency, octave_number, step_number):

        self._name = name
        self._frequency = frequency
        self._octave_number = octave_number
        self._step_number = step_number

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def frequency(self):
        return self._frequency

    @property
    def octave_number(self):
        return self._octave_number

    @property
    def step_number(self):
        return self._step_number

####################################################################################################

#: A440 or A4, also known as the Stuttgart pitch, which has a frequency of 440 Hz,
#  is the musical note of A above middle C
#  and serves as a general tuning standard for musical pitch.
A440 = PitchStandard(name='A440', frequency=440, octave_number=4, step_number=9)

####################################################################################################

class EqualTemperament:

    """Class to define an Equal Temperament.

    Step is an alias for semitone.
    """

    ##############################################

    def __init__(self, number_of_steps, pitch_standard):

        self._number_of_steps = number_of_steps
        self._pitch_standard = pitch_standard

        self._fundamental = self._compute_fundamental()

    ##############################################

    @property
    def number_of_steps(self):
        return self._number_of_steps

    @property
    def pitch_standard(self):
        return self._pitch_standard

    @property
    def fundamental(self):
        """Return the frequency of C0"""
        return self._fundamental

    ##############################################

    def _compute_scale(self, octave_number, step_number):

        octave_factor = 2 ** octave_number
        interval_factor = 2 ** (step_number / self._number_of_steps)
        return octave_factor * interval_factor

    ##############################################

    def _compute_fundamental(self):

        denominator = self._compute_scale(self._pitch_standard.octave_number,
                                          self._pitch_standard.step_number)
        return self._pitch_standard.frequency / denominator

    ##############################################

    def frequency(self, octave_number, step_number):

        """Return the frequency for an octave using the scientific pitch notation and an step number
        ranging from 0 to 11.

        For A440 (La3), use octave 4 and step number 9.

        """

        return self._fundamental * self._compute_scale(octave_number, step_number)

####################################################################################################

class TwelveToneEqualTemperament(EqualTemperament):

    """Twelve-tone equal temperament, also known as 12 equal temperament, 12-TET, or 12-ET"""

    __step_names__ = ('A', 'B', 'C', 'D', 'E', 'F', 'G')

    __step_name_to_number__ = {
        'C' : 0,
        'D' : 2,
        'E' : 4,
        'F' : 5,
        'G' : 7,
        'A' : 9,
        'B' : 11,
    }

    ##############################################

    def __init__(self):

        super().__init__(number_of_steps=12, pitch_standard=A440)

#: Twelve-tone equal temperament alias
ET12 = TwelveToneEqualTemperament()

####################################################################################################

class Accidental:

    """Accidental class, representing the symbolic and numerical representation of
    pitch deviation from a pitch name (e.g. C).
    """

    __accidental_regexp__ = re.compile('[#-]*')

    # __accidental_name_to_modifier__ = {
    #     'natural': '',
    #     'sharp': '#',
    #     'double-sharp': '##',
    #     'triple-sharp': '###',
    #     'quadruple-sharp': '####',
    #     'flat': '-',
    #     'double-flat': '--',
    #     'triple-flat': '---',
    #     'quadruple-flat': '----',
    #     'half-sharp': '~',
    #     'one-and-a-half-sharp': '#~',
    #     'half-flat': '`',
    #     'one-and-a-half-flat': '-`',
    # }

    ##############################################

    @classmethod
    def reduce_accidental(cls, value):

        if isinstance(value, cls):
            return value.accidental
        else:
            value = str(value)
            if not value:
                return 0
            elif cls.__accidental_regexp__.match(value) is not None:
                number_of_flat = value.count('-')
                number_of_sharp = value.count('#')
                return number_of_sharp - number_of_flat
            else:
                raise ValueError("Invalid accidental {}".format(value))

    ##############################################

    def __init__(self, accidental_string):

        self.alteration = accidental_string

    ##############################################

    def clone(self):

        return self.__class__(self)

    ##############################################

    @property
    def alteration(self):
        return self._alteration

    @alteration.setter
    def alteration(self, value):
        self._alteration = self.reduce_accidental(value)

    ##############################################

    @property
    def is_normal(self):
        return self._alteration == 0

    @property
    def is_flat(self):
        return self._alteration < 0

    @property
    def is_sharp(self):
        return self._alteration > 0

    ##############################################

    def __eq__(self, other):

        return self._alteration == other.alteration

####################################################################################################

class Pitch:

    """Class to represents a pitch.
    """

    #! Define an implicit octave so as to be able to define a float value
    __implicit_octave__ = 4

    #! Assume a Twelve-tone equal temperament
    __temperament__ = ET12

    # Fixme: note re
    __pitch_regexp__ = re.compile('(?P<note>[abcdefg])(?P<accidental>[#-]*)(?P<octave>\d*)')

    ##############################################

    @classmethod
    def parse_pitch(cls, name, return_dict=False):

        match = cls.__pitch_regexp__.match(name.lower())
        if match is not None:
            note = match['note'].upper()
            accidental = match['accidental']
            accidental = Accidental(accidental) if accidental else None
            octave = match['octave']
            octave = int(octave) if octave else None
            if return_dict:
                return dict(note=note, accidental=accidental, octave=octave)
            else:
                return note, accidental, octave
        else:
            raise ValueError("Invalid pitch {}".format(name))

    ##############################################

    def __init__(self, name):

         # Fixme. type(self) vs self.__class__
        if isinstance(name, Pitch):
            self._step = name._step
            self.accidental = name._accidental
            self._octave = name._octave
        else:
            step, accidental, octave = self.parse_pitch(name)
            self._step = step
            self._accidental = accidental
            self._octave = octave

    ##############################################

    def clone(self):

        return self.__class__(self)

    ##############################################

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):

        _value = value.upper()
        if _value in self.__temperament__.__step_names__:
            self._step = _value
        else:
            raise ValueError("Invalid step {}".format(value))

    ##############################################

    @property
    def accidental(self):
        return self._accidental

    @accidental.setter
    def accidental(self, value):

        if value is not None:
            self._accidental = Accidental(value)
        else:
            self._accidental = None

    ##############################################

    @property
    def octave(self):
        return self._octave

    @octave.setter
    def octave(self, value):

        _value = int(value)
        if _value > 0:
            self._octave = value
        else:
            raise ValueError("Invalid octave {}".format(value))

    @property
    def implicit_octave(self):
        return self.__implicit_octave__ if self._octave is None else self._octave

    ##############################################

    def __eq__(self, other):

        return (self._pitch == other.pitch and
                self._accidental == other.accidental and
                self._octave == other.octave)

    ##############################################

    def __float__(self):

        value = (self.implicit_octave + 1) * self.__temperament__.number_of_steps
        value += self.__temperament__.__step_name_to_number__[self._step]
        if self._accidental is not None:
            value += self._accidental.alteration
        # if self.microtone is not None:
        #     value += self.microtone.alter
        return float(value)

    @property
    def midi_float(self):
        return float(self)

    ##############################################

    @property
    def midi(self):

        """Return the closest midi code.

        The MIDI specification only defines note number 60 as "Middle C" (C4, Do3), and all other
        notes are relative. Note are encoded by a 7-bit non signed integer, ranging from 0 to 127.
        Consequently, Midi map note C0 to 0, C#0 to 1, ... and G10 to 127.

        """

        return int(round(float(self)))
