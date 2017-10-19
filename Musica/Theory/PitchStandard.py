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

"""This module defines pitch standards.
"""

####################################################################################################

__all__ = [
    'PitchStandard',
    'A440',
    ]

####################################################################################################

class PitchStandard:

    """Class to define a pitch standard.

    Octave are numbered according SPN and step (semitone) numbers lie from 0 to 11.

    To define A440 use :code:`PitchStandard(name='A440', frequency=440, octave_number=4, step_number=9)`
    """

    def __init__(self, name, frequency, octave, step_number):

        self._name = name
        self._frequency = frequency
        self._octave = octave
        self._step_number = step_number # Fixme: pitch class ?

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def frequency(self):
        return self._frequency

    @property
    def octave(self):
        return self._octave

    @property
    def step_number(self):
        return self._step_number

####################################################################################################

#: A440 or A4, also known as the Stuttgart pitch, which has a frequency of 440 Hz,
#  is the musical note of A above middle C
#  and serves as a general tuning standard for musical pitch.
A440 = PitchStandard(name='A440', frequency=440, octave=4, step_number=9)
