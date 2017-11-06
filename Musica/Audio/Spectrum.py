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

"""This module implements spectrum analysis based on Fast Fourier Transform.

References

Efficient Pitch Detection Techniques for Interactive Music
    Patricio de la Cuadra, Aaron Master, Craig Sapp
    Center for Computer Research in Music and Acoustics, Stanford University

"""

####################################################################################################

import math

import numpy as np

####################################################################################################

class Spectrum:

    __window_function__ = {
        'hann': np.hanning,
        }

    ##############################################

    @staticmethod
    def next_power_of_two(x):
        return 2**math.ceil(math.log(x)/math.log(2))

    ##############################################

    @classmethod
    def sample_for_resolution(cls, sampling_frequency, frequency_resolution, power_of_two=True):

        number_of_samples = int(math.ceil(sampling_frequency / frequency_resolution))
        if power_of_two:
            number_of_samples = cls.next_power_of_two(number_of_samples)

        return number_of_samples

    ##############################################

    def __init__(self, sampling_frequency, values, window='hann'):

        # *args, **kwargs
        # Fixme: better way to handle ctor !
        #  args expect sampling_frequency, values
        #  kwargs; window=hann

        # clone = kwargs.get('clone', None)
        # if clone is not None:
        #     self._sampling_frequency = clone._sampling_frequency
        #     self._number_of_samples = clone._number_of_samples
        #     self._values = np.array(clone._values)
        #     self._fft = np.array(clone._fft)
        #     self._frequencies = np.array(clone._frequencies)
        # else:
        #     if len(args) == 2:
        #         sampling_frequency, values = args
        #     elif len(args) == 1:
        #         sampling_frequency = args[0]
        #         values = kwargs['values']
        #     elif len(args) == 0:
        #         sampling_frequency = kwargs['sampling_frequency']
        #         values = kwargs['values']
        #     else:
        #         raise ValueError("require sampling_frequency and values args")
        #     window = kwargs.get('window', 'hann')

        self._sampling_frequency = sampling_frequency
        self._number_of_samples = values.size

        self._values = np.array(values)

        if window is not None:
            window = self.__window_function__[window](self._number_of_samples)
            values = values*window

        self._fft = np.fft.rfft(values)

        # Given a window length N and a sample spacing dt
        #   f = [0, 1, ...,   N/2 - 1,     -N/2, ..., -1] / (dt*N)   if N is even
        #   f = [0, 1, ...,   (N-1)/2, -(N-1)/2, ..., -1] / (dt*N)   if N is odd
        self._frequencies = np.fft.rfftfreq(self._number_of_samples, self.sample_spacing)

    ##############################################

    def clone(self):
        return self.__clone__(clone=self)

    ##############################################

    @property
    def sampling_frequency(self):
        return self._sampling_frequency

    @property
    def sample_spacing(self):
        return 1 / self._sampling_frequency

    @property
    def number_of_samples(self):
        return self._number_of_samples

    @property
    def duration(self):
        # inverse of frequency_resolution
        return self._number_of_samples / self._sampling_frequency

    @property
    def frequency_resolution(self):
        return self._sampling_frequency / self._number_of_samples

    ##############################################

    # time

    @property
    def values(self):
        return self._values

    @property
    def frequencies(self):
        return self._frequencies

    @property
    def fft(self):
        return self._fft

    ##############################################

    # Coefficients:
    #   A0**2
    #   Ak**2 / 4
    #
    # In a two-sided spectrum, half the energy is displayed at the positive frequency, and half the
    # energy is displayed at the negative frequency.
    #
    # single sided : * 2 and discard half
    #
    # amplitude   = magnitude(FFT) / N = sqrt(real**2 + imag**2) / N
    # phase [rad] = arctan(imag/real)
    #
    #
    # amplitude in rms = sqrt(2) * magnitude(FFT) / N for i > 0
    #                  =           magnitude(FFT) / N for i = 0
    #
    # power spectrum = FFT . FFT* / N**2
    #
    # dB = 10 log10(P/Pref)
    # dB = 20 log10(A/Aref)

    @property
    def magnitude(self):
        return np.abs(self._fft)

    @property
    def power(self):
        return self.magnitude**2

    @property
    def decibel_power(self):
        return 10 * np.log10(self.power)

    ##############################################

    def hfs(self, number_of_products):

        # , rebin=False

        """Compute the Harmonic Product Spectrum.

        References

        Noll, M. (1969).
            Pitch determination of human speech by the harmonic product spectrum, the harmonic sum
            spectrum, and a maximum likelihood estimate. In Proceedings of the Symposium on Computer
            Processing ing Communications, pp. 779-797. Polytechnic Institute of Brooklyn.

        """

        spectrum= self.magnitude # Fixme: **2 ???

        # Fixme: ceil ?
        size = int(math.ceil(spectrum.size / number_of_products))
        hfs = spectrum[:size].copy()
        for i in range(2, number_of_products + 1):
            # if rebin:
            #     rebinned_spectrum = spectrum[::i][:size].copy()
            #     for j ixn range(1, i):
            #         array = spectrum[j::i][:size]
            #         rebinned_spectrum[:array.size] += array
            #     rebinned_spectrum /= i
            #     hfs *= rebinned_spectrum # Fixme: wrong for upper bins
            # else:
            hfs *= spectrum[::i][:size]

        # Fixme: return class ???
        return self._frequencies[:size], hfs

    ##############################################

    def h_dome(self, height):

        """Extract h-dome from spectrum using Mathematical Morphology.

        Parameters
        ----------
        height : int
            Minimal height of the peaks

        """

        # Fixme: just for test ...

        values = np.array(self.decibel_power, dtype=np.int)
        values = np.where(values >= 0, values, 0)

        from Musica.Math.Morphomath import Function
        function = Function(values).h_dome(height)

        return function.values
