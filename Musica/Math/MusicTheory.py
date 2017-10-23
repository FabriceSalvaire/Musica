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

"""String Vibration
----------------

There are four physical quantities involved in the string vibration phenomenon :

* the frequency :math:`f` of dimension :math:`s^{-1}`,
* the linear density :math:`\mu` of the string of dimension :math:`kg m^{-1}`,
* the tension :math:`T` applied to the string of dimension :math:`kg m s^{-2}`,
* the length :math:`L` of the string of dimension :math:`m`.

According to the Vaschy-Buckingham theorem, we can build a dimensionless constant:

.. math::

    \alpha = \frac{T}{\mu L^2 f^2}

and thus

.. math::

    f = \frac{\beta}{L} \sqrt{\frac{T}{\mu}}

where :math:`\beta` is a dimensionless constant.

In reality, the vibration of a string corresponds to the superposition of standing waves of
frequencies:

.. math::

    f_n = \frac{n}{2L} \sqrt{\frac{T}{\mu}}

where :math:`n` is an integer greater than 0.

This series of frequencies is called an harmonic series.  The first one is called fundamental
frequency, :math:`n=1`, and the others overtones.

We can notice from this formulae:

* the shorter the string, the higher the frequency of the fundamental,
* the higher the tension, the higher the frequency of the fundamental,
* the lighter the string, the higher the frequency of the fundamental.

Octave and Fifth
----------------

Let be a string of length L with a movable bridge.  We denote :math:`f_0` the fundamental frequency
of the string.

* If we place the mobile bridge at the middle of the string, :math:`L/2`, the string fundamental
  will now ring at :math:`f_8 = 2 \times f_0`, thus at the higher octave of :math:`f_0`.

* If we place the mobile bridge at :math:`2/3 L`, which is the next simpler subdivision of the
  string, the larger string part will ring at :math:`f_5 = \frac{3}{2} \times f_0`, thus at the
  higher perfect fifth of :math:`f_0`.

We define the fourth as the ratio of :math:`f_4 = f_8 / f_5 = \frac{4}{3}`, which is the complement
to the fifth to match the octave.

"""

####################################################################################################

import math

####################################################################################################

class Frequency:

    ##############################################

    def __init__(self, frequency):

        self._frequency = frequency

    ##############################################

    def __repr__(self):
        return "{0.__class__.__name__} {0._frequency}".format(self)

    ##############################################

    @property
    def frequency(self):
        return self._frequency

    @property
    def period(self):
        return 1 / self._frequency

    @property
    def pulsation(self):
        return 2 * math.pi * self._frequency

    ##############################################

    def __float__(self):
        return float(self._frequency)

    ##############################################

    def __eq__(self, other):
        return self._frequency == other._frequency # Fixme: float() ?

    def __lt__(self, other):
        return self._frequency < float(other)

    ##############################################

    def __truediv__(self, other):

        return Cent.from_frequency(self, other)

####################################################################################################

class Cent:

    ##############################################

    @classmethod
    def from_frequency_ratio(cls, frequency_ratio):

        cent = 1200 * math.log(frequency_ratio, 2)

        return cls(cent)

    ##############################################

    @classmethod
    def from_frequency(cls, frequency1, frequency2):

        cent = 1200 * math.log(float(frequency1) / float(frequency2), 2)

        return cls(cent)

    ##############################################

    def __init__(self, cent):

        self._cent = cent

    ##############################################

    def __repr__(self):
        return "{0.__class__.__name__} {0._cent}".format(self)

    ##############################################

    @property
    def cent(self):
        return self._cent

    ##############################################

    def __float__(self):
        return self._cent

    ##############################################

    def __eq__(self, other):
        return self._cent == other._cent # Fixme: float() ?

    def __lt__(self, other):
        return self._cent < float(other)

    ##############################################

    def to_frequency(self, frequency):

        return Frequency(float(frequency) * 2 ** (self._cent / 1200))

####################################################################################################

class FrequencyRatio:

    unisson = 1
    fourth = 4 / 3
    fifth  = 3 / 2
    octave = 2

    et12 = 2**(1/12)

####################################################################################################

