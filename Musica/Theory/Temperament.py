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

"""This module defines temperaments.

"""

####################################################################################################

__all__ = [
    'ET12',
    'EqualTemperament',
    'TemperamentAccidentalStep',
    'TemperamentNaturalStep',
    'TemperamentStep',
    'UsualEqualTemperament',
    ]

####################################################################################################

from ..Locale.Note import translate_et12_note
from ..Math.MusicTheory import ET12Tuning
from .NoteTools import flatten_note, sharpen_note
from .PitchStandard import A440
from .Quality import IntervalQualities

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

    def is_valid_step_number(self, number):
        return 0 <= number < self._number_of_steps

    ##############################################

    def is_last_step_number(self, number):
        return (self._number_of_steps -1) == number

    ##############################################

    def fold_step_number(self, number, octave=False):

        step_number = number % self._number_of_steps
        if octave:
            return step_number, number // self._number_of_steps
        else:
            return step_number

    ##############################################

    def _compute_scale(self, octave, step_number):

        if step_number < 0:
            raise ValueError("Invalid step number {}".format(step_number))

        octave_factor = 2 ** octave
        interval_factor = 2 ** (step_number / self._number_of_steps)
        return octave_factor * interval_factor

    ##############################################

    def _compute_fundamental(self):

        denominator = self._compute_scale(self._pitch_standard.octave,
                                          self._pitch_standard.step_number)
        return self._pitch_standard.frequency / denominator

    ##############################################

    def frequency(self, octave, step_number):

        """Return the frequency for an octave using the scientific pitch notation and an step number
        ranging from 0 to 11.

        For A440 (La3), use octave 4 and step number 9.

        """

        return self._fundamental * self._compute_scale(octave, step_number)

####################################################################################################

class TemperamentStep:

    ##############################################

    def __init__(self, step_number, quality=None):

        self._step_number = step_number
        self._quality = quality

        self._prev_natural = None
        self._next_natural = None
        self._prev_step = None
        self._next_step = None

    ##############################################

    @property
    def step_number(self):
        return self._step_number

    @property
    def quality(self):
        return self._quality

    @property
    def prev_natural(self): # Fixme: previous ?
        return self._prev_natural

    @property
    def next_natural(self):
        return self._next_natural

    @property
    def prev_step(self):
        return self._prev_step

    @property
    def next_step(self):
        return self._next_step

    ##############################################

    def __int__(self):
        return self._step_number

    def __lt__(self, other):
        return self._step_number < int(other)

####################################################################################################

class TemperamentNaturalStep(TemperamentStep):

    ##############################################

    def __init__(self, step_number, degree, name, quality):

        super().__init__(step_number, quality)

        self._name = name
        self._degree = degree

    ##############################################

    @property
    def is_natural(self):
        return True

    @property
    def is_accidental(self):
        return False

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def degree(self):
        return self._degree

    ##############################################

    def __repr__(self):
        return '{0.__class__.__name__} {0._step_number} {0._name}'.format(self)

####################################################################################################

class TemperamentAccidentalStep(TemperamentStep):

    ##############################################

    def __init__(self, step_number):

        super().__init__(step_number, quality=IntervalQualities.minor)

    ##############################################

    def __repr__(self):
        return '{0.__class__.__name__} {0.step_number}'.format(self)

    ##############################################

    @property
    def is_natural(self):
        return False

    @property
    def is_accidental(self):
        return True

    ##############################################

    @property
    def sharpen_name(self):
        return sharpen_note(self._prev_natural.name)

    @property
    def flatten_name(self):
        return flatten_note(self._next_natural.name)

####################################################################################################

class UsualEqualTemperament(EqualTemperament):

    """Base class factory to build for example a twelve-tone equal temperament.
    """

    ##############################################

    def __init__(self, math_implementation, pitch_standard, natural_steps, translator):

        super().__init__(math_implementation.number_of_steps, pitch_standard)

        self._math_implementation = math_implementation
        self._translator = translator

        perfect_steps = math_implementation.perfect_steps
        major_scale = math_implementation.major_scale

        self._natural_steps = []
        for degree, ztuple in enumerate(zip(major_scale, natural_steps)):
            pitch, name = ztuple
            if pitch in perfect_steps:
                quality = IntervalQualities.perfect
            else:
                quality = IntervalQualities.major
            step = TemperamentNaturalStep(pitch.step_number, degree, name, quality)
            self._natural_steps.append(step)
        # complete
        self._number_of_natural_steps = len(self._natural_steps)
        for step in self._natural_steps:
            i_prev = (step.degree - 1) % self._number_of_natural_steps
            i_next = (step.degree + 1) % self._number_of_natural_steps
            step._prev_natural = self._natural_steps[i_prev]
            step._next_natural = self._natural_steps[i_next]

        # Note names
        self._natural_step_names = natural_steps

        # List of natural step number
        self._natural_step_numbers = major_scale

        # Map note name -> step
        self._name_to_step = {step.name:step for step in self._natural_steps}

        # Map step number -> step
        self._steps = [None]*self._number_of_steps
        for step in self._natural_steps:
            self._steps[step.step_number] = step
        # Add accidentals and link steps
        for i in range(self._number_of_steps):
            step = self._steps[i]
            if step is None:
                step = TemperamentAccidentalStep(i)
                self._steps[i] = step
                # prev and next are natural steps
                i_prev = self.fold_step_number(i - 1)
                i_next = self.fold_step_number(i + 1)
                step._prev_natural = self._steps[i_prev]
                step._next_natural = self._steps[i_next]
                for name in (step.flatten_name, step.sharpen_name):
                    self._name_to_step[name] = step
        # Link steps
        for i in range(self._number_of_steps):
            step = self._steps[i]
            i_prev = self.fold_step_number(i - 1)
            i_next = self.fold_step_number(i + 1)
            step._prev_step = self._steps[i_prev]
            step._next_step = self._steps[i_next]

    ##############################################

    def __iter__(self):
        return iter(self._steps)

    ##############################################

    def natural_step_names(self):
        return self._natural_step_names

    @property
    def number_of_natural_steps(self):
        return self._number_of_natural_steps

    ##############################################

    def fold_natural_step_number(self, number, octave=False):

        step_number = number % self._number_of_natural_steps
        if octave:
            return step_number, number // self._number_of_natural_steps
        else:
            return step_number

    ##############################################

    def is_natural_step_number(self, number):
        return number in self._natural_step_numbers

    ##############################################

    def translator(self, *args, **kwargs):
        return self._translator(*args, **kwargs)

    ##############################################

    def is_valid_step_name(self, name):
        return name in self._natural_step_names

    ##############################################

    def __getitem__(self, step_number):
        return self.by_step_number(step_number)

    ##############################################

    def by_step_number(self, step_number):
        return self._steps[step_number]

    ##############################################

    def by_name(self, name):
        return self._name_to_step[name]

    ##############################################

    def by_degree(self, degree):
        return self._natural_steps[degree]

    ##############################################

    def name_to_number(self, name):
        return self.by_name(name).step_number

####################################################################################################

#: Twelve-tone equal temperament, also known as 12 equal temperament, 12-TET, or 12-ET
ET12 = UsualEqualTemperament(
    math_implementation=ET12Tuning,
    pitch_standard=A440,
    natural_steps=( # sorted by step number
        'C', # 1 Do
        'D', # 2 Rè
        'E', # 3 Mi
        'F', # 4 Fa
        'G', # 5 Sol
        'A', # 6 La
        'B', # 7 Si
    ),
    translator=translate_et12_note,
)
