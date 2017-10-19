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
    'Accidental',
    'Pitch',
    ]

####################################################################################################

import re

from ..Locale.Unicode import to_unicode
from .Temperament import ET12

####################################################################################################

class Accidental:

    """Accidental class, representing the symbolic and numerical representation of
    pitch deviation from a pitch name (e.g. C).
    """

    __modifier_regexp__ = re.compile('[#-]*') # Fixme: ~`

    __name_to_alteration__ = {
        'natural': 0,
        #
        'sharp': 1,
        'double-sharp': 2,
        'triple-sharp': 3,
        'quadruple-sharp': 4,
        #
        'flat': -1,
        'double-flat': -2,
        'triple-flat': -3,
        'quadruple-flat': -4,
        #
        'half-sharp': .5,
        'one-and-a-half-sharp': 1.5,
        'half-flat': .5,
        'one-and-a-half-flat': -1.5,
    }

    __name_to_modifier__ = {
        'natural': '',
        #
        'sharp': '#',
        'double-sharp': '##',
        'triple-sharp': '###',
        'quadruple-sharp': '####',
        #
        'flat': '-',
        'double-flat': '--',
        'triple-flat': '---',
        'quadruple-flat': '----',
        #
        'half-sharp': '~',
        'one-and-a-half-sharp': '#~',
        'half-flat': '`',
        'one-and-a-half-flat': '-`',
    }

    ##############################################

    @classmethod
    def parse_accidental(cls, value):

        """Return an alteration from a :class:`Alteration` instance, an alteration name or a modifier
        string.

        """

        # Fixme: ~`

        if isinstance(value, cls):
            return value.alteration
        else:
            try:
                return cls.__name_to_alteration__[value]
            except KeyError:
                value = str(value)
                if not value:
                    return 0
                elif cls.__modifier_regexp__.match(value) is not None:
                    number_of_flat = value.count('-')
                    number_of_sharp = value.count('#')
                    return number_of_sharp - number_of_flat
                else:
                    raise ValueError("Invalid accidental {}".format(value))

    ##############################################

    def __init__(self, accidental_value):

        # Fixme: don't keep modifer string
        self.alteration = accidental_value

    ##############################################

    def clone(self):

        return self.__class__(self)

    ##############################################

    @property
    def alteration(self):
        return self._alteration

    @alteration.setter
    def alteration(self, value):
        self._alteration = self.parse_accidental(value)

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

    @property
    def name(self):
        return self.__alteration_to_name__[self._alteration]

    @property
    def unicode_name(self):
        return to_unicode(self.name)

    @property
    def modifier(self):
        return self.__name_to_modifier__[self.name]

    def __str__(self):
        return self.modifier

    ##############################################

    def __eq__(self, other):

        if other is not None:
            return self._alteration == other.alteration
        else:
            return False

