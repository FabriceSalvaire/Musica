#?##################################################################################################
#?#
#?# Musica - A Music Theory Package for Python
#?# Copyright (C) 2017 Fabrice Salvaire
#?#
#?# This program is free software: you can redistribute it and/or modify
#?# it under the terms of the GNU General Public License as published by
#?# the Free Software Foundation, either version 3 of the License, or
#?# (at your option) any later version.
#?#
#?# This program is distributed in the hope that it will be useful,
#?# but WITHOUT ANY WARRANTY; without even the implied warranty of
#?# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#?# GNU General Public License for more details.
#?#
#?# You should have received a copy of the GNU General Public License
#?# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#?#
#?##################################################################################################

#!# =======================================
#!#  Pythagorean Tuning compared to 12-TET
#!# =======================================

#!# This section compares the Pythagorean tuning and the twele-tone equal temperament (12-TET).

####################################################################################################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

####################################################################################################

from Musica.Math.MusicTheory import *

####################################################################################################

prev_fifth = None
for i, pitch in enumerate(PythagoreanTuning):
    delta_numerator = delta_denominator = ''
    if isinstance(pitch, PythagoreanFifth):
        if prev_fifth is not None:
            # 3**7/2**11 apotome |2**8/3**5 limma
            delta_numerator, delta_denominator = pitch / prev_fifth
        prev_fifth = pitch
    print('{:3} {:3} | {:3} {:3} | {:6} / {:6} | {:4.2f} | {:6.0f}'.format(
        pitch.numerator_power, pitch.denominator_power,
        delta_numerator, delta_denominator,
        pitch.numerator, pitch.denominator,
        float(pitch), float(pitch.cent)))
#o#

figure1 = plt.figure(1, (20, 10))
axe = plt.subplot(111)
axe.set_title('Pythagorean Tuning / 12-tone Equal Temperament')
axe.set_xlabel('Cents')
axe.set_ylabel('Frequency Ratio')
axe.xaxis.set_major_locator(MultipleLocator(100))
axe.grid()
axe.plot([float(pitch.cent) for pitch in PythagoreanTuning],
         [float(pitch) for pitch in PythagoreanTuning],
         'o-')
axe.plot([float(pitch.cent) for pitch in ET12Tuning],
         [float(pitch) for pitch in ET12Tuning],
         'o', color='orange')
for frequency_ratio in (
        FrequencyRatio.unisson,
        FrequencyRatio.fourth,
        FrequencyRatio.fifth,
        FrequencyRatio.octave,
        ):
    axe.axhline(y=frequency_ratio, color='orange')
axe.axhline(y=float(PythagoreanTuning.wolf_interval), color='red')

plt.show()

#fig# save_figure(figure1, 'temperament.png')
