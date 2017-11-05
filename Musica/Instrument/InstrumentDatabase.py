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

"""
"""

####################################################################################################

__all__ = [
    'InstrumentDatabase',
]

####################################################################################################

import os

from ..Notation.Stave import StaveKeys, Stave, StavePair
from ..Theory.Pitch import Pitch, PitchInterval
from .Instrument import Instrument, InstrumentWriting, InstrumentTransposition, Ambitus

####################################################################################################

class InstrumentDatabase:

    ___instance__ = None

    ##############################################

    @classmethod
    def instance(cls):

        if cls.___instance__ is None:
            yaml_path = os.path.join(os.path.dirname(__file__), 'instruments.yml')
            cls.___instance__ = cls(yaml_path)

        return cls.___instance__

    ##############################################

    def __init__(self, yaml_path):

        self._yaml_path = yaml_path
        self._instruments = {}

        self._load()

    ##############################################

    def _load(self):

        import yaml
        with open(self._yaml_path, 'r') as fh:
            data = yaml.load(fh)

        for family, family_dict in data.items():
            if family_dict is not None:
                for instrument_name, instrument_dict in family_dict.items():
                    self._load_instrument(family, instrument_name, instrument_dict)

    ##############################################

    @staticmethod
    def _to_pitch_interval(string):

        lower_pitch, upper_pitch = [Pitch(x) for x in string.split()]
        return PitchInterval(lower_pitch, upper_pitch)

    ##############################################

    def _load_instrument(self, family, instrument_name, instrument_dict):

        writings = []
        if 'writings' in instrument_dict:
            for name, writing_data in instrument_dict['writings'].items():
                writing = self._load_writing(name, writing_data)
                if writing:
                    writings.append(writing)
        else:
            writing = self._load_writing('default', instrument_dict)
            if writing:
                writings.append(writing)

        kwargs = {}

        transposition_data = instrument_dict.get('transposition', False)
        if transposition_data:
            kwargs['transposition'] = [InstrumentTransposition(name, pitch)
                                       for name, pitch in transposition_data]

        if 'ambitus' in instrument_dict:
            kwargs['ambitus'] = [Ambitus(name, self._to_pitch_interval(string))
                                 for name, string in instrument_dict['ambitus'].items()]

        instrument = Instrument(name=instrument_name,
                                family=family,
                                writings=writings,
                                **kwargs,
        )
        self._instruments[instrument_name] = instrument

    ##############################################

    def _load_writing(self, name, data):

        try:
            keys = [StaveKeys[x] for x in data['staff key'].split()]
            if len(keys) == 1:
                stave = Stave(keys[0])
            else:
                stave = StavePair(keys[0], keys[1])
            pitch_interval = self._to_pitch_interval(data['written range'])
            return InstrumentWriting(name, stave, pitch_interval)
        except KeyError:
            return None

    ##############################################

    @property
    def instruments(self):
        return self._instruments.keys()

    ##############################################

    def __getitem__(self, instrument):
        return self._instruments[instrument]
