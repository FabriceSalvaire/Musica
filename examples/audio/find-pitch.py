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

import numpy as np
import matplotlib.pyplot as plt

from Musica.Audio.AudioFormat import AudioFormat

####################################################################################################

audio = AudioFormat.open('data/string-waves/clean/E2.1.wav')

# data = audio.channel(0, as_float=True)
# plt.figure()
# plt.plot(data)

spectrum = audio.spectrum(0, number_of_samples=2**16)

# plt.figure()
# plt.plot(spectrum.values)

plt.figure()
# plt.semilogx(spectrum.frequencies, spectrum.magnitude)
# plt.semilogx(spectrum.frequencies, spectrum.decibel_power)
# plt.semilogx(spectrum.frequencies, spectrum.h_dome(20), 'o-')
frequencies, hfs = spectrum.hfs(5)
i_max = np.argmax(hfs)
print('Frequency: {:.1f} +- {:.1f} Hz'.format(frequencies[i_max], spectrum.frequency_resolution))
plt.semilogx(frequencies, hfs, 'o-')
plt.grid()

plt.show()
