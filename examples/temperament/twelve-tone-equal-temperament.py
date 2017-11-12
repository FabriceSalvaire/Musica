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

#!# ===============================
#!#  Twelve-Tone Equal Temperament
#!# ===============================

#!# This section illustrates the twelve-tone equal temperament (12-TET).

####################################################################################################

import numpy
import matplotlib.pyplot as plt

####################################################################################################

from Musica.Math.MusicTheory import *
from Musica.Theory.Temperament import *

####################################################################################################

fifth_approximations = ET12Tuning.fifth_approximations(number_of_steps_max=20)
print('Perfect fifth 3/2\n         1.5    {:.1f} cent'.format(
    float(Cent.from_frequency_ratio(FrequencyRatio.fifth))))
for pitch in fifth_approximations:
    print('2**{:2}/{:2} {:.4f} {:.1f} cent'.format(
        pitch.number_of_steps,
        pitch.step_number,
        float(pitch),
        float(pitch.cent),
    ))
#o#

####################################################################################################

number_of_octaves = 10
octave_frequencies = [[ET12.frequency(octave_number, interval_number) for interval_number in range(1, 13)] for octave_number in range(1, number_of_octaves +1)]
all_frequencies = []
for octave_number in range(1, number_of_octaves +1):
    frequencies = octave_frequencies[octave_number -1]
    all_frequencies += frequencies
    print("Octave {:2} {}".format(octave_number, ['{:.2f}'.format(x) for x in frequencies]))
#o#

figure = plt.figure(1, (20, 10))

axe = plt.subplot(111)
axe.set_title('Twelve-tone Equal Temperament')
axe.set_xlabel('notes')
axe.set_ylabel('Hz')
axe.grid()
for octave_number in range(number_of_octaves):
    x = octave_number * 12 + 1
    axe.axvline(x, color='blue')
    axe.text(x, 10, 'Octave {}'.format(octave_number +1), color='black')
axe.semilogy(range(1, len(all_frequencies) +1), all_frequencies, 'o-')
axe.axhline(y=440, color='red')
axe.text(2, 460, 'A 440 Hz', color='black')
axe.axhline(y=50, color='red')
axe.axhline(y=60, color='red')
axe.text(20, 65, 'Electric Network Frequency 50/60Hz', color='black')
axe.axhline(y=20e3, color='red')
axe.text(2, 22e3, 'Human Ear Limit 20 kHz', color='black')

plt.show()

#fig# save_figure(figure, '12tet.png')