Accidental.__alteration_to_name__ = {
    alteration:name for name, alteration in Accidental.__name_to_alteration__.items()}

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

        _name = str(name).lower()
        match = cls.__pitch_regexp__.match(_name)
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

    def __init__(self, name=None, **kwargs):

        self._spelling_is_inferred = False

        if name is not None:
            # Fixme. type(self) vs self.__class__
            if isinstance(name, Pitch):
                self._init_from_clone(name)
            else:
                try:
                    step_number = int(name)
                except ValueError:
                    step_number = None
                if step_number is not None:
                    self._init_from_number(step_number, kwargs)
                else:
                    self._init_from_string(name)
        else:
            self._init_from_kwargs(kwargs)

    ##############################################

    def _init_from_clone(self, other):

        self._step = other._step
        self.accidental = other._accidental
        self._octave = other._octave

    ##############################################

    def _init_from_string(self, name):

        step, accidental, octave = self.parse_pitch(name)
        self._step = step
        self._accidental = accidental
        self._octave = octave

    ##############################################

    def _init_from_number(self, step_number, kwargs):

        try:
            name = self.__temperament__.number_to_name(step_number)
        except KeyError:
            raise ValueError('Invalid pitch number {}'.format(name))

        if name is None: # alteration
            self._step = self.__temperament__.number_to_name(step_number -1)
            self._accidental = Accidental('#')
            self._spelling_is_inferred = True
        else:
            self._step = name
            self._accidental = None

        self._octave = kwargs.get('octave', None)

    ##############################################

    def _init_from_kwargs(self, kwargs):

        self.step = kwargs['step']
        accidental = kwargs.get('accidental', None)
        if accidental is not None:
            self.accidental = Accidental(accidental)
        else:
            self._accidental = None
        self._octave = kwargs.get('octave', None)

    ##############################################

    def clone(self):

        return self.__class__(self)

    ##############################################

    def __repr__(self):

        return '{} {}'.format(self.__class__.__name__, str(self))

    ##############################################

    @property
    def temperament(self):
        return self.___temperament__

    ##############################################

    @property
    def pitch_class(self):
        """Returns the integer value for the pitch, between 0 and 11, where C=0, C#=1, D=2, ... B=11.
        """
        return self.__temperament__.name_to_number(self._step) + int(self.alteration)

    @pitch_class.setter
    def pitch_class(self, value):
        self._init_from_number(value) # Fixme: reset octave !

    ##############################################

    @property
    def step(self):
        """The diatonic name of the note; i.e. it does not give the accidental and octave."""
        return self._step

    @step.setter
    def step(self, value):

        _value = value.upper()
        if self.__temperament__.is_valid_step_name(_value):
            self._step = _value
        else:
            raise ValueError("Invalid step {}".format(value))

    @property
    def spelling_is_inferred(self):
        return self._spelling_is_inferred

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

    @property
    def alteration(self):
        if self._accidental is not None:
            return self._accidental.alteration
        else:
            return 0

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

    def _to_string(self, unicode=False, octave=False):
        name = self._step
        if self._accidental is not None:
            name += str(self._accidental)
        if octave and self._octave is not None:
            name += str(self._octave)
        return name

    @property
    def name(self):
        return self._to_string()

    @property
    def full_name(self):
        return self._to_string(octave=True)

    @property
    def unicode_name(self):
        return self._to_string(unicode=True)

    @property
    def unicode_name_with_octave(self):
        return self._to_string(octave=True, unicode=True)

    def __str__(self):
        return self.full_name

    ##############################################

    @property
    def locale(self):
        # Return :class:`Musica.Locale.Note.NoteNameTranslation`
        return self.__temperament__.translator(self.pitch_class) # self.name

    ##############################################

    @property
    def english_locale(self):
        return self.locale['english']

    ##############################################

    @property
    def french_locale(self):
        return self.locale['français']

    ##############################################

    def __eq__(self, other):

        # By default, __ne__() delegates to __eq__() and inverts the result

        return (self._step == other.step and
                self._accidental == other.accidental and
                self._octave == other.octave)

    ##############################################

    def _compute_float_value(self, octave):

        value = (octave + 1) * self.__temperament__.number_of_steps
        value += self.__temperament__.name_to_number(self._step)
        if self._accidental is not None:
            value += self._accidental.alteration
        # if self.microtone is not None:
        #     value += self.microtone.alter
        return float(value)

    def __float__(self):
        return float(self._compute_float_value(self.implicit_octave))

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

    ##############################################

    def __lt__(self, other):
        return float(self) < float(other)

    def __le__(self, other):
       return float(self) <= float(other)

    def __gt__(self, other):
        return float(self) > float(other)

    def __te__(self, other):
       return float(self) >= float(other)

    ##############################################

    @property
    def frequency(self):

        return self.__temperament__.frequency(self.implicit_octave, self.pitch_class)

    ##############################################

    def is_enharmonic(self, other):

        # Fixme: _compute_float_value, same __temperament__
        bool1 = self.octave is not None
        bool2 = other.octave is not None
        if bool1 and bool2:
            ps1 = float(self)
            ps2 = float(octave)
        elif bool1 and not bool2:
            ps1 = float(other)
            ps2 = self._compute_float_value(self.octave)
        elif not bool1 and bool2:
            ps1 = self._compute_float_value(other.octave)
            ps2 = float(other)
        else:
            # use __implicit_octave__ for both
            ps1 = float(self)
            ps2 = float(octave)

        return ps1 == ps2 and self.alteration != other.alteration

    ##############################################

    # get_enharmonic(*, in_place=False)

    # Returns a new Pitch that is the(/an) enharmonic equivalent of this Pitch. Can be thought of as flipEnharmonic or something like that.
    #
    # N.B.: n1.name == getEnharmonic(getEnharmonic(n1)).name is not necessarily true. For instance:
    #
    #     getEnharmonic(E##) => F# getEnharmonic(F#) => G- getEnharmonic(A–) => G getEnharmonic(G) => F##
    #
    # However, for all cases not involving double sharps or flats (and even many that do), getEnharmonic(getEnharmonic(n)) = n
    #
    # For the most ambiguous cases, it’s good to know that these are the enharmonics:
    #
    #     C <-> B#, D <-> C##, E <-> F-; F <-> E#, G <-> F##, A <-> B–, B <-> C-
    #
    # However, isEnharmonic() for A## and B certainly returns True.

    ##############################################

    def pitch_iterator(self, until):

        # Fixme: complex accidental ???

        if until < self:
            raise StopIteration

        number_of_steps = self.__temperament__.number_of_steps

        pitch_class = self.pitch_class
        octave = self.octave

        while True:
            pitch = self.__class__(pitch_class, octave=octave)
            yield pitch
            if pitch == until:
                raise StopIteration
            pitch_class += 1
            if pitch_class == number_of_steps:
                pitch_class = 0
                octave += 1
