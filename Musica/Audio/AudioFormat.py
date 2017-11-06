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

import logging
# import math
import os

# import numpy as np

from .Spectrum import Spectrum

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class AudioFormatMetadata:

    ##############################################

    def __init__(self,
                 number_of_channels, # int > 0
                 sampling_frequency, # e.g. 44.1kHz 48kHz 96kHz
                 bits_per_sample, # e.g. 8 16 24-bit
    ):

        self._number_of_channels = number_of_channels
        self._sampling_frequency = sampling_frequency
        self._bits_per_sample = bits_per_sample

    ##############################################

    @property
    def number_of_channels(self):
        return self._number_of_channels

    @property
    def sampling_frequency(self):
        return self._sampling_frequency

    @property
    def time_resolution(self):
        return 1 / self._sampling_frequency

    @property
    def bits_per_sample(self):
        return self._bits_per_sample

    @property
    def float_scale(self):
        # N-bit signed integer range from -2**(N-1) to 2**(N-1) -1
        return 2**(self._bits_per_sample -1)

    ##############################################

    def sample_to_time(self, i):
        return i / self._sampling_frequency

    def time_to_sample(self, t):
        return int(t * self._sampling_frequency)

####################################################################################################

class AudioFormatMetaclass(type):

    __extensions__ = {}

    _logger = _module_logger.getChild('AudioFormatMetaclass')

    ##############################################

    def __new__(cls, class_name, base_classes, attributes):
        return super().__new__(cls, class_name, base_classes, attributes)

    ##############################################

    def __init__(cls, class_name, base_classes, attributes):

        type.__init__(cls, class_name, base_classes, attributes)

        if cls.__extensions__ is not None:
            for extension in cls.__extensions__:
                AudioFormatMetaclass._logger.info('Register {} for {}'.format(cls, extension))
                AudioFormatMetaclass.__extensions__[extension] = cls

    ##############################################

    @classmethod
    def get(cls, extension):

        if extension.startswith('.'):
            extension = extension[1:]

        return cls.__extensions__[extension]

####################################################################################################

class AudioFormat(metaclass=AudioFormatMetaclass):

    __extensions__ = None

    _logger = _module_logger.getChild('AudioFormat')

    ##############################################

    @classmethod
    def open(cls, path):

        basename, ext = os.path.splitext(path)
        audio_format_cls = AudioFormatMetaclass.get(ext)

        return audio_format_cls(path)

    ##############################################

    def __init__(self, metadata, channels):

        self._metadata = metadata
        self._channels = channels

    ##############################################

    @property
    def metadata(self):
        return self._metadata

    def channel(self, i, as_float=False):

        data = self._channels[i]
        if as_float:
            return data / self._metadata.float_scale
        else:
            return data

    ##############################################

    def spectrum(self, channel, **kwargs):

        sampling_frequency = self._metadata.sampling_frequency
        window = kwargs.get('window', 'hann')

        data = self.channel(channel, as_float=True)

        if 'start' in kwargs:
            start = self._metadata.time_to_sample(kwargs['start'])
        else:
            start = kwargs.get('start_sample', 0)

        if 'number_of_samples' in kwargs:
            stop = start + kwargs['number_of_samples']
        elif 'stop_sample' in kwargs:
            stop = kwargs['stop_sample'] + 1
        elif 'stop' in kwargs:
            stop = self._metadata.time_to_sample(kwargs['stop']) + 1
        elif 'frequency_resolution' in kwargs:
            number_of_samples = Spectrum.sample_for_resolution(sampling_frequency,
                                                               kwargs['frequency_resolution'],
                                                               kwargs.get('power_of_two', True))
        else:
            stop = data.size

        if stop > data.size:
            raise ValueError("stop is too large")
        data = data[start:stop]

        self._logger.info("spectrum from {} to {}".format(start, stop))

        return Spectrum(sampling_frequency, data, window)
