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
    'EqualTemperament',
    'ET12',
    ]

####################################################################################################

from ..Locale.Note import translate_et12_note
from .PitchStandard import A440

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

    def fold_step_number(self, number, octave_number=False):

        step_number = number % self._number_of_steps
        if octave_number:
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

    def __init__(self, step_number, name=None, quality=None, degree=None):

        super().__init__(step_number, quality)

        self._name = name
        self._degree = degree

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

        super().__init__(step_number, quality='m')

    ##############################################

    def __repr__(self):
        return '{0.__class__.__name__} {0.step_number}'.format(self)

####################################################################################################

class UsualEqualTemperament(EqualTemperament):

    """Base class factory to build for example a twelve-tone equal temperament.
    """

    ##############################################

    def __init__(self, number_of_steps, pitch_standard, natural_steps, translator):

        super().__init__(number_of_steps, pitch_standard)

        self._translator = translator

        # ensure sorted by degree
        self._natural_steps = sorted(natural_steps)
        # complete
        number_of_natural_steps = len(natural_steps)
        for degree, step in enumerate(self._natural_steps):
            step._degree = degree
            i_prev = (degree - 1) % number_of_natural_steps
            i_next = (degree + 1) % number_of_natural_steps
            step._prev_natural = self._natural_steps[i_prev]
            step._next_natural = self._natural_steps[i_next]

        # Note names
        self._natural_step_names = [step.name for step in self._natural_steps]

        # List of natural step number
        self._natural_step_numbers = [step.step_number for step in self._natural_steps]

        # Map note name -> step
        self._name_to_step = {step.name:step for step in self._natural_steps}

        # Map step number -> step
        self._steps = [None]*number_of_steps
        for step in self._natural_steps:
            self._steps[step.step_number] = step
        # Add accidentals
        for i in range(number_of_steps):
            if self._steps[i] is None:
                self._steps[i] = TemperamentAccidentalStep(i)
                i_prev = (i - 1) % number_of_steps
                i_next = (i + 1) % number_of_steps
                prev_step = self._steps[i_prev]
                next_step = self._steps[i_next]
                name = prev_step.name + '-'
                self._name_to_step[name] = prev_step
                name = next_step.name + '#'
                self._name_to_step[name] = next_step
        # link steps
        for i in range(number_of_steps):

    ##############################################

    def __iter__(self):
        return iter(self._steps)

    ##############################################

    def natural_step_names(self):
        return self._natural_step_names

    @property
    def number_of_natural_steps(self):
        return len(self._natural_step_names)

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

####################################################################################################

#: Twelve-tone equal temperament, also known as 12 equal temperament, 12-TET, or 12-ET
ET12 = UsualEqualTemperament(
    number_of_steps=12,
    pitch_standard=A440,
    natural_steps=(
        # step number, name, quality
        TemperamentNaturalStep( 0, 'C', 'P'), # 1 Do
        TemperamentNaturalStep( 2, 'D', 'M'), # 2 Rè
        TemperamentNaturalStep( 4, 'E', 'M'), # 3 Mi
        TemperamentNaturalStep( 5, 'F', 'P'), # 4 Fa
        TemperamentNaturalStep( 7, 'G', 'P'), # 5 Sol
        TemperamentNaturalStep( 9, 'A', 'M'), # 6 La
        TemperamentNaturalStep(11, 'B', 'M'), # 7 Si
    ),
    # altered steps are minor, excepted step 6 between F/Fa and G/Sol which is particular
    translator=translate_et12_note,
)
