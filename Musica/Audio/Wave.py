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

import wave

import numpy as np

from .AudioFormat import AudioFormat, AudioFormatMetadata

####################################################################################################

class WaveFormat(AudioFormat):

    __extensions__ = ['wav']

    ##############################################

    def __init__(self, path):

        wave_file = wave.open(path, 'r')

        number_of_channels = wave_file.getnchannels()
        sample_width = wave_file.getsampwidth() # in bytes
        sampling_frequency = wave_file.getframerate() # Hz
        number_of_frames = wave_file.getnframes()
        # wave_file.getcomptype()

        bits_per_sample = sample_width * 8

        # print(number_of_channels, sample_width, sampling_frequency, number_of_frames)
        # 1 2 44100 82256

        metadata = AudioFormatMetadata(
            number_of_channels=number_of_channels,
            sampling_frequency=sampling_frequency,
            bits_per_sample=bits_per_sample,
        )

        dtype = '<i{}'.format(sample_width)
        data = np.frombuffer(wave_file.readframes(number_of_frames), dtype=dtype)
        data = data.reshape(number_of_frames // number_of_channels, number_of_channels)
        channels = [np.array(data[:,i]) for i in range(number_of_channels)]

        super().__init__(metadata, channels)
