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

    __alteration_to_name__ = {alteration:name for name, alteration in __name_to_alteration__.items()}

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

####################################################################################################

class Pitch:

    """Class to represents a pitch.
    """

    # Fixme: negative octave
    #  use ~ for bemol : C-1 versus C~-1

    #! Define an implicit octave so as to be able to define a float value
    __implicit_octave__ = 4

    #! Assume a Twelve-tone equal temperament
    __temperament__ = ET12

    # Fixme: note re
    __pitch_regexp__ = re.compile('(?P<note>[abcdefg])(?P<accidental>[#-]*)(?P<octave_sign>(/-)?)(?P<octave>\d*)')

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
            if match['octave_sign']:
                octave = - octave
            if return_dict:
                return dict(note=note, accidental=accidental, octave=octave)
            else:
                return note, accidental, octave
        else:
            raise ValueError("Invalid pitch {}".format(name))

    ##############################################

    def __init__(self, name=None, **kwargs):

        # self._step = 'C', 'D', ... 'G'
        # self._step_number = 0 2 ... 11 only natural
        # self._accidental = Accidental()
        # self._octave = int

        self._spelling_is_inferred = False # for accidental, e.g. 1 is inferred as C# versus D-

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
                    self._init_from_string(name, kwargs)
        else:
            self._init_from_kwargs(kwargs)

        # Fixme: self.step = ... ?
        self._step_number = self.__temperament__.name_to_number(self._step)

    ##############################################

    def _init_from_clone(self, other):

        self._step = other._step
        self.accidental = other._accidental
        self._octave = other._octave

    ##############################################

    def _init_from_string(self, name, kwargs):

        step, accidental, octave = self.parse_pitch(name)
        self._step = step
        self._accidental = accidental
        self._octave = octave

        if octave is None:
            self._octave = kwargs.get('octave', None)

    ##############################################

    def _init_from_number(self, step_number, kwargs):

        try:
            step = self.__temperament__[step_number]
        except IndexError:
            raise ValueError('Invalid pitch number {}'.format(step_number))

        if step.is_natural:
            self._step = step.name
            self._accidental = None
        else:
            self._step = step.prev_natural.name
            self._accidental = Accidental('#')
            self._spelling_is_inferred = True

        self._octave = kwargs.get('octave', None)

    ##############################################

    def _init_from_kwargs(self, kwargs):

        if 'midi' in kwargs:
            pitch_int = kwargs['midi']
            step_number, octave = self.__temperament__.fold_step_number(pitch_int, octave=True)
            octave -= 1 # C4 60 -> 0, 5
            self._init_from_number(step_number, dict(octave=octave))
        else:
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
        return self.__temperament__

    ##############################################

    @property
    def pitch_class(self):
        """Returns the integer value for the pitch, between 0 and 11, where C=0, C#=1, D=2, ... B=11.
        """
        if self.alteration is None:
            return self._step_number
        else:
            # Fixme: cache ?
            return self.__temperament__.fold_step_number(self._step_number + int(self.alteration))

    @pitch_class.setter
    def pitch_class(self, value):
        self._init_from_number(value) # Fixme: reset octave !

    ##############################################

    @property
    def step_number(self):
        return self._step_number

    @property
    def step(self):
        """The diatonic name of the note; i.e. it does not give the accidental and octave."""
        return self._step

    @step.setter
    def step(self, value):

        _value = value.upper()
        if self.__temperament__.is_valid_step_name(_value):
            self._step = _value
            self._step_number = self.__temperament__.name_to_number(self._step)
        else:
            raise ValueError("Invalid step {}".format(value))

    @property
    def spelling_is_inferred(self):
        return self._spelling_is_inferred

    @property
    def degree(self):
        return self.__temperament__[self._step_number].degree

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
    def is_altered(self):
        return self._accidental is not None

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

        # Fixme: complex accidental can alter octave too !

        _value = int(value)
        if _value > 0:
            self._octave = value
        else:
            raise ValueError("Invalid octave {}".format(value))

    @property
    def implicit_octave(self):
        return self.__implicit_octave__ if self._octave is None else self._octave

    ##############################################

    def _locale(self, natural=False):

        translator = self.__temperament__.translator
        if natural:
            note = self._step_number
        else:
            note = self.pitch_class

        return translator(note)

    ##############################################

    @property
    def natural_locale(self):
        # Return :class:`Musica.Locale.Note.NoteNameTranslation`
        return self._locale(natural=True)

    @property
    def locale(self):
        # Return :class:`Musica.Locale.Note.NoteNameTranslation`
        return self._locale()

    @property
    def english_locale(self):
        return self.locale['english']

    @property
    def french_locale(self):
        return self.locale['français']

    ##############################################

    def str(self, locale=None, latin=False, unicode=False, octave=False):

        if latin:
            locale = 'français' # or similar
        if locale is not None:
            name = self.natural_locale[locale].name # to get step without accidental
        else:
            name = self._step

        if self._accidental is not None:
            if unicode:
                accidental = self._accidental.unicode_name
            else:
                accidental = str(self._accidental)
            name += accidental

        if octave and self._octave is not None:
            if self._octave < 0:
                name += '/' # Fixme: ???
            name += str(self._octave)

        return name

    ##############################################

    @property
    def name(self):
        return self.str()

    @property
    def full_name(self):
        return self.str(octave=True)

    @property
    def unicode_name(self):
        return self.str(unicode=True)

    @property
    def latin_unicode_name(self):
        return self.str(latin=True, unicode=True)

    @property
    def unicode_name_with_octave(self):
        return self.str(unicode=True, octave=True)

    # Fixme: shorter ???
    @property
    def latin_unicode_name_with_octave(self):
        return self.str(latin=True, unicode=True, octave=True)

    def __str__(self):
        return self.full_name

    ##############################################

    def __eq__(self, other):

        # By default, __ne__() delegates to __eq__() and inverts the result

        return (self._step == other.step and
                self._accidental == other.accidental and
                self._octave == other.octave)

    ##############################################

    def _compute_float_value(self, octave, add_microtone=True):

        value = (octave + 1) * self.__temperament__.number_of_steps
        value += self._step_number
        if self._accidental is not None:
            value += self._accidental.alteration
        if add_microtone:
            # if self.microtone is not None:
            #     value += self.microtone.alter
            return float(value)
        else:
            return value

    def __int__(self):
        return self._compute_float_value(self.implicit_octave, False)

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
        Consequently, Midi map note C/-1 to 0, C#0 to 1, ... and G9 to 127.

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
        octave1 = self.octave is not None
        octave2 = other.octave is not None
        if octave1 == octave2:
            # use __implicit_octave__ if octave is None
            ps1 = float(self)
            ps2 = float(other)
            return ps1 == ps2 and self.alteration != other.alteration
        else:
            return False

        # elif octave1 and not octave2:
        #     ps1 = float(other)
        #     ps2 = self._compute_float_value(self.octave)
        # elif not octave1 and octave2:
        #     ps1 = self._compute_float_value(other.octave)
        #     ps2 = float(other)

    ##############################################

    def get_enharmonic(self):

        """Returns a new Pitch that is the enharmonic equivalent of this Pitch."""

        # Fixme: check

        alteration = self.alteration
        if alteration == 0:
            return self
        else:
            temperament = self.__temperament__
            step_number = self._step_number + alteration
            step_number, octave_offset = temperament.fold_step_number(step_number, octave=True)
            step = temperament[step_number]
            if step.is_accidental:
                if alteration < 0: # flat
                    step = step.sharpen_name
                else: # sharp
                    step = step.flatten_name
            octave = self._octave + octave_offset
            return self.__class__(step, octave=octave)

    ##############################################

    def simplify_accidental(self):

        # Fixme: enharmonic

        alteration = self.alteration
        if alteration:
            temperament = self.__temperament__
            step_number = self._step_number + self.alteration # Fixme: int ?, self.pitch_class ?
            if temperament.is_valid_step_name(step_number):
                return self
            else:
                step_number, octave_offset = temperament.fold_step_number(step_number, octave=True)
                octave = self._octave + octave_offset
                return self.__class__(step_number, octave=octave)
        else:
            return self # Fixme: clone ???

    ##############################################

    def pitch_iterator(self, until=None):

        return PitchIterator(self, until)

    ##############################################

    def _prev_next_pitch(self, offset):

        pitch = self.simplify_accidental()
        step_number = pitch.pitch_class + offset
        step_number, octave_offset = self.__temperament__.fold_step_number(step_number, octave=True)
        octave = pitch._octave + octave_offset
        return self.__class__(step_number, octave=octave)

    ##############################################

    def next_pitch(self):
        return self._prev_next_pitch(1)

    ##############################################

    def prev_pitch(self):
        return self._prev_next_pitch(-1)