class PythagoreanPitch:

    ##############################################

    def __init__(self, numerator_power, denominator_power):

        self._numerator_power = numerator_power
        self._denominator_power = denominator_power

    ##############################################

    def __repr__(self):
        return "{0.__class__.__name__} {0.numerator}/{0.denominator}".format(self)

    ##############################################

    @property
    def numerator_power(self):
        return self._numerator_power

    @property
    def denominator_power(self):
        return self._denominator_power

    @property
    def cent(self):
        return Cent.from_frequency_ratio(float(self))

    ##############################################

    def __float__(self):
        return self.numerator / self.denominator

    ##############################################

    def __lt__(self, other):
        return float(self) < float(other)

####################################################################################################

class PythagoreanFifth(PythagoreanPitch):

    ##############################################

    @property
    def numerator(self):
        return 3**self._numerator_power

    @property
    def denominator(self):
        return 2**self._denominator_power

    ##############################################

    def __truediv__(self, other):

        delta_numerator = abs(self.denominator_power - other.denominator_power)
        delta_denominator = abs(self.numerator_power - other.numerator_power)

        return delta_numerator, delta_denominator

####################################################################################################

class PythagoreanFourth(PythagoreanPitch):

    ##############################################

    @property
    def numerator(self):
        return 2**self._numerator_power

    @property
    def denominator(self):
        return 3**self._denominator_power

####################################################################################################

class PythagoreanTuningSingleton:

    ##############################################

    @staticmethod
    def generate_fifth_series():

        # Generate a series of fifth
        #   https://fr.wikipedia.org/wiki/Accord_pythagoricien
        #   https://en.wikipedia.org/wiki/Pythagorean_tuning

        pitchs = []
        i = 0
        octave_power = 0
        stop = False
        while not stop:
            pitch = PythagoreanFifth(i, i + octave_power)
            ratio = float(pitch)
            if 2 <= ratio < 2.05: # 3**12 / 2**18 = 2.027
                stop = True
            elif ratio > 2:
                octave_power += 1
                pitch = PythagoreanFifth(i, i + octave_power)
            pitchs.append(pitch)
            i += 1

        return pitchs

    ##############################################

    @staticmethod
    def add_fourths(fifth_series):

        fifth_series = sorted(fifth_series)
        fourth_series = []
        for i, pitch in enumerate(fifth_series):
            if 0 < i:
                prev_pitch = fifth_series[i-1]
                delta_numerator, delta_denominator = pitch / prev_pitch
                if delta_numerator == 8: # apotome
                    fourth = PythagoreanFourth(pitch.denominator_power + 1, pitch.numerator_power)
                    fourth_series.append(fourth)

        return fifth_series + fourth_series

    ##############################################

    def __init__(self):

        self._pitchs = sorted(self.add_fourths(self.generate_fifth_series()))

        # Wolf interval = 7 octaves - 11 perfect fifths = 2**7 / (3/2)**11
        self._wolf_interval = PythagoreanFourth(11 + 7, 11) # ~ 1.480 versus 1.5 for perfect fifth

    ##############################################

    def __iter__(self):
        return iter(self._pitchs)

    ##############################################

    def __len__(self):
        return len(self._pitchs)

    ##############################################

    def __getitem__(self, i):
        return self._pitchs[i]

    ##############################################

    @property
    def wolf_interval(self):
        return self._wolf_interval


PythagoreanTuning = PythagoreanTuningSingleton()

####################################################################################################

class EqualTemperamentPitch:

    ##############################################

    def __init__(self, step, number_of_steps):

        self._step = step
        self._number_of_steps = number_of_steps

    ##############################################

    @property
    def step(self):
        return self._step

    @property
    def number_of_steps(self):
        return self._number_of_steps

    @property
    def cent(self):
        return Cent.from_frequency_ratio(float(self))

    ##############################################

    def __float__(self):
        return 2**(self._step / self._number_of_steps)

    ##############################################

    def __lt__(self, other):
        return float(self) < float(other)

####################################################################################################

class EqualTemperamentTuningSingleton:

    ##############################################

    def __init__(self, number_of_steps):

        # Waring: include octave !

        self._pitchs = [EqualTemperamentPitch(step, number_of_steps)
                        for step in range(number_of_steps + 1)]

    ##############################################

    def __iter__(self):
        return iter(self._pitchs)

    ##############################################

    def __len__(self):
        return len(self._pitchs)

    ##############################################

    def __getitem__(self, i):
        return self._pitchs[i]

ET12Tuning = EqualTemperamentTuningSingleton(number_of_steps=12)