####################################################################################################

class PitchIterator:

    ##############################################

    def __init__(self, start_pitch, stop_pitch=None):

        self._start = Pitch(start_pitch)
        if stop_pitch is not None:
            self._stop = Pitch(stop_pitch)
        else:
            self._stop = None

    ##############################################

    def iter(self, reverse=False, natural=False, inclusive=True):

        start = self._start.simplify_accidental()
        stop = self._stop
        if stop is not None:
            stop = stop.simplify_accidental()

        cls = start.__class__
        fold_step_number = start.__temperament__.fold_step_number

        if reverse:
            offset = -1
        else:
            offset = 1

        step_number = start.pitch_class
        octave = start.octave

        while True:
            pitch = cls(step_number, octave=octave)
            must_stop = stop is not None and pitch == stop
            if inclusive and must_stop:
                return
            if not (natural and pitch.is_altered):
                yield pitch
            if not inclusive and must_stop:
                return
            # Fixme: could use Pitch API
            step_number += offset
            step_number, octave_offset = fold_step_number(step_number, octave=True)
            octave += octave_offset

    ##############################################

    def __iter__(self):
        return self.iter()

####################################################################################################

class PitchInterval:

    ##############################################

    def __init__(self, lower_pitch, upper_pitch=None):

        if upper_pitch < lower_pitch:
            raise ValueError('{} < {}'.format(upper_pitch, lower_pitch))

        self._lower = Pitch(lower_pitch)
        if upper_pitch is not None:
            self._upper = Pitch(upper_pitch)
        else:
            self._upper = None

    ##############################################

    def clone(self):
        return self.__class__(self._lower, self._upper)

    ##############################################

    @property
    def lower(self):
        return self._lower

    @property
    def upper(self):
        return self._upper

    ##############################################

    def __iter__(self):

        return PitchIterator(self._lower, self._upper).iter() # inclusive=True

    ##############################################

    def iter(self, reverse=False, natural=False):

        if reverse:
            return PitchIterator(self._upper, self._lower).iter(reverse=True, natural=natural)
        else:
            return PitchIterator(self._lower, self._upper).iter(natural=natural)
